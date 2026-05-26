# Overview: BEMYAGENT

BEMYAGENT is a lightweight, markdown-based bootstrapping protocol designed to initialize AI-assisted software projects. It provides a standardized directory structure and a rigid workflow (Fractal TTEV & Lazy Loading) to prevent AI context bloat, reduce token consumption, and maintain deep historical logs of executions without confusing the AI.

## ⚠️ Self-Referential Project

This repository IS the source code of the BEMYAGENT protocol. The protocol governs its own development (dogfooding).

**Key distinction:**
- **`/BEMYAGENT.md`** — The **source template** (SRC). This is the distributable artifact: the prompt users drop into their repos. It MUST be updated whenever `00-ai-rules.md` or the bootstrap workflow evolves. Treat it as production code, not documentation.
- **`/.bemyagent/`** — The **live instance** of BMA governing this project. Same protocol, applied to itself.

**Rule:** Never delete `BEMYAGENT.md`. When integrating a draft or changing a rule in `00-ai-rules.md`, always propagate the change to the corresponding section in `BEMYAGENT.md`.

## Success Metrics (Measurable KPIs)
- Token consumption per task (reduction)
- Context window drift and hallucinations (reduction)
- Human orientation time when returning to a project (reduction)

## Repository Structure
- `/BEMYAGENT.md` — Source template (SRC). The distributable bootstrap prompt.
- `/README.md` — Human-facing project description.
- `/.bemyagent/docs/` — Permanent knowledge (architecture, rules, decisions).
- `/.bemyagent/work/` — Volatile memory (execution traces, task logs).

## Quick Start Commands
- Drop `BEMYAGENT.md` in your repo and ask the AI: "Read BEMYAGENT.md and execute the bootstrap".

## Environment Variables
*(None for this documentation project)*

## Ports
*(None for this documentation project)*
