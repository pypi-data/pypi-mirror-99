=============
Release Notes
=============

pkgdev 0.1.2 (2021-03-19)
-------------------------

- pkgdev commit: Support pulling historical data from unconfigured repos.

- Add initial zsh completion support (#16).

pkgdev 0.1.1 (2021-03-12)
-------------------------

- Replace --ignore-failures option with -A/--ask for ``pkgdev commit`` and
  ``pkgdev push``.

- pkgdev push: Drop explicitly enabled --signed option for gentoo repo (#27).

- pkgdev commit: Add support for -b/--bug and -c/--closes options.

- pkgdev commit: Initial support for summary generation for metadata.xml
  changes (#9).

- pkgdev commit: Enabled signed commits and signoffs based on repo metadata
  (#25).

- pkgdev commit: Initial support for generating modify summaries.

- pkgdev commit: Support summary generation for single rename changes that
  don't involve revbumps.

- pkgdev commit: Add -M/--message-template support.

- pkgdev commit: Support multiple -m/--message options similar to ``git
  commit``.

- pkgdev commit: Support generating manifest summaries (#12).

pkgdev 0.1 (2021-03-05)
-----------------------

- Initial release.

- pkgdev commit: Add subcommand wrapping ``git commit`` supporting commit
  message templating, ebuild manifesting, structured file mangling, and commit
  scanning via pkgcheck.

- pkgdev push: Add subcommand wrapping ``git push`` that verifies local commits
  with pkgcheck before pushing them upstream.

- pkgdev manifest: Add subcommand for manifesting ebuilds.
