# Task 6.1 Execution Plan

## Contextual DNA Mapping (CDM)
- `🎯 Drift`: We start creating a massive configuration system instead of a simple JSON file, or we modify parts of `00-ai-rules.md` outside of section 4.
- `✅ Validation`: `settings.json` exists with the `dynamicPivoting` block. `00-ai-rules.md` section 4 contains the word "Dynamic Pivot Rule" and the word count tip.
- `🔄 Pivot`: If `settings.json` conflicts with any other existing configuration pattern, we stop and ask the user.

## Checklist
- [x] Create `work/6/6.1/` directory.
- [x] Write `01_think.md` and `02_tasks.md`.
- [ ] Create `.bemyagent/settings.json` with default configuration.
- [ ] Update `docs/00-ai-rules.md` section 4 to replace the CDM bullet points with the token-based evaluation, add the dynamic pivot rule, and the `wc` estimation tip.
- [ ] Create `03_execute.log`.
- [ ] Verify execution and write `04_verify.md`.
