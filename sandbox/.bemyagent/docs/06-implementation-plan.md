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
**Status**: in-progress

| Task | Description | Status |
|------|-------------|--------|
| 4.1 | Localization & directory encapsulation in `.bemyagent/` | done |
| 4.2 | Hierarchical structure for `work/` directory | done |
| 4.3 | Evolution modules (Context Probing, Session Restore, Quick Ref Card) | done |
| 4.4 | Bootstrap hardening & anti-hallucination rules | done |
| 4.5 | Test Context Probing on a real task | next |

## Backlog (unscheduled)
- Capability Handshake as Operations Manifest in `02_tasks.md` (Fase 3 from evaluation)
- Evaluate creating a CLI tool (e.g., `npx bemyagent`) in the future to automate the file copy.
