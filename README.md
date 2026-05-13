# BEMYAGENT

> **Mission**: Save tokens for the machine. Save orientation for the human.

BEMYAGENT is a lightweight, self-bootstrapping protocol designed to initialize AI-assisted software projects. It establishes a structured environment that prevents AI context bloat, reduces token consumption, and keeps developers perfectly oriented.

## The Problem

When working with autonomous agents or AI coding assistants on complex projects, the context window quickly becomes cluttered. Agents lose track of the architecture, hallucinate changes outside the scope, or read thousands of irrelevant lines, slowing down the process and increasing costs. 

## The Solution: TTE Workflow & Lazy Loading

BEMYAGENT provides a single markdown file (`BEMYAGENT.md`) that acts as a bootstrap prompt. When fed to an AI, it automatically generates a structured filesystem:

- **`.bemyagent/docs/`**: Permanent, immutable truth (architecture, code map, tech stack).
- **`.bemyagent/work/`**: Tactical, volatile memory organized by Task/Milestone.

### Key Concepts

1. **Lazy Loading**: The AI is explicitly instructed *never* to read documentation drafts or specs during context restoration unless strictly required by the current task. 
2. **Think-Task-Execute (TTE)**: A rigid workflow inside the `.bemyagent/work/` directory. The AI must strategize (`01_think.md`), plan atomic steps (`02_tasks.json`), and log actions (`03_execute.log`) before writing any code.
3. **Self-Registration**: The AI automatically configures the project's native rule files (e.g., `.cursorrules`, `AGENTS.md`) to read the core `.bemyagent/docs/00-ai-rules.md` at the start of every session.

## Usage

1. Drop `BEMYAGENT.md` into the root of your project.
2. Ask your AI assistant to read the file and execute its instructions sequentially.
3. The AI will generate the directories and templates.
4. Delete `BEMYAGENT.md` (or keep it if you are iterating on the protocol!) and start coding.

## Contributing & Dogfooding

This repository itself uses the BEMYAGENT protocol. You can explore the `sandbox/` directory to see a live example of the generated architecture. In fact, we use this very sandbox to document, plan, and evolve the BEMYAGENT protocol itself.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
