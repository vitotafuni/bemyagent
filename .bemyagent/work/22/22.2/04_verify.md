# 22.2 — VERIFY (independent)
**Verdict: PASS_WITH_CAVEATS** — nothing the diff adds contradicts `BEMYAGENT.md`, the settings table and the page are exact, but six added sentences say more than their source (three of them in the harness block, one against the record's own line), and each needs the small rewording below before the README goes out.

Verifier: an agent that did not write the change, holding the diff, `BEMYAGENT.md` (read whole, 306 lines), the criteria and the record. Every line number below was read in this pass. `B:n` = `BEMYAGENT.md` line n; `05:n` = `.bemyagent/docs/05-decisions-and-issues.md` line n; `V:n` = `work/20/20.12/04_verify.md` line n.

## Criteria

| | Criterion | Result | Evidence |
|---|---|---|---|
| (a) | every added/changed sentence about the protocol has a supporting line | **FAIL for 6 sentences (all "partly", none unsupported), PASS for the other 30** | table below |
| (b) | settings table = the shipped block | **PASS** | README 54–61 against `B:146–153`: 8 keys, same order, same 8 defaults (`"en"`, `false`, `false`, `true`, `false`, `2`, `200`, `".bemyagent/log"`); no ninth row |
| (c) | harness numbers are in 20.12 with the same N; fixture size and cost stated | **PASS on the numbers**, with one N the README leaves unstated | 2 of 3: `V:15`, `V:23–24`. "none": `V:17` (test cases added 0/3) — but the *teeth* metric on the control side is 0/2 + 1 n/a (`V:15`, `V:47–48`). ~4×: `V:19`, recomputed 499 k / 123 k = 4.06. Ten-file app: `V:50`; `git ls-files harness/fixture` → 10. Model: `claude-sonnet-5-5` (`V:5`) |
| (d) | no version number in the README | **PASS** | `grep -nE '[0-9]+\.[0-9]+\.[0-9]+' README.md` → no line, exit 1 (absence is what is asked). The only `N.N` is the path `work/1/1.1/` on line 30 |
| (e) | page builds; one HTML table per markdown table, all rows | **PASS** | pandoc 3.1.1 container, exit 0, `<out>/readme.html` 24 676 bytes. 2 `<table>`: 11 `<tr>` (1 head + 10) and 9 `<tr>` (1 head + 8); markdown has 10 and 8 data rows. One `<pre>`, 22 lines, holding `settings.json`, `micro.log`, `04_verify.md`. Tags link `href="https://github.com/vitotafuni/bemyagent/tags"`, HTTP 200, lists `3.4.0` |
| (f) | nothing outside the listed steps changed | **PASS** | `git status --short`: `README.md`, `.bemyagent/docs/06-implementation-plan.md` (row 22.2 reworded, row 22.3 added; its draft exists), untracked `work/22/22.2/` (three files). Nothing outside `.bemyagent/` but the README |

## Sentence by sentence

| README phrase (line) | Source | |
|---|---|---|
| Micro tasks skip the task files and leave one logged line with its evidence (32) | `B:84` | S |
| Standard → Validation; Heavy → Drift, Validation, Pivot (32) | `B:85–89` | S |
| evaluated against the CDM criteria, verdict before results are presented (33) | `B:98–101` | S |
| Evidence … from commands run during verification, never from recollection (33) | `B:98` | S |
| a search that finds nothing is evidence that the thing is missing (33) | `B:98` | S |
| Where a second agent or model is available, the check is run by one that did not do the work (33) | `B:102` | S |
| registers once, in the rule file your tool actually loads (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, …) (34) | `B:33–34` ("Register **once**", "the one the tool loads") | S |
| rebuilds from disk: the plan, the active task's checklist, the last entry of its log (35) | `B:49–50` — that is Quick Resume, "try first"; the log entry is read "if `03_execute.log` exists"; Full Restore reads `01`, `02`, `05` when it is not enough | **P** |
| The rules file is read whole every time, a context compaction included (35) | `B:30` | S |
| verdict / recommendation / comparison → written to `drafts/` in that same response. Conversation is not storage (36) | `B:124` | S |
| Rules > plan > the tool's private memory; a contradicting plan step is a defect of the plan; memory binds nobody else (37) | `B:54` | S |
| **Everything above** lives in `.bemyagent/settings.json` (50) | `B:143–155`, `B:295` — only the pacing and model switches do; "above" also holds the whole Core Concepts table | **P** |
| Edit it, or ask the agent to (50) | `B:289`, `B:295–296` | S |
| `language` — set at bootstrap to the language you are writing in; independent of the chat language (54) | `B:141`, `B:121` | S |
| `interactiveMode` — the two human gates (55) | `B:106` | S |
| `strictVerification` — deep (edge cases, performance, architecture alignment) / light (56) | `B:104` | S |
| `autoModelSwitching` — strongest for THINK and VERIFY, cheaper for mechanical steps, where your tool permits (57) | `B:107` | S |
| `autoCommit` — commit on PASS / propose (58) | `B:109` | S |
| `obstacleThreshold` — obstacles in one task before the agent stops and re-evaluates (59) | `B:89`, `B:289` (source: obstacles *exceed* the threshold) | S |
| `contextSlicingThreshold` — lines above which a doc is searched in slices (60) | `B:68` | S |
| `conversationLog` — optional log of your messages, written by your harness (a prompt hook, a transcript converter), never by the agent; `""` = off (61) | `B:70` | S |
| empty workspace: asks what you are building before it creates anything (72) | `B:20` ("Create nothing before that") | S |
| existing codebase: shallow scan, fills the docs from what it finds (72) | `B:19` | S |
| Where a `.bemyagent/` **with content** already exists, it runs an upgrade (72) | `B:12` — content means a `docs/` or `work/` file or a file the protocol does not name; a folder holding only `settings.json` is *not* an upgrade | **P** |
| compares … writes `upgrade-plan.md` as a checklist and stops; you tick what to apply (76) | `B:13–15` | S |
| Protocol files (`00-ai-rules.md`, the templates) are overwritten, with a backup (76) | `B:14`, `B:15` ("Backup before overwrite (`file.bak-YYYYMMDD`)"), `B:17`, `B:18` | S |
| keep your own rules in `05-…` and your tool's rule file, which an upgrade never overwrites (76) | `B:18` | S |
| Files … the protocol does not name are listed and left alone (76) | `B:14` ("list it, never touch it") | S |
| a tag is cut only when `BEMYAGENT.md` itself changes (78) | `05:185` ("iff `BEMYAGENT.md` changed since the last tag") | S |
| tree: `settings.json`, `log/` optional, `micro.log` one line per trivial task with its evidence, `04_verify.md` Validation report (109–129) | `B:143`, `B:153` + `B:70`, `B:84`, `B:95` | S |
| Most rules proposed here did not survive measurement — several inert, one … worse before it was reworked (142–144) | `05:21` (2 of 5 survived), `05:22` (1 of 3), `05:132` + `05:222` (the harmful first draft, reworded); `decisions/rejected.md` tallied now: 10 measured-null, 4 harm, 6 under-powered against a handful of measured landings. No sentence in the record states the tally; the count carries "most" | S |
| On controls certified to contain no protocol text (149) | `V:14`, `V:23`; what the certificate reads: `work/20/20.11/04_verify.md` 36–40 | S |
| a mid-tier model **working with the protocol** left behind a test … in 2 of 3 runs; without the protocol, none of the runs did (149–151) | `V:15`, `V:23–24`. Left out: the protocol runs were *told* "Read BEMYAGENT.md … and follow it" with a standing approval (`work/20/20.3/prompt_P.txt`; `V:44–46` "the whole package against a bare tree"), and with the protocol installed and the prompt silent 0 of 3 wrote a test (`work/20/20.11/04_verify.md` 47–49, "recorded, not read"). Control side on teeth is 0/2 + 1 n/a | **P** |
| a test that catches a deliberately introduced bug (150) | `V:15–16`, `V:50` ("two specific tally mutations", agreeing per arm) | S |
| It cost about 4× the tokens (151) | `V:19`, `V:39` | S |
| runs without it **often verified thoroughly and left nothing behind** (153–155) | `05:415` (three arms, another round, strong tier: two verified live, the third *wrote three tests* — so not "nothing"); `05:491` (one arm "the most thorough in the round", another named the omission). First half of the bullet is `05:415` verbatim. Nothing read here says it of 20.12's own controls | **P** |
| A rule telling the agent **to do something at every reply** measures near zero without a mechanism (156) | `B:70` ("a rule telling an agent to *append every turn* measures at ~0"); `05:248` (two per-turn *writes*, 0 of 9 and 0 of 10); **`05:541`: "'Every reply' has never been measured as a forced output — only as an off-screen append"** | **P — outruns** |
| which is why the conversation log is written by a hook, not by the agent (157–158) | `B:70` ("written by your harness — never by you"; a hook is one example), `05:249` | S |

## Must-fix, with proposed text

1. **Line 156–158.** → `A rule telling the agent to append to a file at every turn measured zero — twice, on two different rules — which is why the conversation log is written by your tooling (a hook, for instance), not by the agent.`
2. **Line 149–152.** → `On controls certified to contain no protocol text, a mid-tier model told to read the protocol file and follow it left behind a test that catches a deliberately introduced bug in 2 of 3 runs; without the protocol, none of the three runs added a test. It cost about 4× the tokens. With the protocol installed and the prompt not mentioning it, a single unplanned set of three ran the ceremony and wrote no test.` (The last sentence is the author's and the user's call; without it, "working with the protocol" reads as ordinary use, which the record measured once at 0 of 3.)
3. **Line 153–155.** → `What the protocol changed is whether the check **stays in the repository**, not whether the work was checked: in earlier rounds the runs without it were not careless — some checked the running app more thoroughly than any protocol run — and their checks ended with the session.`
4. **Line 50.** → `The switches named above, and a few more, live in `.bemyagent/settings.json`. Edit it, or ask the agent to.`
5. **Line 35.** → `A new session — or one that lost its context — rebuilds from disk: first the plan, the active task's checklist and the last entry of its log, the wider docs only if that is not enough.`
6. **Line 72.** → `Where a `.bemyagent/` already holds docs or work files, it runs an **upgrade**.`

## Stale in the unchanged text

- **Line 173–174**, "`fixture/` … ~120 lines": the tracked fixture is 10 files and 469 lines without its README (493 with it); `server/session.js` alone is 309 and entered on 2026-09-11, after the README's last edit. It now sits thirty lines under "one ten-file app". → `~470 lines in ten files`.
- **Line 135**, "`harness/` is never referenced by it": true of the path, but `B:70` now says "written by your harness", and the README repeats "your harness" at lines 61 and 121 in that other sense — the user's tool — a hundred lines before a section that says `harness/` is "not shipped to you". A first-time reader will join the two. → at 61 and 121 write `your tool` / `your tooling`; or at 135 `the `harness/` folder is never referenced by it`.
- **Line 28**, TTEV row, "self-validates before notifying the human": `B:102` now calls the author's own check the weakest available and asks for a verifier that did not do the work. The diff took "Self-" out of the tree comment (129) and out of row 33, and left it here. → `executes, and validates the result before notifying the human`.
- **Line 97**, "`.bemyagent/` is tracked in git by default": no line of `BEMYAGENT.md` says so (`grep -niE 'gitignore|tracked'` → no line). It predates this change; what is new is that the default `conversationLog` puts the user's messages, as received, under that tracked folder (`B:70`, `B:153`). Worth a clause: `…may `.gitignore` `work/` — and `log/`, which holds your messages verbatim.`
- **Line 32**, "scaled by complexity": `B:83` sizes the ceremony "by the files the task intends to touch". Loose, not false (Heavy also names "complex/repetitive logic", `B:86`). No change required.
- **Line 78**, minor: the rule is `05:185` and dates from Decision 23; the public tags page still carries one earlier tag with no protocol change (`git diff 3.2.0 3.2.1 -- BEMYAGENT.md` → empty). `a new tag is cut only when…` would be exact.

Not a README matter, seen while reading: `B:14` announces "5 sections" and lists six; and names "5. Self-Registration files to regenerate" while `B:18` says the tool's rule file is never overwritten.

## What could not be checked

- How GitHub renders the README (only the pandoc page was built), and the live site.
- Whether 20.12's numbers are themselves right: the file was read, its instruments were not re-run, and the arm trees and transcripts are not in the repository.
- "Mid-tier" as a description of the served model: the record gives the model's name, not its tier.
- The built page was read as HTML, not seen in a browser.

## Second pass — the rewrite (independent), 2026-11-18
**Verdict: FAIL** — the page builds, links, scope and numbers are right, but one sentence of the evidence section is false against `BEMYAGENT.md` line 94, the first strength leans on that same rule, and seven more sentences say more than their source; all nine are small rewordings (below), after which this is a PASS.

Verifier: an agent that did not write the rewrite. Read now: `README.md` (128 lines), `git show HEAD:README.md` (152), `BEMYAGENT.md` whole (306), `work/20/20.12/04_verify.md` whole, `harness/README.md` 1–45, 78–150, 325–345, and the greps named. `R:n` README line · `B:n` `BEMYAGENT.md` · `05:n` decisions file · `V:n` 20.12 verify · `H:n` `harness/README.md`.

### Criteria
| | Result | Evidence |
|---|---|---|
| (a) | **FAIL for 9 sentences** (1 contradicted, 8 partly); the rest supported | table below |
| (c) | **Numbers PASS; one sentence FAIL; one count wrong** | 2 of 3: `V:15`, `V:23–24`. "none of the three added a test": `V:17` (0/3). ~4×: `V:19`, 499 k / 123 k = 4.06. "told to read the protocol file and follow it": `work/20/20.3/prompt_P.txt` line 3. Ten-file app: `V:52`, `git ls-files harness/fixture` → 10. Method sentence: `H:14–22`. "Most … did not survive": `H:7–11` (9 proposed, 4 survived, one first draft harmful). `R:90` and `R:33`: must-fix 1 and 6 |
| (d) | **PASS** | `grep -nE '[0-9]+\.[0-9]+\.[0-9]+' README.md` → no line (absence is what is asked) |
| (e) | **PASS** | pandoc 3.1.1 container, exit 0, `<out>/readme.html` 19 339 bytes. One `<pre>` (lines 334–350, 16 tree rows), 0 `<table>`. Body `href`s, 8, all absolute `https://`: `bemyagent.md`; `github.com/vitotafuni/bemyagent`; `…/blob/3.4.0/BEMYAGENT.md` ×2 (template); `…/blob/main/.bemyagent/docs/05-decisions-and-issues.md`; `…/blob/main/harness/README.md`; `…/blob/main/LICENSE`; `…/tags`. Relative: none (count of body `href` not starting `h` → 0). Line 290 reads `PASS_WITH_CAVEATS`, no backslash. Branch is `main`, `LICENSE` exists |
| (f) | **PASS** | `git status --short`: ` M README.md`, ` M .bemyagent/docs/06-implementation-plan.md`, `?? .bemyagent/work/22/22.2/` — nothing else |
| (g) | **PASS — three small things lost, named below** | section "Removed" |

### Sentence by sentence
S supported · P says more than the source · U unsupported · X contradicted
| README phrase (line) | Source | |
|---|---|---|
| one markdown file … sets up a workspace of plain files … plans, decisions, evidence (7) | `B:8`, `B:23`, `B:91–95` | S |
| you check its work at the level of what and why — not line by line (7) | no line; a promise, as in the old README | U (judgement) |
| No install, no runtime, no service (9) | `B:6`, `B:8`; by inspection | S |
| **A session can end at any moment.** The state of the work is on disk, not in the chat (21) | `B:49`, `B:94`, `B:96`. But the rule that puts the *current* state on disk — the log's next intended action — is recorded at **0 of 10** (`05:248`), and "state needed to resume must live outside the session … already measured at 0/10" (`05:259`) | **P — outruns** |
| reads the plan, the current task's checklist and the last entry of its log (21) | `B:49` — the log "if `03_execute.log` exists"; a trivial task has neither (`B:84`) | P |
| **The agent reads less** (22) | no line and no measurement; the one cost figure is 4× more (`V:19`); `grep -i "reads less"` in `05` → no line | **U** |
| small maps, loaded only when the task needs it (22) | `B:66`, `B:55–64`; but `01`, `02`, `05` are read at Full Restore (`B:50`) | P |
| Specs, drafts and **past decisions** stay unread until they matter (22) | `B:53` covers the folders `decisions/ specs/ drafts/`; `05-decisions-and-issues.md` is read at Full Restore (`B:50`) and for any bug (`B:60`) | P |
| Before a task … target files, behaviour, constraints, dependencies. If two or more are unknown, it stops and asks you (23) | `B:92`, `B:252–256`. Lives in `01_think.md`, which a trivial task does not have (`B:84`); with one unknown it assumes and says so | S (minor P) |
| Any task beyond a trivial edit is written down before it is executed: approach, alternatives, what success will look like (24) | `B:84–86`, `B:96`, `B:257–263` | S |
| **You approve a plan, not a diff** … You can require your approval at that point, or let the agent run (24) | `B:106`; the shipped default is `interactiveMode: false` (`B:147`) — out of the box nothing is approved | P (headline) |
| checked against the criteria fixed in the plan, with commands run at that moment; PASS / PASS_WITH_CAVEATS / FAIL (25) | `B:98–101` | S |
| Where a second agent or model is available, the check is run by one that did not do the work (25) | `B:102`, word for word | S |
| written into the project as they happen — including the conclusions reached in conversation (26) | `B:124`, `B:125` | S |
| A one-line fix leaves one line in a log, with its evidence (27) | `B:84` | S |
| Only work that touches several files gets the full trail (27) | `B:85–86`: the four files start at two files; a new dependency or complex logic also triggers it | P (minor) |
| **It works with the assistant you already use** (28) | `B:33` names the rule files; no line says "works". `specs/resume-block.md:35`: "Outside Claude Code: R assumes nothing, but nothing has measured it there." `05`: 2 hits for Cursor/Copilot/Gemini/Codex (165, 273), neither a run; every round read here is Claude (`V:5`, `05:497`) | **P — outruns** |
| registers the protocol in the rule file your tool reads (…) (28) | `B:33–37` | S |
| Upgrading starts with a checklist you approve; replaces the protocol's own files, with a backup, never your project's documents (29) | `B:14`, `B:15`, `B:18` | S |
| about 300 lines (35) | `wc -l` → 306 | S |
| Every task that is not trivial goes through four phases, each leaves a file (45); the tree (48–64) | `B:84`, `B:91–95`, `B:143`, `B:157–266`, `B:53`, `B:80` | S |
| A task too large for one session is split into sub-tasks, each with its own four files (67) | `B:80–81` ("fits one fresh context window") | S |
| seamless: stops **only** when verification finds a problem (69) | `B:106`; but it also stops when two or more things are unknown (`B:92`) — which `R:23` itself promises | P |
| interactive: stops twice, after the plan and after the verdict (69) | `B:106` | S |
| the agent explains **each one** when it sets the project up (69) | `B:289` lists seven of the eight fields; `conversationLog` is not among them | P |
| In an empty project it first asks what you are building; existing codebase: shallow scan, fills the documents (75) | `B:20`, `B:19`, `B:140` | S |
| Delete the file, fresh session; reads `00-ai-rules.md` before every task (76–78) | `B:305–306`, `B:34` | S |
| Upgrading: compares, writes a checklist and stops; you tick (80) | `B:13–15` | S |
| a new tag is cut only when `BEMYAGENT.md` itself changes (80) | `05:185` | S |
| So **the rules in this protocol are tested** (84) | `H:3–4` says candidates are tested *before entering*; `B:94` is in the protocol at 0 of 10; the conversation-log contract landed "on a judgement the evidence could not make" (`05:251`) | P |
| the same task … with and without a rule, what they leave behind is compared (84) | `H:14–22` | S |
| bullet 1 (88) | `V:15`, `V:17`, `V:19`, `V:23–24` | S |
| not careless … **some** checked the running app more thoroughly than any protocol run … **their checks ended with the session** (89) | `05:415`, `05:491`: *one* arm (q88) was "the most thorough in the round"; one no-protocol arm of `05:415` "wrote three tests" — its check stayed | P |
| append at every turn measured zero — twice, on two different rules (90) | `05:248` (0 of 9; 0 of 10) | S |
| **Rules of that kind were not shipped** (90) | true of the conversation log (`B:70`). The other rule is `B:94`: "command → result → **next intended action** (mandatory; write before executing it)" — shipped | **X** |
| harness not part of the protocol, never lands in your project; no runtime, package manager, OS (92) | `grep -n "harness/" BEMYAGENT.md` → no line (the folder is never named; absence is what is claimed); `B:6` | S |

### Must-fix, with proposed text
1. **R:90** → `A rule telling the agent to append to a file at every turn measured zero — twice, on two different rules. One was never shipped. The other, the task's running log, is still in the protocol: treat it as the least reliable of the four files.`
2. **R:21** → `**Work survives the end of a session.** Plans, checklists and decisions are files in your project, not messages in the chat. A new session reads the plan and the current task's checklist — and the task's log, when there is one — and picks up from there.`
3. **R:28** → `**It is not tied to one assistant.** The agent registers the protocol in the rule file your tool reads (…). Everything measured below was run on Claude Code; on other tools it is untested.`
4. **R:22** → `**The agent is told what to leave unread.** Project knowledge is kept in short maps that point to the details. Specs, drafts and detailed decision records stay unread until a task needs them.`
5. **R:69** → `…runs the four phases by itself and stops only if it is missing what it needs to start, or if verification finds a problem.` and `…live in `.bemyagent/settings.json`; the agent goes through them when it sets the project up.`
6. **R:33** — 20.11 is a second round on the same clean controls (`V:39` "the same ratio 20.11 showed"; plan, "Where the evidence stands", third bullet; 407 k / 123 k = 3.3). → `In the two small comparisons run so far on clean controls, the same task cost three to four times the tokens with the protocol.` Also `*Is there evidence?*` → `*Is There Evidence?*` (the heading's case).
7. **R:84** → `So rules proposed for this protocol are tested before they go in: …`
8. **R:89** → `…the runs without it were not careless — one checked the running app more thoroughly than any protocol run beside it — but most of their checks ended with the session.`
9. **R:24** → `**The plan is written before the work.** … You can require your approval at that point (it is off by default), or let the agent run.`
Smaller, optional: R:23 `Before any task that is not trivial…`; R:27 `Only work that touches more than one file gets the four files.`

### Removed, and where it lives
| Removed from the old README | Now |
|---|---|
| Lazy Loading row | `B:52–53`; R:22 |
| Fractal Decomposition (HTN) row | `B:79–81`; R:67 |
| Context Saturation Check row | `B:92`, `B:251–256`; R:23 |
| CDM row (three tiers) | `B:83–89`. The expansion "Contextual DNA Mapping" is not in `BEMYAGENT.md` (grep → no line); it is in `docs/01-overview.md:23` |
| Symbiotic Validation row | `B:98–104`; R:25. "The human validates the *sense*, the agent the *form*": **lost** (a slogan; R:7 says the same in other words) |
| Self-Registration row | `B:32–44`; R:28 |
| TTEV row, Pacing Modes | `B:91–95`, `B:106`; R:45, R:69 |
| `autoModelSwitching` paragraph | `B:107`, `B:149`, `B:289`; not named in the README (inside "…" at R:69) |
| tree comments (routes, schemas, "volatile", "retrospective") | `B:157–198`, `B:96` |
| harness method — one variable, two arms, N=3, four steps | `H:14–22` |
| "not a downstream proxy like token count … false positives" | `H:22`, `H:82–85` |
| fixture description | `H:24–27` (layers, why). "Express + sqlite + vanilla client, ~120 lines": **lost** — and stale (the first pass counted 469 lines). "Swap in your own codebase if you prefer": **lost** (`grep -i "own codebase" harness/README.md` → no line) |
| `tokens.py`, cache-weighted | `H:329–335`; the weighting at `H:294` |
| traps: consent-shaped rules · directory names · fixture that advertises itself · planted defect | `H:105–112` · `H:131–135` · `H:127–129` · `H:114–117` |
| "its tooling — Node, sqlite, Python — is not a requirement" | **lost** as a list; R:92 keeps "no runtime, no package manager" |
| "Across three milestones here" | `H:5–11` |

### What a visitor still cannot tell
1. **What ordinary use gives.** The 2-of-3 is for a prompt that says "read the file and follow it" with a standing approval. With the protocol installed and the prompt silent — "the condition a real user creates" — 3 of 3 ran the phases and 0 of 3 wrote a test (`work/20/20.11/04_verify.md` 47–49). The README does not say it.
2. **Whether it saves tokens anywhere.** The mission line says "Save tokens", the Problem says context bloat inflates cost, and the only number on the page is 4× more. Nothing read here measures a saving.
3. **Whether resuming works.** It is the first strength; no round read here measured a second session, and the log it relies on is the 0-of-10 rule.
4. **Which tools it has run on.** Only Claude Code appears in the record.
5. **What it touches outside `.bemyagent/`, and how to get out.** It creates or appends to the tool's rule file (`B:35–37`); "What It Costs" names only the folder. Nothing says how to remove the protocol, or what it costs in time.

Judgement sections, against the record: only R:33 "the one clean comparison" (must-fix 6). "Probably yes if the work spans many sessions" is not contradicted, and not measured (point 3).

English: no wrong sentence found. Only the heading case at R:33.

### Could not check
- How GitHub renders the file, the live site, and the page in a browser (HTML read as text). The links were not fetched in this pass.
- 20.12's numbers themselves: the file was read, its instruments not re-run. "Mid-tier": the record gives a model name (`V:5`), not a tier.
- "0 of 10" for the task log is a count over this repository's history quoted from `05:248`; it was not recounted.

## Third pass — after the tone change (independent), 2026-11-19
**Verdict: PASS_WITH_CAVEATS** — none of the nine failed sentences is back, the new sentences are supported as worded, the page builds; one sentence (`R:29`) still says more than `B:84–86` and wants a four-word rewording.

Verifier: an agent that did not write the edit. Read now: `README.md` (123 lines), `BEMYAGENT.md` whole (306), the second pass above, Amendment 2 in `02_tasks.md`, `work/20/20.12/04_verify.md` whole, `work/20/20.12/launch.sh` and `prompt.txt`. `R:n` README line · `B:n` `BEMYAGENT.md` · `V:n` 20.12 verify.

### 1. Sentences about the protocol (intro, What You Get, Is It for You?, How It Works, Get Started)
Must-fix, one:
- **`R:29`** "Only work that touches more than one file gets the four files." — `B:84` makes the one-line tier "one file, **no new dependency**, trivial edit", and `B:86` gives the four files to "a new dependency, or complex/repetitive logic" whatever the file count; it also sits against `R:26` ("any task beyond a trivial edit is written down"). The second pass offered this wording itself; it is still wider than the source. → `Anything larger gets the four files.`

New sentences, all supported:
| README (line) | Source | |
|---|---|---|
| *Save tokens* means less context to read: never the whole project just to start again (11) | `B:49` (plan + the task's checklist first), `B:50` (Full Restore "only if 1 is insufficient", three docs), `B:53` | S — worded as intent ("should"), which is what the source is |
| It loads the knowledge a task needs, and widens it only when necessary (11) | `B:55–64` (per task type, "Read first"), `B:50` ("lazy-load the rest"), `B:68` (grep → expand → full read "only as last resort") | S |
| Starting again does not mean reading everything (24) | `B:49–50`, `B:53` | S |
| short maps that point to the details; the agent is told which of them a task calls for (24) | `B:66` ("only logical trees + pointers"), `B:55–64` | S |
| Specs, drafts and detailed decision records stay unread until a task needs them (24) | `B:53`, `B:61–62` | S |
| It is not tied to one assistant (30) | `B:33` (four tools' rule files, "…"), `B:11`, `B:107` ("if your CLI permits") — a statement about the text, not a claim that it was run elsewhere | S |
| adds a few lines to your assistant's rule file (71) | `B:35–37`, `B:39–43` (five lines), `B:287`; the file is created when missing (`B:35`) | S |
| It is not an orchestrator: it does not run agents for you … no program behind it (37) | `B:6`, `B:8`; `B:133–136` gives a worktree per task and launches nothing; `B:102` asks for a second verifier only "where … available" | S |
The rest (`R:7`, `9`, `23`, `25–28`, `31`, `41–65`, `69–76`) is the text the second pass marked S or corrected; re-read against the same lines, unchanged in meaning. `R:26` no longer carries "(it is off by default)": true as worded (`B:106`). `R:7` "what and why — not line by line" and `R:35` are judgement, as before.

### 2. The nine failed forms
`grep -n -i -E "any moment|reads less|already use|not shipped|the one clean|approve a plan|stops only when|explains each one|rules in this protocol are tested" README.md` → no line, exit 1 (absence is what is asked). Read as well: `R:23`, `R:65`, `R:80`, `R:85` carry the corrected text; the per-turn bullet and *What It Costs* are gone, as Amendment 2 says.

### 3. "about 4× the tokens — on one task in a single session, where there is nothing to resume" (`R:84`)
**Supported.** 4×: `V:19`, `V:39`. One task: `V:49` ("One fixture, one task, N=3 a side"); `prompt.txt` holds one task. Single session: `launch.sh:21` is one `claude -p` per arm, and the file has no resume or continue flag; the plan (line 270) calls 21.1 "the first two-session round this repo runs", and (line 247) records the same limit for 20.2 — "one task in one unbroken context, so the context-reset mechanism … never had an occasion to fire". No line of 20.12 uses the words "single session": it follows from the launcher and from 21.1 being the first.

### 4. Evidence block
`R:80`, `R:82` and the second bullet `R:85` read word for word as the second pass's must-fix 7 and 8 left them.

### 5. Build
pandoc 3.1.1 container, exit 0, `<out>/readme.html` 19 032 bytes. Body `href`s: 8, all `https://` (`bemyagent.md`; the repository; `…/blob/3.4.0/BEMYAGENT.md` ×2; `05-decisions-and-issues.md`; `harness/README.md`; `LICENSE`; `…/tags`). Relative: none.

### Could not check
- Whether `R:80`–`R:85` are byte-identical to the state the second pass left: that state was never committed, so there is nothing to diff against; they match its proposed text.
- GitHub's rendering, the live site, the page in a browser; links not fetched. 20.12's numbers were read, not re-run.
- Whether any tool other than Claude Code follows the file (`R:30` does not claim it).
