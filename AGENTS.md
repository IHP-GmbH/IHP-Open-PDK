# Instructions for AI coding agents

This file is read by Claude Code (via `CLAUDE.md`), Gemini CLI (via
`GEMINI.md`) and other agents that support `AGENTS.md`. Review-time
guidance for GitHub Copilot is in `.github/copilot-instructions.md`.

The rules for this repository are in [CONTRIBUTING.md](CONTRIBUTING.md).
Follow them; this file only adds what an agent needs while editing.

## Before you change anything

- Identify which PDK a path belongs to (`ihp-sg13g2`, `ihp-sg13cmos5l`)
  or whether it is shared (`ihp-common`). Section "Repository structure
  and multi-PDK rules" in CONTRIBUTING.md decides where a file may go.
- Many paths under `ihp-sg13cmos5l` are symlinks into `ihp-sg13g2`. Run
  `readlink -f <path>` before editing: a change to the link target
  changes both PDKs. Say so in the commit message and test both.
- Do not create new symlinks between PDK directories. Shared content goes
  to `ihp-common`.
- Files under `libs.ref/**` (GDS, CDL, LEF, LIB, Verilog) and device
  models under `libs.tech/*/models` are foundry data. Do not edit their
  values; only move or rename them when a rule requires it.
- `versions.txt` pins the tool versions for the whole repository. Do not
  change it as a side effect of another change.
- Submodules (`.gitmodules`) are bumped in their own commit. Do not
  include a changed submodule pointer in an unrelated commit.

## Building and testing

There is exactly one Makefile, in the repository root; run `make` from
there. Targets act on `$(PDK)`, default `ihp-sg13g2`:

    make help PDK=ihp-sg13cmos5l         # what the PDK offers
    make env                             # Python venv in ./actions_venv
    make lint PDK=ihp-sg13g2             # flake8 on the DRC/LVS scripts
    make test-DRC-main PDK=ihp-sg13g2
    make test-LVS-main PDK=ihp-sg13cmos5l

Shared targets: `lint`, `test-DRC-main`, `test-DRC-cells`,
`test-LVS-main`, `test-LVS-cells`, `test-LVS-switch`, `test-SRAM`. A
target a PDK does not carry prints a notice and succeeds; check the
output, a green run may have run nothing. PDK-specific targets are in
`Makefile.<pdk>`.

CI additionally rejects broken symlinks anywhere in the repository and
non-ASCII characters in the KLayout PCell libraries.

## Writing code

- New source files carry the Apache-2.0 header used throughout the
  repository (copy it from a neighbouring file, keep the comment style of
  that file type).
- Python: flake8 with `max-line-length = 120` (see `.flake8`). ASCII only
  in `libs.tech/klayout/python/**`.
- Match the conventions of the directory you are in; the tool directories
  under `libs.tech` differ from each other on purpose.

## Committing

- Follow section "Commit messages" in CONTRIBUTING.md: path-prefixed
  title, body that explains the problem.
- Exactly two kinds of trailer are allowed at the end of a commit
  message:
  - `Co-Authored-By: <model name> <noreply@...>` for the model that
    helped, optional;
  - `Signed-off-by: <name> <e-mail>` of the human contributor
    (`git commit -s`), mandatory and always the last line. It is the
    contributor's DCO statement and belongs to a person, never to a tool.
- Nothing else: no session or generation tags, no "Generated with ..."
  footer, no links to the agent or its vendor. This applies to commit
  messages and pull request descriptions alike.
- One logical change per commit; never merge the target branch into a
  feature branch.
- Add a `CHANGELOG.md` entry, naming the PDK, for user-visible changes.
