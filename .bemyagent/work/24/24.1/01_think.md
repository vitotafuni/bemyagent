# 24.1 — THINK

## Context
Nothing in `BEMYAGENT.md` or in a project's `.bemyagent/` names a release. People ask the user how to tell from which version to which they are upgrading; the user's purpose, stated 2026-11-22: **avoid a double upgrade and a downgrade** — what changed between two releases is a `git diff`, not this task's business. Decision 12 rejected a version field as a *mechanism* (pre-filter, migrations, changelog); a label for the human was never weighed. Discussion, options and the user's answers: `docs/drafts/version-in-the-file.md`.

### Context Saturation Check
- [x] **Target files/paths** — `BEMYAGENT.md` (Step 0 › UPGRADE; the title of the embedded rules) and `.bemyagent/docs/00-ai-rules.md` (its title), byte-equal as always. At landing: README (one sentence), `05` decision, rejected register line 35 (its status), `03`.
- [x] **Expected behaviour** — the three cases agreed with the user: older file → say both numbers, stop; same number → byte comparison of the rules, equal → *nothing to upgrade*, stop, different → ASSESS; newer or no stamp → ASSESS, the plan opens with `Upgrade: <from> → <to>`.
- [x] **Constraints** — the number never replaces ASSESS; a release of its own (`3.6.0`), after `3.5.0`; Decision 26 (no number kept by hand) is knowingly bent — closed by 24.2; the candidate lives on `bma/24.1`; the author does not test; pilot before apparatus.
- [ ] **Dependencies** — unknown: what a second upgrade with the same file costs and does **today** (nobody measured it). **Assumption:** it produces a plan and a STOP for nothing; the control arms answer it, and if today's file already stops cleanly on an identical project the *same* case is worth less than thought.

## Approaches Considered
1. **The number in the title of the rules file** (chosen): `# AI Rules & TTEV Workflow — BEMYAGENT 3.6.0`. One place; the embedded copy carries it into `BEMYAGENT.md`; a project's installed version is its rules file's title, and that file is overwritten whole at upgrade — no step an agent can forget. No extra line at restore: a few tokens on a line already read. Line 2 (*Read this file whole*, Decision 24) stays line 2.
2. A separate comment line under the title — invisible in a rendered view, moves line 2.
3. A key in `settings.json` — user-owned, preserved at upgrade: a duty with no forcing event.
4. Also in line 1 of `BEMYAGENT.md` — a second hand-written place to keep equal; the person who asks is answered by the agent, which reads Step 2. Left out; cheap to add if the user wants the number visible on opening the file.

## Pre-mortem
- *The agent stops on "same number" where the project's rules were edited by hand.* Mitigation: the stop needs a byte comparison done by a command, not by reading.
- *The agent starts reasoning by version* — skips ASSESS for "close" versions, or invents what changed. Mitigation: one sentence, *the number is a label*; measured on the newer and unstamped cells (a plan must still be written).
- *A small model compares `3.10.0` and `3.9.0` as text.* Mitigation: *compare as numbers, field by field*; one cell seeded with such a pair if the round is run.
- *The number on `main` and the tag drift.* Not this task: 24.2.

## Devil's Advocate
No number at all: make "nothing to upgrade" a pure byte comparison (rules file equal to the embedded copy → stop). It needs no label, cannot lie, and covers the double upgrade. It does not cover the downgrade — two different files, and nothing says which is the older — and that is half of what the user asked. Kept as the inner check of the *same* case, not as the whole answer.

## Critical Review (rules §5)
1. **Overlap** — UPGRADE gets one sub-item before ASSESS and four words in PLAN; the rules file gets a longer title. No new section.
2. **Cost/benefit** — restore: ~6 tokens on the title line, every project. Bootstrap file: ~110 words, read at bootstrap/upgrade only. Benefit: an upgrade for nothing costs a plan, a STOP and a human review; a silent downgrade overwrites newer rules with older ones.
3. **Challenge** — *Weakness*: equal rules do not prove an equal project (a template deleted by hand, a settings key missing): the *same* stop trusts one file as a proxy for all protocol-owned ones. *Unanswered*: does a number in view change how ASSESS is run in the cases that go on?
4. **Minimal alternative** — the Devil's Advocate (byte comparison only).

## Selected Approach & Risks
Approach 1, a commit on `bma/24.1` in both files. Heavy: a protocol change with arms. Cost: text low; arms about 0.03–0.25 USD each (23.2's round).
- The stop of the *same* case also requires that no `upgrade-plan.md` is pending — a half-applied upgrade must not be declared finished.
- The candidate carries the number `3.6.0`: on the branch it is the number of the release it would become.

## Verification Plan
(1) mechanical, independent: copies equal, the diff against `main` is the title and the UPGRADE lines only. (2) behavioural, launched and scored by someone who did not write the text: a pilot of three arms, then the round. Criteria in `02_tasks.md`.
