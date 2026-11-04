# VERIFY — 14.13, the re-run as a VERIFY obligation

Every criterion executed in the arm's own tree. Raw output `03d_score_output.json`, scorer
`score.py`, per-arm table `03c_arm_evidence.txt`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| Delta is one sentence in §4 | PASS | `03b_delta.diff`, line 97 only |
| Both sides' code maps byte-identical | PASS | `cmp` q28 against the other five, no divergence |
| Drift reproduced before launch | PASS | command 30 lines for `session.js`, map 3, 27 missing |
| Each batch complete before the next | PASS | three batches, two arms each, all six returned |
| Scorer and raw output copied here before the verdict | PASS | `score.py`, `03d_score_output.json` |

## The result

| | q28 A | q29 B | q30 A | q31 B | q32 A | q33 B |
|---|---|---|---|---|---|---|
| (i) drift caught | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| (ii) forged lines | 0 | 0 | 0 | 0 | 0 | 0 |
| (iii) scoreboard works | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| (iv) underivable ⚠️ line kept | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**A 3/3, B 3/3.** The bar was B 3/3 against A 0/3. The control is at ceiling.

## Verdict: the clause does not land, and the generated-code-map line closes

Not because the clause failed. Because **there was nothing left for it to buy.** Unaided, under
the shipped protocol, 3 of 3 arms re-ran the command and refreshed the block. A rule competing
for attention in a file that has to stay installable as one page cannot earn its lines by
duplicating what agents already do.

This is a measured ceiling, not a null from noise, and the distinction decides what gets
recorded. A null says the rule was tested and had no effect. A ceiling says the behaviour was
already there. Both end with the clause not shipping; only the second also says something true
about the baseline.

The stopping rule fixed in `06-implementation-plan.md` when 14.12 closed holds: anything short of
3/3 against 0/3 and the line closes. It closes.

## The finding that outgrew the round

**14.12's control condition and this round's control condition are the same condition, and they
read 1/3 and 3/3.** Verified file by file against the surviving trees — protocol, rules file,
seeded map, prompt, model pin, all identical. At a true rate near 0.6 both readings are ordinary
draws from the same coin.

Two consequences, and neither is cosmetic.

**1. 14.12's verdict is wrong and has to be corrected.** It concluded the generated code map does
not catch drift, from a 1/3 that the identical condition now contradicts at 3/3. The round's
other findings survive — the forged block was real and is in that round's evidence — but its
headline reverses: the generated map catches drift most of the time, and 14.12 sampled the tail.

**2. `harness/README.md` line 140 is wrong as written.** *"At N=3 a real mechanism shows as clean
separation (0/3 vs 3/3); anything narrower is noise and should be treated as a null."* That holds
when the control sits at zero. Where the control has a middling true rate, three arms do not
measure the condition, they draw from it, and this repo has been reading those draws as facts.
14.11 was already refused on this arithmetic and was called *uninterpretable* rather than null;
the README never absorbed the distinction. The fix is a separate change and is listed in `06`.

## The instrument nearly manufactured a harm

q32 improved the command its map names. Against the seeded command its block carried nine lines
that command cannot emit — its own new test file. Under the scorer's original definition that
reads as **nine forged lines in a control arm**, the same count as 14.12's genuine forgery. It
was caught because the fix ran in the direction the harness's own bias note demands: check a
proxy for bias *against the treatment*, and here against the arms, before believing its output.
Corrected with the last arm still in flight, both figures kept.

## Caveats

1. **`ran_the_command` is an unreliable field** and is reported as such, not as a result. It
   greps the arms' prose for the command string and read `false` for arms that demonstrably ran
   it. Same class as 14.12's contamination proxy.
2. **Arms share the scratchpad root.** Generic capture filenames (`inv_actual.txt`, `inv2.txt`,
   `blk3.txt`) are written side by side by concurrent arms, and one arm's verifier saw a *false*
   drift from a clobbered file. It does not reach this round's scoring, which re-runs the command
   in each arm's own tree, but it is the port-collision rule extended to the scratchpad and
   belongs in the README.
3. **Independent VERIFY is not scored here**, but 5 of 6 arms ran it with a second agent and
   those verifiers found real defects in their own arm's work. One arm said plainly that no
   second agent was available. Recorded, not counted.
4. **One subagent request refused.** q33 asked that a delete it had been denied be run by the
   coordinator. Not executed, surfaced to the user.
