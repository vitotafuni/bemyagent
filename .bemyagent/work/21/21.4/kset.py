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
