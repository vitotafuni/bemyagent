# 21.4 — THINK

## Context
`specs/restore-integrity.md`, third criterion: the candidate line — *"Read this file whole — first line to last, every time, a context compaction included. A slice of it, or what you recall of it, is not a read."*, second line of the rules file — is tested by clean arms that did not write it, against the same arm without it, on a restore after a compaction. It stays in both files on a pass and leaves both otherwise. The agent that wrote the line designs nothing it will read alone: the apparatus is built by a subagent, checked by an independent one, launched by the user, and read by a script and a second independent agent.

What is known before designing:
- At session start clean arms read the rules whole — 0 of 6 incomplete (`work/21/21.2/04_verify.md`). A start-of-session round is at ceiling.
- In main sessions 7 of the 9 chosen slices followed a compaction (same file). The occasion is the segment after a compaction.
- From the tool's documentation (doc-lookup agent, 2026-11-14; *stated* or *inferred* as marked):
  - `/compact` sent as a prompt runs a compaction in the SDK loop (*stated*); that `claude -p --resume <id> "/compact"` does the same is *inferred* — `-p` wraps the same loop. **Untested: the pilot tests it.**
  - A resumed call keeps the session id and appends to the same transcript (*stated*). `--model` is repeated on every resumed call (*stated*).
  - After a compaction the project-root `CLAUDE.md` is loaded again (*stated*) — the sentinel is back in context without the arm doing anything. Up to five files the session read or edited are re-read, most recently modified first; a file over 5,000 tokens returns as a path only (*stated*). The rules file is about 14 KB — under that limit — and was last modified when the tree was seeded, so it ranks behind everything turn 1 writes; whether it comes back is **recorded per arm, not assumed**.
  - The stream output carries a `system` / `compact_boundary` message with `compact_metadata.trigger` and `pre_tokens` (*stated* for the SDK, *inferred* for `-p`). The form of a compaction in the transcript on disk is not documented.
- `--resume` under `-p` has never run in this repo: 21.1's pilot was to be the first, and has not been launched. This round's pilot answers the same question for itself, so 21.4 no longer waits on 21.1.

### Context Saturation Check
- [x] **Target files/paths** — `work/21/21.4/` (apparatus, on `main`); the candidate itself is one commit on `bma/21.4` touching `.bemyagent/docs/00-ai-rules.md` and `BEMYAGENT.md`; arm trees and outputs in the scratchpad.
- [x] **Expected behavior** — the readings table of `02_tasks.md`.
- [x] **Constraints** — clean headless arms, launched by the user; the main agent never runs the real binary; numbers only out of transcripts; no machine trace in repo files (`harness/README.md`, last section); control and treatment in the same batch (`harness/README.md`, *Which model the arms run*).
- [ ] **Dependencies** — one unknown: whether `/compact` works under `-p --resume`. **Assumption: it does.** The pilot arm is the test; the launcher gates each arm on a proven compaction; the fallback is approach B.

## Approaches Considered
- **A — three calls on one session**: turn 1 (a task; the arm restores and works) → `/compact` → turn 2 (a second task). The segment after the boundary is the restore under test. Deterministic occasion, same session, the compaction is the tool's own.
- **B — auto-compaction forced by a small window** (`--autocompact 100k`): the compaction arrives mid-work, as it does in a real session. But the lowest window is 100k tokens and the trigger point is not guaranteed; a turn that never reaches it is an arm with no occasion.
- **C — a fresh session told it has been compacted** (a hand-written summary in the prompt). Cheap and exact, but the summary would be the author's text: the proxy would measure the author's idea of a compaction.
- **D — census of the main agent's next restores**: the author checking itself; ruled out by the user (2026-11-12).

## Selected Approach & Risks
**A**, with B as the pivot. Two conditions, three Sonnet arms each, one pilot: **C** = the rules as released (`main`), **L** = the same with the line, taken from the ref `bma/21.4` (`git show`), never retyped. All six in one batch; the control is read first.

Estimated cost (weights of `harness/tokens.py`; turn 1 measured in 20.11, the rest assumed): turn 1 ≈ 136k, the compaction ≈ 15k, turn 2 ≈ 60–130k → ≈ 240k per arm, **≈ 1.7 M for seven arms** (1.3–2.1 M).

**Pre-mortem**
1. *`/compact` is refused or does nothing under `-p`.* → pilot first; per arm the launcher requires proof of the compaction (boundary in the stream output or in the transcript) and skips turn 2 without it.
2. *The harness hands the rules back whole after the compaction.* Then the arm has them without acting and the line has nothing to do. → the reader looks for the rules' section headings in the segment after the boundary outside the arm's own tool results; an arm where all eight are present is **not an occasion** and leaves reading (i).
3. *The control sits in the middle.* Likely on the census (some restores after a compaction were whole). → stated in the readings before launch: 1–2 of 3 in the control is *under-powered* and licenses nothing; the round then says so and the choice — ten arms a side or drop the candidate — is the user's.
4. *The reader calls a slice whole, or a whole read a slice.* → it reuses the 21.2 census's access classifier, is run on built transcripts of every class before launch, prints each arm's sequence after the boundary (tool, class, sections covered — never text) for a hand-read, and is attacked by the independent verifier.
5. *Turn 2 is too small to be "a task".* → it is a feature of turn 1's size, asked for now, in words that do not name the rules.
6. *The arm's own tool memory carries "read it whole" across the compaction.* → the launcher records whether the arm's memory folder exists after turn 1 and how many files it holds; reported beside (i), not removed — a main session has it too.

**Devil's Advocate** — do not run it: the census already says nine of ten partial restores were chosen slices, the line costs 35 tokens, ship it. Not taken: the user's ruling of 2026-11-14 — `main` holds only what is measured — and the census cannot say whether a sentence the agent reads only when it opens the file changes what it does when it believes it has already read it.

## Verification Plan
1. Before launch — independent VERIFY of the apparatus (strongest tier: the job is to attack the reader's classes and the eligibility rule, a judgement task; not the builder, not the author): seeds differ between C and L by one line in two files and nothing else; the launcher cannot reach the real binary in the dry-run; the reader is right on built transcripts of every class and wrong on none; the readings can fail in both directions.
2. Pilot (one C arm, the user's launch): `check_pilot.sh` prints whether resume kept the session, whether the compaction is proven and how, whether the rules came back by themselves, and the cost of each call.
3. After the six: the script's output and each arm's sequence go to an independent agent for the hand-read and the verdict by `harness/README.md`'s table; `04_verify.md` is written by it. The main agent reports, it does not score.

## Pivot — 2026-11-16 (the user chose a new design after the pilot)

### What the pilot of approach A showed (2026-11-15, `03_execute.log`)
`/compact` compacts under `-p --resume`, the session is kept, nothing of the rules is handed back — and the control arm (released rules) re-read the file whole by its own act before its first write. After the boundary the tool had left a **reference** to the rules file (`compact_file_reference`: the file was read before, is too large to include, read it again if needed). Read by the designer alone from the reader's output; the check stopped on one request copy it could not read. The pilot is not counted. The six of approach A are not run: with one control arm reading whole they would most likely end in *ceiling*.

### What the census's occasions looked like (a Sonnet agent, 2026-11-16; numbers and type names only; scripts in `<scratchpad>/p218/`)
The event-level script of 21.2 is no longer on disk; the agent rebuilt the events from `census.py` and this task's `boundary.py` and does **not** reproduce 21.2's totals (34 events after a compaction, 9 partial, against 21.2's 7). Same order of size, not the same counts.
- Trigger: automatic in 33 of 34. The one manual compaction was partial. Tokens before the boundary: 170k–800k; the pilot had 65k.
- A user prompt between the boundary and the first access to the rules: 8 of 9 partial, 11 of 15 whole. **It does not separate them** — the designer's first guess (the control read whole because turn 2 was a new task and the sentinel says *before every task*) is not supported.
- **A reference to the rules file after the boundary: 0 of 9 partial, 5 of 15 whole**, and the 5 sit in two transcripts. Every partial event is a shell slice (`sed`, `grep`, `awk`, `wc` with a range); 9 of the 15 whole ones are a plain `Read`.
- When the tool leaves that reference: `file` plus reference attachments never exceed 5 per boundary; 8 of the 9 events with a reference are in sessions that had touched 5 distinct files or fewer (the pilot: exactly 5, the rules file last of them). Neither recency rank nor distance in tool calls separates yes from no cleanly; one event with a reference had 29 files, two without had 4. This agrees with the tool's documentation (up to five files the session read or edited, most recently modified first, a file over 5,000 tokens as a path only) and does not prove it.

### What the documentation says about an automatic compaction (doc-lookup agent, 2026-11-16)
*Stated*: `--autocompact <tokens>` (100K–1M), `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (1–100, the share of the window at which it triggers; the only documented way below 100K); after a compaction the project instruction file is loaded again and up to five recent files are re-read. *Inferred, not stated*: that the percentage applies to a window set by the flag; that auto-compaction runs under `-p`; that the turn goes on by itself after it.

### Approaches re-evaluated
- **A2 — approach A with the reference removed.** Same three-call shape and the same verified apparatus; the session touches more than five files after its restore and before the compaction, so the rules file falls out of the set the tool hands back. Done by one more call before the compaction (a second small feature, **turn 1b**), not by a longer prompt: the files touched are then the arm's own, and the rules read is one task old, as in the census. Aims at the one difference that stands out. What it changes in the apparatus: one more call in `launch.sh`, one prompt file, a gate "no attachment of any kind names the rules file after the boundary", the window unchanged.
- **B — automatic compaction inside one long turn.** Nearer the census on trigger and on size, but rests on three inferred behaviours, needs a turn several times longer (the pilot's turn 1 ended at 65k tokens; the lowest documented window is 100K) and a new way to prove where the compaction fell. The census does not say the trigger matters (33 of 34 automatic in both classes).
- **A2 on a larger model**, or with a longer history: more of the census's conditions at once, several times the cost, and a result that would not say which condition did it.
- **Stop**: record the pilot and drop the line. Turned down by the user (2026-11-16).

### Selected: A2, pilot first, and the pilot decides whether the six are worth launching
Stated before the pilot of A2 is run:
1. The pilot (`q902`, C, not counted) must show **no reference and no text** of the rules file after the boundary. If the reference is still there, the occasion was not produced: the six are not launched, the design goes back to the user.
2. If the occasion is produced and the pilot's control arm **still reads whole** before its first write, the six are not launched: two control pilots out of two at `whole` say *ceiling* cheaply. Recorded as that, not as a verdict on the line; the line then stays untested and the choice — drop it, or another harness — is the user's.
3. Only a pilot that produced the occasion and did **not** read whole opens the six, by the table and the definition of `whole` closed in Amendment 3. The pilot's class decides whether tokens are spent, never how the six are read.

**Cost** (weights of `harness/tokens.py`; the pilot of A measured 565k: turn 1 139k, the compaction 161k, turn 2 266k): with turn 1b about 0.8M for the pilot, about 5M for the six if they are opened.

**Pre-mortem**
1. *The rules file is still among the files handed back.* The rule the tool picks by is not established. → the gate of point 1; the launcher records the count of distinct files touched before the boundary; if five more files are not enough the pilot says so for 0.8M, not for 5M.
2. *Turn 1b's restore re-reads the rules (the sentinel) and brings the file back to the front.* If the tool orders by the file's modification time this does not matter; if by last read it does. → not assumed: the gate of point 1 catches it either way.
3. *The proxy still is not the census* (a clean Sonnet arm of 100k tokens against main sessions of 170k–800k). → said in the verdict whatever it is; a *ceiling* here is "not reproduced by this harness", not "the failure does not exist".
4. *The apparatus is changed again after three verify passes.* → the change is one call and one gate; the builder's selftest and a narrow pass of the same verifier on the changed path, as for C4; the five findings left open (G1–G3, X1, P1) and the request-copy stop go in the same batch.

**Devil's advocate** — ship the line untested: it costs 35 tokens a restore and the census says the slice is chosen. Not taken, for the reason of 2026-11-14: `main` holds only what is measured. The opposite — drop it now — is cheaper than any pilot and loses nothing measured; it is the user's to choose and they chose to test.
