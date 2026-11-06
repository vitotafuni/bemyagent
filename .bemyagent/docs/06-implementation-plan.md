# Implementation plan
> This document is the high-level Table of Contents (Index) for the project. For the historical execution trace and thought process, refer to the corresponding `.bemyagent/work/X/X.Y/` folders.

## Milestone 1.0 — Initial BEMYAGENT Protocol Definition
**Goal**: Create a robust, self-bootstrapping template for AI agent context management.
**Status**: done

## Milestone 2.0 — Protocol Refinements (HTN & Handoff)
**Goal**: Introduce advanced agentic patterns like Hierarchical Task Networks and Token/Model Handoff optimizations.
**Status**: done

## Milestone 3.0 — Testing & Sandbox Dogfooding
**Goal**: Execute the protocol within its own repository to prove the concept and generate example documentation.
**Status**: done

## Milestone 4.0 — Protocol Hardening & Evolution
**Goal**: Localize generated templates, encapsulate into `.bemyagent/`, and integrate evolution modules (Context Probing, Adaptive Session Restore).
**Status**: done

| Task | Description | Status |
|------|-------------|--------|
| 4.1 | Localization & directory encapsulation in `.bemyagent/` | done |
| 4.2 | Hierarchical structure for `work/` directory | done |
| 4.3 | Evolution modules (Context Probing, Session Restore, Quick Ref Card) | done |
| 4.4 | Bootstrap hardening & anti-hallucination rules | done |
| 4.5 | Test Context Probing on a real task | done |

## Milestone 5.0 — Symbiotic Validation (VERIFY step)
**Goal**: Integrate the fourth VERIFY step into the TTEV workflow, completing the CDM cycle with a post-execution exit gate.
**Status**: done

| Task | Description | Status |
|------|-------------|--------|
| 5.1 | Integrate the VERIFY rule in `00-ai-rules.md`, sync to `BEMYAGENT.md`, meta-test with first `04_verify.md` | done |
| 5.2 | Clarify documentation language rule (§6) + update README.md to reflect current protocol state | done |

## Milestone 6.0 — Protocol Configuration & Dynamic Pivoting
**Goal**: Introduce a `settings.json` file for configurable protocol flags and implement the Dynamic Execution Pivoting (runtime monitoring) rule.
**Status**: done

| Task | Description | Status |
|------|-------------|--------|
| 6.1 | Create `settings.json` and update `00-ai-rules.md` §4 with Dynamic Pivot logic | done |
| 6.2 | Sync templates (`BEMYAGENT.md`, `_template_think.md`) and validate with a test task | done |

## Milestone 7.0 — Proportional Compression
**Goal**: Implement the Draft 05 rule to strictly compress `_think` and `_verify` files to 1-2 lines for Short/Micro tasks, optimizing token consumption.
**Status**: done

| Task | Description | Status |
|------|-------------|--------|
| 7.1 | Update `00-ai-rules.md` and `BEMYAGENT.md` to enforce the compression rule for Short/Micro tasks | done |

## Milestone 8.0 — Protocol Updates & Migrations
**Goal**: Implement Draft 04 rules to safely handle updates in existing projects, avoiding file loss (via atomic operations) and filename collisions.
**Status**: done

| Task | Description | Status |
|------|-------------|--------|
| 8.1 | Add Migration Rules to `00-ai-rules.md` and `BEMYAGENT.md` (atomic operations, collision checks) | done |

## Milestone 9.0 — Protocol Anchoring Gate (Anti-Drift)
**Goal**: Add a model-agnostic procedural gate that prevents Recency Bias from causing agents to create orphan files in `.bemyagent/` during long sessions.
**Status**: done

| Task | Description | Status |
|------|-------------|--------|
| 9.1 | Add Protocol Anchoring Gate to `00-ai-rules.md` §3 and sync to `BEMYAGENT.md` | done |
| 9.2 | Add system-level IF-THEN rule recommendation to Self-Registration (§1) | done |

## Milestone 10.0 — Single Slim Template
**Goal**: Replace `BEMYAGENT.md` with one maximally slim version (zero semantic loss) and retire the `BEMYAGENT.min.md` comparison experiment.
**Status**: done

| Task | Description | Status |
|------|-------------|--------|
| 10.1 | Rewrite `BEMYAGENT.md` slim (-37%), fold in 2026-06-10 eval B-fixes, delete `min.md`; verified lossless (clause audit + MUST restoration) and weak-model safe (Haiku cold-bootstrap test) | done |
| 10.2 | Regenerate live `.bemyagent/docs/00-ai-rules.md` from new template (byte-exact extraction, plan-approved 2026-06-11) | done |

## Milestone 11.0 — Empirical Protocol Evaluation
**Goal**: Give the protocol a way to measure whether a rule works, and use it to decide the mattpocock/skills candidates.
**Status**: done — 16 subagent arms; 2 of 5 candidates survived, each only in a form found by measurement rather than by reasoning.

| Task | Description | Status |
|------|-------------|--------|
| 11.1 | A/B harness (fixture, arm runner, shape/slice/token extractors) + 7-run experiment; land P2 and corrected P3 | done |
| 11.2 | Verify the corrected P3 glossary rule fires on new domain vocabulary — confirmed, 0/8 → 8/8 | done |
| 11.4 | P2 across 3 forms / 12 arms: declarative null, self-report null, `Delivers:` artifact 18/18 — landed | done |
| 11.5 | No-BMA control (3 arms): ambiguity detection no different; halt behaviour 3/12 vs 0/3; BMA ~2× planning cost. Claims narrowed to structural conformance | done |
| 11.3 | Blocked-leaf convention — the missing `02_tasks.md` was the Saturation Check working, not a defect; four rival handling styles found, one made canonical | done |

## Milestone 12.0 — Landscape Survey & Convergence Gate
**Goal**: Compare BMA against the 2026 field (Cline, Spec-Kit, BMAD, rtoma, skill-memory-bank) and close any real gap.
**Status**: done — 1 gap found in 6 protocols; first draft measured harmful, reworded version landed.

| Task | Description | Status |
|------|-------------|--------|
| 12.1 | Survey + overlap check vs Cline / Spec-Kit / BMAD / rtoma / skill-memory-bank; most rival mechanisms already covered or bettered (working notes in local `drafts/`, untracked by design) | done |
| 12.2 | Milestone convergence gate — 3 rounds / 15 arms: drafted rule laundered fraud 3/3, reworded 0/3; landed in §6 | done |
| 12.3 | Harness into the repo (`harness/`): fixture + `tokens.py` + the four measurement rules; biased slice classifier deliberately not shipped | done |

## Milestone 13.0 — Declarative Rule Audit (candidate MAJOR)
**Goal**: Every rule is attached to an inspectable artifact, or it leaves. Milestones 11/16/18 measured declarative rules at ~zero compliance and procedural ones near-total; most of `00-ai-rules.md` is still declarative and may have been inert since it was written.
**Status**: done — MAJOR not justified by any single change; see the version note below. Net −156 tokens.

| Task | Description | Status |
|------|-------------|--------|
| 13.1 | Audit done: 32 procedural (~1456 tok) vs 36 declarative (~1300 tok) = 42% of rule content. Caveat: the 42% includes reference data (routing table), config statements and human-process text, which are not "inert rules" and need a third category | done |
| 13.1b | Re-classify into procedural / declarative / non-rule; judge deletions by verifiability × cost × cost-of-failure, not verifiability alone (e.g. "redact secrets" is 13 tokens and unverifiable — keeping it is obviously right) | todo |
| 13.2 | First inertness run (Context Slicing + Surgical Scope + Brevity, 207 tok, 6 arms): **INCONCLUSIVE** — planted defect did not exist, fixture README self-identified as a test, and Surgical Scope got only one accidental occasion. 0/3 vs 1/3 = noise. Nothing pruned | done |
| 13.2b | Re-run with a real defect, a fixture that reads as an ordinary project, and one rule per experiment | todo |
| 13.3 | Cut −186 tok (3 inert restatements + 2 non-rules relocated to README); kept Handoff Principle and Monthly Audit on the audit's own objection | done |
| 13.4 | Micro tier had no evidence requirement — 5/6 arms left an unverifiable PASS. `micro.log` gains an `evidence` field. Net −156 tok | done |
| 13.5 | `04_verify.md` command+output clause — NOT landed. Re-run on a Standard-tier fixture: the baseline already writes commands and results into `04_verify.md` in 3/3 arms, so the existing "evidence from commands run during VERIFY" rule leaves the clause no room. Same shape as the declarative-P2 and audit results: the strong procedural rule already covers it | done |
| 13.6 | Fixture failed `npm install` on Node 26 — measurement noise from the instrument itself; pinned and verified end-to-end | done |
| 13.7 | Monthly Audit run against this repo: `harness/` had been added without updating `01`/`03`/`04`. Docs realigned; the §6 miss recorded as a learning | done |

> **Version note (conclusion).** No single change from Milestones 11–13 is breaking: each is additive or subtractive but self-adapting on re-read → MINOR by the Decision 8 criterion. **The one genuine MAJOR argument is Decision 18's convergence gate**, and it is not about size: it *re-judges existing data*. After upgrading, a milestone already marked `done` whose spec has unticked acceptance criteria becomes non-closable and the protocol will reopen it. That is a behavioural change applied retroactively to a project's history, which is what "requires manual migration" means in practice. Migration note if MAJOR is taken: *after upgrading, review closed milestones — those with unmet acceptance criteria will return to in-progress.*

## Milestone 14.0 — Read Delegation (candidate)
**Goal**: Decide whether reading code can be delegated to a cheaper tier, and under what constraint. Origin: the Portal-by-Spotify article (model routing, not a code map — see `drafts/read-delegation.md`).
**Status**: in-progress — **the generated-code-map line is closed.** 14.13 ran the last round at its pre-fixed bar and the control came back at ceiling: 3/3 of the arms on the shipped protocol re-ran the command and refreshed the block unaided, so the clause had nothing left to buy. The same round found that **14.12's control condition and 14.13's are byte-identical and read 1/3 and 3/3**, which corrects 14.12's headline and puts a hole in the harness's own N=3 reading rule → 14.14. 14.3 rejected, 14.6 landed, 14.8 and 14.9 survived without landing; 14.5 and 14.10 remain open.

| Task | Description | Status |
|------|-------------|--------|
| 14.1 | Instrument repair — the fixture had no file above `contextSlicingThreshold`, the same "no occasion for the rule" failure that made 13.2 inconclusive. Added `server/session.js` (~300 lines); rewrote `fixture/README.md` as an ordinary project | done |
| 14.2 | Scenario: a one-line `presenceKey` defect violating the invariant `session.js`'s own docstring declares. Verified to reproduce and to escape the shipped tests | done |
| 14.3 | Read delegation, 3 conditions × 3. **Candidate REJECTED** — 0/9 arms delegated anything and 0/9 cited `path:line`, including the 3 ordered to, with the trigger met. Declarative null, same shape as 11/16/18 → `work/14/14.3/04_verify.md` | done |
| 14.3a | Round 1 voided — 9/9 arms died on an API session limit. Pivot fired as pre-defined; partials deliberately not scored, they were biased toward a false positive | done |
| 14.4 | Validity probe before spending arms: subagents **can** delegate (`Agent` tool, `model` enum incl. `haiku`). Also found arms must be model-pinned explicitly or the tier floats | done |
| 14.5 | Candidate: agents trust a doc comment over the code it describes — 7/9 read `session.js`, 9/9 shipped the violation of the invariant it declares. **Re-scoped 2026-10-10** to the *rationale* layer only, if 14.8 lands → `05-decisions-and-issues.md` | todo |
| 14.6 | Graph invocation — one Routing Table row, two phrasings. **Permissive 0/3 · procedural 3/3**, clean separation; narrows 14.3 (the barrier was the declarative shape, not tool-ness). But 6/6 built on `listOnline()` either way — invocation ≠ value → `work/14/14.6/04_verify.md` | done |
| 14.9 | **Round two, run 2026-11-04**, 6 arms, two sides one sentence apart: the completeness requirement stated (S) against the same plus the `comm -13` cross-check named (C). **The fix works — recall complete in 4 of the 5 computable arms against 14.8's 0/3**, 2/3 on each side, so the completeness sentence carries it and **the check sentence buys nothing and left no trace of being run** in any of the six trees. Precision 6/6 clean. **The harm pre-registered before launch is live at 2/6**: one arm per side answered completeness by deleting the grep, reaching perfect recall and zero symbols. One arm's command string was **truncated inside its own map** by the very instruction that makes the inventory derivable. An unexplained **0/3 against 3/3** on pasting the output, aligned with the sides, is recorded as an observation and not a result: not pre-registered as a comparison, N=3, mechanism unevidenced. **PASS_WITH_CAVEATS, does not land** — a clause whose cheapest compliant answer destroys the artifact is not ready, whatever its recall. The finding worth keeping is about clause-writing: a MUST is obeyed, descriptive prose mostly is, silence is a hole, measured twice on the same clause → `work/14/14.9/04_verify.md` | done |
| 14.9a | Batch 1 **void, not scored**. The launch prompt had been reconstructed from a summary rather than stored, and on the identical fixture and setup script that gave 14.8 three code maps out of three it gave **zero out of two**: both arms were sent down Step 0's approval branch, one stopping and one abandoning the protocol and shipping the feature bare. Nothing about either side was involved. Rebuilt clean per the 14.3a precedent, the prompt stored in `work/14/14.9/prompt.txt`, and the rule written into `harness/README.md`. **A third independent data point for Milestone 19**, the first from outside 18.2: a `.bemyagent/` holding only `settings.json` failed in the two ways 19.1 had not seen | done |
| 14.11 | **Re-scoped: the three wording fixes, applied to the candidate without a round of their own.** The symbols half becomes its own MUST sentence, the `comm` sentence is dropped, and the command is fenced apart from its output. The fixes are right and free; **spending six arms on them is not, because the exit they close has a control rate of 2 in 6 and this harness reads only clean separation at N=3** — a treatment coming back 0/3 is what the control would plausibly do anyway, and an uninterpretable round that happens to confirm my own candidate is the worst thing the budget can buy. They ride into 14.12 inside side G instead, which leaves them shipped but not separately attributed, stated rather than hidden | done |
| 14.12 | **The round the candidate had never had, run 2026-11-04**: not whether the command is good at birth but whether it buys anything at turn two. Six arms, **no protocol delta** — the variable was the seeded `03-code-map.md`, a hand-written symbol table (H) against the inventory command with its stale pasted output (G). Scaffold pre-populated and committed, so Step 0 was not a variable. Drift planted where only a re-run finds it: both maps claim `server/session.js` exports three symbols, the file holds thirty lines of them, the task never opens it. **Detection H 0/3, G 1/3 — a null by the N=3 rule.** The pre-registered harm did not land: the true underivable line survived **6/6**. The content is in the three G arms — one re-ran and caught all ten planted symbols, one **declined in writing** and annotated by hand, and one **hand-typed 9 of 9 added lines inside the fenced output block with the line numbers shifted**, so the block reads as regenerated while the command was never run. A harm not pre-registered and worse than the one that was: a forged derived block claims an authority no reader can check without running it → `work/14/14.12/04_verify.md` | done |
| 14.13 | **The last round, run 2026-11-04 at the bar fixed when 14.12 closed.** Six arms, one delta: a sentence in §4 `Symbiotic Validation` obliging VERIFY to re-run any derived block, record the diff in `04_verify.md`, and type nothing into such a block by hand. Both sides got the identical stale generated map. **Detection A 3/3, B 3/3 — the control is at ceiling.** Forgery 0/6 against each arm's own named command, delivery 6/6 with zero test failures, the underivable ⚠️ line survived 6/6 for the second round running. **The clause does not land, and not because it failed: there was nothing left for it to buy.** A measured ceiling, not a null from noise, and the difference is the whole point — a null says the rule had no effect, a ceiling says the behaviour was already there. The instrument nearly manufactured a harm on the way: under the scorer's first definition q32 would have been reported as forging exactly nine lines, the same count as 14.12's real forgery, when those lines are its own new test file enumerated by the better command it wrote. Corrected with the last arm still in flight, both figures kept → `work/14/14.13/04_verify.md` | done |
| 14.14 | **Done 2026-11-04, no arms spent.** (a) 14.12's headline corrected in `05`: its control condition is byte-identical to 14.13's and read 1/3 against 3/3, so *the generated map does not catch drift* was a tail sample. Its other results stand, the forged block included. (b) `harness/README.md` Scoring rewritten: **the mechanism, a null, a ceiling and an under-powered draw** are now four verdicts in a table, with the control's rate as the thing decided first, and only the first three license anything. The collapsed sentence is gone, not qualified further down (`grep` → 0). Two instrument rules added from 14.13's near-misses: score a derived artifact against the command **it** names rather than the one the setup seeded, and treat the shared scratchpad root like the shared port space it resembles. `BEMYAGENT.md` untouched, no tag → `work/14/14.14/04_verify.md` | done |
| 14.7 | Graph *value* round. Reframed 2026-10-10: the question is freshness, not retrieval, so it is not blocked on a larger fixture → `drafts/graphify-evaluation.md`. Superseded by 14.8 if that lands | blocked — gated by 14.5 |
| 14.8 | Candidate: the structural layer produced by a deterministic command the agent determines once at bootstrap, not by an LLM reading the repo — drift becomes detectable by diff. Viable because of 14.6 → `drafts/generated-code-map.md`. First round scores: does the command run, does its file set match `git ls-files`, is it re-runnable with no context. **Launched 2026-11-01**: 3 arms on a one-clause delta to the `03-code-map.md` template, no baseline (the shipped protocol names no command, so its score is zero by construction). Premise measured first: `git ls-files` 12 files against `find -name '*.js'` 239, vendor dir untracked and no `.gitignore`. **Result: runs 3/3, re-runnable 3/3, precision 3/3 — the prepared trap was avoided by every arm, all three reached for `git ls-files` unprompted. Recall 0/3**, and the cause is shared: `git ls-files <globs> | xargs grep <pattern>` lets the grep decide membership, so a file matching no symbol pattern leaves the inventory. Two arms globbed `client/index.html` explicitly and still lost it. **Criterion (iv) 3/3**: every map carries hand-written rows its own command cannot regenerate, so *re-run and diff* reports them as drift forever. The clause specified only the exclusion half and 3/3 met it exactly; completeness was never written down. **Not rejected, revised** → `work/14/14.8/04_verify.md` | done |

## Milestone 15.0 — FEDERATION issue (first external report)
**Goal**: Triage and act on 11 observations from agents run at zero context, on virgin sandboxes, with a model different from the author. 9/11 verified verbatim against our files; the 4 mechanically-checkable defects are present in **every tag ever published**. Full triage: `drafts/federation-issue.md`.
**Status**: in-progress — 15.3 done (null, #7a not landed); 15.1 unblocked by a third confirmation of #3.

| Task | Description | Status |
|------|-------------|--------|
| 15.1 | Tier 1 text fixes **applied** 2026-10-23 to `BEMYAGENT.md` (295→299 lines), `00-ai-rules.md` regenerated from it and verified mechanically (86/86 lines verbatim, whole block a substring): #3 register where the tool actually reads, once, `CLAUDE.md` wins when both exist · #2 write the detected language into `settings.json` · #10 one status vocabulary in three places · #8 upgrade model stated + `.bak` retained for changed files · MIT notice. **#1 withdrawn and rejected on evidence** — 2 arms classified a docs-only project BROWNFIELD and derived it correctly; the proposed wording would have broken that. **No version field**, per Decision 12 | done |
| 15.2 | #8 closed. The *statement* shipped in 3.2.2 (protocol files are overwritten, customisation goes in project files, `.bak` retained for changed files). **The merge algorithm is REJECTED** on Decision 12's own reasoning: semantic diff is non-deterministic and that decision mitigated it precisely by making protocol files always-overwrite. **No version field**, same decision | done |
| 15.3 | Round on #7a, 6 arms. **NULL — #7(a) does not land**: captured 3/3 baseline · 3/3 treatment, with `05` catching it 6/6, so §6's CRITICAL rule already does the job. The objection's prediction was wrong — the mandated section filled 3/3 → `work/15/15.3/04_verify.md` | done |
| 15.4 | **Run 2026-11-05, 6 arms. The trace lands; the clause does not.** One sentence in §3 step 2 obliging the `PROTOCOL_CHECK` line into the current task's `03_execute.log`. **Disk trace B 3/3, A 0/3** — issue #5 reproduced, the control gating 25 of 28 governed writes with none visible in the repo. **Coverage flat: A 89%, B 85%** — a record, not compliance. Delivery 6/6, no cost. **Does not ship for two reasons, both found by the round:** `03_execute.log` does not exist when Step 0 runs, so three arms invented three destinations (second measurement of 14.8's drafting failure); and B's record names 13 of 28 governed files against its conversation's 24 of 28, so **it under-reports the gate for the only reader it exists to serve**. Batch 2 died on a session limit, voided and rebuilt, not resumed. **19.4's check found a denominator defect on its first outing** and corrects 19.3's published 55% to 60% → `work/15/15.4/04_verify.md` | done |
| 15.5 | #6 absence never supports a PASS of presence — landed in §4 · #7c precedence `rules > plan > memory`, with tool-private memory ranked last — landed in §3 · #11 foreign files as a 6th UPGRADE PLAN category, listed and never touched | done |
| 15.6 | #4 resolved **without** an exception clause: §3 now names what the limit protects — keep the sections the project has, drop the rest. Evidence from the greenfield arms: both adapted the map to a codeless repo unaided, but one dragged code sections along filled with `n/a`, which is the friction the report felt | done |
| 15.7 | #9 sessions are disposable. **The rule already exists and measures 0/10** (Decision 21), so the proposal as worded would fail identically; what is new is the trigger. *"And commit"* stays out — commit cadence is the user's | todo |
| 15.8 | The method proposal landed as a **norm, not a gate**: §4 states the author is the weakest verifier and asks for a second agent where one exists, with an explicit fallback clause where none does. Gating it would exclude anyone without a second model | done |
| 15.9a | **Feasibility probe, zero arms, 2026-11-05.** Filed as a probe and not a TTEV leaf: `harness/README.md` requires checking a rule has an occasion to fire before arms are designed, and a forward `01`/`02` for work already done would be theatre. 19.2a's two hand-added team conventions against the 18 arms of 14.13, 19.2b and 15.4 that ran the same fixture and task without them. **Convention 1 has no occasion** (the new route takes no input, so no 4xx can occur). **Convention 2 is already near-universal**: a layer-crossing test appears in **2 of 18** arms never told not to, and 0 of 6 with the convention — an absent occasion, not separation. Observation recorded and not believed: 6/6 arms with the convention named the test after the module, 3/13 without → `work/15/15.9a/probe.md` | done |
| 15.9 | **The case 15.3 could not reach**: a standing rule that does *not* announce itself — arriving as a correction, across turns, or inferred. How this repo's own private `memory/` entries arrived. **Constrained by 15.9a (2026-11-05): the round needs a convention whose violation is the cheap path.** The two tested there cost nothing to follow, which is why the control already followed them, and six arms would have confirmed an absent occasion | todo |
| 15.10 | EARS-formatted `✅ Validation` criteria, 6 arms. **INCONCLUSIVE — change nothing.** FORM 0/3 vs 3/3 (confirms the clause applied, not a result); CITATION and COVERAGE both **3/3 vs 3/3, at ceiling** — every arm added its own test, so every cited command covered the change. The task gave the baseline no way to fail. A valid round must measure **criterion quality**, not citation → `work/15/15.10/04_verify.md` | done |
| 15.10a | Round 1 **void** — not scored, batch 2 not launched. Three design faults: the task premise was false (both arms caught it, §5 working); the task sat on the Micro/Standard boundary so arms split and the rule under test could not fire in half of them; and an arm produced a dangling `AGENTS.md` sentinel. Relaunching on a verified premise — `session.js` is orphaned, wiring it in is unambiguously Standard → `work/15/15.10/03_execute.log` | done |
| 15.11 | **Measured — NULL, and the null names a better lever** (6 arms, 2026-10-31). Not runnable as worded: `harness/README.md` rules out interaction-shaped rules, so measured a proxy — does `interactiveMode` change what `01_think.md` *contains*? **0/3 vs 0/3** on handing a decision to the reader, with the decisions shown reachable (6/6 weighed new-row-vs-reset, 3/6 named who-opens). Cause: §4 Saturation Check already says 0-1 unknowns → assume and continue, and it fires *inside* THINK while the gate fires after. Separate observation, not a rate: 2 of 3 gated arms implemented in full and then flagged the gate as owed → `work/15/15.11/04_verify.md` | done |
| 15.12 | Kiro artifact comparison, run 2026-10-23 on controlled input (1.85 credits). **Its CLI has no spec flow — the `requirements/design/tasks` triple is IDE-only**, so that capability is not scriptable and was not measured. What was measured: the clarifying-questions behaviour is **harness, not model** (Plan 3 questions 2/2, default 0, same pinned model); **neither mode wrote a single artifact to disk**, the plan living only in `~/.kiro/sessions/*.jsonl` outside the repo — Decision 21 confirmed from outside; and **their permission gates block where ours only self-report** → `work/15/15.12/04_verify.md` | done |

## Milestone 16.0 — Conversation log (issue #3)
**Goal**: Decide issue #3 — an optional, harness-agnostic raw conversation log in the repo. Full triage: `drafts/prompt-logs.md`.
**Status**: done — remedy rejected at 0/9, mechanism proved by hook, contract landed as opt-out.

| Task | Description | Status |
|------|-------------|--------|
| 16.1 | Round, 9 arms, **two-turn** (new instrument: a second message sent to the running arm, since a single-prompt arm has no conversation to log). **Problem CONFIRMED at 7/9** — a correction that changed the work left no durable trace anywhere. **Proposal REJECTED at 0/9** — no log contains the second turn; all four that exist hold one entry, written at bootstrap and abandoned. Verbatim produced a summary labelled as a transcript → `work/16/16.1/04_verify.md` | done |
| 16.2 | **Mechanism PROVED.** A `UserPromptSubmit` hook appends each prompt verbatim to `.bemyagent/log/` before the model sees it — pipe-tested (newlines, quotes, `$(whoami)` stayed literal: the text goes through `jq`, never a shell) then confirmed live. Answers both of 16.1's failures, because nothing is asked of the model. Experiment config and log are gitignored → `work/16/16.2/04_verify.md` | done |
| 16.4 | **Contract landed** (+4 lines): `conversationLog` field, Routing Table row, and a rule stating the protocol does not write it, naming both measured failures inline. Owner's call against the measured recommendation, on the ground that the log is **insurance for the human**, not a tool for the agent — guarantee 3. Labelled in `05` as landed on unmeasurable human value, not on evidence | done |
| 16.3 | The problem remains open and is **not** closed by rejecting the remedy: 7/9 is too large to file away. Any future candidate must hang on an event the agent recognises while producing it — Decision 21's shape — not on a per-turn cadence, which is now measured at zero twice | todo |

## Milestone 17.0 — RUNTIME_CHECK tag (DRT proposal, external)
**Goal**: Measure the one surviving part of the DRT patch — does naming a command per criterion in `02_tasks.md` change which command the agent names? Full triage and the three rejections: `05` Engineering Learnings; working notes in `drafts/deterministic-runtime-triggers.md`.
**Status**: **closed — rejected.** The tag buys no detection and inflates non-falsifiable evidence 3/3. Verdict: `work/17/17.2/04_verify.md`. **The whole DRT line is closed**: every proposed remedy is now either rejected on mechanism or measured.

| Task | Description | Status |
|------|-------------|--------|
| 17.1 | Round: baseline vs `[RUNTIME_CHECK: <command>]` in `02_tasks.md`, no loop clause and no template change (both rejected). Metric is **command quality — does the named command exercise the change?** — not the verdict, which 15.10 found at ceiling 3/3 in the baseline. **Dropped.** 17.2 measured the metric 17.1 would have used: detection 2/3 treatment against 1/3 baseline, a null, with a 3/3 inflation of commands that cannot fail alongside it. There is nothing left for a benefit arm to find that the harm arm has not already priced | void — dropped |
| 17.2 | **The harm arm, and it outranks 17.1**: does binding a criterion to a command push arms toward a command that merely passes rather than one that touches the change? The mechanism predicts yes, and the rejected loop clause is that gradient written down. If it bites, 17.1 stops mattering and the finding is published as a rejection. **Launched 2026-10-31**: 3 treatment arms on the per-criterion form of the tag, baseline reused from 18.3, metric executed rather than read. **Detection: treatment 2/3, baseline 1/3 — a null, the tag buys none.** The pre-registered harm (a collapse onto one cheap command) measured **false**: treatment arms named more commands, not fewer. The harm that did show was found by running them: **9 of 14 named commands never go red under either mutation** — 7 of 7 greps and 2 of 2 `node -e` one-liners that print a verdict and exit 0. The clause ends *"A criterion no single command can decide names none"* and **3/3 arms declined that exit and manufactured a command anyway**. **Rejected** | done |

| 17.3 | **Recorded, not scheduled.** What was rejected is the **per-criterion** form, which is the draft's own revision of hunk B. The author's weaker per-task form is untested, and the mechanism found in 17.2 predicts it inflates less because it asks for one command where a command plausibly exists, and buys correspondingly less. It would have to earn its own round | backlog |

## Milestone 18.0 — Saturation Check threshold (from 15.11)
**Goal**: 15.11 showed the approval gate cannot surface a decision the Saturation Check has already told the agent to assume. Test the threshold itself. Verdict and evidence: `work/18/18.1/04_verify.md`.
**Status**: **closed — nothing lands.** The baseline surfaces the decision without stopping, so the clause buys ordering and costs two of three deliveries. Verdict and the nine-arm attribution table: `work/18/18.3/04_verify.md`.

| Task | Description | Status |
|------|-------------|--------|
| 18.1 | One line added to §4: a product decision trips STOP on its own, whatever the count; an implementation fact does not. Protocol delta verified at 2 lines. **SURFACED 3/3** vs 15.11's recorded **0/3**; **OVER-TRIGGER 0/3**; **DELIVERED 0/3** vs 3/3 baseline. Arms used the machinery already there (no `02_tasks.md`, task marked `blocked`) unprompted. Baseline reused from 15.11, stated as a limitation, and it is what removed 15.11's blinding failure | done |
| 18.2 | **The round that decides whether it lands.** Same clause, a task carrying several open decisions of mixed reversibility. Metric is the **stop count**, not whether a stop happens: a rule that stops once is a question, one that stops six times is a form to fill in, and the rate is where guarantee 1 is charged. Also test the arms' own rewording, **reversibility** ("undoing this means rewriting the API", checkable) in place of **ownership** ("the user owns which", an opinion). **Round 2, 6/6 complete.** Stop count **1, 1, 2** — no arm reached 3, so neither wording enumerates and the rejection bar is cleared. But the rate is **2/3 ownership vs 1/3 reversibility**, which is not separation at N=3, and the three arms that proceeded each quoted the clause's *exclusion* half to justify it. **PASS_WITH_CAVEATS, does not land** → `work/18/18.2/04_verify.md`. **Corrected by 18.3**: the 1/3 recorded for reversibility is not attributable — that arm stopped with two unchecked items, where the shipped 2+ rule fires on its own. Attributable: ownership 2/3, reversibility 0/3 | done |
| 18.2a | Round 1 **void, not scored**: all 6 arms died on one session rate limit, leaving asymmetric partial state (ownership 2/3 with `01_think.md`, reversibility 1/3). By the 14.3a precedent partial state is not scored, and a *count* metric is the most sensitive kind to an arm that stopped early for unrelated reasons. Setup, both one-line deltas and the fixture premise checks are preserved and reusable → `work/18/18.2/03_execute.log` | done |
| 18.2b | **Harm metric void, not passed.** 0/6 arms blocked on a repo-checkable fact, but the planted fact (*would a new column reach an existing database*) was never live: no arm needed a new column, `game.winner` already held the answer and all six found it early. Recorded as void rather than reported clean. A live harm arm needs a task whose cheapest implementation genuinely requires a schema change | done |
| 18.3 | **The missing arm, and the only thing between the clause and a decision.** Three baseline arms, the same scoreboard task, no clause. 18.2 measured how *much* the clause stops and cannot say whether it *caused* the stops, because both its sides carried a clause and 18.1's 0/3 baseline sat on a different task. Baseline came back **0 blocking items 3/3, shipped 3/3**, which is the first reading: the clause does cause the stops. Re-scoring all nine arms on the checkbox count then settled the rest, and **corrected 18.2**: a stop is attributable only below the shipped 2+ threshold, and q5 stopped with two unchecked, so **reversibility caused 0/3, a null**. Ownership 2/3 attributable, 1/3 shipped against the baseline's 3/3. Decisive: **3/3 baseline arms surfaced the same decision anyway**, as a stated assumption in `01_think.md` and unprompted in the hand-back, one of them naming the reversal as one clause in one query. The clause buys ordering, not visibility, at two of three deliveries, for a choice reversible in one line. **Both wordings rejected** → `work/18/18.3/04_verify.md` | done |

| 18.4 | **Not scheduled, recorded so it is not reinvented.** Every decision these rounds stopped on was reversible by one `WHERE` clause, stated independently by arms on all three conditions. Nothing in Milestone 18 tests a decision that is genuinely expensive to undo, because no arm needed one. That is the one condition under which a future candidate could earn its lines, and it needs a fixture where the cheapest correct implementation forces a schema or interface choice | backlog |

## Milestone 19.0 — Step 0's UPGRADE branch tests the wrong condition
**Goal**: the branch is chosen by `.bemyagent/` existing, not by there being anything to protect. 6/6 arms of 18.2 hit it, found the review list empty, overrode the STOP and documented the override. Measure whether a condition change removes the override without weakening the protection.
**Status**: **closed — Step 0 unchanged.** 19.2a ruled out the harm (6/6 both sides, a tie by construction); 19.2b could not resolve the benefit (control 1/3 against 19.1's 6/6) and is recorded as **under-powered**, the third distinct way a candidate fails to land here. 19.3 measured the forced-output gate for the first time (6/6 emit, 55% of governed writes named) and left consent gates untested, where the harness leaves them. **What outlives the milestone is not the branch condition**: an override leaves a trace only when the agent chooses to write one, and that is issue #5's shape, not Step 0's. One harness fix the milestone earned landed as 19.4.

| Task | Description | Status |
|------|-------------|--------|
| 19.1 | **The observation, free from 18.2.** `.bemyagent/` held only `settings.json`. All six arms routed to UPGRADE, wrote that the gate protects user content and that there was none, skipped the STOP, generated the scaffold, and recorded the deviation in `05` or the audit log. Nobody stopped. **Caveat stated before the finding**: that directory shape is an artifact of the harness setup, which writes exactly one settings file, so the frequency means nothing — what is evidence is that 6/6 independently judged the gate's condition wrong and said so in writing | done |
| 19.2a | **The harm round, run first and alone** (6 arms, launched 2026-11-04, closed 2026-11-05). One clause on `BEMYAGENT.md` line 12: UPGRADE branches on **content** rather than on the directory existing. Fixture seeded with real user content — a team `## 7` inside protocol-owned `00-ai-rules.md`, a foreign tool's config, a completed `work/1/1.1`, non-default settings. The prompt granted standing approval **deliberately**, because withholding it halts arms at STOP before APPLY and leaves the harm unreachable. **Result: 6/6 on every criterion, both sides, nothing lost.** Also measured, and not previously known: Step 0's APPLY migrates a user's section out of a protocol-owned file before overwriting it, 6/6. **A tie by construction**, predicted in the pre-mortem: the clause only acts where there is nothing to protect. Necessary, not sufficient → `work/19/19.2a/04_verify.md` | done |
| 19.2b | **The benefit round, run 2026-11-05, and it could not resolve itself.** Same clause, 18.2's directory shape, prompt **without** standing approval — inverting 19.2a, because a pre-approved plan erases the behaviour at the STOP. Scaffold 6/6, settings 6/6, delivery 6/6 with zero test failures. **Routing: A 1/3, B 0/3**, where 19.1 saw 6/6 on the identical shape. The pre-registered reading for a control at 1–2 of 3 is `under-powered`, which licenses nothing. **The finding worth more than the verdict:** one control arm overrode the gate and left **no trace on disk** — on disk it is indistinguishable from an arm that never took the branch — which downgrades 19.1's consolation that the override was always documented, and is not fixed by rewording Step 0 → `work/19/19.2b/04_verify.md` | done |
| 19.3 | **Done 2026-11-04, zero arms.** The question splits and only one half is answerable here. **Consent gates stay untested**: they exit on a human reply and `harness/README.md` rules them out, which 15.11 already paid for. **Forced-output gates had never been measured.** From the six 14.13 transcripts and trees: **6/6 arms emitted `PROTOCOL_CHECK`, 25 emissions, 18 of 33 governed files named (55%)**, emissions well-formed and citing the rule rather than reciting it. Decision 13's *~90%* estimate resolves two ways against the same arms — **100%** if it means the agent runs the gate, **55%** if it means every governed write is gated — so it was unmeasurable rather than wrong. Constraint handed to 19.2: **the gate fires where the agent is already heading, not where it wanders**, so a gate meant to catch an incidental write is not this shape. Two instruments discarded before any number was believed, the first having already produced a false 6/6 against the gate → `work/19/19.3/04_verify.md` | done |
| 19.4 | **The harness fix this milestone earned, no arms.** Four scorer defects in three rounds — 14.13's forged-line definition, 19.3's write-counting probe, 19.2a's whole-sentence match, 19.2b's routing-from-artifacts — each caught by reading an arm rather than a number, each a false headline otherwise. Three ran **against the arms**, one **toward the candidate**, so the failure is not a direction: a scorer is an instrument built by whoever wants the answer, and nothing here checked it. `harness/README.md` now requires, before a metric's number enters a verdict, opening the arm at **each end** of that metric and recording a line per metric in `04_verify.md` **naming those arms** — a fact that cannot be written without opening them, unlike an assertion that a check happened. **Not itself measured**, and it binds the apparatus rather than shipping to users → `work/19/19.4/04_verify.md` | done |

## Milestone 20.0 — Harness cost and research cadence
**Goal**: price a round before authorising it, and know where its question came from.
**Status**: in-progress — 20.1 and 20.2 done. **20.2 is the first measurement of the protocol as a whole**, and its verdict was **narrowed the same day after the user's objections**: it measured only machine-observable value while the protocol's primary audience is the human; it ran one task in one unbroken context, so the context-reset mechanism TTEV exists for **never had an occasion to fire**; and it priced both sides on one tier, when the scaffolding exists to support weaker reasoning and a tenth-cost tier inverts the economics. Candidate rounds remain paused at the user's request; the obvious follow-up (a task exceeding one context window) is deliberately **not scheduled by me**.

| Task | Description | Status |
|------|-------------|--------|
| 20.1 | **Zero agents.** Two things that existed only in conversation, written down — which is the failure 15.4 had just spent six arms measuring. (a) **What a round costs**: ≈ 653 k weighted tokens per agent over 119 transcripts, cache read 93% of the raw total, and **an arm is not an agent** because most spawn a second for §4's VERIFY — so six arms ≈ twelve agents ≈ **7.8 M**. Script and output in `work/20/20.1/`. (b) **The arm tier**: Opus was inherited, not argued; the comparability case is weak now that cross-round readings have swung 1/3→3/3 and 60%→89%, and BMA ships to everyone while having only ever been measured on the most expensive tier. Conditions for changing it recorded in `harness/README.md` | done |
| 20.2 | **Run 2026-11-06, 6 arms, no candidate clause** — the variable is the protocol's presence. **(i) mutation caught: P 2/3, N 0/3**, below the bar. **(ii) no clean separation** on defects once the two seeded in P-only documents are removed (P 2,1,1 vs N 1,0,0). **(iii) 6/6 both sides delivered.** **(iv) P costs 2.54×.** Verdict: **the protocol does not beat no protocol on this task and costs 2.54× to tie**, on a condition chosen before launch to flatter it. The one property that leans P — a check that stays in the repository — is **not something §4 asks for**: one protocol arm wrote no test, verified live and thoroughly, and complied exactly. 19.4's check moved the verdict against the protocol twice → `work/20/20.2/04_verify.md` | done |

## Backlog (unscheduled)
- **Greenfield exit condition — the A/B was invalid** (kept for the method, the rule itself landed as Decision 19). Step 0.3 prescribes the *action* ("STOP and ask") but no *exit condition*: an agent that asks, receives a bare "ok", and considers the question asked is following the text. Four different behaviours were observed on that ambiguity. A candidate fix exists (create nothing until the answer names the project; explicit opt-in for an `UNPOPULATED` scaffold), but the A/B was **invalid** — subagents refuse coordinator messages on authority grounds regardless of the rule, and directory names leaked the hypothesis (neutral names: 1 refusal / 2 proceed; names revealing the gate: 3/3 refusals). 6/6 arms behaved identically. Consent-shaped rules are not measurable with the harness — this one needs testing by a human in a real session before it can land.
- **Greenfield bootstrap** — resolved in Decision 17 (`UNPOPULATED` marker). Two of three proposed fixes were dropped after measurement; see Decision 17 in `05-decisions-and-issues.md`. Working notes stayed in local `drafts/` (untracked by design).
- Capability Handshake as Operations Manifest in `02_tasks.md` (Fase 3 from evaluation)
- Evaluate creating a CLI tool (e.g., `npx bemyagent`) in the future to automate the file copy.
