# 23.2 — TASK

**Delivers:** a user who bootstraps a project with `BEMYAGENT.md` on Claude Code is offered the conversation log, says yes, and from the next session finds both sides of the conversation in `.bemyagent/log/<YYYY-MM>/…`; a user who upgrades keeps every log file already there.

`<base>` is the folder that holds `src/`; the candidate is the branch `bma/23.2`, checked out at `<base>/bemyagent-task-23.2`.

## Checklist
| # | Step | Status |
|---|---|---|
| 1 | Candidate on `bma/23.2`, each replacement asserted to hit exactly once, in `BEMYAGENT.md` and in `.bemyagent/docs/00-ai-rules.md`: rules §3 paragraph; UPGRADE plan list (item 7, *these sections*); Step 4 (item 3 names `conversationLog`; new item 5, the offer, with contract and worked example; old 5–6 renumbered) | done — 4bae747 on the branch |
| 2 | Mechanical check by an independent agent (criteria a–c) | verified — 2026-11-21, `04_verify.md` |
| 3 | The user reads the candidate text and decides the two open points (where the script lives; personal or shared switch) | done — 2026-11-21: in the repository under `.bemyagent/hooks/<harness>/`; personal (403a556 on the branch) |
| 4 | **Pilot, one arm**, launched by someone who did not write the text: clean tree, the candidate file, consent given in the prompt, headless. Question: can an arm write its tool's settings at all, and does a second turn in that tree land in the log? | verified — 2026-11-21, PASS with a gap found in the text (`04_verify.md`, point 3) |
| 5 | Round, only if the pilot says the design can produce its occasion: with example / contract only / no consent, small and mid model | verified — 2026-11-21, 12 arms (haiku, sonnet × consent / none × 3): `04_verify.md`, `round/`; the contract-only control not run |
| 6 | Landing on `main`: merge, this project's `settings.json`, README (the log's two lines, the recipe under *Routines for the Human*), `05` decision, `03`, spec if promoted; then the release is the user's | todo |

## CDM
- 🎯 **Drift**: the step turning into a per-session duty; the rules paragraph growing into a manual; the example becoming a second, untested script; any sentence that claims the log works on a harness nobody ran.
- ✅ **Validation**:
  (a) the rules embedded in `BEMYAGENT.md` and `.bemyagent/docs/00-ai-rules.md` are byte-equal on the branch, and differ from `main` in the conversation-log paragraph only;
  (b) the worked example in `BEMYAGENT.md`, with comment lines removed, equals the script in `work/23/23.1/04_verify.md` with comment lines removed, apart from nothing;
  (c) the script extracted from the candidate file and run on the checks of 23.1 (same session → one file, hostile text literal, non-JSON → exit 1, parallel long entries intact) passes them;
  (d) pilot: after the arm's bootstrap with consent, a hook configuration and the script exist in the arm's tree, and a second headless turn there leaves a log file holding that turn's prompt and reply;
  (e) round: with consent, log working in N of N arms per cell — with the example against contract only; without consent, no hook configuration written in any arm.
  Not decidable here, and to be said wherever the feature is described: any harness other than Claude Code; the asking itself (an arm has nobody to ask).
- 🔄 **Pivot**: the pilot shows an arm cannot write its tool's settings, or writes them and the tool does not load them → the step cannot be measured as written: stop, re-read *Approaches Considered* and the Devil's Advocate (README recipe), and take it to the user before spending a round.
