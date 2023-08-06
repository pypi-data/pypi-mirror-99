import argparse
import atexit
import os
import re
import shlex
import subprocess
import tarfile
import tempfile
import textwrap
from collections import defaultdict, deque, UserDict
from dataclasses import dataclass
from itertools import chain

from pkgcheck import reporters, scan
from pkgcore.ebuild.atom import MalformedAtom
from pkgcore.ebuild.atom import atom as atom_cls
from pkgcore.ebuild.repository import UnconfiguredTree
from pkgcore.operations import observer as observer_mod
from pkgcore.restrictions import packages
from snakeoil.cli import arghparse
from snakeoil.cli.input import userquery
from snakeoil.klass import jit_attr
from snakeoil.mappings import OrderedFrozenSet, OrderedSet
from snakeoil.osutils import pjoin

from .. import git
from ..mangle import GentooMangler, Mangler
from .argparsers import cwd_repo_argparser, git_repo_argparser


class ArgumentParser(arghparse.ArgumentParser):
    """Parse all known arguments, passing unknown arguments to ``git commit``."""

    def parse_known_args(self, args=None, namespace=None):
        namespace.footer = OrderedSet()
        namespace, args = super().parse_known_args(args, namespace)
        if namespace.dry_run:
            args.append('--dry-run')
        if namespace.verbosity:
            args.append('-v')
        namespace.commit_args = args
        return namespace, []


class CommitTags(argparse.Action):
    """Register tags to inject into the commit message footer."""

    def __call__(self, parser, namespace, value, option_string=None):
        try:
            url = f'https://bugs.gentoo.org/{int(value)}'
        except ValueError:
            url = value
            if not url.startswith(('https://', 'http://')):
                raise argparse.ArgumentError(self, f'invalid URL: {url}')
        namespace.footer.add((self.dest.capitalize(), url))


commit = ArgumentParser(
    prog='pkgdev commit', description='create git commit',
    parents=(cwd_repo_argparser, git_repo_argparser))
# custom `pkgcheck scan` args used for tests
commit.add_argument('--pkgcheck-scan', help=argparse.SUPPRESS)
commit_opts = commit.add_argument_group('commit options')
commit_opts.add_argument(
    '-b', '--bug', action=CommitTags,
    help='add Bug tag for a given Gentoo or upstream bug')
commit_opts.add_argument(
    '-c', '--closes', action=CommitTags,
    help='add Closes tag for a given Gentoo bug or upstream PR URL')
commit_opts.add_argument(
    '-n', '--dry-run', action='store_true',
    help='pretend to create commit',
    docs="""
        Perform all actions without creating a commit.
    """)
commit_opts.add_argument(
    '-s', '--scan', action='store_true',
    help='run pkgcheck against staged changes',
    docs="""
        By default, ``pkgdev commit`` doesn't scan for QA errors. This option
        enables using pkgcheck to scan the staged changes for issues, erroring
        out if any failures are found.
    """)
commit_opts.add_argument(
    '-A', '--ask', action='store_true',
    help='confirm creating commit with QA errors',
    docs="""
        When running with the -s/--scan option enabled, ``pkgdev commit`` will
        ask for confirmation before creating a commit if it detects failure
        results.
    """)
commit_opts.add_argument(
    '--mangle', nargs='?', const=True, action=arghparse.StoreBool,
    help='forcibly enable/disable file mangling',
    docs="""
        File mangling automatically modifies the content of relevant staged
        files including updating copyright headers and fixing EOF newlines.

        This is performed by default for the gentoo repo, but can be forcibly
        disabled or enabled as required.
    """)

msg_actions = commit_opts.add_mutually_exclusive_group()
msg_actions.add_argument(
    '-m', '--message', metavar='MSG', action='append',
    help='specify commit message',
    docs="""
        Use a given message as the commit message. If multiple -m options are
        specified, their values are concatenated as separate paragraphs.

        Note that the first value will be used for the commit summary and if
        it's empty then a generated summary will be used if available.
    """)
msg_actions.add_argument(
    '-M', '--message-template', metavar='FILE', type=argparse.FileType('r'),
    help='use commit message template from specified file',
    docs="""
        Use content from the given file as a commit message template. The
        commit summary prefix '*: ' is automatically replaced by a generated
        prefix if one exists for the related staged changes.
    """)
msg_actions.add_argument('-F', '--file', help=argparse.SUPPRESS)
msg_actions.add_argument('-t', '--template', help=argparse.SUPPRESS)

add_actions = commit_opts.add_mutually_exclusive_group()
add_actions.add_argument(
    '-u', '--update', dest='git_add_arg', const='--update', action='store_const',
    help='stage all changed files')
add_actions.add_argument(
    '-a', '--all', dest='git_add_arg', const='--all', action='store_const',
    help='stage all changed/new/removed files')


class _HistoricalRepo(UnconfiguredTree):
    """Repository of historical packages stored in a temporary directory."""

    def __init__(self, repo, *args, **kwargs):
        self.__parent_repo = repo
        self.__tmpdir = tempfile.TemporaryDirectory()
        self.__created = False
        repo_dir = self.__tmpdir.name

        # set up some basic repo files so pkgcore doesn't complain
        os.makedirs(pjoin(repo_dir, 'metadata'))
        with open(pjoin(repo_dir, 'metadata', 'layout.conf'), 'w') as f:
            f.write(f"masters = {' '.join(x.repo_id for x in repo.trees)}\n")
        os.makedirs(pjoin(repo_dir, 'profiles'))
        with open(pjoin(repo_dir, 'profiles', 'repo_name'), 'w') as f:
            f.write(f'{repo.repo_id}-old\n')
        super().__init__(repo_dir)

    def add_pkgs(self, pkgs):
        """Update the repo with a given sequence of packages."""
        self._populate(pkgs)
        if self.__created:
            # notify the repo object that new pkgs were added
            for pkg in pkgs:
                self.notify_add_package(pkg)
        self.__created = True

    def _populate(self, pkgs):
        """Populate the repo with a given sequence of historical packages."""
        paths = list({pkg.key for pkg in pkgs})
        old_files = subprocess.Popen(
            ['git', 'archive', 'HEAD'] + paths,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=self.__parent_repo.location)
        if old_files.poll():
            error = old_files.stderr.read().decode().strip()
            raise Exception(f'failed populating archive repo: {error}')
        with tarfile.open(mode='r|', fileobj=old_files.stdout) as tar:
            tar.extractall(path=self.location)


def change(*statuses):
    """Decorator to register change status summary methods."""

    class decorator:
        """Decorator with access to the class of a decorated function."""

        def __init__(self, func):
            self.func = func

        def __set_name__(self, owner, name):
            owner.status_funcs[frozenset(statuses)] = self.func
            setattr(owner, name, self.func)

    return decorator


class ChangeSummary:
    """Generic summary generation support for git changes."""

    # mapping of handled statuses to functions
    status_funcs = None

    def __init__(self, options):
        self.options = options
        self.repo = options.repo

    @jit_attr
    def old_repo(self):
        """Create a repository of historical packages removed from git."""
        return _HistoricalRepo(self.repo)

    def generate(self):
        """Generate summaries for the package changes."""
        statuses = frozenset(x.status for x in self.changes.values())
        try:
            return self.status_funcs[statuses](self)
        except KeyError:
            pass


class MetadataSummary(ChangeSummary):
    """Summary generation support for metadata.xml changes."""

    status_funcs = {}

    def __init__(self, options, changes):
        super().__init__(options)
        self.changes = {x.atom: x for x in changes}

    @change('M')
    def modify(self):
        """Generate summaries for modify actions."""
        atom = next(iter(self.changes))
        self.old_repo.add_pkgs([atom])
        try:
            old_pkg = self.old_repo.match(atom)[0]
            new_pkg = self.repo.match(atom)[0]
        except IndexError:
            return

        if old_pkg.maintainers != new_pkg.maintainers:
            new = {x.email for x in new_pkg.maintainers}
            old = {x.email for x in old_pkg.maintainers}
            p = git.run('config', 'user.email', stdout=subprocess.PIPE)
            git_email = p.stdout.strip()
            if git_email in new - old:
                return 'add myself as a maintainer'
            if git_email in old - new:
                return 'drop myself as a maintainer'
            return 'update maintainers'
        elif old_pkg.stabilize_allarches != new_pkg.stabilize_allarches:
            status = 'mark' if new_pkg.stabilize_allarches else 'drop'
            return f'{status} ALLARCHES'
        elif old_pkg.upstreams != new_pkg.upstreams:
            new = set(new_pkg.upstreams)
            old = set(old_pkg.upstreams)
            added = new - old
            removed = old - new
            msg = []
            for action, data in (('add', added), ('remove', removed)):
                if data:
                    upstreams = [x.type for x in data]
                    msg.append(f"{action} {', '.join(upstreams)} upstream metadata")
            # return action-specific shorter summary if a single type exists
            if len(msg) == 1 and len(msg[0]) <= 50:
                return msg[0]
            return 'update upstream metadata'


class PkgSummary(ChangeSummary):
    """Summary generation support for single package ebuild changes."""

    status_funcs = {}

    def __init__(self, options, changes):
        super().__init__(options)
        self.changes = {x.atom: x for x in changes}

    @jit_attr
    def versions(self):
        """Tuple of package versions that were changed."""
        return tuple(x.fullver for x in sorted(self.changes))

    @jit_attr
    def revbump(self):
        """Boolean for any package changes involving version revisions."""
        return any(x.revision for x in self.changes)

    @jit_attr
    def existing(self):
        """Existing packages in the tree related to the package."""
        return tuple(self.repo.match(next(iter(self.changes)).unversioned_atom))

    @change('A')
    def add(self):
        """Generate summaries for add actions."""
        if len(self.existing) == len(self.changes):
            return 'initial import'
        elif not self.revbump:
            msg = f"add {', '.join(self.versions)}"
            if len(self.versions) == 1 or len(msg) <= 50:
                return msg
            return 'add versions'
        elif len(self.changes) == 1:
            # adding a new revbump
            atom = next(iter(self.changes))
            # assume revbump was based on the previous version
            pkgs = sorted(x for x in self.repo.match(atom.unversioned_atom) if x <= atom)
            try:
                old_pkg, new_pkg = pkgs[-2:]
            except ValueError:
                # probably a broken ebuild
                return

            if old_pkg.eapi in new_pkg.eapi.inherits[1:]:
                return f'update EAPI {old_pkg.eapi} -> {new_pkg.eapi}'

    @change('D')
    def remove(self):
        """Generate summaries for remove actions."""
        if self.existing:
            msg = f"drop {', '.join(self.versions)}"
            if len(self.versions) == 1 or len(msg) <= 50:
                return msg
            return 'drop versions'
        return 'treeclean'

    @change('R')
    def rename(self):
        """Generate summaries for rename actions."""
        if len(self.changes) == 1 and not self.revbump:
            # handle single, non-revbump `git mv` changes
            change = next(iter(self.changes.values()))
            return f'add {change.atom.fullver}, drop {change.old.fullver}'

    @change('M')
    def modify(self):
        """Generate summaries for modify actions."""
        if len(self.changes) == 1:
            atom = next(iter(self.changes))
            self.old_repo.add_pkgs([atom])
            try:
                old_pkg = self.old_repo.match(atom)[0]
                new_pkg = self.repo.match(atom)[0]
            except IndexError:
                return

            if old_pkg.eapi in new_pkg.eapi.inherits[1:]:
                return f'update EAPI {old_pkg.eapi} -> {new_pkg.eapi}'
            elif new_pkg.keywords != old_pkg.keywords:
                new_keywords = set(new_pkg.keywords)
                old_keywords = set(old_pkg.keywords)
                added = new_keywords - old_keywords
                removed = old_keywords - new_keywords
                if removed == {f'~{x}' for x in added}:
                    action = f'stabilize {atom.fullver}'
                    msg = f"{action} for {', '.join(sorted(added))}"
                elif not removed and all(x.startswith('~') for x in added):
                    action = f'keyword {atom.fullver}'
                    msg = f"{action} for {', '.join(sorted(added))}"
                elif removed == {x.lstrip('~') for x in added}:
                    action = f'destabilize {atom.fullver}'
                    msg = f"{action} for {', '.join(sorted(added))}"
                elif not added:
                    action = f'unkeyword {atom.fullver}'
                    msg = f"{action} for {', '.join(sorted(removed))}"

                if len(msg) <= 50:
                    return msg
                return action


class GitChanges(UserDict):
    """Mapping of change objects for staged git changes."""

    def __init__(self, options, changes):
        super().__init__(changes)
        self._options = options
        self._repo = options.repo

    @jit_attr
    def pkg_changes(self):
        """Ordered set of all package change objects."""
        return OrderedFrozenSet(self.data.get(PkgChange, ()))

    @jit_attr
    def ebuild_changes(self):
        """Ordered set of all ebuild change objects."""
        return OrderedFrozenSet(x for x in self.pkg_changes if x.ebuild)

    @jit_attr
    def paths(self):
        """Ordered set of all staged paths."""
        return OrderedFrozenSet(x.path for x in chain.from_iterable(self.data.values()))

    @jit_attr
    def prefix(self):
        """Determine commit message prefix using GLEP 66 as a guide.

        See https://www.gentoo.org/glep/glep-0066.html#commit-messages for
        details.
        """
        # changes limited to a single type
        if len(self.data) == 1:
            change_type, change_objs = next(iter(self.data.items()))
            if len(change_objs) == 1:
                # changes limited to a single object
                return change_objs[0].prefix
            else:
                # multiple changes of the same object type
                common_path = os.path.commonpath(x.path for x in change_objs)
                if change_type is PkgChange:
                    if os.sep in common_path:
                        return f'{common_path}: '
                    elif common_path:
                        return f'{common_path}/*: '
                    return '*/*: '
                elif common_path:
                    return f'{common_path}: '

        # no prefix used for global changes
        return ''

    @jit_attr
    def summary(self):
        """Determine commit message summary."""
        # all changes made on the same package
        if len({x.atom.unversioned_atom for x in self.pkg_changes}) == 1:
            if not self.ebuild_changes:
                if len(self.pkg_changes) == 1:
                    if self.pkg_changes[0].path.endswith('/Manifest'):
                        return 'update Manifest'
                    elif self.pkg_changes[0].path.endswith('/metadata.xml'):
                        if summary := MetadataSummary(self._options, self.pkg_changes).generate():
                            return summary
            elif summary := PkgSummary(self._options, self.ebuild_changes).generate():
                return summary
        return ''


@dataclass(frozen=True)
class Change:
    """Generic file change."""
    status: str
    path: str

    @property
    def prefix(self):
        if os.sep in self.path:
            # use change path's parent directory
            return f'{os.path.dirname(self.path)}: '
        # use repo root file name
        return f'{self.path}: '


@dataclass(frozen=True)
class EclassChange(Change):
    """Eclass change."""
    name: str

    @property
    def prefix(self):
        return f'{self.name}: '


@dataclass(frozen=True)
class PkgChange(Change):
    """Package change."""
    atom: atom_cls
    ebuild: bool
    old: atom_cls = None

    @property
    def prefix(self):
        return f'{self.atom.unversioned_atom}: '


def determine_changes(options):
    """Determine changes staged in git."""
    # stage changes as requested
    if options.git_add_arg:
        git.run('add', options.git_add_arg, options.cwd)

    # determine staged changes
    p = git.run(
        'diff', '--name-status', '--cached', '-z',
        stdout=subprocess.PIPE)

    # ebuild path regex, validation is handled on instantiation
    _ebuild_re = re.compile(r'^(?P<category>[^/]+)/[^/]+/(?P<package>[^/]+)\.ebuild$')
    _eclass_re = re.compile(r'^eclass/(?P<name>[^/]+\.eclass)$')

    # if no changes exist, exit early
    if not p.stdout:
        commit.error('no staged changes exist')

    data = deque(p.stdout.strip('\x00').split('\x00'))
    changes = defaultdict(OrderedSet)
    while data:
        status = data.popleft()
        old_path = None
        if status.startswith('R'):
            status = 'R'
            old_path = data.popleft()
        path = data.popleft()
        path_components = path.split(os.sep)
        if path_components[0] in options.repo.categories and len(path_components) > 2:
            if mo := _ebuild_re.match(path):
                # ebuild changes
                try:
                    atom = atom_cls(f"={mo.group('category')}/{mo.group('package')}")
                    old = None
                    if status == 'R' and (om := _ebuild_re.match(old_path)):
                        old = atom_cls(f"={om.group('category')}/{om.group('package')}")
                    changes[PkgChange].add(PkgChange(
                        status, path, atom=atom, ebuild=True, old=old))
                except MalformedAtom:
                    continue
            else:
                # non-ebuild package level changes
                atom = atom_cls(os.sep.join(path_components[:2]))
                changes[PkgChange].add(PkgChange(status, path, atom=atom, ebuild=False))
        elif mo := _eclass_re.match(path):
            changes[EclassChange].add(EclassChange(status, path, name=mo.group('name')))
        else:
            changes[path_components[0]].add(Change(status, path))

    return GitChanges(options, changes)


def determine_msg_args(options, changes):
    """Determine message-related arguments used with `git commit`."""
    args = []
    if options.file:
        args.extend(['-F', options.file])
    elif options.template:
        args.extend(['-t', options.template])
    else:
        if options.message_template:
            message = options.message_template.read().splitlines()
            try:
                # TODO: replace with str.removeprefix when py3.8 support dropped
                if message[0].startswith('*: '):
                    message[0] = message[0][3:]
            except IndexError:
                commit.error(f'empty message template: {options.message_template.name!r}')
        else:
            message = [] if options.message is None else options.message

        # determine commit message
        if message:
            # ignore generated prefix when using custom prefix
            if not re.match(r'^\S+: ', message[0]):
                message[0] = changes.prefix + message[0]
        elif changes.prefix:
            # use generated summary if a generated prefix exists
            message.append(changes.prefix + changes.summary)

        if message or options.footer:
            tmp = tempfile.NamedTemporaryFile(mode='w')
            tmp.write(message[0])
            if len(message) > 1:
                # wrap body paragraphs at 85 chars
                body = ('\n'.join(textwrap.wrap(x, width=85)) for x in message[1:])
                tmp.write('\n\n' + '\n\n'.join(body))

            # add footer tags
            if options.footer:
                tmp.write('\n\n')
                for tag, url in options.footer:
                    tmp.write(f'{tag}: {url}\n')

            tmp.flush()

            # force `git commit` to open an editor for uncompleted summary
            if not message[0] or message[0].endswith(' '):
                args.extend(['-t', tmp.name])
            else:
                args.extend(['-F', tmp.name])

            # explicitly close and delete tempfile on exit
            atexit.register(tmp.close)

    return args


@commit.bind_final_check
def _commit_validate(parser, namespace):
    # flag for testing if running under the gentoo repo
    namespace.gentoo_repo = namespace.repo.repo_id == 'gentoo'

    # mangle files in the gentoo repo by default
    if namespace.mangle is None and namespace.gentoo_repo:
        namespace.mangle = True

    # determine `pkgcheck scan` args
    namespace.scan_args = ['-v'] * namespace.verbosity
    if namespace.pkgcheck_scan:
        namespace.scan_args.extend(shlex.split(namespace.pkgcheck_scan))
    namespace.scan_args.extend(['--exit', 'GentooCI', '--staged'])

    # assume signed commits means also requiring signoffs
    if namespace.repo.config.sign_commits:
        namespace.commit_args.extend(['--signoff', '--gpg-sign'])


@commit.bind_main_func
def _commit(options, out, err):
    repo = options.repo
    git_add_files = []
    # determine changes from staged files
    changes = determine_changes(options)

    if atoms := {x.atom.unversioned_atom for x in changes.ebuild_changes}:
        # manifest all changed packages
        failed = repo.operations.digests(
            domain=options.domain,
            restriction=packages.OrRestriction(*atoms),
            observer=observer_mod.formatter_output(out))
        if any(failed):
            return 1

        # include existing Manifest files for staging
        manifests = (pjoin(repo.location, f'{x.cpvstr}/Manifest') for x in atoms)
        git_add_files.extend(filter(os.path.exists, manifests))

    # mangle files
    if options.mangle:
        # don't mangle FILESDIR content
        skip_regex = re.compile(rf'^{repo.location}/[^/]+/[^/]+/files/.+$')
        mangler = GentooMangler if options.gentoo_repo else Mangler
        paths = (pjoin(repo.location, x) for x in changes.paths)
        git_add_files.extend(mangler(paths, skip_regex=skip_regex))

    # stage modified files
    if git_add_files:
        git.run('add', *git_add_files, cwd=repo.location)

    # scan staged changes for QA issues if requested
    if options.scan:
        pipe = scan(options.scan_args)
        with reporters.FancyReporter(out) as reporter:
            for result in pipe:
                reporter.report(result)
        # fail on errors unless they're ignored
        if pipe.errors:
            with reporters.FancyReporter(out) as reporter:
                out.write(out.bold, out.fg('red'), '\nFAILURES', out.reset)
                for result in sorted(pipe.errors):
                    reporter.report(result)
            if not (options.ask and userquery('Create commit anyway?', out, err)):
                return 1

    # determine message-related args
    args = determine_msg_args(options, changes)
    # create commit
    git.run('commit', *args, *options.commit_args)

    return 0
