# Think: Test Context Probing & CDM on a Real Task

## Context
- Task 4.5 serves a dual purpose: (1) test Context Probing (from 4.3) and (2) validate the new Contextual DNA Mapping (Decision #9) format on a real TTE explosion.
- This is a "meta-test" — the act of writing this TTE is itself the test. If the CDM metadata in `02_tasks.md` makes the plan easier for the human to validate, the feature is proven.

### Context Saturation Check
- [x] **Target files/paths** — Known: `00-ai-rules.md` (§4 CDM rule already added), `05-decisions-and-issues.md` (#9 already added), `BEMYAGENT.md` (sync pending)
- [x] **Expected behavior** — Clear: apply CDM to `02_tasks.md`, have the user judge if validation is faster
- [x] **Constraints** — Defined: no emoji in checkbox format (use `[x]`/`[ ]`), CDM emoji markers (🎯✅🔄) are acceptable as visual anchors
- [x] **Dependencies** — Mapped: CDM rule in `00-ai-rules.md` §4 (already written), Decision #9 (already logged)

## Approaches Considered

### A. Test CDM on an external project task
- **Pro:** Tests CDM in a "real" context outside the protocol itself.
- **Con:** No external project is active right now. Would require artificial setup.

### B. Test CDM on the BEMYAGENT.md sync task (chosen)
- **Pro:** Natural next step (sync is pending). The task has mixed complexity — some subtasks are simple (copy-paste), others are medium (verify consistency). Good CDM stress test.
- **Con:** Self-referential (testing a feature by using it on itself).

### C. Write a purely synthetic test plan
- **Pro:** Controlled environment.
- **Con:** Doesn't prove anything about real-world usability.

## Selected Approach & Risks
- **Chosen:** Approach B — Apply CDM to the `BEMYAGENT.md` sync task. The mix of simple and complex subtasks will exercise all three CDM levels (none / Lite / Full).
- **Risk:** Self-referential bias — we might be too lenient judging our own output. Mitigated by asking the user for honest feedback.

## Verification Plan
- [ ] `02_tasks.md` written with CDM metadata applied at varying levels
- [ ] User confirms the CDM format improves (or at least doesn't hinder) plan readability
- [ ] `BEMYAGENT.md` synced with `00-ai-rules.md` changes (§4 CDM rule)
- [ ] Commit pushed with all changes from this session
