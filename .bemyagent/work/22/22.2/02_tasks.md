# 22.2 — TASK

**Delivers:** a visitor reading the README (on GitHub or at bemyagent.md) gets a description that is true of the protocol at `3.4.0`, including how to upgrade.

## Checklist
| # | Step | Status |
|---|---|---|
| 1 | Core Concepts: correct the CDM, Symbiotic Validation and Self-Registration rows; add Session Restore, Discussion Capture, Precedence | done |
| 2 | Settings table under Pacing Modes (the eight fields of the shipped `settings.json`) | done |
| 3 | Usage: what the agent does in an empty workspace, an existing codebase, an existing `.bemyagent/`; subsection *Upgrading* | done |
| 4 | File tree: `settings.json`, `log/`, `micro.log` | done |
| 5 | Harness section: drop *Across three milestones here*; add what has been measured about the protocol as a whole, with its size | done |
| 6 | Build the page; VERIFY by an agent that did not write it; `04_verify.md`; plan row | done — first version PASS_WITH_CAVEATS; rewrite FAIL as written, corrected once (`03_execute.log` [4]) |

## CDM
- ✅ **Validation**: (a) every sentence the diff adds or changes about the protocol is supported by a line of `BEMYAGENT.md` at HEAD — the verifier cites the line; a sentence with no supporting line is a FAIL of that sentence; (b) the settings table has the eight keys and defaults of the shipped `settings.json` block, no more, no fewer; (c) every number in the harness block is in `work/20/20.12/04_verify.md` with the same N, and the block states the fixture's size and the cost; (d) no version number is written in the README; (e) the page builds and each markdown table renders as one HTML table with all its rows; (f) nothing outside the listed steps changed.

## Amendment 1 — 2026-11-18, from the user after reading the first version
The user: *the README must not be too technical, otherwise it equals `BEMYAGENT.md`; it must list the protocol's strengths and let a visitor of the site decide easily whether to use it for their projects.* The first version went the other way (a settings table, three more concept rows). It is replaced by a rewrite — approach 2 of `01_think.md`, now asked for: what it is · the problem (kept) · *What You Get* (nine strengths) · *What It Costs* · *Is It for You?* · *How It Works* (the tree, the two paces, one sentence on settings) · *Get Started* with upgrading · *Is There Evidence?* (the verifier's corrected texts; the harness reduced to a pointer to `harness/README.md`) · the three routines for the human (kept) · contributing · license. Removed: the Core Concepts table, the Settings table, the harness method and inventory (both in `harness/README.md`).
Criteria as amended: (a) unchanged — every statement about the protocol supported by a line of `BEMYAGENT.md`; (b) dropped with the table; (c) unchanged; (d) unchanged; (e) the page builds, the tree is one block, links are absolute (the page is served from another domain); (f) unchanged; **(g) new** — nothing a user needs is lost: each removed passage is either in `BEMYAGENT.md`, in `harness/README.md`, or named in `04_verify.md` as lost. *Is It for You?* and *What It Costs* are the author's judgement, not protocol statements: the verifier reports any that a line of the record contradicts; whether they say what the owner wants said is the owner's reading.

## Amendment 2 — 2026-11-19, from the user after the second VERIFY
The user: *should we not avoid bringing out points against in the README — above all on things we know nothing about yet?* and, asked what *save tokens* means: *less context read, of course — the idea was that the agent must not read the whole project just to start again, but load knowledge selectively and widen it only if necessary.* Recommendation and options in `drafts/readme-tone.md` (option B taken): the strengths carry no hedges but stay true as worded; what is not known is not listed and not claimed; *What It Costs* is removed and the one measured cost stays in the evidence block, with the condition it was measured in; the *no* side of *Is It for You?* becomes what the protocol is not; the bullet on per-turn rules is removed (a sentence about rules not adopted; the false sentence of the second pass goes with it). A sentence under the mission says what *save tokens* means, from the owner's words. Criterion (a) holds for every sentence that remains or is new; none of the nine corrected sentences returns in its earlier form.
