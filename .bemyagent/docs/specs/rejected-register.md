# Rejected register
**Status**: specced

## Description
Two things the protocol does not say today: which ideas deserve an evaluation, and where an idea that was evaluated and turned down leaves a trace, so that the same idea proposed again — usually in other words — is answered from the record instead of walked again.

**Triage, one question:** *did answering produce something the files did not already hold?*
- **No — dismissed at the door.** The idea duplicates a rule, falls under a standing decision, or lies outside `01-overview`'s scope. The reply cites the place. Nothing is written: the record already has it.
- **Yes — evaluated.** Answering took reading beyond the restore path, weighing options, running something, or resting the verdict on a premise that could change. The reply is a verdict, so Discussion capture already sends it to `drafts/`. When the draft closes: built → `specs/`; **not built → one line in `decisions/rejected.md`, then the draft is deleted.**

**The register:** `decisions/rejected.md`, one line per idea — the idea as someone would propose it again, the verdict and its kind, **the premise it rests on**, what would reopen it, where the evidence is. Short enough to read whole, because a re-proposal arrives paraphrased and a keyword search misses it (*"`activeContext.md`"* against *"a short-term memory"*). It lives in `decisions/`: tracked, and never read at restore.

Origin: the user, chat 2026-11-12.

## What is known
- Rejections exist, scattered: Engineering Learnings bullets, dropped plan rows with a reopening condition (`05`:505), verdicts inside gitignored drafts (`drafts/prompt-logs.md`). No index keyed to the idea.
- `drafts/` is gitignored here and the rule says *promote, then delete*: a draft that is not promoted has no prescribed end. The gitignored-draft trap fired twice (`05`:251).
- A rejection can outlive its premise unnoticed: `activeContext.md` (Decision 18) rested on `03_execute.log` covering the need, later measured 0/10; nobody reopened it until the idea came back on 2026-11-12. Others: 20.4/20.5, 14.12 → 14.14, EARS (`05`:241).
- *Rejections on harm are robust; rejections on redundancy are fragile* (`05`:410) — the kind belongs on the line.
- The Critical Review's Overlap check searches *target files* only.

## Rule text, candidate (≈ 35 words, both edits to existing sentences)
- §5 Overlap check: *"search target files **and read `decisions/rejected.md`** — an idea already turned down is answered by its line unless the premise it rests on has changed"*.
- §6 `drafts/`: *"promote to `specs/` when ready to build, **or add its line to `decisions/rejected.md`**, then delete the draft."*

## Critical review
1. **Overlap** — §6 already sends rejected approaches to `05`; the register is an index to those entries, not a second copy: each line points at its evidence.
2. **Cost** — zero on the restore path. One read of ~40 lines when a proposal is reviewed.
3. **Weakness** — the triage question is a classification, and rules that hang on one miss the unanticipated case; an index drifts from `05` if a verdict is reopened in one place only. **Unanswered** — does an agent handed a paraphrased re-proposal actually find its line?
4. **Minimal alternative** — no file: require `Rests on` / `Reopens when` on rejections in `05` and widen the Overlap check to grep it. Smaller, and blind to paraphrase in a 175 KB file.

## Acceptance criteria
- [ ] The register exists for this repo, backfilled from `05`, `06` and the drafts, every line traceable to a source line; nothing invented where the source is silent (21.3).
- [ ] An independent reader confirms a sample of lines against their sources.
- [ ] Recall measured: an arm given a paraphrased re-proposal of a registered idea cites the earlier verdict (control: the same verdict only in `05`).
- [ ] Rule text in `BEMYAGENT.md` and `00-ai-rules.md`; the bootstrap creates the empty register.
- [ ] `drafts/` in this repo reconciled: every draft carrying a verdict is promoted, registered or still open — and says which.

## Open questions
- Should the protocol recommend tracking `drafts/`, given the trap? Out of scope here; the register makes the question smaller.
