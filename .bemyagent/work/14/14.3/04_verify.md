# VERIFY — 14.3 read delegation

Verdict: **FAIL for the candidate rule — do not land it.** Not because delegation was measured
harmful, but because it was never exercised: 0/9 arms delegated anything. The clause is inert.

## Evidence per CDM criterion

### ✅ All 9 arms completed, bootstrapped, and shipped a working feature
9/9 reached completion, generated `.bemyagent/`, sized the task Heavy, forward-wrote TTEV.
Test suites 7–11 passing per arm (baseline was 4). The round is valid; nothing was voided.

### ✅ Defect survival, scored from artifacts not self-reports
Decisive check — what `presenceKey` returns in each arm's shipped `session.js`:

| | a (baseline) | b (free delegation) | c (bounded) |
|---|---|---|---|
| FIXED | 0/3 | 1/3 (b-1) | 1/3 (c-1) |
| Leaderboard collapses per playerId | 0/3 | 0/3 | 0/3 |

Artifact scoring matched every arm's self-report exactly — no arm claimed a fix it had not made.

**2/9 total. No separation.** Harness scoring rule: at N=3 only 0/3 vs 3/3 is signal; anything
narrower is noise and is treated as a null. 0/3 vs 1/3 vs 1/3 is a null.

*Proxy checked for bias before reporting:* the scorer initially flagged a-3 as deduping. It was
a false positive — a-3's `new Map` indexes ratings for a join, and `online` is still iterated
directly, so duplicates would pass through. Corrected to 0/9. This is the third time a proxy
metric in this harness has needed checking *against* the treatment before its result was
believed (see the classifier note in harness/README).

### ❌ The mechanism under test never engaged — this is the actual finding
Searched all nine generated `.bemyagent/` trees for any trace of delegation:

- **path:line citations: 0/9** — including all three c-arms, whose rule explicitly ordered
  "log the citation in `03_execute.log`".
- Every keyword hit resolved to one of two things: the word "delegates" in arms' own
  architecture docs (about module responsibilities), or **the rule text itself**, copied
  verbatim into the arm's generated `00-ai-rules.md`.

The trigger condition was met and visible: `session.js` is 309 lines against a
`contextSlicingThreshold` of 200, and arm b's rule named that threshold explicitly. Capability
was confirmed available before the round (14.4). Arms could delegate, were told to delegate,
and did not.

This is the declarative-rule null in its familiar shape (Milestones 11/16/18): the clause
states a permission, and permissions measure at ~zero compliance in this protocol. Arm c's
forced artifact — the citation — failed at 0/3, which is the `Layers:` header result again:
an instruction to record something is not the same as an artifact that cannot be produced
without doing the work.

### ⚠️ Cost — reported, does not decide, and cannot be attributed to the rule
a 280.2k tok (8/10/7 tests) · b 254.2k (10/7/7) · c 291.1k (11/9/9).

b is ~13% cheaper than c. **This difference must not be read as delegation saving tokens**:
nobody delegated, so nothing in these numbers is caused by the rule. c also wrote the most
tests (29 vs 24), so per harness rule 2 the raw totals partly measure "did more work". Treated
as variance.

## Caveats that cap what this round can support

1. **Runtime discovery path.** The defect changes observable HTTP behaviour, so an arm could
   reach it by curling its own endpoint rather than by reading. The claim in 14.2 that it was
   "reachable only by reading" was verified for the shipped *tests* and then over-generalised.
   b-1 found it exactly this way. A difference between conditions would still have been
   evidence; a null is weakly informative, since this path is open to every condition equally.
2. **Covariate unbalanced.** Wiring a session-creation route determines whether the runtime
   path existed at all: wired 2/3 a, 2/3 b, 3/3 c. Both fixers were wired arms. With 2 events
   total, stratifying is meaningless — stated rather than computed.
3. **Both fixes landed in batch 1.** No mechanism is proposed for this; with 2 events it is
   as consistent with chance as with anything else. Recorded so it is not discovered later
   and mistaken for structure.

## Finding worth more than the original question

7/9 arms read `session.js` (they wired it, documented its API, quoted it). c-3's report quoted
the module's own doc comment — *"Anything that counts, ranks or pairs players reads presence"* —
and still shipped the violated invariant. The file **declares its invariant in a header comment
and breaks it 40 lines below**, and 7/9 readers took the comment as the truth about the code.

That is not a fact about delegation. It is a fact about reading: a documented invariant is
treated as an assertion about the system rather than as a claim to be checked against the
implementation. It is the same failure the delegation hypothesis predicted for *summaries* —
present here without any summary involved, which is why the treatment could not separate.

Promote to its own candidate: an anti-hallucination clause aimed at doc comments
(§5 already says "NEVER assume a function, variable, or import exists without seeing it" —
it does not say the comment describing them may be lying). Needs its own round.
