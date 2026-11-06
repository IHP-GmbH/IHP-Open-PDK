# Copilot instructions

This repository hosts the IHP open-source PDKs (`ihp-sg13g2`,
`ihp-sg13cmos5l`) and their shared content (`ihp-common`). The rules for
contributions are in [CONTRIBUTING.md](../CONTRIBUTING.md); read it before
reviewing and treat it as the source of truth. Do not restate it here.

## Reviewing pull requests

Review for the rules in CONTRIBUTING.md, in this order of importance:

1. **Repository structure** (section "Repository structure and multi-PDK
   rules"). Flag:
   - new symlinks from one PDK directory into another PDK directory;
   - absolute symlink targets, or links to gitignored build products;
   - files copied between PDKs instead of shared through `ihp-common`;
   - files in an `ihp-<pdk>/` directory that are not part of the PDK
     (build rules, CI helpers, repository tooling);
   - new top-level directories in a PDK, or tool files outside
     `libs.tech/<tool>/`;
   - Makefiles inside PDK directories.
2. **Cross-PDK impact.** A change to `ihp-common`, or to a file in
   `ihp-sg13g2` that `ihp-sg13cmos5l` reaches through a symlink, affects
   both PDKs. Ask for the tested PDKs to be named if the description does
   not say so.
3. **Commit messages** (section "Commit messages"): title prefixed with the
   component path, imperative summary, body explaining the problem, and a
   `Signed-off-by:` trailer on every commit. Point out fix-up commits that
   should be squashed.
4. **Housekeeping**: a `CHANGELOG.md` entry for user-visible changes, the
   Apache-2.0 license header on new source files, and README/docs updates
   when behaviour a user relies on changes.

## Scope

- Do not review the correctness of device models, measurement data, DRC
  or LVS rule values, or layout geometry. These come from the foundry and
  are verified by the regression workflows, not by review.
- Do not comment on Python style; `flake8` (configured in `.flake8`) and
  the non-ASCII check in CI already cover it.
- Do not treat large generated files (`libs.ref/**`: GDS, CDL, LEF, LIB,
  Verilog) as hand-written code. Check only that they are in the right
  place and named for the right PDK.

## Language

Comments are read by contributors from several companies. Be concrete:
name the file, the rule from CONTRIBUTING.md that is affected, and what
would resolve it.
