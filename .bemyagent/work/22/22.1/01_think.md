# 22.1 — THINK

## Context
The user (2026-11-18): start from the site — a trigger on push that inserts the version, besides the one that fires when the README changes. Spec: `docs/specs/site-version.md`.

Read in the repo, 2026-11-18: `.github/workflows/pages.yml` builds `README.md` with pandoc through `site/template.html` on a push to `main` filtered by path, and on a manual run; the checkout is shallow, so the build sees no tag; the template has two pandoc variables (`$title$`, `$body$`) and a button that links to `BEMYAGENT.md` on `main`. All 20 tags have the shape `N.N.N`; the latest is `3.4.0`, annotated, 2026-11-17.

### Context Saturation Check
- [x] **Target files/paths** — `.github/workflows/pages.yml`, `site/template.html`
- [x] **Expected behavior** — the spec's four criteria
- [x] **Constraints** — `05` Decision 23 (a tag is a release of `BEMYAGENT.md`); no version written by hand
- [ ] **Dependencies** — one unknown: whether the `github-pages` environment accepts a deployment started by a tag. Not readable from here (the session has no API access). **Assumption:** it may refuse; the change is still right, and the owner gets the exact setting to add. Until then the page is still rebuilt, with the right number, by every push to `main` that meets the path filter.

## Approaches Considered
1. **Tag trigger + latest tag read at build** (chosen). `on.push.tags` beside the branch and path filters (path filters are not evaluated for tags); `fetch-depth: 0`; `git describe` gives the tag, `for-each-ref` its date; pandoc gets both as metadata. Pro: the page changes when the release happens, in whichever order `main` and the tag are pushed. Con: depends on the environment's rule for tag runs.
2. **No tag trigger: build on every push to `main`, read the latest tag.** Pro: no setting. Con: the owner pushes `main` first and the tag second, so the page would show the previous number until some later push.
3. **The tag's run only starts a manual run on `main`** (`gh workflow run` from a second job). Pro: deploys from the default branch, no setting. Con: a second job, a write permission on Actions, two runs per release — machinery to avoid one checkbox. Kept as the fallback if the owner does not want tags allowed in the environment.
4. **Client-side: the page asks the GitHub API for the latest tag.** Con: a script and a third-party request on a static page; rate limits; nothing at all without JavaScript.

## Pre-mortem
- *The tag's deployment is refused by the environment.* Named in the spec and in the hand-off; criterion 4 stays open until a real tag run is seen. Fallback: approach 3.
- *The template's conditionals break the page* (pandoc's `$if$` syntax written from memory). Mitigation: build locally with pandoc in a container, with and without the variable, and read the HTML.
- *The build picks a wrong tag* (a future tag of another shape, or none reachable). Mitigation: `--match` on the release shape; with no tag `git describe` fails and the run fails loudly rather than publishing a page without a version — and the template still renders without one if the variable is ever empty.

## Devil's Advocate
Write the version into the README by hand at each release: zero CI change, and it would also show on GitHub. Not taken: it is a second thing to remember at every tag, and `3.3.1` already showed what a hand-kept release step does here (`05` Decision 23). The README can link to the site, which carries the number.

## Selected Approach & Risks
Approach 1. Standard: two files. Estimated cost: low.
- The button moves from `main` to the tag: a visitor gets the released file, not whatever `main` holds between a push and its tag. Without a version the template falls back to `main`.
- The date is the tag's creation date (`creatordate`), the tagger's date for an annotated tag.

## Verification Plan
- Local build in a pandoc container from the real README and template, tag and date read by the workflow's own commands: the HTML holds `3.4.0`, its date and the tag's URL.
- Same build with a different version value → that value on the page (nothing stored); with none → the page renders and the button points at `main`.
- The workflow file parses as YAML and its `on:` holds branch, tag, paths and manual run.
- Not verifiable before a push: the run itself and the environment's answer to a tag.
