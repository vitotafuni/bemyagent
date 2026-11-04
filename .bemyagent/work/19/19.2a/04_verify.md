# VERIFY — 19.2a, the harm arm of the content-branch candidate

Every criterion executed in the arm's own tree, against the seeded bytes recovered from that
arm's own setup commit. Raw output `03d_score_output.json`, scorer `score.py`, table
`03c_arm_evidence.txt`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| Delta is one clause | PASS | `03b_delta.diff`, line 12, two changed lines |
| The condition cannot leak through the rules file | PASS | `00-ai-rules.md` byte-identical across sides (`cmp`) |
| Six seeded `.bemyagent/` trees identical | PASS | `diff -r`, no divergence |
| The things worth protecting present before launch | PASS | §7 hand-edit, foreign file, `work/1/1.1`, non-default settings |
| Fixture green | PASS | `npm test` 4 pass 0 fail |
| Each batch complete before the next | PASS | three batches, six arms returned |
| Scorer and raw output copied here before the verdict | PASS | `score.py`, `03d_score_output.json` |

## The result

| | q34 A | q35 B | q36 A | q37 B | q38 A | q39 B |
|---|---|---|---|---|---|---|
| routed to UPGRADE | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| user's team rules alive | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `work/1/1.1` untouched | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| foreign file byte-identical | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| non-default settings kept | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Nothing was lost on either side, 6/6.**

## Verdict: the clause does not cost the protection, and that is all this round bought

The pre-registered reading was *B loses nothing that A does not also lose → the clause is safe
and 19.2b may buy the benefit round*. That is the outcome. **19.2b is authorised, and nothing
more.**

The honest size of the result has to be stated with it, because the number is 6/6 and 6/6 reads
as strong. The clause changes behaviour **only where `.bemyagent/` holds nothing to protect**.
This fixture holds a great deal, so both conditions route to UPGRADE and run the same path, and
a tie was the expected outcome before launch — it is pre-mortem 1, written down in `01_think.md`
before any arm ran. A tie here is **necessary and not sufficient**: it rules out the harm, it
does not evidence a benefit, and quoting 6/6 as support for the clause working would be the
substitution this repo's whole record exists to avoid.

## What the round found that was not the question

**Step 0's APPLY behaves well under pressure, measured rather than assumed.** 6/6 arms spotted a
user's section inside a protocol-owned file, moved it into `05-decisions-and-issues.md` *before*
overwriting, and kept the backup. 6/6 identified the foreign file as another tool's and left it
byte-identical. 6/6 preserved non-default settings instead of resetting to template defaults.
None of that was known; 19.1 observed arms on an install with nothing to protect, so the
protective path had never actually been exercised.

**The hand-edit trap also exposed a real defect in the fixture's own content**, found by several
arms independently: the team's appended section was numbered `## 7`, colliding with the
protocol's own §7. Not planted deliberately, and the arms renumbering or flagging it is evidence
they read rather than pattern-matched.

## Caveats

1. **A tie by construction is not a measurement of the clause.** Stated above and in
   `01_think.md` before launch rather than discovered here.
2. **The scorer produced a false negative against the treatment** and it would have been the
   headline: matching the user's conventions as whole sentences marked q35 as having preserved
   them only in a backup, when it had migrated them into `05` in its own words. Corrected with
   four arms still unrun. **Third instrument correction in two rounds, every one of them running
   against the arms**, and every one caught by reading the failing arm rather than its number.
3. **One arm was stopped by the coordinator.** q35 sent five identical completion notices with
   its tool count frozen at 40 and its token count climbing. Before stopping it: all four TTEV
   files present, upgrade log written, `upgrade-plan.md` cleaned up, no file modified in three
   minutes, no process and no listener. The tree was final, so the arm counts. Had any check
   failed the arm would have been voided and rebuilt.
4. **An observation that belongs to 19.3, not here.** Two arms installed the `PROTOCOL_CHECK`
   directive block into `CLAUDE.md` themselves. 19.3 measured Write Gate coverage at 55% in trees
   where that block was absent from the file the tool loads, so **55% may be a floor rather than
   a ceiling**. Recorded, not folded into 19.3's verdict after the fact.
5. **Delivery was not scored.** This is a harm round; whether the clause costs deliveries is the
   benefit round's business.
