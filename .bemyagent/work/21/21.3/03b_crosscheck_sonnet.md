> Mechanical cross-check on Sonnet, 2026-11-12 — a sample check, **not** the VERIFY verdict (§4 puts VERIFY on the strongest tier). Kept as written.

# 21.3 — VERIFY (independent)

**Run by an agent that did not write the register.** It held only `docs/decisions/rejected.md`, the criteria (`02_tasks.md` Validation line; first two acceptance criteria of `specs/rejected-register.md`) and the sources. Every figure below comes from a command run during this VERIFY. No file under `docs/` was edited; no commit; no `claude` process.

Notation: `05` = `docs/05-decisions-and-issues.md` (531 lines), `06` = `docs/06-implementation-plan.md` (268 lines), `SR` = `drafts/state-review-2026-11-11.md` (138 lines), `LA` = `drafts/landscape-analysis.md` (334 lines). Every cited source line was opened (long lines read with `sed -n 'Np' | cut -c1-3000`; none exceeded the cut, lengths checked with `wc -c`). Nothing was truncated or unreadable.

## Verdict: PASS_WITH_CAVEATS — 61 of 72 sampled cells SUPPORTED, 11 PARTLY, 0 NOT SUPPORTED

The mechanical criteria all pass and no sampled line is invented or points at a line that does not say the thing. The caveats: one `not stated` that the source does state (line 54), one status that looks stale (line 9), one line that records as turned down something the source says was not rejected (line 20), and several numbers or labels taken from source lines the row does not cite.

## Criterion 1 — mechanical, all lines
Script `mech.py` (in the session scratchpad) (Python, parses `rejected.md`):
- Table lines: `grep -c '^|'` equivalent gave **52** (header + separator + 50 data lines) — limit 60: PASS.
- Evidence references: 94 references across 50 lines; each resolved to an existing file (`05`, `06`, `drafts/*`) and its line number is within the file length (script printed no `unresolved`/`beyond`): PASS. (No `work/...` references occur.) That the *line says what the row claims* is criterion 2.
- Empty cells: none; every row has exactly 6 cells: PASS.
- Verdict kind: every row matches exactly one of `measured-null|harm|redundancy|design|under-powered`: PASS.
- Status: every row is `stands`, `reopened → …` (line 7) or `reversed → …` (lines 29, 32): PASS.
- Idea ≤ 12 words: max 12 words after the bold theme tag; **line 28 is 13 words if the theme tag (`**Step0**`) is counted** (awk word count). Caveat only; the tag is a grouping label.
- Validation clause "`activeContext.md` line reads `reopened → specs/resume-block.md`": line 7 Status = `reopened → specs/resume-block.md (Milestone 21.1)`: PASS. Spec confirms: `resume-block.md` Critical review 1 "that premise measures 0/10 → rejection withdrawn"; `05`:517 and `SR`:132 say the same.

## Criterion 2 — sample against sources
Rule: data lines 7–56 numbered by register line; every 4th data line starting at the 2nd, i.e. register lines **8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52** (12 lines: themes Memory, Verify, Step0, Rules, Gates, Release; kinds measured-null, design, under-powered, redundancy), plus the five flagged lines **13, 51, 54, 9, 55** and the `activeContext.md` line **7**. 18 lines. Not reached by the rule: Codemap, Upgrade, Process, Packaging as themes (Process and Packaging are covered by the flagged lines); no `harm` row fell in the sample (lines 19, 22, 25, 30 unsampled).

S = SUPPORTED, P = PARTLY, N = NOT SUPPORTED. (a) evaluated and not adopted; (b) Rests on; (c) Reopens when; (d) Verdict kind and Status.

| L | Idea (short) | a | b | c | d | Decisive source lines and quotes |
|---|---|---|---|---|---|---|
| 7 | activeContext.md pointer | S | S | S | S | 05:131 "Rejected from the survey: `activeContext.md` pointer file (hand-sync drift"; 05:155 "`03_execute.log` carries a next intended action in 0 of 10 cases"; LA:16 "covered; a separate pointer file = the hand-sync drift"; none of the three states a reopening; reopened per resume-block.md Critical review 1 and 05:517. Date 2026-08 comes from LA, Decision 18 itself undated |
| 8 | log every user message | S | S | S | S | 05:225 "0 of 9 logs contain the second turn"; LA/prompt-logs:3 "MEASURED 2026-10-27 and REJECTED in this form"; 06:195 "Any future candidate must hang on an event the agent recognises" |
| 9 | resume-state-outside-session rule | S | S | S | P | 06:177 "The rule already exists and measures 0/10 (Decision 21)"; 05:236 "#9 ... a rule we already have and already measured at 0/10"; 06:177 "no trigger candidate has ever been written". (d): Status `stands` is doubtful — see Q3(i) and defect D2 |
| 12 | empty `## Project rules` section | S | S | S | S | 05:245 "the standing rule reached a durable file in 3/3 baseline and 3/3 treatment"; 06:173 "NULL — #7(a) does not land"; no reopening in either |
| 13 | capture implicit standing rules | P | S | S | S | 06:180 "Dropped 2026-11-10: 15.9a's constraint was never met"; 06:180 "Reopens only with a second fixture."; 06:179 "Convention 1 has no occasion". (a): the round was never run; the idea was probed for feasibility and dropped, not measured and turned down. (d): `under-powered` is the nearest kind (source says "absent occasion") |
| 16 | OS exit code forces PASS | S | P | S | S | 05:250 "patch REJECTED as written"; 05:250 "exit 0 as PASS is the converse of a rule §4 already states"; 05:280 "each of those 9 commands forces a PASS against a broken implementation". (b): "9 of 14" appears only in 05:278 (uncited here); 05:280 says 9, not 14 |
| 20 | EARS-form criteria | P | S | S | P | 05:242 "change nothing, land nothing, reject nothing."; 05:241 "Untested, and by our own rule it needs a round"; 05:244 "The next EARS round should measure criterion quality". (a),(d): source calls it INCONCLUSIVE (ceiling) and says "reject nothing"; the row presents it as turned down, `under-powered`, `stands`. See D3 |
| 24 | re-run derived code-map block | S | P | S | S | 05:454 "Not enough evidence, not evidence of no effect"; 05:307 "every arm re-ran the command."; 05:454 "the control is 1/3 fully fresh". (b): "Opus" is not on 05:307 or 05:454 (it is implied by 05:428, uncited). No reopening stated in either line |
| 28 | remove "do not ask permission" | S | S | S | S | 05:119 "Preamble contradiction (dropped)"; "6/6 arms stopped and quoted Step 0.3"; "a bare "yes" read as consent" |
| 32 | branch UPGRADE on content | S | S | S | S | 05:350 "unresolvable at this budget. Raising N is the documented remedy"; "between 1 in 3 and 6 in 6"; 05:446 "Step 0's UPGRADE branches on content, not on the directory existing" — later adopted, Status `reversed → Milestone 19.5` is right. 19.2b/19.1 labels are in 06:230 |
| 36 | `Layers:` header | S | S | S | S | 05:102 "100% compliance, no behaviour change"; "One leaf declared `Layers: [schema, API]` while naming zero files. Discarded." |
| 40 | Dormancy mode | S | S | S | S | 05:94 "Reverted: ... (D) Dormancy — creates an escape hatch that undermines the Write Gate"; "the Micro tier already covers lightweight tasks"; 05:235 "the shape Decision 15 rejected as Dormancy" |
| 44 | delete Handoff Principle | S | S | S | S | 05:145 "Handoff Principle (kept): judged redundant against the Git rule"; "an agent that executes first and retro-writes the plan passes it". 05:489 (20.9) calls its null "a statement about the fixture, not a refutation" — not a reopening |
| 48 | product decision alone trips STOP | S | S | S | S | 05:274 "3/3 baseline arms named the scope question explicitly"; "3/3 down to 1/3"; 05:436 "18.1's ownership clause stays rejected, now on two tiers"; 06:220 "Reopens only with a second fixture." |
| 51 | hand-build a second fixture | P | S | S | P | SR:130 "same author, same scorer-bias exposure; item 7 dominates it."; item 7 = SR:98 "Borrowed fixture, external scorer". (a),(d): SR:5 say "Nothing here is decided — every item is the user's call"; the line is "ruled out" by a fresh-session draft, never by the user; verdict date 2026-11-11 is not stated (file named 11-11, last modified 2026-11-12). Not contradicted by 05/06 — see Q3(ii) |
| 52 | tag every push | S | P | S | S | 05:186 "a tag that carries no protocol change notifies watchers of nothing"; 05:188 "this entry withdraws it". (b): "consumers install only BEMYAGENT.md" is on 05:184 "the distributable surface is exactly `BEMYAGENT.md`", not cited |
| 54 | ship BMA as SKILL.md | P | S | P | S | SR:133–134 "Shipping as `SKILL.md` — activation by description match is wrong for a protocol that must govern every task"; LA:316 same argument. (c): LA:333–334 "Do nothing about ... the skill-packaging question until (3) has a result." — a stated reopening condition, so `not stated` is wrong (D1). (a): SR says nothing is decided; LA defers rather than rejects |
| 55 | adopt Spec-Kit/OpenSpec/GSD | S | S | S | S | LA:333 "OpenSpec/Spec-Kit/GSD (wrong layer)"; LA:282–283 "Both are tooling (a CLI that generates markdown)"; condition "until (3) has a result" (LA:334) where (3) is Actions item 3, the three-rule A/B. No result for that A/B exists in 05/06 (`grep -i 'three-rule\|Surgical Scope'` finds only 06:132, 13.2 INCONCLUSIVE), so `stands` is right. Scope of "until" in the sentence is grammatically ambiguous |

Cell count: S = 61, P = 11 (lines 9d, 13a, 16b, 20a, 20d, 24b, 51a, 51d, 52b, 54a, 54c), N = 0; total 72.

## Criterion 3 — the two specific questions
(i) **Does anything make the resume-state-rule line "reopened"?** Commands: `sed -n 4,25p 06`, `cut -c1-2500 specs/resume-block.md`, `sed -n 517,518p 05`.
- No source marks line 9 itself as reopened. `06` `Resume here` (lines 4–24) is a hand-written resume note and says nothing about the 15.7 rule. `resume-block.md` and `05`:517 name only the `activeContext.md` rejection as withdrawn.
- But `resume-block.md` is the same idea (state a fresh session resumes from, held outside the session; "a context reset costs the user nothing"), and its table "The open question: what triggers the write" lists trigger candidates E, R and hook. Line 9's own `Reopens when` is "A trigger candidate is written", and 06:177 says "no trigger candidate has ever been written". That condition is now met. So `stands` is stale, or at minimum should read `reopened → specs/resume-block.md`. Finding: PARTLY supported — defect D2. (Line 8, the per-turn log, is a different payload, per resume-block.md "16.1's payload was an append to a log nobody reads"; `stands` is defensible there.)

(ii) **Does anything contradict "Hand-build a second synthetic fixture" being rejected?** Commands: `grep -n -i 'second fixture\|hand-built\|hand-build\|synthetic\|borrowed' 05 06 specs/*.md`.
- 06:20 (`Resume here`): "A second fixture is the next real lever: four of the nine dropped rows reopen only with one" under "Not scheduled — the user's call". It does not say hand-built or synthetic, so it does not contradict the line, but it is in tension: the plan leaves a second fixture open as the user's call, while the register says its hand-built form is ruled out, on the strength of a draft that says "Nothing here is decided". The distinguishing text is only in SR:97–98, 130 (item 7: borrowed real repo). No line in 05 or 06 says hand-building is rejected, and none says it is wanted. Verdict: no contradiction, but the line's Status/provenance overstate (D4); a reader of `Resume here` alone would not learn this register entry exists.
- The register's own `Reopens only with a second fixture` on lines 13, 45, 48 matches 06:180, 06:133, 06:220.

## Criterion 4 — omissions
Dropped rows in `06` (awk over the Status column, `dropped*`): 9 rows — line 133 (13.2b), 153 (14.5), 161 (14.7), 177 (15.7), 180 (15.9), 195 (16.3), 203 (17.1), 206 (17.3), 220 (18.4).
- 13.2b → register line 45 (cites 06:133). 15.7 → line 9. 15.9 → line 13. 16.3 → lines 8, 9 (cite 06:195). 17.3 → line 19 (06:206). 18.4 → line 48 (06:220). 17.1 → covered by line 19 via 05:277 ("17.1 is dropped because that was the metric"), though 06:203 is not cited: acceptable.
- **14.5 (06:153): no line.** A candidate fix for agents trusting a doc comment over the code, dropped because its gate 14.8 never landed as a clause; "Reopens only with a second fixture". Should have a line.
- **14.7 (06:161): no line and not cited** in the Graphify line 26; "Graph value round ... Dropped 2026-11-10 with 14.5, which gated it". Should be cited by line 26 or get its own line.

Evaluated-and-rejected ideas in `05` without a line (grep for reject/dismiss/discarded outside the cited lines):
1. The reversibility (and ownership) wording of the Saturation Check STOP — 05:266, 05:272 "Both wordings rejected", 05:273 "Reversibility caused nothing — a null". Line 48 covers only the "product decision alone" clause and cites ownership via 05:436.
2. Declarative rules as the anchoring mechanism (Decision 13) — 05:165 "Declarative rules were rejected (estimated ~50-60% compliance after 15 turns)".
3. The "does the code-map clause name a `comm -13` cross-check" variant — 06:155 (14.9) "the check sentence buys nothing"; line 25 cites only the 14.12 harm.
4. Rejected formulations of the "what may we impose" principle — 05:169 (marginal: kept as examples of error, not as proposals).
5. A third "Opus + protocol" condition — 05:470 struck through, "rejected on price" (marginal; struck-through text).

## Defects (register line — what is wrong — what the source says)
- **D1, line 54** — `Reopens when` = `not stated`. LA:333–334 (same draft, cited for line 55) says "Do nothing about ... the skill-packaging question until (3) has a result." Line 54 should carry that condition, or the two lines disagree on one sentence.
- **D2, line 9** — Status `stands`. The line's own reopening condition ("A trigger candidate is written") is met by `specs/resume-block.md` (triggers E, R, hook); the spec is about exactly this idea.
- **D3, line 20** — presented as a turned-down idea with `stands`. 05:242 "change nothing, land nothing, reject nothing"; 05:241 "Untested". The verdict is "inconclusive, ceiling in the baseline", which the five kinds do not name; `under-powered` is the nearest, but Status should not suggest a rejection.
- **D4, lines 51 and 54** — verdict attributed to a draft whose header says "Nothing here is decided — every item is the user's call" (SR:5); `stands` and a 2026-11-11 verdict date are firmer than the source. 06:20 lists a second fixture as the user's call.
- **D5, uncited support (lines 16, 24, 52)** — "9 of 14" (05:278), "Opus" (05:428), "consumers install only `BEMYAGENT.md`" (05:184) are true but come from lines the Evidence cell does not list; a reader cannot trace them from the row.
- **D6, line 13** — recorded as a measured-or-judged rejection; the round was never run (06:180 "Dropped 2026-11-10: ... never met"). Wording "under-powered" is approximate.
- **D7, line 28** — Idea is 13 words with the theme tag.
- **D8** — omissions above (14.5, 14.7, and the five `05` candidates).

## What could not be checked
Lines of the register not in the 18-line sample (32 lines) were checked mechanically only: references resolve and are in range, but their content was not compared with the sources. The sampled rule gave no `harm` row. Verdict dates written `2026-08`/`2026-10-20` rely on drafts' headers and file modification times (`stat`), not on dated lines in the cited rows. Criterion 3 of the spec (recall by an arm) is outside this VERIFY.
