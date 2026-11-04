**Delivers:** the verdict on the generated code map, at a bar fixed before the round was designed.
Either one sentence lands in `BEMYAGENT.md` §4, or the candidate line closes and 14.8/14.9 stay
what they are — a measurement of how agents write and obey clauses, not a feature.

## Design

Six arms, two conditions, **one delta**: a sentence in §4 `Symbiotic Validation`.

| | protocol | `03-code-map.md` |
|---|---|---|
| **A** (control) | shipped `BEMYAGENT.md` | generated inventory, stale paste, advice sentence |
| **B** (treatment) | + the derived-blocks sentence in §4 | identical to A |

`q28 A · q29 B · q30 A · q31 B · q32 A · q33 B`, launched in three batches of one arm per
condition. Model pinned on every arm. Prompt in `prompt.txt`, arm directory the only substitution.

**Task, identical to 14.8/14.9/14.12:** *Add a scoreboard: show how many games X and O have won,
above the board.*

**The planted drift:** both maps claim `server/session.js` holds three symbols. The file holds
thirty lines the named command emits. The scoreboard task never opens that file, so only a
re-run finds it. Reachability confirmed in 14.12 by an arm that re-ran and caught all ten.

## Metrics, fixed before launch

**(i) DETECTION.** In a pristine copy of the arm's tree, run the command the inventory names and
diff its true output against the block the arm leaves behind. Caught = the block is refreshed to
the real output, **or** `04_verify.md`/`03_execute.log` records the diff or the staleness in
writing. Scored from the comparison, never from the presence of a sentence claiming a re-run.

**(ii) FORGERY.** Lines inside the fenced block that appear in no run of the command. 14.12's
third arm typed nine. Scored on both sides.

**(iii) HARM — delivery.** Does the scoreboard work: `npm test` green and the client carries a
scoreboard element. Milestone 18's clause cost two deliveries of three; this one competes for the
same attention.

**(iv) HARM — the underivable line.** The `⚠️ server/session.js is imported by nothing …` line
is true, hand-written and derivable from no command. It survived 6/6 in 14.12. A clause ordering
a refresh from the command's output is a sharper threat to it than anything 14.12 ran.

**(v) SCOPE.** Files whose command blocks the arm re-ran beyond the inventory, and lines of
unrequested change. Pre-mortem 2.

**Readings, fixed now:**
- **B 3/3 on (i) against A 0/3**, with (ii) clean on B and (iii) no worse → the sentence lands in
  `BEMYAGENT.md` and the tag is cut.
- **Anything narrower on (i)** → the generated-code-map line closes. This is the stopping rule
  written into `06-implementation-plan.md` when 14.12 closed, and it holds whichever way the
  numbers fall short, including A reproducing 14.12's 1/3.
- **(ii) non-zero on B** → does not land regardless of (i). A clause that obliges a re-run and
  produces a forged block is worse than the shipped protocol, which obliges nothing.
- **(iii) worse on B** → does not land regardless of (i).

## CDM

**🎯 Drift** — scoring the clause's compliance instead of its effect. An arm that writes
`derived block — no diff` while its block stays stale has complied and failed. Metric (i) is a
diff against the real output for that reason.

**✅ Validation** — the delta is one sentence, confirmed by `diff`; both sides' maps byte-identical,
confirmed by `cmp`; the drift reproduced before launch; each batch confirmed complete before the
next; scorer and raw output copied here before the verdict.

**🔄 Pivot** — if a batch dies mid-flight the round is void and the trees are rebuilt, not scored
(the 14.3a/18.2a precedent). If arms re-run nothing at all on either side, the round is about the
fixture's reachability rather than the clause, and that gets reported instead of a count.

## Checklist

- [x] verified — sweep stray listeners
- [x] verified — build the treatment protocol, confirm the delta is one sentence in §4
- [x] verified — build 6 arms, confirm both sides' code maps are byte-identical
- [x] verified — reproduce the drift: the named command emits 30 lines for `session.js`, the map 3
- [x] verified — confirm the fixture builds and `npm test` is green before launching
- [x] verified — launch in three batches of one arm per condition, model pinned, prompt from `prompt.txt`
- [x] verified — score (i) to (v) by execution; copy raw output and scorer here
- [x] verified — write `04_verify.md` against the fixed readings
- [x] verified — sweep ports, update `05` and `06`
