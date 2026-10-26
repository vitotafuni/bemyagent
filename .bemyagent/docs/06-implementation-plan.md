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
**Status**: in-progress — 14.3 rejected, 14.6 measured; 14.5 and 14.8 open.

| Task | Description | Status |
|------|-------------|--------|
| 14.1 | Instrument repair — the fixture had no file above `contextSlicingThreshold`, the same "no occasion for the rule" failure that made 13.2 inconclusive. Added `server/session.js` (~300 lines); rewrote `fixture/README.md` as an ordinary project | done |
| 14.2 | Scenario: a one-line `presenceKey` defect violating the invariant `session.js`'s own docstring declares. Verified to reproduce and to escape the shipped tests | done |
| 14.3 | Read delegation, 3 conditions × 3. **Candidate REJECTED** — 0/9 arms delegated anything and 0/9 cited `path:line`, including the 3 ordered to, with the trigger met. Declarative null, same shape as 11/16/18 → `work/14/14.3/04_verify.md` | done |
| 14.3a | Round 1 voided — 9/9 arms died on an API session limit. Pivot fired as pre-defined; partials deliberately not scored, they were biased toward a false positive | done |
| 14.4 | Validity probe before spending arms: subagents **can** delegate (`Agent` tool, `model` enum incl. `haiku`). Also found arms must be model-pinned explicitly or the tier floats | done |
| 14.5 | Candidate: agents trust a doc comment over the code it describes — 7/9 read `session.js`, 9/9 shipped the violation of the invariant it declares. **Re-scoped 2026-10-10** to the *rationale* layer only, if 14.8 lands → `05-decisions-and-issues.md` | todo |
| 14.6 | Graph invocation — one Routing Table row, two phrasings. **Permissive 0/3 · procedural 3/3**, clean separation; narrows 14.3 (the barrier was the declarative shape, not tool-ness). But 6/6 built on `listOnline()` either way — invocation ≠ value → `work/14/14.6/04_verify.md` | done |
| 14.7 | Graph *value* round. Reframed 2026-10-10: the question is freshness, not retrieval, so it is not blocked on a larger fixture → `drafts/graphify-evaluation.md`. Superseded by 14.8 if that lands | blocked — gated by 14.5 |
| 14.8 | Candidate: the structural layer produced by a deterministic command the agent determines once at bootstrap, not by an LLM reading the repo — drift becomes detectable by diff. Viable because of 14.6 → `drafts/generated-code-map.md`. First round scores: does the command run, does its file set match `git ls-files`, is it re-runnable with no context | todo |

## Milestone 15.0 — FEDERATION issue (first external report)
**Goal**: Triage and act on 11 observations from agents run at zero context, on virgin sandboxes, with a model different from the author. 9/11 verified verbatim against our files; the 4 mechanically-checkable defects are present in **every tag ever published**. Full triage: `drafts/federation-issue.md`.
**Status**: in-progress — 15.3 done (null, #7a not landed); 15.1 unblocked by a third confirmation of #3.

| Task | Description | Status |
|------|-------------|--------|
| 15.1 | Tier 1 text fixes **applied** 2026-10-23 to `BEMYAGENT.md` (295→299 lines), `00-ai-rules.md` regenerated from it and verified mechanically (86/86 lines verbatim, whole block a substring): #3 register where the tool actually reads, once, `CLAUDE.md` wins when both exist · #2 write the detected language into `settings.json` · #10 one status vocabulary in three places · #8 upgrade model stated + `.bak` retained for changed files · MIT notice. **#1 withdrawn and rejected on evidence** — 2 arms classified a docs-only project BROWNFIELD and derived it correctly; the proposed wording would have broken that. **No version field**, per Decision 12 | done |
| 15.2 | #8 closed. The *statement* shipped in 3.2.2 (protocol files are overwritten, customisation goes in project files, `.bak` retained for changed files). **The merge algorithm is REJECTED** on Decision 12's own reasoning: semantic diff is non-deterministic and that decision mitigated it precisely by making protocol files always-overwrite. **No version field**, same decision | done |
| 15.3 | Round on #7a, 6 arms. **NULL — #7(a) does not land**: captured 3/3 baseline · 3/3 treatment, with `05` catching it 6/6, so §6's CRITICAL rule already does the job. The objection's prediction was wrong — the mandated section filled 3/3 → `work/15/15.3/04_verify.md` | done |
| 15.4 | Round on #5, `PROTOCOL_CHECK` leaves no trace. Principle settled (guarantee 3); the form costs a write per file touched, so it needs a harm arm | todo |
| 15.5 | #6 absence never supports a PASS of presence — landed in §4 · #7c precedence `rules > plan > memory`, with tool-private memory ranked last — landed in §3 · #11 foreign files as a 6th UPGRADE PLAN category, listed and never touched | done |
| 15.6 | #4 resolved **without** an exception clause: §3 now names what the limit protects — keep the sections the project has, drop the rest. Evidence from the greenfield arms: both adapted the map to a codeless repo unaided, but one dragged code sections along filled with `n/a`, which is the friction the report felt | done |
| 15.7 | #9 sessions are disposable. **The rule already exists and measures 0/10** (Decision 21), so the proposal as worded would fail identically; what is new is the trigger. *"And commit"* stays out — commit cadence is the user's | todo |
| 15.8 | The method proposal landed as a **norm, not a gate**: §4 states the author is the weakest verifier and asks for a second agent where one exists, with an explicit fallback clause where none does. Gating it would exclude anyone without a second model | done |
| 15.9 | **The case 15.3 could not reach**: a standing rule that does *not* announce itself — arriving as a correction, across turns, or inferred. How this repo's own private `memory/` entries arrived. The next round | todo |
| 15.10 | EARS-formatted `✅ Validation` criteria, 6 arms. **INCONCLUSIVE — change nothing.** FORM 0/3 vs 3/3 (confirms the clause applied, not a result); CITATION and COVERAGE both **3/3 vs 3/3, at ceiling** — every arm added its own test, so every cited command covered the change. The task gave the baseline no way to fail. A valid round must measure **criterion quality**, not citation → `work/15/15.10/04_verify.md` | done |
| 15.10a | Round 1 **void** — not scored, batch 2 not launched. Three design faults: the task premise was false (both arms caught it, §5 working); the task sat on the Micro/Standard boundary so arms split and the rule under test could not fire in half of them; and an arm produced a dangling `AGENTS.md` sentinel. Relaunching on a verified premise — `session.js` is orphaned, wiring it in is unambiguously Standard → `work/15/15.10/03_execute.log` | done |
| 15.11 | **The higher-value sibling, and nobody has measured it** — not Kiro, not us, not arXiv:2607.25398 or :2602.11988: does the approval gate (`interactiveMode=true`, stop after THINK and VERIFY) change outcomes, or only latency? It costs the user wall-clock on every task. We already have both the flag and the harness | todo |
| 15.12 | Kiro artifact comparison, run 2026-10-23 on controlled input (1.85 credits). **Its CLI has no spec flow — the `requirements/design/tasks` triple is IDE-only**, so that capability is not scriptable and was not measured. What was measured: the clarifying-questions behaviour is **harness, not model** (Plan 3 questions 2/2, default 0, same pinned model); **neither mode wrote a single artifact to disk**, the plan living only in `~/.kiro/sessions/*.jsonl` outside the repo — Decision 21 confirmed from outside; and **their permission gates block where ours only self-report** → `work/15/15.12/04_verify.md` | done |

## Milestone 16.0 — Conversation log (issue #3)
**Goal**: Decide issue #3 — an optional, harness-agnostic raw conversation log in the repo. Full triage: `drafts/prompt-logs.md`.
**Status**: in-progress — 16.1 answered the proposal; 16.2 is the form that survived it.

| Task | Description | Status |
|------|-------------|--------|
| 16.1 | Round, 9 arms, **two-turn** (new instrument: a second message sent to the running arm, since a single-prompt arm has no conversation to log). **Problem CONFIRMED at 7/9** — a correction that changed the work left no durable trace anywhere. **Proposal REJECTED at 0/9** — no log contains the second turn; all four that exist hold one entry, written at bootstrap and abandoned. Verbatim produced a summary labelled as a transcript → `work/16/16.1/04_verify.md` | done |
| 16.2 | The form that survived: **declare where the harness's own transcript lives** — one `settings.json` field, no write rule, no cadence. The harness writes it whether the agent remembers or not. Cost to state plainly: it abandons projects whose harness keeps no transcript | todo |
| 16.3 | The problem remains open and is **not** closed by rejecting the remedy: 7/9 is too large to file away. Any future candidate must hang on an event the agent recognises while producing it — Decision 21's shape — not on a per-turn cadence, which is now measured at zero twice | todo |

## Backlog (unscheduled)
- **Greenfield exit condition — the A/B was invalid** (kept for the method, the rule itself landed as Decision 19). Step 0.3 prescribes the *action* ("STOP and ask") but no *exit condition*: an agent that asks, receives a bare "ok", and considers the question asked is following the text. Four different behaviours were observed on that ambiguity. A candidate fix exists (create nothing until the answer names the project; explicit opt-in for an `UNPOPULATED` scaffold), but the A/B was **invalid** — subagents refuse coordinator messages on authority grounds regardless of the rule, and directory names leaked the hypothesis (neutral names: 1 refusal / 2 proceed; names revealing the gate: 3/3 refusals). 6/6 arms behaved identically. Consent-shaped rules are not measurable with the harness — this one needs testing by a human in a real session before it can land.
- **Greenfield bootstrap** — resolved in Decision 17 (`UNPOPULATED` marker). Two of three proposed fixes were dropped after measurement; see Decision 17 in `05-decisions-and-issues.md`. Working notes stayed in local `drafts/` (untracked by design).
- Capability Handshake as Operations Manifest in `02_tasks.md` (Fase 3 from evaluation)
- Evaluate creating a CLI tool (e.g., `npx bemyagent`) in the future to automate the file copy.
