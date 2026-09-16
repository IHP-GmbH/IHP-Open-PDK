# How to Contribute

We'd love to accept your patches and contributions to this project.
There are just a few small guidelines you need to follow.

## Developer Certificate of Origin

Contributions to this project must be accompanied by a Developer 
Certificate of Origin statement agreement. You (or your employer) retain the copyright to your
contribution; this simply gives us permission to use and redistribute
your contributions as part of the project. Head over to
[https://developercertificate.org](https://developercertificate.org)
to see the text of the agreement. When you're signin-off your update it means that you agree with the 
Developer Certificate of Origin statements.

## Code reviews

All submissions, including submissions by project members, require review.
We use GitHub pull requests for this purpose.
Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

## Commit messages

Every commit must be self-contained and describe one logical change. A
reviewer (or a future reader running `git log`/`git blame`) should be able to
understand *what* changed and *why* from the commit message alone, without
opening the pull request.

A commit message consists of a title, a blank line, a body and the trailers:

```
ihp-sg13g2: libs.tech: klayout: Fix LVS extraction of dantenna contact

The "cifinput" section of the tech file reads the dantenna contact on the
wrong plane. In some layouts the contact is missing on metal1, so the
dantenna device becomes disconnected in the extracted netlist and LVS of
the analog I/O pad cell fails.

Read the contact on the metal1 plane like the other diode contacts.

Fixes #1208
Signed-off-by: Jane Doe <jane.doe@example.com>
```

### Title

* Prefix the title with the path of the changed component, separated by
  `: `, so the affected PDK and tool are visible at a glance:
  `ihp-sg13cmos5l: libs.tech: ngspice: ...`,
  `ihp-common: ...`, `.github: workflows: ...`, `docs: ...`.
  Use `ihp-sg13*:` when the change touches both PDKs in the same way.
* After the prefix, summarise the change in the imperative mood
  ("Fix", "Add", "Remove", not "Fixed" or "Adds"), starting with a capital
  letter and without a trailing period.
* Keep the whole title at 72 characters or less.

### Body

* Describe the **problem** first: what is wrong, how it shows up, which
  tool or device is affected. Then describe **what** the commit does and,
  if it is not obvious, **why** this solution was chosen over alternatives.
* Do not repeat the diff. Explain the motivation and the consequences
  instead; the code already shows what was changed line by line.
* Wrap lines at 72 characters.
* Trivial changes (typo, whitespace) may omit the body.

### Trailers

* Reference related issues at the end of the body with `Fixes #123`
  (closes the issue on merge) or `Related to #123`.
* Every commit must carry a `Signed-off-by:` trailer with your real name
  and e-mail address (`git commit -s`), see
  [Developer Certificate of Origin](#developer-certificate-of-origin).

### History

* Split unrelated changes into separate commits, and squash fix-up commits
  ("Fix typo", "Address review comments") into the commit they belong to
  before the pull request is merged.
* Commits are rebased on the target branch; do not merge the target branch
  into your feature branch.

## Repository structure and multi-PDK rules

This repository hosts several PDKs (`ihp-sg13g2`, `ihp-sg13cmos5l`) next
to each other. Each PDK is shipped on its own: packagers such as Ciel
archive one `ihp-<pdk>` directory and install it as `$PDK`, without the
rest of the repository. The rules below exist so that a change in one
place cannot silently break a packaged PDK.

### Layout

* Every PDK follows the
  [open-pdks format](https://github.com/fossi-foundation/open-pdks#open-pdks-format):
  `libs.doc`, `libs.qa`, `libs.ref/<library>/<format>/` and
  `libs.tech/<tool>/`. Add a new tool as a directory under `libs.tech`;
  do not add new top-level directories to a PDK.
* A PDK directory contains only what a user of that PDK needs. Files that
  serve this repository but not the PDK itself (build rules, CI helpers,
  cross-PDK tests) live in the repository root or in `ihp-common`.
* `ihp-common` holds content shared by more than one PDK. It mirrors the
  PDK layout but is deliberately not a PDK and must never be installable
  as `$PDK`; see [ihp-common/README.md](ihp-common/README.md).
* There is one `Makefile`, in the repository root. Shared regression
  targets go to `ihp-common/pdk.mk`, PDK-specific ones to `Makefile.<pdk>`.
  PDK directories carry no build system.

### Sharing content between PDKs

* Do not copy files from one PDK into another. Content that is identical
  in several PDKs is moved to `ihp-common` and linked from each PDK.
  Content that differs stays in the PDK that owns it.
* Do not add new symlinks from one PDK into another. A PDK that needs a
  file from another PDK is the signal that the file belongs in
  `ihp-common`. The existing links from `ihp-sg13cmos5l` into `ihp-sg13g2`
  are a leftover of the merge and are being migrated; do not extend them.
* Symlinks are relative and point into `ihp-common` (or within the same
  PDK). Absolute paths and links to gitignored build products are not
  accepted; CI rejects every broken link.
* A change to `ihp-common` or to a file that other PDKs link to affects
  every PDK. Run the regression of each affected PDK
  (`make test-... PDK=ihp-<pdk>`) and name the tested PDKs in the pull
  request.

### Repository-wide files

* `versions.txt` pins one version per tool for the whole repository; a
  PDK cannot require a different tool version.
* Git submodules are registered under the PDK that uses them, or under
  `ihp-common` when several PDKs do. Bump a submodule in its own commit.
* User-visible changes get a `CHANGELOG.md` entry that names the affected
  PDK.

## Community Guidelines

This project follows [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
