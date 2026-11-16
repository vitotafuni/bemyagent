"""21.4 - K (Amendment 3, C3): the lines the two rules files share that are 20 characters or more and that the seeded instruction
file does not hold. One list for both conditions; the added line of L is not in it. Derived here from the released rules file (the
repo's working tree, which is what setup.py builds C from) and the seeded instruction file; the count is asserted to be 86.
SEED_CLAUDE_MD is the text setup.py writes as every arm's CLAUDE.md.
"""
import pathlib

SEED_CLAUDE_MD = "Read .bemyagent/docs/00-ai-rules.md before every task.\n"
K_SIZE = 86
THRESHOLD = 43          # C3: an arm leaves (i) when x + n >= THRESHOLD (half of K; arbitrary, fixed before any data)
RULES_REL = ".bemyagent/docs/00-ai-rules.md"


def long_lines(text, exclude=SEED_CLAUDE_MD):
    """non-empty lines of 20+ characters, trailing blanks dropped, that `exclude` does not hold (duplicates kept)"""
    return [l.rstrip() for l in text.splitlines() if len(l.rstrip()) >= 20 and l.rstrip() not in exclude]


def k_lines(repo):
    k = long_lines((pathlib.Path(repo) / RULES_REL).read_text())
    assert len(k) == K_SIZE, f"K has {len(k)} lines, not {K_SIZE}: the released rules file is not the one this round was designed on"
    return k


DEFAULT_PILOTS = ["q901", "q902", "q903"]
COUNTED = ["q112", "q113", "q114", "q115", "q116", "q117"]


def pilots_from_env(env=None):
    """D5/G3: the pilot names. R214_PILOTS overrides them for the selftest and dry-run; an override that names a counted arm or leaves out
    a pilot is refused unless R214_TEST_ONLY is set, and every use of the override is said on stderr."""
    import os, sys
    env = os.environ if env is None else env
    raw = env.get("R214_PILOTS")
    if not raw:
        return list(DEFAULT_PILOTS)
    names = raw.split()
    bad = [n for n in names if n in COUNTED] + [n for n in DEFAULT_PILOTS if n not in names]
    if bad and not env.get("R214_TEST_ONLY"):
        sys.exit(f"R214_PILOTS={raw!r} names a counted arm or leaves out a pilot ({' '.join(bad)}): refused (R214_TEST_ONLY is for tests only)")
    print(f"note: R214_PILOTS override in use: {raw}" + (" (R214_TEST_ONLY)" if env.get("R214_TEST_ONLY") else ""), file=sys.stderr)
    return names


def marker_ok(out_dir, pilots):
    """D5/G2: a marker the check wrote: <out>/pilot_ok.<pilot> holding exactly `PILOT OK <pilot>`, <pilot> one of the pilot names"""
    import glob
    for f in glob.glob(str(pathlib.Path(out_dir) / "pilot_ok.*")):
        name = f.rsplit("pilot_ok.", 1)[1]
        try:
            if name in pilots and pathlib.Path(f).read_text().strip() == f"PILOT OK {name}":
                return True
        except OSError:
            pass
    return False


if __name__ == "__main__":
    import sys
    if sys.argv[1:2] == ["pilots"]:
        print(" ".join(pilots_from_env()))
    elif sys.argv[1:2] == ["marker"]:
        sys.exit(0 if marker_ok(sys.argv[2], pilots_from_env()) else 1)
