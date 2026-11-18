# 22.1 — VERIFY (independent, Sonnet)
**Verdict: PASS_WITH_CAVEATS** — all four criteria pass on a local docker build; the run on GitHub and the environment's answer to a tag-started deploy remain undecidable before a push.

| Crit | Result | Evidence (commands run now) |
|---|---|---|
| (a) parse, `on.push` keys, dispatch kept | PASS | PyYAML load of `pages.yml`: `{'push': {'branches': ['main'], 'tags': ['[0-9]+.[0-9]+.[0-9]+'], 'paths': ['README.md','site/**','.github/workflows/pages.yml']}, 'workflow_dispatch': None}` |
| (b) page has latest tag, date, `blob/<tag>/` | PASS | `git describe --tags --abbrev=0 --match '[0-9]*.[0-9]*.[0-9]*'` -> `3.4.0`; `for-each-ref ... refs/tags/3.4.0` -> `2026-11-17`. Pandoc 3.1.1 (docker) page `<out>/new.html`: `blob/3.4.0/BEMYAGENT.md`, `Get BEMYAGENT.md 3.4.0`, `Release 3.4.0 · 2026-11-17 — MIT License` |
| (c) other value shown; none -> `main` | PASS | `--metadata version=7.7.7 released=2020-01-02`: `blob/7.7.7/BEMYAGENT.md`, `Release 7.7.7 · 2020-01-02`. No version: `blob/main/BEMYAGENT.md`, plain `Get BEMYAGENT.md`, footer `MIT License — ...` |
| (d) body otherwise unchanged | PASS | Old template built with the old command (`<out>/old.html`). `diff old.html none.html` -> empty, rc=0. `diff old.html new.html` -> only lines 468-469 (button) and 474 (footer) differ. |

## Extra points
1. GitHub docs (https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax; fetched through a summarizing tool, quotes as returned):
   (i) "Path filters are not evaluated for pushes of tags." So a matching tag starts the run regardless of `paths`. YES.
   (ii) Cheat sheet: "`+`: Matches one or more of the preceding character."; "`[]` Matches one alphanumeric character listed in the brackets or included in ranges. Ranges can only include `a-z`, `A-Z`, and `0-9`."; example row `v[12].[0-9]+.[0-9]+` matches `v1.10.1`. By the same rules `[0-9]+.[0-9]+.[0-9]+` is valid and matches `3.4.0` and `3.10.12` (inference from the rules and the example; I did not run it on GitHub). `.` is not special in these globs per the table I saw; not separately confirmed.
   (iii) "If you define both `branches`/`branches-ignore` and `paths`/`paths-ignore`, the workflow will only run when both filters are satisfied." So `main` still needs a path match. YES.
2. https://github.com/actions/checkout README: "Set `fetch-depth: 0` to fetch all history for all branches and tags." and "`fetch-tags`: Whether to fetch tags, even if fetch-depth > 0" (default false). So tags come with depth 0 on branch pushes. For a tag push the README does not say; it mentions nothing on annotated tags or tag-triggered checkouts. Tag fetch on tag push: not documented there. Local fact: `creatordate` is the tagger date for annotated tags, commit date for lightweight ones; here 16 tags are annotated and 4 lightweight (`for-each-ref %(objecttype)`), 3.4.0 is annotated (`git cat-file -t` -> `tag`). Whether the runner keeps the annotation object on a tag-triggered checkout: not settled by docs.
3. Both git commands run in the repo give `3.4.0` and `2026-11-17`. No matching tag: `bash -e -c 'v=$(git describe ... --match "9*.9*.9*"); echo reached'` -> `fatal: No names found`, rc=128, `reached` not printed. So the step fails and nothing is published (no empty version). GitHub's default `run:` shell is bash with `-e`; I did not fetch that sentence. Quoting: `"refs/tags/$version"` quoted, `--match` pattern in single quotes; no problem found. Note `describe` finds the nearest tag reachable from HEAD, not the highest version; the `--match` glob is a shell glob, so it also matches `1.2.3-rc1` (the repo has no such tags).
4. github-pages environment, https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site: GitHub recommends that "only the default branch can deploy to this environment"; tags are not mentioned. The manage-environments page only says "Selected branches and tags" exists and gives no default. NOT SETTLED: whether a tag-started deploy is refused. Risk: if the environment rule allows only `main`, a tag run fails at deploy, though the push to main usually already published the same page.
5. Diff review: no change outside the stated scope in the two files. Other uncommitted files exist (06-implementation-plan.md, specs/resume-block.md, specs/site-version.md, work/22/), outside the diff I was asked about. Small risks: the apt pandoc on ubuntu-latest may differ from 3.1.1 in template handling (`$if(...)$` is old syntax, low risk). A tag pushed on a commit that is not on main yields that tag's page, possibly older content; push of more than three tags at once creates no event (docs: "Events will not be created for tags when more than three tags are pushed at once."). Concurrency of a main-push run and a tag-push run both deploying is as before the change; not examined further.

## What could not be checked
- The actual GitHub run (tag filter match, checkout behaviour on tag push, environment rule for tags).
- The pandoc version the workflow installs via apt (built with 3.1.1 as instructed; also amd64 image emulated on arm64).
- GitHub docs were read through a summarizing fetch tool, not raw HTML; the `bash -e` default for `run:` was not fetched.

## Second pass — final template (independent, Sonnet), 2026-11-18
**Verdict: PASS_WITH_CAVEATS** — all of (a)–(d) hold on the final diff, built with pandoc 3.1.1 (docker, amd64) into `<out>`; no overflow at a true 390 px viewport. Caveats are the pass-1 ones that need a push (GitHub run, tag-deploy rule).

| # | Point | Result | Evidence (run now) |
|---|---|---|---|
| 1 | (a) workflow | PASS | PyYAML: `on.push` keys = `branches, tags, paths`; top-level keys `push, workflow_dispatch`. Diff touches only `tags`, `fetch-depth: 0`, two `--metadata`, the two git lines. |
| 2 | (b) built page | PASS | `git describe` -> `3.4.0`, `for-each-ref` -> `2026-11-17`. Line 241 (above `<h1>`): `<p class="release"><a href=".../blob/3.4.0/BEMYAGENT.md">v3.4.0</a> · 2026-11-17</p>`. Button text `Get BEMYAGENT.md`, href `.../blob/3.4.0/BEMYAGENT.md`. Footer `Release 3.4.0 · 2026-11-17 — MIT License — GitHub`. |
| 3 | (c) other / no version | PASS | `version=7.7.7 released=2020-01-02`: release line, button href and footer all 7.7.7 / 2020-01-02; `grep 3.4.0` -> empty. No version: `grep -c 'class="release"'` -> 0 (the CSS rule is `.release {`, not the attribute), button href `blob/main/BEMYAGENT.md`, footer `MIT License — GitHub` only. Version without date (8.0.0): `v8.0.0` with no ` · `, footer `Release 8.0.0 — MIT License`. |
| 4 | (d) diff vs old template | PASS | old vs no-version: only the added CSS block (`/* Release line above the title */ .release {...}`, 8 lines + 1 blank), rc=1, nothing else. old vs with-version: same CSS block; +1 line 241 (release `<p>`); line 468->478 button href `main`->`3.4.0`; line 474->484 footer. Nothing else differs. |
| 5 | (5) validity | PASS | `grep -nE '\$if\|\$endif\|\$version\|\$released'` on new, seven, none, nodate, old -> empty (rc=1). Changed regions: `<p class="release">...</p>` opened and closed, `<a>` closed, in all builds; no empty `<p>` in the no-version build. Not run through a W3C validator. |
| 6 | responsive | PASS | Viewport meta present (1). Chrome headless `--window-size` below ~500 is not honoured, so the earlier cut text is the tool. True 390 px: pages loaded in a 390 px-wide iframe, numbers written to DOM and dumped. Old: `innerWidth=390 scrollW=390 clientW=390`, no element with right edge > 390. New: same, `release.right=370`, release `scrollWidth=350 = clientWidth=350`, no overflowing element. The release line adds no horizontal overflow. Screenshots at 500 px: `<out>/s500-old.png`, `s500-new.png` (taken, not inspected). |

### Could not check
- The actual GitHub run (tag filter match, checkout on tag push, tag-deploy rule of the `github-pages` environment): unchanged from pass 1.
- The pandoc that apt installs on ubuntu-latest (built with 3.1.1, emulated amd64).
- Visual look of the release line (screenshots not viewed); no HTML validator run.
