# 22.1 — TASK

**Delivers:** a visitor of bemyagent.md sees which release the page describes and gets that release's `BEMYAGENT.md` from the button; pushing a release tag rebuilds the page.

## Checklist
| # | Step | Status |
|---|---|---|
| 1 | `pages.yml`: add `tags` to `on.push`; `fetch-depth: 0` on the checkout; in the build step read the latest release tag and its date and pass both to pandoc as metadata | done |
| 2 | `site/template.html`: button text and link carry the version (fallback `main` when absent); footer prints release and date | done |
| 3 | Local build in a pandoc container: real tag, another value, no value | done |
| 4 | VERIFY by an agent that did not write the change; `04_verify.md` | done — PASS_WITH_CAVEATS |
| 5 | `03-code-map.md` (site rows), `05` (decision), spec criteria ticked with evidence, plan row | done |

## CDM
- ✅ **Validation**: (a) the workflow parses and `on.push` holds `branches`, `tags`, `paths`, with `workflow_dispatch` kept; (b) a page built from the repo's README and template by the workflow's own commands contains the latest tag, its date and `blob/<tag>/BEMYAGENT.md`; (c) the same sources with another version value show that value, and with none render a page whose button points at `main`; (d) the page's body is otherwise unchanged against a build from the template before the change. Not decidable before a push, and reported as such: the run on GitHub and the environment's answer to a tag-started deployment.

## Amendment 1 — 2026-11-18, after the first VERIFY, from the user's reading of a preview
The version moves from the button's text to a line above the title (`v<version> · <date>`, the number linking to the tag's `BEMYAGENT.md`); the button's text is again `Get BEMYAGENT.md` and its link still goes to the tag; the footer line stays. Criteria (b)–(d) are read on this form: (b) the tag, its date and `blob/<tag>/BEMYAGENT.md` are on the page, the tag in the line above the title; (d) against the old template the differences are the new CSS rule, the line above the title, the button's link and the footer. `04_verify.md` was written on the earlier form → a second pass on the final diff, appended there.
