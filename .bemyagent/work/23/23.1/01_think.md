# 23.1 — THINK

## Context
The user (2026-11-20): the conversation log holds only their words; they want the agent's replies beside them, kept in the project until they delete them, and parallel sessions kept apart. After a probe (design, trial and its results: `docs/drafts/log-both-sides.md`) the user approved the layout and said *go on*: write the real hook in place of the probe and try it here for some days.

What the probe showed, on this harness (Claude Code), in headless and in an interactive session: a prompt hook, an end-of-turn hook and a hook on the agent-launching tool receive the user's message, the agent's final message and the brief; a subagent's report arrives at the parent as a prompt inside a block of the harness; events without an agent type arrive after every turn and are noise; a message the user sends straight to a subagent reaches no hook (left out by the user's choice, as a stated limit).

### Context Saturation Check
- [x] **Target files/paths** — outside the repo, in the base: `<base>/.claude/conversation-log.sh` (new), `<base>/.claude/settings.local.json` (the one hook it holds is replaced), `<base>/23.1-probe.settings.json` (removed at the end). In the repo: this folder, the plan row, the draft.
- [x] **Expected behavior** — `log/<UTC date>/<HHMM>-<session>.md`; three kinds of entry (prompt as received, agent's final message, brief); one file per session; nothing asked of the model.
- [x] **Constraints** — the text is data and is never evaluated by a shell (16.2); the protocol's line on the log is not touched here (that is 23.2, a release); the log stays git-ignored; no machine path in what the repo keeps.
- [x] **Dependencies** — `jq` and a POSIX shell, both on the machine (`/usr/bin/jq`). No new dependency for the project: the hook is local tooling.

## Approaches Considered
1. **One script, called by three hooks, the entry built by one `jq` program** (chosen). The event's JSON goes to `jq`, which decides the kind of entry and emits heading and text together; the shell only names the file. One place to read, one append per event.
2. **Three inline commands in the settings file**, as the present hook is. Pro: no second file. Con: three copies of the file-naming logic inside JSON-escaped strings — unreadable, and the worked example for 23.2 has to be readable by a small model.
3. **A converter run at the end of the session over the harness transcript.** Pro: everything is there, the message to a subagent included. Con: reads an undocumented format; nothing is written if the session dies; the log would lag the conversation it is insurance for.

## Pre-mortem
- *The hook breaks the turn* (a non-zero exit of a prompt hook can block the prompt). Mitigation: the script never exits 2; every failure ends in exit 1 with one line on stderr; checked with a broken input.
- *The session's file is not found again and every turn opens a new file.* Mitigation: the file is looked up by the session's short id inside the day's folder before one is created; checked with two events of the same session, and with two sessions.
- *Text is mangled or evaluated* (quotes, `$(…)`, backslashes, a newline). Mitigation: the text never leaves `jq` except as the entry's bytes, appended with `printf '%s'`; checked with the 16.2 strings and by replaying the probe's real payloads.

## Devil's Advocate
Keep the one-voice log and tell the user to keep the harness transcripts instead (a setting of the tool lengthens their life). Zero code. Not taken: it leaves the record in a folder outside the project, in a format only this tool reads, and the user asked for the opposite — the project owns it, the user deletes it.

## Selected Approach & Risks
Approach 1. Standard: a script and a settings file. Estimated cost: low.

The script, as planned (the final text is whatever passes the checks, logged in `03`):
```sh
#!/bin/sh
# Conversation log — one file per session in a folder per day.
# Called by three hooks with the event as JSON on stdin:  conversation-log.sh <log folder>
log=${1:?usage: conversation-log.sh <log folder>}
input=$(cat) || exit 1
sid=$(printf '%s' "$input" | jq -r '(.session_id // "nosession") | gsub("[^A-Za-z0-9]"; "") | .[0:8]') || exit 1
entry=$(printf '%s' "$input" | jq -r --arg ts "$(date -u +%TZ)" '<program>') || exit 1
[ -n "$entry" ] || exit 0
dir=$log/$(date -u +%F)
mkdir -p "$dir" || exit 1
file=$(find "$dir" -name "*-$sid.md" | head -n 1)
[ -n "$file" ] || file=$dir/$(date -u +%H%M)-$sid.md
printf '\n%s\n' "$entry" >> "$file" || exit 1
```
`<program>`: `UserPromptSubmit` with a prompt → heading `user`, or `harness` when the prompt opens with a `<task-notification>` or `<agent-message` block, then the prompt; `Stop` with a `last_assistant_message` → heading `agent`, then the message; `PreToolUse` with a `tool_input.prompt` → heading `brief → <subagent_type> — <description>`, then the brief; anything else → nothing.

Hooks: `UserPromptSubmit`, `Stop`, `PreToolUse` with matcher `Agent|Task`, each `"$CLAUDE_PROJECT_DIR/.claude/conversation-log.sh" "$CLAUDE_PROJECT_DIR/src/.bemyagent/log"`, synchronous, timeout 10 s.

Risks:
- Sessions started elsewhere than the base have another `CLAUDE_PROJECT_DIR` and no hook: as today.
- Old day files (`log/YYYY-MM-DD.md`) stay beside the new folders; nothing converts them.
- The `harness` label depends on two tag names of this tool; a block of another shape is headed `user`. The user judged the blocks well marked by themselves; the label is a courtesy.
- A session that crosses midnight UTC opens a second file in the next day's folder.

## Verification Plan
Replay of the probe's recorded payloads through the script into a scratch folder; hostile strings; a broken input; then two real headless runs with a settings file that points the hooks at a scratch folder, one of them launching a subagent; then activation and one real turn of this session read in the log. Criteria in `02_tasks.md`. VERIFY by an agent that did not write the script.
