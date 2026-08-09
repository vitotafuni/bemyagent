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
| 12.1 | Survey + overlap check → `drafts/landscape-analysis.md`; most rival mechanisms already covered or bettered | done |
| 12.2 | Milestone convergence gate — 3 rounds / 15 arms: drafted rule laundered fraud 3/3, reworded 0/3; landed in §6 | done |

## Backlog (unscheduled)
- **Greenfield bootstrap loses the project description** (reported 2026-08-05) — the Step 0 GREENFIELD stop is contradicted by the preamble's "Do NOT ask permission between steps", and no rule routes late-arriving project context into `01-overview.md`. Root causes confirmed, fix not chosen → `drafts/greenfield-context-capture.md`
- Capability Handshake as Operations Manifest in `02_tasks.md` (Fase 3 from evaluation)
- Evaluate creating a CLI tool (e.g., `npx bemyagent`) in the future to automate the file copy.
