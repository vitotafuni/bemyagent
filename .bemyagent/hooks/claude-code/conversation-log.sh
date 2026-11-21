#!/bin/sh
# Conversation log: appends one entry to <log folder>/<YYYY-MM>/<DD>-<HHMM>-<session>.md (UTC).
# Called by the harness with the event as JSON on stdin:  conversation-log.sh <log folder>
# The text goes from jq to the file and is never evaluated. Never exits 2 (in this harness 2 blocks the turn).

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
file=$(find "$log" -type f -name "*-$sid.md" | head -n 1)   # any month: a session that runs past the end of one stays in its file
[ -n "$file" ] || file=$dir/$(date -u +%d-%H%M)-$sid.md
printf '\n%s\n' "$entry" >> "$file"
status=$?
rmdir "$lock" 2>/dev/null
[ "$status" -eq 0 ] || exit 1
