# 23.1 — VERIFY

**Verdict: PASS_WITH_CAVEATS.** Run by an agent that did not write the script (Sonnet — the check is a script re-run on recorded inputs and short files read against written criteria), in two passes; criterion (e) and the activation were checked by the author, and are marked so.

| Criterion | Result | Evidence (commands run during VERIFY) |
|---|---|---|
| (a) one file per session, in a folder per UTC day, nothing for events without text | MET | the 34 recorded payloads replayed by the verifier → 4 files `<date>/<HHMM>-<8 chars>.md`, one per session id; none for `PostToolUse`, `SubagentStart`, `SubagentStop` |
| (b) order, headings, voices, text | MET | expected files rebuilt from the payloads with `jq` and compared with `cmp`, timestamps normalised: 4 of 4 identical; headings counted: 9 `agent`, 6 `user`, 3 `harness`, 2 `brief → general-purpose — …`; the six `SubagentStop` with an empty agent type left nothing. The verifier's caveat: its expectation uses the script's own selection rules |
| (c) hostile text literal, never exit 2 | MET | the verifier's own list (command substitutions that would leave a file, quotes, backslashes, `%` signs, a leading dash, 100 KB, unicode, CRLF, path traversal in the session id, a folder with a space): text identical by `cmp`, no trace file, nothing written outside the log folder; non-JSON, empty stdin, missing argument → exit 1, nothing written |
| (d) live runs | MET | the verifier's own headless run printed its three words and left one file with the `user` and `agent` entries; the run with a subagent was read in the author's files only (user, brief, agent, harness block with the result, agent) |
| (e) active in the new layout, old hook silent | MET — author's check | one headless run from the base after activation → `log/<date>/<HHMM>-<id>.md` with both voices; the old day file did not grow |

## Found by the verifier and corrected (first pass → second pass)
- Two events with long text at the same instant interleaved (a heading lost in 2 of 3 runs of 20 parallel 3 KB events) → per-session lock; second pass: 6 of 6 runs intact, no lock left, a stale lock costs about 2 s once.
- A directory with the session file's name was taken for the file → `find -type f`.
- An empty subagent type left the heading open → falls back to `agent`.

## Caveats that stand
- Trailing newlines of a message are dropped.
- A session id that is not a string, or holds no letter or digit, loses its entry (exit 1). Not seen in any real payload.
- Two session ids with the same first 8 characters share a file.
- An unwritable log folder costs about 2 s per event before exit 1.
- `sleep 0.1` was tried on macOS only.
- A message the user sends straight to a subagent reaches no hook and is not logged (the user's choice, 2026-11-20).
- The `harness` label recognises two block names of this tool; any other block is headed `user`.
- Not decidable here: several days of use; any harness other than this one.

## Amendment 1 (2026-11-21) — checked by the author only
The layout became a folder per month (`<YYYY-MM>/<DD>-<HHMM>-<session>.md`, full timestamp in the heading) after both independent passes. Four lines of the script changed; the checks are in `03_execute.log` [9] — same session → one file, parallel long entries intact, hostile text literal, one live run in the new layout. The verdict above was given on the day layout; nothing the verifier tested depends on the folder's name, but nobody other than the author has run the script in this form.

## The script as activated (`<base>/.claude/conversation-log.sh`, outside the repo)
```sh
#!/bin/sh
# Conversation log — one file per session in a folder per month:  <log folder>/<YYYY-MM>/<DD>-<HHMM>-<session>.md
# (UTC; the name is the session's first entry — a session that runs past midnight stays in its file)
# Called by three hooks, with the event as JSON on stdin:        conversation-log.sh <log folder>
#   UserPromptSubmit      -> what arrived as a prompt (the user's message, or a block of the harness)
#   Stop                  -> the agent's final message of the turn
#   PreToolUse on Agent   -> the brief handed to a subagent
# The text is data: it goes from jq to the file and is never evaluated. Never exits 2 (2 would block the turn).

log=${1:-}
[ -n "$log" ] || { echo "usage: conversation-log.sh <log folder>" >&2; exit 1; }
input=$(cat) || exit 1

sid=$(printf '%s' "$input" | jq -r '(.session_id // "nosession") | gsub("[^A-Za-z0-9]"; "") | .[0:8]') || exit 1
[ -n "$sid" ] || exit 1

entry=$(printf '%s' "$input" | jq -r --arg ts "$(date -u +%FT%TZ)" '
  def entry(voice; text): "## \($ts) · \(voice)\n\n\(text)";
  if .hook_event_name == "UserPromptSubmit" and ((.prompt // "") != "") then
    entry(if (.prompt | test("^\\s*<(task-notification|agent-message)[ >]")) then "harness" else "user" end; .prompt)
  elif .hook_event_name == "Stop" and ((.last_assistant_message // "") != "") then
    entry("agent"; .last_assistant_message)
  elif .hook_event_name == "PreToolUse" and ((.tool_input.prompt // "") != "") then
    entry("brief → \(if (.tool_input.subagent_type // "") != "" then .tool_input.subagent_type else "agent" end)"
          + (if (.tool_input.description // "") != "" then " — \(.tool_input.description)" else "" end);
          .tool_input.prompt)
  else empty end') || exit 1
[ -n "$entry" ] || exit 0

dir=$log/$(date -u +%Y-%m)
mkdir -p "$dir" || exit 1

# one writer at a time per session: two events can land in the same instant (a reply and a subagent's report)
lock=$dir/.lock-$sid
tries=0
until mkdir "$lock" 2>/dev/null; do
  tries=$((tries + 1))
  [ "$tries" -lt 20 ] || break   # about 2 s; a lock left by a dead run is then taken over and removed below
  sleep 0.1
done
file=$(find "$dir" -type f -name "*-$sid.md" | head -n 1)
[ -n "$file" ] || file=$dir/$(date -u +%d-%H%M)-$sid.md
printf '\n%s\n' "$entry" >> "$file"
status=$?
rmdir "$lock" 2>/dev/null
[ "$status" -eq 0 ] || exit 1
```
