| # | § | unit | lines | class | VERIFY's class | verifiable | cost (tok) | cost of failure | evidence | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | Self-Registration | 3-15 | P | P | high | 274 | high | sentinel obeyed by 58/118 arms (20.10); CLAUDE.md precedence landed in 15.1 (#3) | **KEEP** |
| 2 | 2.0 | Pending upgrade | 18-18 | P | P | high | 36 | high | 19.5 UPGRADE rounds | **KEEP** |
| 3 | 2.0 | UNPOPULATED search | 19-19 | P | P | high | 63 | high | Decision 17 | **KEEP** |
| 4 | 2.1 | Quick Resume | 20-20 | P | P | med | 80 | med | none in isolation | **KEEP** |
| 5 | 2.2 | Full Restore | 21-21 | P | P | med | 44 | med | none in isolation | **KEEP** |
| 6 | 3 | Lazy-load prohibition | 24-24 | D | D | med | 19 | low | none | **KEEP** |
| 7 | 3 | Precedence rules>plan>memory | 25-25 | D | D | low | 78 | high | landed 15.5 (#7c); occasion never measured | **KEEP** |
| 8 | 3 | Routing Table | 26-35 | N | N | n/a | 127 | high | consumed by the Write Gate (Decision 13) | **KEEP** |
| 9 | 3 | Conceptual maps | 37-37 | D | **P** | high | 85 | med | decisions: map shape entries | **KEEP** |
| 10 | 3 | Context Slicing | 39-39 | D | **N** | med | 82 | low | 13.2 INCONCLUSIVE; 14.3 gave it an occasion nobody scored; semantics of the live key contextSlicingThreshold, which a cut would leave meaningless | **KEEP-untested** |
| 11 | 3 | Conversation log | 41-41 | N | **P** | high | 153 | low | rationale inline on purpose (05 L229), and it is the only way the reason travels: BEMYAGENT.md ships to projects without this repo's 05 | **KEEP** |
| 12 | 3 | Write Gate | 43-47 | P | P | high | 95 | med | Decision 13; 19.3: 6/6 arms emit PROTOCOL_CHECK, 55% of governed files named | **KEEP** |
| 13 | 4 | HTN structure | 50-51 | N | **P** | high | 87 | med | every round's work/ tree | **KEEP** |
| 14 | 4 | Decomposition | 52-52 | D | D | low | 74 | med | none; overlaps Delivers re-cut (L64) and depth cap (L51) | **KEEP-untested** |
| 15 | 4 | Ceremony sizing + CDM | 54-60 | P | P | high | 321 | high | 13.4; every round since | **KEEP** |
| 16 | 4 | THINK (with the TTEV-files header) | 62-63 | P | P | high | 116 | high | 20.8: Verification Plan predicts the artifact 6/6 | **KEEP** |
| 17 | 4 | TASK | 64-64 | P | P | high | 145 | high | Delivers line, every round | **KEEP** |
| 18 | 4 | EXECUTE (incl. redact secrets) | 65-65 | P | P | high | 40 | high | the 13.1b canonical case: 13 tokens, unverifiable, keep | **KEEP** |
| 181 | 4 | VERIFY pointer | 66-66 | N | N | n/a | 14 | low | points at Symbiotic Validation | **KEEP** |
| 19 | 4 | Handoff Principle | 67-67 | D | **P** | high | 44 | med | 20.9 null, fixture-limited; enforced by Git (L80) | **KEEP** |
| 20 | 4 | Symbiotic Validation | 69-72 | P | P | high | 168 | high | 13.5; 15.5 (#6) | **KEEP** |
| 21 | 4 | Who verifies | 73-73 | P | P | high | 88 | high | 15.8; 5/6 arms ran an independent VERIFY, unscored; 20.10's verifier moved 49->58 | **KEEP** |
| 22 | 4 | Autonomous rigor | 74-74 | D | D | low | 90 | high | Decision 15, never measured in isolation | **KEEP** |
| 23 | 4 | strictVerification depth | 75-75 | N | N | n/a | 37 | low | config semantics | **KEEP** |
| 24 | 4 | Pacing | 77-77 | N | **P** | high | 65 | high | config semantics + STOP | **KEEP** |
| 25 | 4 | Model switching | 78-78 | N | N | low | 46 | low | config semantics; no round exercised it | **KEEP** |
| 26 | 4 | Git | 80-80 | P | P | high | 70 | med | every round's commit order | **KEEP** |
| 27 | 5 | Read before modify | 83-83 | D | **P** | high | 31 | high | harness-enforced in most CLIs | **KEEP** |
| 28 | 5 | Label inferences | 84-84 | D | D | med | 38 | med | none that isolates it: 20.9's 3/3 split was about where the documents came from | **KEEP** |
| 29 | 5 | User premises | 85-85 | D | D | med | 38 | high | decisions: 3/3 spot-checked a fabricated premise | **KEEP** |
| 30 | 5 | New dependency | 86-86 | P | P | high | 24 | med | none in isolation | **KEEP** |
| 31 | 5 | Critical Review Protocol | 87-87 | P | P | med | 109 | med | decisions: guarantee-3 entry | **KEEP** |
| 32 | 6 | Surgical scope | 90-90 | D | **P** | high | 55 | med | 13.2: one accidental occasion | **KEEP** |
| 33 | 6 | Brevity | 91-91 | D | D | med | 70 | low | 13.2 INCONCLUSIVE; overlap with harness defaults seen on Claude Code only | **KEEP-untested** |
| 34 | 6 | Language | 92-92 | N | N | n/a | 36 | low | config semantics | **KEEP** |
| 35 | 6 | Glossary use | 93-93 | D | D | med | 32 | low | its declarative sibling (P3) measured 0/8 | **KEEP-untested** |
| 36 | 6 | Unpopulated 01 guard | 94-94 | P | P | high | 27 | high | Decision 17 | **KEEP** |
| 37 | 6 | Discussion capture | 95-95 | P | P | high | 83 | med | drafts/ writes | **KEEP** |
| 38 | 6 | CRITICAL same-response | 96-96 | P | P | high | 85 | high | Milestone 11: 7-8/8 against 0/8 declarative | **KEEP** |
| 39 | 6 | specs/ milestone done | 97-97 | P | P | high | 113 | med | none in isolation | **KEEP** |
| 40 | 7 | Migration | 100-101 | P | P | high | 62 | high | UPGRADE rounds | **KEEP** |
| 41 | 8 | Multi-Agent Parallelism | 104-107 | P | P | high | 95 | med | none: no round ever ran parallel worktrees; 13.3 already relocated the human-choice part (dispatch); steps 2-3 guard shared docs | **KEEP-untested** |

P: 21 units, 2138 tok, 62%
D: 13 units, 736 tok, 21%
N: 8 units, 565 tok, 16%
total classified: 3439 tok over 42 units
under VERIFY's classes: P 28 units 2658 tok 77% · D 8 units 439 tok 13% · N 6 units 342 tok 10%
disputed: 8 of 42 units, 602 tok
KEEP-untested: 5 units, 353 tok — Context Slicing, Decomposition, Brevity, Glossary use, Multi-Agent Parallelism
TRIM : 0 units, 0 tok — 
non-blank, non-heading lines NOT covered by any unit: []
