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

## Backlog (unscheduled)
- Capability Handshake as Operations Manifest in `02_tasks.md` (Fase 3 from evaluation)
- Evaluate creating a CLI tool (e.g., `npx bemyagent`) in the future to automate the file copy.
