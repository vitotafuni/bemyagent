# VERIFY — 16.2 the conversation log as a hook, not a rule

Verdict: **PASS.** The mechanism works, and it answers 16.1's failure at a level the protocol
cannot reach by itself. Ceremony: Micro by files touched, but recorded here rather than in
`micro.log` because it closes a round and the evidence matters.

## What was built

A `UserPromptSubmit` hook in `.claude/settings.local.json`. On every message received it appends
a UTC timestamp and the prompt to `.bemyagent/log/YYYY-MM-DD.md`, before the model sees it.
Async, 10s timeout. Both the settings file and the log directory are gitignored: this is an
experiment and does not belong in the repo until it is decided.

## Evidence

Pipe-tested before being configured, with a prompt containing newlines, quotes, backticks and
`$(whoami)`:

```
## 2026-10-27T00:06:29Z

prima riga
seconda riga con "virgolette" e un `backtick` e $(whoami)
```

Verbatim, newlines preserved, and **`$(whoami)` stayed literal** — the prompt reaches the file
through `jq`, never through shell evaluation, so arbitrary text cannot execute. Worth verifying
rather than assuming, given what passes through there.

Then live: the user sent a message, and it was in the file before this session read it.

```
## 2026-10-27T00:10:00Z

prova con questo messaggio
```

Schema validated with `jq -e`; `git status` confirms nothing new is tracked.

## What it settles

| | rule in the protocol | hook |
|---|---|---|
| the agent must remember | yes → **0/9** (16.1) | no |
| actually verbatim | no — the one arm that tried summarised | yes, never passes through the model |
| lines on the restore path | yes | zero |

16.1 measured a per-turn write rule at 0/9, and the one verbatim attempt produced a
reconstruction wearing the label of a transcript. Both failures are properties of asking a model
to remember. Neither survives when nothing is asked of it.

**This also beats the form that survived 16.1.** "Declare where the harness keeps its transcript"
accepts the harness's format, outside the repo. A hook writes the file issue #3 actually
describes: in the repo, in a format we choose.

## The limit, and it is structural

**BMA cannot ship this hook.** It can specify the contract — where the file lives, what shape it
has, how `01_think.md` and decisions cite it — and leave each harness to fill it. Claude Code
has `UserPromptSubmit`; Cursor, Codex and the rest must be checked one at a time, and a harness
without hooks gets nothing.

Same pattern already landed for the algorithm-not-script principle and the generated code map:
**specify what must be true, not how it is produced.**

## The finding that outlives this issue

Two rounds and eighteen arms to measure at zero a rule that asked for something "every turn".
The answer was never a better wording. **It was the wrong layer.**

Anything that must happen *before* X or *on every* X cannot be a prose rule — the protocol has
no way to intercept anything. This is the same boundary found against Kiro in 15.12, where their
permission gates block and ours only speak. `PROTOCOL_CHECK` is the ceiling of what a markdown
file can do.

## Recommendation

**16.3 is now the open question, not 16.2.** The mechanism is proved; what is unproved is the
contract: which path, which format, how the distilled files cite it, and what a project whose
harness has no hooks is told to do instead. That is a protocol change and needs the usual
scrutiny, not a demo.
