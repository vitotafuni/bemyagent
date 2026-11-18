# 22.2 — THINK

## Context
The user (2026-11-18): update the README — they believed it followed every step of the protocol. It does not: last changed 2026-08-10, at `3.1.0`; the protocol is at `3.4.0`. The page at bemyagent.md is this file, and since 22.1 it shows `v3.4.0` above it; an announcement is planned.

Read now: `README.md` whole (152 lines); `git diff 3.1.0 HEAD -- BEMYAGENT.md` (22 lines added, 10 changed); the bootstrap steps and the settings block of `BEMYAGENT.md`; `work/20/20.12/04_verify.md` lines 1–30 for the one comparison quoted.

What the protocol gained since the README: discussion capture (3.2.0); evidence of absence and *who verifies*, precedence rules > plan > memory, single registration, conceptual maps keep only the sections a project has, status words, language written into settings (3.2.2, 3.2.3); the optional conversation log (3.3.0); Step 0 branching on content, foreign files, `.bak` kept when changed, *read this file whole* (3.4.0).
What the README never had: Session Restore; the upgrade path; the settings as a list.
What is stale in it: *Micro tasks get none* (they leave a logged line with evidence); the Self-Registration row; *Across three milestones here* in the harness paragraph; the file tree (no `settings.json`, no `micro.log`, no `log/`).

### Context Saturation Check
- [x] **Target files/paths** — `README.md`
- [x] **Expected behavior** — every statement true of `BEMYAGENT.md` at HEAD; the additions above named
- [x] **Constraints** — no version number written by hand (Decision 26); numbers from the record only with their size and their source read (plan, *Where the evidence stands*); the README stays an introduction, not a second copy of the rules
- [x] **Dependencies** — none; the page build is unchanged

## Approaches Considered
1. **Surgical update** (chosen): keep the structure and the voice; correct the stale rows, add three concept rows, a settings table, an *Upgrading* subsection, the tree, and a short *what has been measured* block.
2. **Rewrite around the reset** (the user, 2026-11-06: a context reset is the main mechanism). A better pitch, perhaps — but a new pitch is the author's voice, not a catch-up, and it would go out the same day as an announcement, unread. Left as an idea for the user.
3. **A changelog section in the README.** Duplicates the tags by hand — the thing Decision 26 just refused for the version. Belongs to 22.3 (generated, if at all).

## Pre-mortem
- *A statement about the protocol is slightly wrong* (paraphrase drift). Mitigation: VERIFY reads each changed sentence against `BEMYAGENT.md` by an agent that did not write it.
- *A number is quoted larger than the record holds.* Mitigation: one comparison only, with N, the fixture's size and the cost beside it; the verifier opens the source file.
- *The table breaks in pandoc or on GitHub* (pipes, escapes). Mitigation: build the page and read the HTML tables' row counts.

## Devil's Advocate
Leave the README alone and let the page generate a *what changed* list from the tags (22.3): no hand-written catch-up at all. Not instead: the stale statements (Micro, registration, *three milestones*) stay wrong whatever is generated beside them.

## Selected Approach & Risks
Approach 1. One file, not trivial → Standard. Cost: low-medium.

## Verification Plan
Independent agent, strongest tier (public text, claims about the protocol and one measured number — reading, not mechanics): each changed or added statement against `BEMYAGENT.md` at HEAD and, for the numbers, `work/20/20.12/04_verify.md`; a page build to see the tables render.
