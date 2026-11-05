**Delivers:** whether obliging the Write Gate to leave its line in the repository makes the gate
auditable by someone who was not in the conversation — and what that obligation costs.

## Design

Six arms, two conditions, **one sentence** of delta in §3 step 2.

| | Write Gate step 2 |
|---|---|
| **A** (control) | `Output: PROTOCOL_CHECK: target=[path], reason=[why]` |
| **B** (treatment) | the same, **and append that same line to the current task's `03_execute.log`** (`micro.log` for Micro). *The conversation is not a record.* |

`q46 A · q47 B · q48 A · q49 B · q50 A · q51 B`, three batches of one arm per condition, model
pinned, prompt stored. Fixture and task identical to 14.13: pre-populated `.bemyagent/`,
hand-written code map, *add a scoreboard above the board*.

## Metrics, fixed before launch

**(i) TRACE ON DISK — the thing the issue is about.** How many `PROTOCOL_CHECK` lines does the
arm's tree hold, and how many of the governed files it actually changed do they name? Governed
files from `git`, as 19.3 established, minus §3's exemption.

**(ii) COVERAGE IN THE CONVERSATION — the comparison.** The same count from the transcripts, both
sides, the instrument 19.3 used. **This is what the two conditions are compared on**, because
the control cannot be measured from disk at all and comparing disk-to-transcript would be
comparing instruments. 19.3's figure on the shipped protocol was 18/33, 55%.

**(iii) HARM — batching.** Where do the lines sit in `03_execute.log`? Appended one at a time
beside the work they gate, or in one block at the end. A block at the end is compliance that
disproves the gate's own claim — *"proceed only after step 2"* — and it counts as a failure of
the mechanism even at perfect coverage.

**(iv) HARM — delivery.** `npm test` green and a working scoreboard, both sides. Milestone 18's
clause cost two deliveries of three.

**(v) HARM — reason quality.** 19.3 found the shipped gate's reasons cite the rule doing the
work. Read all lines on both sides; a drop to restating the rule is a cost.

**Readings, fixed now:**
- **B 3/3 holds the line on disk and (ii) is no worse than A**, with (iii), (iv), (v) clean →
  the sentence lands and the tag is cut.
- **B holds the trace but (ii) drops** → the obligation buys a record by costing coverage. Does
  not land.
- **(iii) batched on 2 of 3 or more of B** → does not land regardless of coverage.
- **Both sides the same on (ii) and B's disk trace is partial** → report the partial figure and
  do not round it up.

## CDM

**🎯 Drift** — counting the string instead of the behaviour. The string lives in
`00-ai-rules.md`; an arm that reads it has not complied. Every count separates what the arm
produced from what it read, as 19.3's scorer does.

**✅ Validation** — the delta is one sentence, confirmed by `diff`; six seeded trees identical;
each batch complete before the next; scorer and raw output copied here before the verdict;
**19.4's check performed and the arms named, one line per metric, in `04_verify.md`**.

**🔄 Pivot** — if arms on both sides write no TTEV `03_execute.log` at all, the treatment had
nowhere to append and the round measures ceremony sizing rather than the gate. Report that.

## Checklist

- [x] verified — sweep stray listeners
- [x] verified — build the treatment, confirm the delta is one sentence in §3 step 2 of both files
- [x] verified — build 6 arms, confirm the seeded trees are identical
- [x] verified — confirm the fixture builds and `npm test` is green
- [x] verified — store `prompt.txt`
- [x] verified — launch in three batches of one arm per condition
- [x] verified — score (i) to (v) by execution; copy raw output and scorer here
- [x] verified — **19.4 check: open the arms at each end of every metric, name them in `04_verify.md`**
- [x] verified — write `04_verify.md` against the fixed readings
- [x] verified — sweep ports, update `05` and `06`
