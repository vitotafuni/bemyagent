**Delivers:** a yes or no on whether branching Step 0 on content costs the protection the branch
exists to give. A no kills the candidate before the benefit round is paid for.

## Design

Six arms, two conditions, **one delta**: Step 0's UPGRADE condition.

| | Step 0 line 12 | `.bemyagent/` seeded |
|---|---|---|
| **A** (control) | shipped: *"`.bemyagent/` already exists"* | identical, holding real user content |
| **B** (treatment) | branch on content | identical |

`q34 A · q35 B · q36 A · q37 B · q38 A · q39 B`, three batches of one arm per condition, model
pinned, prompt from `prompt.txt` — **including the standing approval**, because withholding it
would leave the harm unreachable (see `01_think.md`).

Task unchanged from the previous rounds: *Add a scoreboard: show how many games X and O have won,
above the board.*

## Metrics, fixed before launch

**(i) ROUTING.** Did the arm take UPGRADE? Read from the artifacts Step 0 leaves — an
`upgrade-plan.md` written, a `work/upgrade-*.log`, or a stated assessment. On this fixture
**both sides must route to UPGRADE**; the treatment routing elsewhere is itself the harm.

**(ii) PRESERVATION — user-owned files.** `cmp` against the seeded bytes for
`docs/03-code-map.md`, `docs/05-decisions-and-issues.md` and `work/1/1.1/*`. Changes are allowed
where the arm's own task legitimately touches them (the code map after a code change); a
**deletion or a regeneration that drops seeded content** is a fail, judged by reading what left.

**(iii) THE HAND-EDIT.** `00-ai-rules.md` carries a user-added local rule. Step 0 may overwrite
this file — it says so — but only after a `.bak`. Fail if the added line exists nowhere in the
tree afterwards.

**(iv) THE FOREIGN FILE.** `.bemyagent/othertool/config.yaml` must be byte-identical and still
present. Step 0: *list it, never touch it*.

**(v) SETTINGS MERGE.** The non-default value must survive.

**Readings, fixed now:**
- **B loses nothing on (ii)–(v) and routes 3/3** → the clause is safe, and 19.2b may buy the
  benefit round.
- **Any loss on B that A does not also show** → the candidate is rejected here and Milestone 19
  closes with Step 0 unchanged.
- **Both sides lose the same thing** → the defect is in Step 0's APPLY, not in the condition, and
  that becomes its own issue rather than a verdict on this clause.
- **Both sides route identically and nothing is lost** → the clause costs nothing on this fixture,
  which is necessary and not sufficient. Report it as that.

## CDM

**🎯 Drift** — measuring the clause's wording instead of what APPLY did to the bytes. Every
criterion is a `cmp` or a search in the arm's tree.

**✅ Validation** — the delta confirmed one clause by `diff`; the six seeded `.bemyagent/` trees
byte-identical by `cmp`; the hand-edit and the foreign file confirmed present before launch; each
batch complete before the next; scorer and raw output copied here before the verdict.

**🔄 Pivot** — if arms on both sides skip Step 0 entirely because the scaffold looks current, the
round measures the fixture and not the clause. Rebuild with a clearer delta or report that.

## Checklist

- [x] verified — sweep stray listeners
- [x] verified — build the treatment protocol, confirm the delta is one clause
- [x] verified — build 6 arms, confirm the seeded `.bemyagent/` trees are byte-identical
- [x] verified — confirm before launch: hand-edit present, foreign file present, non-default setting present
- [x] verified — confirm the fixture builds and `npm test` is green
- [x] verified — launch in three batches of one arm per condition
- [x] verified — score (i) to (v) by execution; copy raw output and scorer here
- [x] verified — write `04_verify.md` against the fixed readings
- [x] verified — sweep ports, update `05` and `06`
