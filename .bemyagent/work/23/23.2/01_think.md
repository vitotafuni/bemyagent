# 23.2 — THINK

## Context
The protocol's paragraph on the conversation log is addressed to nobody: *if your harness can write it, point it there*, with no step that does it and no example (the user, 2026-11-20: *how do we explain it to the model now? … an example, even in pseudo-code, would help — I think of small models that have to be led step by step*). 23.1 built and verified the thing on one harness. 23.2 puts into `BEMYAGENT.md` what a model needs to set it up for its own harness, describes the log as it now is, and says what an upgrade does to logs already there. Design, trial and the user's decisions: `docs/drafts/log-both-sides.md`; the script and its checks: `work/23/23.1/04_verify.md`; release size: `docs/drafts/log-other-harnesses.md` (minor, `3.5.0`).

### Context Saturation Check
- [x] **Target files/paths** — `BEMYAGENT.md` and its embedded copy of the rules, `.bemyagent/docs/00-ai-rules.md` (the two must stay equal); at landing also `.bemyagent/settings.json` (this project's own lacks `conversationLog`), `README.md` (two lines), `05`, `03`.
- [x] **Expected behavior** — the user's decisions of 2026-11-20/21: both voices; a folder per month, a file per session; a contract in pseudo-code and one worked example; the user enables the hook, not the agent; a message sent straight to a subagent is left out; existing logs are never converted; one optional item in the upgrade plan.
- [x] **Constraints** — Decision 21 (a duty hangs on an event the agent recognises, not on a cadence); 16.1 (a per-turn sentence measures at zero); every line of the rules file is read at each restore, the bootstrap part once; the candidate lives on `bma/23.2`, `main` holds only what is measured; the author of a protocol change does not test it; no harness other than Claude Code can be measured here.
- [ ] **Dependencies** — one unknown: whether an arm in headless can write its tool's settings file at all (the tool may refuse edits to its own configuration). **Assumption:** unknown either way; a single pilot arm answers it before any apparatus is built (*pilot before apparatus*, Milestone 21).

## Approaches Considered
1. **A step at the end of bootstrap (contract + worked example) and a rewritten paragraph in the rules** (chosen). The step is an event that happens once; the rules keep only what every session needs: who writes the log, its shape, that it is the user's, that it is not read at restore.
2. **Everything in the rules paragraph.** One place. Con: the contract and the example would be read at every restore of every project, for a set-up that happens once; and a per-session reminder to "check the log is set up" is the cadence shape that measured at zero.
3. **The example as a file of the repository, the protocol pointing at it.** Smallest protocol text. Con: `BEMYAGENT.md` is self-contained by its own first lines — the file is all a user copies; a pointer to GitHub is a dependency on the network and on a path that can move.
4. **Contract only, no example.** Shortest. Con: the user's point is precisely the small model; and whether the example is what does the work is measurable — so it is the control arm, not a decision taken here.

## Pre-mortem
- *The agent installs the hook without asking.* A command that runs on the user's machine at every turn, enabled by a bootstrap that says "do NOT ask permission between steps". Mitigation: the step says *show, then enable only on the user's yes* in its own sentence, and the line at the top of the file already exempts nothing — so the step states its own exception explicitly; an arm with no consent given measures that nothing was written.
- *A small model copies the Claude Code example into another tool.* Mitigation: the example is labelled *translate, do not copy*, and step 1 is *read your harness's documentation*. Not measurable here; said so.
- *An upgrade "migrates" old day files.* Mitigation: one clause in the plan's list, in capitals like its neighbours.
- *The rules paragraph grows.* Counted before and after; the growth has to be words that change behaviour (the file's shape, *never delete*).

## Devil's Advocate
Ship nothing in the protocol: publish the script and its configuration in the README under *Routines for the Human*, as a thing the person installs. No protocol change, no release, no consent problem — the human does it knowingly. It is a real alternative and it is cheaper. Not taken as the whole answer: the user asked that the *model* be able to handle it by harness, and a README recipe is Claude Code only for ever; but it is the fallback if the arms show the step does not work, and the README should carry the recipe anyway.

## Critical Review (rules §5)
1. **Overlap** — the paragraph in rules §3 is edited in place, not added to; the UPGRADE list gets one item beside *Foreign files*, whose wording it mirrors; Step 4 gets one item. The sentence *5 sections* in UPGRADE already lists six (found by 22.2's verifier): adding a seventh forces the count to be touched — it becomes *these sections*, which closes that inconsistency and nothing else.
2. **Cost/benefit** — rules paragraph: counted in `03` (words before/after), paid at every restore. Bootstrap: about 55 lines, paid once and deleted with the file. Benefit: the log stops being a setting nobody can act on.
3. **Challenge** — *Weakness*: the step asks for consent, and consent-shaped rules are the one kind this project's instrument could not measure (Backlog, greenfield exit condition: 6 of 6 arms identical for reasons unrelated to the rule). What can be measured is the two ends — consent given in the prompt → a working log; no consent → nothing installed — not the asking itself. *Unanswered*: should the script live in `.bemyagent/hooks/` (travels with the project, a team shares it) while its switch lives in a personal settings file?
4. **Minimal alternative** — the Devil's Advocate above: README only.

## Selected Approach & Risks
Approach 1, as a commit on `bma/23.2` in both files. Heavy: a protocol change with arms. Estimated cost: the text low; the arms are the cost (a round of six is of the order of millions of weighted tokens — `harness/README.md`), so a pilot of one arm first and the round only on the user's word.
- The worked example is the script of 23.1 with its comments shortened and nothing else changed: any other change would make it an untested script.
- The step sits last but two in Step 4, before *delete this file* and *close this chat*: after it nothing else of the bootstrap depends on the user's answer.

## Verification Plan
Two layers, criteria in `02_tasks.md`: (1) mechanical, by an independent agent — the two copies of the rules equal, the example byte-equal to the verified script apart from comments, counts; (2) behavioural, on clean arms launched by someone who did not write the text — a pilot first.

## Amendment 1 — 2026-11-21, the user's two decisions on the candidate
- **The script goes into the project's repository, in a folder named after the harness**: `.bemyagent/hooks/<harness>/` (here `claude-code/`). It is an example and it travels with the project; the name says it is specific to one tool, and scripts for other tools, once tried, go beside it. The user's open point — *how not to get tangled with its use inside this project*: this repository would then hold the script three times (the block inside `BEMYAGENT.md`, the project's own active copy under `.bemyagent/hooks/claude-code/`, and — today — the pilot's copy in the base). Proposed: at landing the pilot's copy is removed and the base's personal settings point at the repository's file; and the equality of that file with the block in `BEMYAGENT.md` is checked by a command, as the two copies of the rules are — one script, embedded once, checked equal.
- **The switch is personal**: the hook is enabled in the user's own settings for the tool, never in the shared ones — the log holds that person's words. The candidate no longer offers the choice.
Applied on the branch: 403a556.
