# Overview: BEMYAGENT

BEMYAGENT is a lightweight, markdown-based bootstrapping protocol designed to initialize AI-assisted software projects. It provides a standardized directory structure and a rigid workflow (Fractal TTE & Lazy Loading) to prevent AI context bloat, reduce token consumption, and maintain deep historical logs of executions without confusing the AI.

## Repository Structure
- `/BEMYAGENT.md` - The core executable prompt/template to be fed to AI.
- `/README.md` - The human-facing description of the project.
- `/sandbox/` - The dogfooding directory where the protocol is tested and where the project itself is managed.
  - `/sandbox/.bemyagent/docs/` - Permanent, immutable truth (architecture, rules).
  - `/sandbox/.bemyagent/work/` - Volatile memory, execution traces, and tasks.

## Quick Start Commands
- Drop `BEMYAGENT.md` in your repo and ask the AI: "Read BEMYAGENT.md and execute the bootstrap".

## Environment Variables
*(None for this documentation project)*

## Ports
*(None for this documentation project)*
