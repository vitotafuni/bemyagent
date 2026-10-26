# VERIFY — 15.3 mandated `## Project rules` section

Verdict: **NULL on the primary measure — and the null is the useful result.** The section does
not fail the way I predicted. It is simply unnecessary: the protocol already captures an
explicitly-stated standing rule, in every arm, without it.

## The result

| | a (baseline) | b (treatment) |
|---|---|---|
| Standing rule captured in a **durable** file | **3/3** | **3/3** |
| …reached `05-decisions-and-issues.md` | 3/3 | 3/3 |
| …also reached the rule file (`AGENTS.md`/`CLAUDE.md`) | 2/3 | **3/3** |
| `## Project rules` section filled (not left as the guide comment) | n/a | **3/3** |
| SPURIOUS — task-specific instruction generalised into a standing rule | 1/3 | 0/3 |

**6/6 captured. No separation on the measure that decides the proposal** — at N=3 only clean
separation is signal, so this is a null, not a weak positive. SPURIOUS at 1/3 vs 0/3 is noise by
the same criterion (the 13.2 standard), so no harm is established either.

Scored by reading files on disk. `BEMYAGENT.md` and `00-ai-rules.md` were excluded from the
search: they carry the protocol text, and counting them is the false positive that made 14.3's
arms look like they were citing files when they were copying rule text.

## I was wrong about the mechanism, and the reason is worth keeping

I objected that a mandated section *"even empty, with a guide line"* is the shape measured at
**0/8** in the P3 glossary round — *a mandated empty section stays empty*. **It was filled 3/3.**

The refinement: in P3 the section had to be filled with vocabulary **that did not yet exist**,
so there was nothing obvious to put in it. Here an explicit user instruction was sitting in the
prompt. **A mandated section stays empty only when nothing obvious belongs in it** — which is
the harness's own *"give the rule an occasion to fire"* trap seen from the other side. The 0/8
result was never about mandated sections; it was about mandating a container for content the
agent had no reason to produce.

So the prediction was wrong. The recommendation survives, for a different reason than I gave.

## What actually did the work

`05-decisions-and-issues.md` caught the rule **6/6**, baseline included. That is §6's CRITICAL
same-response rule — *"update `03-code-map.md` and `05-decisions-and-issues.md` in the SAME
response as any change — including discussion-only decisions"* — already doing the job the new
section was proposed to do. Two of three baseline arms *also* wrote it into `AGENTS.md`
unprompted.

**FEDERATION #7(a) is already covered for this case.** Adding the section would add lines to the
file read at every restore to buy a capability the protocol demonstrably has.

## The limit, and it is the half that matters

`01_think.md` stated this before the round: this tests the **explicit** case — an instruction
flagged in the prompt as applying to future work. A real standing rule more often arrives
**implicitly**: as a correction, across several turns, or inferred from the user's reaction.
That is the case FEDERATION #7 is actually about, and it is the case that produced the two
preferences sitting in this repo's own private `memory/` directory right now.

So the honest reading is narrow: **the protocol captures a standing rule that announces itself.
Whether it captures one that does not is untested**, and nothing here licenses a claim about it.

## Uncontrolled variable, recorded

From the *same* §1 text, arms split on where to register: `AGENTS.md` 5/6, `CLAUDE.md` 1/6
(b-1). This is FEDERATION issue #3 reproducing inside our own harness — the third independent
confirmation, and the first we produced rather than received. It did not confound this round
(the directive block travels into whichever file is chosen, and scoring searched both), but it
is why scoring had to search both.

## Caveats

1. **One model, one harness.** Every arm ran pinned to the same model. The 2026-10-20 survey's
   open question applies directly: if these numbers are one model's instruction-following curve,
   they are not a claim about rule shape.
2. **N=3 per condition**, one task.
3. **b-1's hand-back report was the literal word `placeholder`** while its disk work was
   complete. Scoring from artifacts rather than reports is what kept the arm in the round.

## Recommendation

**Do not land FEDERATION #7(a).** Not because the section fails, but because §6 already
delivers it. Record the refinement to the P3 learning, and keep #7(c) — precedence
`rules > plan > memory` — which this round does not touch and which remains the cheap, useful
half of issue #7.

**The next round is the implicit case**, not a reworded section.
