# BEMYAGENT.md

> **Mission**: Save tokens for the machine. Save orientation for the human.

📖 **Website**: [bemyagent.md](https://bemyagent.md)

BEMYAGENT.md is one markdown file. You hand it to your AI coding assistant once, and it sets up a small workspace of plain files inside your project where the agent keeps its plans, its decisions and the evidence of what it did. From then on the agent works in the open, and you check its work at the level of *what* and *why* — not line by line.

No install, no runtime, no service. The protocol is text, and everything it produces is text in your repository.

*Save tokens* means less context to read: the agent should never have to read the whole project just to start again. It loads the knowledge a task needs, and widens it only when necessary.

## The Problem

When working with AI agents on complex projects, three things break down:

1. **Context bloat** — The agent reads thousands of irrelevant lines, inflating costs and slowing down.
2. **Silent drift** — The agent executes a task but drifts from the original intent. Nobody catches it until it's too late.
3. **Validation fatigue** — The human must review every line of output because there's no structured checkpoint between "done" and "delivered".

## What You Get

- **Work survives the end of a session.** Plans, checklists and decisions are files in your project, not messages in the chat. A new session reads the plan and the current task's checklist — and the task's log, when there is one — and picks up from there.
- **Starting again does not mean reading everything.** Project knowledge is kept in short maps that point to the details, and the agent is told which of them a task calls for. Specs, drafts and detailed decision records stay unread until a task needs them.
- **It asks instead of guessing.** Before any task that is not trivial the agent checks that it knows the target files, the expected behaviour, the constraints and the dependencies. If two or more are unknown, it stops and asks you.
- **The plan is written before the work.** Any task beyond a trivial edit is written down before it is executed: the approach, the alternatives considered, what success will look like. You can require your approval at that point, or let the agent run.
- **"Done" comes with evidence.** After the work, the result is checked against the criteria fixed in the plan, with commands run at that moment, and gets a verdict: PASS, PASS\_WITH\_CAVEATS or FAIL. Where a second agent or model is available, the check is run by one that did not do the work.
- **Decisions don't evaporate.** What was decided, what was turned down and why are written into the project as they happen — including the conclusions reached in conversation.
- **The ceremony fits the task.** A one-line fix leaves one line in a log, with its evidence. Anything larger gets the four files.
- **It is not tied to one assistant.** The agent registers the protocol in the rule file your tool reads (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, Copilot instructions, …).
- **Your files stay yours.** Upgrading to a newer version starts with a checklist you approve. It replaces the protocol's own files, with a backup, and never your project's documents.

## Is It for You?

It is made for work that spans many sessions, for projects that more than one person or agent touches, for wanting to know a month from now why something was done — and for anyone who has been told "done" once too often.

It is not an orchestrator: it does not run agents for you. It is a protocol the agent follows, and there is no program behind it.

## How It Works

Every task that is not trivial goes through four phases — **T**hink, **T**ask, **E**xecute, **V**erify — and each leaves a file:

```
.bemyagent/
├── settings.json                  # How the agent behaves (see below)
├── docs/                          # Permanent project memory
│   ├── 00-ai-rules.md             # The protocol itself (the agent reads this first)
│   ├── 01-overview.md             # What the project does
│   ├── 02-architecture.md         # Components and how they fit
│   ├── 03-code-map.md             # Where things are
│   ├── 04-tech-stack.md           # Technologies and versions
│   ├── 05-decisions-and-issues.md # What was decided, and why
│   ├── 06-implementation-plan.md  # Milestones and tasks
│   └── decisions/ specs/ drafts/  # Read only when a task needs them
└── work/                          # One folder per task
    └── {milestone}/{task}/
        ├── 01_think.md            # The approach, and what was considered
        ├── 02_tasks.md            # The checklist and the success criteria
        ├── 03_execute.log         # What happened
        └── 04_verify.md           # The verdict, with its evidence
```

A task too large for one session is split into sub-tasks, each with its own four files.

**You choose the pace.** In *seamless* mode the agent runs the four phases by itself and stops only if it is missing what it needs to start, or if verification finds a problem. In *interactive* mode it stops twice — after the plan and after the verdict — and waits for you. This and a handful of other switches (documentation language, depth of verification, automatic commits, …) live in `.bemyagent/settings.json`; the agent goes through them when it sets the project up.

## Get Started

1. Drop `BEMYAGENT.md` into the root of your project.
2. Ask your AI assistant to read the file and execute its instructions.
3. The AI generates the `.bemyagent/` workspace and adds a few lines to your assistant's rule file. In an empty project it first asks what you are building; in an existing codebase it does a shallow scan and fills the documents from what it finds.
4. Delete `BEMYAGENT.md` and start a fresh chat session (the bootstrap context is no longer needed).

That's it. From this point on, the agent reads `.bemyagent/docs/00-ai-rules.md` before every task and knows how to operate.

**Upgrading.** Drop the new `BEMYAGENT.md` into the project and ask the agent to execute it. It compares the file with what you have, writes a checklist and stops; you tick what to apply. Since `3.5.0` the rules file carries its release in its title (`BEMYAGENT x.y.z`), so the agent can tell you where you stand before it does anything: handed a file older than what the project runs, it says so and stops, going on only if you answer that a downgrade is what you want; handed the same one, with the rules untouched since, it says there is nothing to upgrade; otherwise — a newer file, a project with no number yet, or rules edited by hand — the checklist opens with `Upgrade: <from> → <to>`. The number is a label for you — what changes is still decided by comparing the files, and what changed between two releases is a `git diff` between their tags. Releases are the [tags](https://github.com/vitotafuni/bemyagent/tags) of this repository; a new tag is cut only when `BEMYAGENT.md` itself changes.

## Is There Evidence?

A rule written for an AI agent is a claim about behaviour, and reasoning about such a claim predicts the outcome badly. So rules proposed for this protocol are tested before they go in: the same task is given to agents with and without a rule, and what they leave behind is compared. Most rules proposed here did not survive that — several turned out inert, and one made the agent measurably worse before it was reworked.

What has been measured about the protocol as a whole — small numbers, one ten-file app; read them as that:

- On controls certified to contain no protocol text, a mid-tier model told to read the protocol file and follow it left behind a test that catches a deliberately introduced bug in 2 of 3 runs; without the protocol, none of the three runs added a test. It cost about 4× the tokens — on one task in a single session, where there is nothing to resume.
- What the protocol changed is whether the check **stays in the repository**, not whether the work was checked: in earlier rounds the runs without it were not careless — one checked the running app more thoroughly than any protocol run beside it — but most of their checks ended with the session.

The record, nulls included, is in [`.bemyagent/docs/05-decisions-and-issues.md`](https://github.com/vitotafuni/bemyagent/blob/main/.bemyagent/docs/05-decisions-and-issues.md). The test environment is in [`harness/`](https://github.com/vitotafuni/bemyagent/blob/main/harness/README.md): it is **not part of the protocol and never lands in your project** — `BEMYAGENT.md` is the only thing you copy, and it needs no runtime, no package manager and no particular operating system. The harness is kept here for anyone tuning agent instructions who wants evidence instead of intuition.

## Routines for the Human

These live here rather than in `00-ai-rules.md` so they cost nothing at session restore —
they are for you to run, not for the agent to carry in context every turn.

### Monthly audit

Every procedural rule in the protocol forces an artifact to *exist*; none checks that it is
*true*. This prompt is the reconciliation pass. Paste it into a session roughly monthly:

> "Compare `03-code-map.md` vs the real file structure; report drift. Check `01-overview.md`
> env vars vs actual config. Verify `.gitignore` coverage. Check test coverage vs recent
> changes. List recent decisions missing from `05-decisions-and-issues.md`. Flag placeholder
> sections and language inconsistencies in docs/."

### Version-control conventions

`.bemyagent/` is tracked in git by default. Teams preferring a clean VCS history may
`.gitignore` `work/` — the audit trail is kept locally and lost in VCS — and `log/`:
the optional conversation log holds both sides of your conversations verbatim (below).

### Conversation log (optional)

Your tool keeps its own transcript outside the project and deletes it after a while. The
conversation log keeps both sides **in the project** — what you wrote, the agent's final
message of each turn, the brief it hands a subagent — one file per session under
`.bemyagent/log/<YYYY-MM>/`, until *you* delete them. The agent never writes it and never
reads it at session start: a small script run by your tool's hooks does the writing.

At the end of bootstrap the agent offers to set it up and **asks first**: it writes the
script to `.bemyagent/hooks/<tool>/`, shows you the configuration, and switches it on only
on your yes, in your *personal* settings for the tool — it is a command your machine runs
at every turn. Already bootstrapped? Upgrade with the current `BEMYAGENT.md`: the plan
carries it as an optional item and never touches the log files you already have.

What is known, and what is not: the worked example is for **Claude Code** (it needs `jq`),
and that is the only tool it has been tried on — for any other the agent is told to read
its tool's documentation and translate, and nobody has measured that. On Claude Code, two
models, three runs each: told yes in advance, 4 of 6 runs ended with a working log and in
the other 2 the tool itself refused the agent's write to its settings — the agent stopped
and said so; told nothing, 0 of 6 switched it on and all 6 left the decision to the user.
A message you send directly to a subagent reaches no hook and is not in the log.

### Multi-agent dispatch

In the worktree workflow (`00-ai-rules.md` §8) the human dispatches one session per worktree,
merges via PR, and resolves conflicts. There is no automated orchestrator by design.

## Contributing & Dogfooding

This repository uses the BEMYAGENT.md protocol to develop itself. The `.bemyagent/` directory contains the live workspace where the protocol is planned, documented, and evolved — using its own rules.

Explore `.bemyagent/work/` to see real plans, logs and verification reports.

## License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/vitotafuni/bemyagent/blob/main/LICENSE) file for details.
