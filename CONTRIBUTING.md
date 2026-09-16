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

## Community Guidelines

This project follows [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
