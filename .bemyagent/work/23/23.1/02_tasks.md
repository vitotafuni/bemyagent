# 23.1 — TASK

**Delivers:** after a turn in a session started at the base, the user opens `log/<date>/<time>-<session>.md` and reads their message and the agent's reply under it; a second session the same day has a file of its own.

`<base>` is the folder that holds `src/`; `<out>` is a scratch folder.

## Checklist
| # | Step | Status |
|---|---|---|
| 1 | Write `<base>/.claude/conversation-log.sh` as planned in `01_think.md`; executable | done |
| 2 | Replay: every line of `log/probe.jsonl` through the script into `<out>`; read the files | done |
| 3 | Hostile input: a prompt with quotes, `$(whoami)`, a backtick command, a backslash, a newline, a leading `-`; an input that is not JSON; an event with no text | done |
| 4 | Live: a settings file with the three hooks pointing at `<out>`; two headless runs (`claude -p --settings …`), one plain, one launching a subagent; read the files | done |
| 5 | VERIFY by an agent that did not write the script; `04_verify.md` | done — PASS_WITH_CAVEATS, two passes |
| 6 | Activate: `<base>/.claude/settings.local.json` gets the three hooks in place of the present one (a copy of the old file kept beside it); the next real turn of a session is read in the log | done |
| 7 | Remove the probe's settings file and `log/probe.jsonl`; plan row; draft updated | done |

## CDM
- ✅ **Validation**:
  (a) replaying the probe's payloads gives one file per session id, named `<HHMM>-<8 characters>.md` inside a folder named by the UTC date, and no file for an event that carries no text;
  (b) inside a file the entries are in the order of the events, each under `## <time> · <voice>`, with `user`, `agent`, `brief → …` and `harness` each present where the payload calls for it, and the events with an empty agent type leave nothing;
  (c) the hostile prompt is in the file byte for byte and no command in it ran; a non-JSON input ends in exit 1, never 2, and writes nothing;
  (d) two live headless runs leave two files, each with the prompt and the reply that the run printed; the run with a subagent also holds the brief and the block that carries the report;
  (e) after activation, a turn of a real session is in the new layout, and the old one-voice hook no longer writes.
  Not decidable here, and reported as such: several days of use; any harness other than this one.

## Amendment 1 — 2026-11-21, from the user, after activation
*Not convinced by a folder with the full date: a user who never deletes ends with a folder per day for ever.* → a folder per month, the day in the file's name: `log/<YYYY-MM>/<DD>-<HHMM>-<session>.md`; the heading carries the full timestamp (`## <date>T<time>Z · <voice>`), since a session that runs past midnight now stays in its file. Criteria (a) and (e) are read on this form. No filesystem limit was at stake (365 folders a year); the reason is a listing a person can read and clean.
