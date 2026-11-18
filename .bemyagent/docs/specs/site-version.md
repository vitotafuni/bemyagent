# The site shows the release it describes
**Status**: in-progress — promoted from `drafts/site-version.md` on 2026-11-18 (the user: start from the site; a trigger on push that inserts the version, besides the one on a README change).

## Description
The page at bemyagent.md is `README.md` rendered by pandoc through `site/template.html` (`.github/workflows/pages.yml`). It names no version, and it is rebuilt only by a push to `main` that touches the README, `site/` or the workflow — a pushed tag rebuilds nothing. A tag is a release of `BEMYAGENT.md` (`05` Decision 23), so the latest tag is the version a visitor wants. The build reads it from git and prints it; nobody writes a version by hand.

## Acceptance criteria
- [x] The workflow runs on a pushed release tag as well as on the existing path filter and the manual run. — in the file: `pages.yml` `on.push.tags`, parsed (`work/22/22.1/04_verify.md` a); **the run itself not yet seen on GitHub**
- [x] The built page shows the latest release tag and its date, and the *Get BEMYAGENT.md* button opens the file at that tag. — local build, `04_verify.md` b
- [x] No version string is stored in the repo: with a different latest tag the same sources build a page with that tag. — `04_verify.md` c
- [ ] A deployment started by a tag is accepted by the `github-pages` environment — seen on the first release after this change, or the environment's rule is changed by the owner.

## Open questions
- The `github-pages` environment may accept deployments from the default branch only; not readable from the development session (no API access). If a tag's run is refused: Settings → Environments → `github-pages` → deployment branches and tags → add a tag rule.
- The page's **content** is the README, last changed 2026-08-10: the conversation log, Step 0's content branch, the harness results and the restore line are not in it. A current version over a text that is not current — the README needs its own pass (plan, 22.2).
- An installed `BEMYAGENT.md` carries no version, so a user cannot tell which release they hold. Not this spec.

## Ruled out
- *Build on every push to `main` and read the latest tag, no tag trigger*: needs no environment setting, but shows the old number whenever `main` is pushed before its tag — which is the order the owner pushes in.
- *A line in the README linking to the releases page*: never lies and costs nothing, but does not show the version.
