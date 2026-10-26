# Kiro side of the artifact comparison — everything it produced

Kiro CLI 2.33.1, model pinned `claude-sonnet-4.5`, default agent, context cleared, run
2026-10-23 in a clean copy of the harness fixture with **no BMA present** (no `BEMYAGENT.md`,
no `AGENTS.md`, no `.bemyagent/`). Task text byte-identical to the one given to the six arms in
`work/15/15.10/arms/`.

**These two files are the complete output.** Kiro produced no `.kiro/` directory, no markdown,
no spec, no plan, no decision record — nothing persistent about its reasoning. 9 tests pass
(5 new + 4 shipped). Session cost: **1.30 credits of 50**.

Compare against `work/15/15.10/arms/`, where each of six agents produced `.bemyagent/` with
docs 01–06, a TTEV folder holding `01_think` / `02_tasks` / `03_execute` / `04_verify`,
`AGENTS.md`, and decisions recorded in `05` — including the limitations (no heartbeat, stale
sessions still listed) that this run never wrote down anywhere.

**Read the caveat in `04_verify.md` before using this**: default mode is Kiro's unstructured
agent, so this is not its spec flow. The spec flow is not available in the CLI at all.
