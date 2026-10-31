# VERIFY — 14.8, can an agent write a structural generator

Every criterion executed: the commands were run, their output diffed against `git ls-files`,
and re-run in a pristine copy. Raw results in `03c_arm_evidence.txt`, script in `score.py`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| Delta confined to the template block | PASS | `03b_delta.diff`, two lines |
| Fixture premise confirmed by measurement | PASS | `git ls-files` 12 against `find -name '*.js'` 239, vendor untracked, no `.gitignore` |
| 3/3 arms produce `03-code-map.md` with the section | PASS | all three, command verbatim in `03c` |
| Raw outputs and counts here before the verdict | PASS | `03c_arm_evidence.txt`, `score.py` |

## The result

| | q13 | q14 | q15 |
|---|---|---|---|
| (i) runs | PASS | PASS | PASS |
| (ii) precision — vendor leak | PASS | PASS | PASS |
| (ii) recall — every tracked source file | **FAIL** (1 missing) | **FAIL** (2) | **FAIL** (2) |
| (iii) re-runnable with no context | PASS | PASS | PASS |
| (iv) claims more than it derives | **YES** | **YES** | **YES** |

**The obvious failure did not happen.** The fixture was prepared so a naive enumeration would be
twenty times wrong, and 3/3 arms reached for `git ls-files` without being told to. Two wrote the
reasoning into the doc unprompted. Precision is perfect.

**The failure that did happen is one none of the three noticed.** All three composed
`git ls-files <globs>` with `| xargs grep <symbol pattern>`, and that pipeline makes the **grep
decide membership**. A file whose content matches no symbol pattern leaves the inventory
entirely. `client/index.html` is the clean case: two arms globbed it explicitly and it still
disappears, because markup holds no `function` or `CREATE TABLE` line.

**Enumeration and extraction are two jobs.** Composed into one pipeline, a file's presence in
the inventory becomes a property of its contents rather than of the repository. That is the
draft's predicted harm — *"a generator that silently misses files is the main harm, because a
derived artifact is trusted"* — confirmed at 3/3 by a route nobody predicted.

## The clause asked for the wrong half, and that is the finding worth keeping

The line under test required the command to *"exclude vendor directories, build output and
anything untracked"*. **3/3 obeyed it exactly.** It never required the command to emit every
tracked source file. The half that was specified was met; the half that was never written down
failed everywhere.

This is a drafting error in my candidate, not a failure of the arms, and it is the second time
this round's family has shown the same property: **agents comply precisely with what a clause
says and supply nothing it omits.** 17.2 found the mirror image, where an optional field inside
a forced artifact was filled 3/3 because the clause asked for a command per criterion.

## Verdict: not rejected. Revised, and this is the first candidate in months to earn a round two

Four candidates in a row have just been rejected or measured null. This one is different on a
property the others never had, and the property is the reason the draft proposed it:

**its failure was found mechanically, in one command, by the artifact itself.** The recall gap
took a `comm` against `git ls-files`. Every previous candidate's failure needed six arms, a day
and a mutation harness. A rule whose breakage is a diff is a different class of thing from a
rule whose breakage is a judgement, and that difference is now demonstrated on the candidate's
own first round rather than argued in a draft.

**Round two (14.9) carries three changes, all forced by this round's evidence:**
1. The clause states the **completeness** requirement, not only the exclusion one.
2. The clause requires the command to be **checkable against `git ls-files`** — the cross-check
   the draft named as the bound on this exact harm, which went unwritten and therefore unused.
3. The inventory must be **the command's output, not prose beside it**. Criterion (iv) at 3/3
   says a hand-written table living under a regenerable command is a contradiction that reads
   as fine, and that is the strongest form the draft already named: delete the rows, keep the
   command.

## Caveats

1. **Single-language fixture.** Pre-mortem 1 predicted a possible ceiling from every arm naming
   the same obvious command, and that half happened: all three chose `git ls-files`. The
   polyglot case is untested and is where a generator is actually hard.
2. **No baseline arm**, by construction — the shipped protocol names no command. Stated in
   `01_think.md` before launch, not after.
3. **Criterion (iv) is the cheapest observable form** of the draft's authority weakness, not a
   full test of it. A command can enumerate every file and still mis-attribute what calls what,
   and nothing here touches that.
4. **A finished arm left a server listening** and reported that it could not stop it. Killed
   during the round's own port sweep, which is a standing harness step and not an action taken
   on a subagent's request. Second occurrence in two rounds, recorded in `05`.
