#!/usr/bin/env python3
"""Independent recount for leaf 21.2 (written from the definition, not from census.py).

Convention: only counts, tool names, command strings cut to 200 chars, paths and
transcript basenames leave this script. No message text, no tool-result text.
Streams every transcript line by line.
"""
import json, os, pathlib, re, sys, collections, datetime

TOOL_CFG = pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude")      # the tool's own CLAUDE_CONFIG_DIR
ROOT = str(TOOL_CFG / 'projects')
REPO_ROOT = pathlib.Path(os.environ.get('BMA_REPO') or pathlib.Path(__file__).resolve().parents[4])
PARENT_DIR = str(REPO_ROOT.parent)      # the folder that holds the repo
HOME = str(pathlib.Path.home())
CFG_NAME = TOOL_CFG.relative_to(HOME).parts[0] if TOOL_CFG.is_relative_to(HOME) else TOOL_CFG.name      # the config folder's own name
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '03c_verify_census.json')
REPO_PROJECT = re.sub(r'[^A-Za-z0-9]', '-', str(REPO_ROOT))
CURRENT_SESSION = '<session-id>'
# 2026-11-12 00:30 local (CET, UTC+1) == 2026-11-11T23:30:00Z
CUTOFF_UTC = '2026-11-11T23:30:00'
RULES = '00-ai-rules.md'
TITLES = {1: 'Self-Registration', 2: 'Session Restore', 3: 'Routing Table', 4: 'Fractal TTEV', 5: 'Anti-Hallucination', 6: 'Coding', 7: 'Protocol Updates', 8: 'Multi-Agent'}

HEAD_RE = re.compile(r'(?m)^\s*(?:\d+\s*[→\t])?\s*##\s+(\d+)\.')
CUT_RES = {
    'chars-truncated-marker': re.compile(r'\.\.\. \[\d+ (?:characters|chars|lines|bytes) truncated\] \.\.\.'),
    'persisted-output': re.compile(r'<persisted-output>|Output too large'),
    'read-token-limit': re.compile(r'exceeds maximum allowed tokens'),
}

# ---------------------------------------------------------------- shell lexer
def lex(cmd):
    """Tiny shell lexer. Returns (segments, heredoc_bodies); each segment is a
    dict(tokens=[...], redirs=[...], pipe_next=bool). Quotes are removed from tokens.
    Operators: && || ; | & newline, > >> < ( ). Heredoc bodies are skipped."""
    segs = []; bodies = []
    toks = []; redirs = []
    cur = None  # current token being built
    i = 0; n = len(cmd)
    pending_heredocs = []
    expect_redir = None
    def flush():
        nonlocal cur, expect_redir
        if cur is not None:
            if expect_redir is not None:
                if expect_redir == 'heredoc':
                    pending_heredocs.append(cur)
                else:
                    redirs.append((expect_redir, cur))
                expect_redir = None
            else:
                toks.append(cur)
            cur = None
    def endseg(pipe=False):
        nonlocal toks, redirs
        flush()
        if toks or redirs:
            segs.append({'tokens': toks, 'redirs': redirs, 'pipe_next': pipe})
        toks = []; redirs = []
    while i < n:
        c = cmd[i]
        if c == '\\' and i + 1 < n:
            cur = (cur or '') + cmd[i + 1]; i += 2; continue
        if c == "'":
            j = cmd.find("'", i + 1)
            if j < 0: j = n
            cur = (cur or '') + cmd[i + 1:j]; i = j + 1; continue
        if c == '"':
            j = i + 1; buf = ''
            while j < n and cmd[j] != '"':
                if cmd[j] == '\\' and j + 1 < n: buf += cmd[j + 1]; j += 2; continue
                buf += cmd[j]; j += 1
            cur = (cur or '') + buf; i = j + 1; continue
        if c == '#' and cur is None:
            j = cmd.find('\n', i)
            i = n if j < 0 else j; continue
        if c in ' \t':
            flush(); i += 1; continue
        if c == '\n':
            endseg(False)
            for d in pending_heredocs:
                # skip body up to a line equal to the delimiter
                body = []; i += 1
                while i < n:
                    j = cmd.find('\n', i)
                    line = cmd[i:] if j < 0 else cmd[i:j]
                    i = n if j < 0 else j + 1
                    if line.strip() == d: break
                    body.append(line)
                bodies.append('\n'.join(body))
                i -= 1  # compensate the i += 1 below
            pending_heredocs = []
            i += 1; continue
        if c == '&' and i + 1 < n and cmd[i + 1] == '&': endseg(False); i += 2; continue
        if c == '|' and i + 1 < n and cmd[i + 1] == '|': endseg(False); i += 2; continue
        if c == '|': endseg(True); i += 1; continue
        if c == ';': endseg(False); i += 1; continue
        if c == '(' or c == ')': endseg(False); i += 1; continue
        if c == '&':
            # &> or >& handled below; lone & is a separator
            if i + 1 < n and cmd[i + 1] == '>':
                flush(); expect_redir = '>' ; i += 2
                if i < n and cmd[i] == '>': i += 1
                continue
            endseg(False); i += 1; continue
        if c == '<':
            if i + 1 < n and cmd[i + 1] == '<':
                flush(); i += 2
                if i < n and cmd[i] == '-': i += 1
                if i < n and cmd[i] == '<': i += 1  # here-string
                expect_redir = 'heredoc'; continue
            flush(); expect_redir = '<'; i += 1; continue
        if c == '>':
            # fd-number prefix such as 2> is a token of digits already in cur
            if cur is not None and cur.isdigit():
                cur = None
            else:
                flush()
            i += 1
            if i < n and cmd[i] == '>': i += 1
            if i < n and cmd[i] == '&':
                # >&2 / >&1: not a file
                i += 1
                j = i
                while j < n and cmd[j].isdigit(): j += 1
                i = j; expect_redir = None; continue
            expect_redir = '>'; continue
        cur = (cur or '') + c; i += 1
    endseg(False)
    return segs, bodies

WRAPPERS = {'sudo', 'time', 'command', 'nohup', 'env', 'exec', 'builtin'}
def cmdword(tokens):
    k = 0
    while k < len(tokens):
        t = tokens[k]
        if re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', t) or t in WRAPPERS:
            k += 1; continue
        return k
    return None

READERS = {'cat', 'head', 'tail', 'sed', 'awk', 'gawk', 'grep', 'egrep', 'fgrep', 'rg', 'ag', 'less', 'more', 'nl', 'bat',
           'tac', 'od', 'xxd', 'strings', 'cut', 'sort', 'uniq', 'tr', 'fold', 'paste', 'pr'}
SCRIPTERS = {'python', 'python3', 'node', 'perl', 'ruby', 'php'}
SLICERS = {'head', 'tail', 'grep', 'egrep', 'fgrep', 'rg', 'ag', 'awk', 'gawk', 'cut'}

def is_rules_tok(t):
    return bool(re.match(r'^[^\s"\'`]*' + re.escape(RULES) + r'$', t))

def classify_bash_access(cmd):
    """Return None if the command does not mention the file as a path argument;
    otherwise dict(kind, slice_shape, chained)."""
    segs, bodies = lex(cmd)
    hit = None
    for si, s in enumerate(segs):
        toks = s['tokens']
        k0 = cmdword(toks)
        if k0 is not None and os.path.basename(toks[k0]) in SCRIPTERS and any(RULES in t for t in toks[k0 + 1:]):
            hit = {'kind': 'script', 'shape': os.path.basename(toks[k0]), 'chained': len(segs) > 1, 'cmd': os.path.basename(toks[k0])}
            break
        # a redirect '>' target is a write, not a read: only argv tokens and '<' redirects count
        mention = any(is_rules_tok(t) for t in toks) or any(op == '<' and is_rules_tok(t) for op, t in s['redirs'])
        if not mention: continue
        k = cmdword(toks)
        cw = os.path.basename(toks[k]) if k is not None else ''
        redir_read = any(op == '<' and is_rules_tok(t) for op, t in s['redirs'])
        if cw in READERS or redir_read:
            shape = None
            args = toks[k + 1:] if k is not None else []
            if cw in ('head', 'tail'):
                m = re.search(r'-n\s*(\d+)|^-(\d+)$', ' '.join(args))
                nn = None
                for a in args:
                    mm = re.match(r'^-(\d+)$', a)
                    if mm: nn = mm.group(1)
                for idx, a in enumerate(args):
                    if a == '-n' and idx + 1 < len(args): nn = args[idx + 1]
                    if a == '-c' and idx + 1 < len(args): nn = args[idx + 1] + 'c'
                    mm = re.match(r'^-n(\d+)$', a)
                    if mm: nn = mm.group(1)
                shape = '%s -%s' % (cw, nn if nn else '?')
            elif cw == 'sed':
                if any(a == '-i' or a.startswith('-i') for a in args):
                    hit = hit or {'kind': 'other', 'detail': 'sed-i'}; continue
                rng = [a for a in args if re.match(r"^\d+(,\d+|,\$)?p$", a) or re.match(r'^\d+,\d+p?$', a) or re.match(r'^/.*/', a)]
                if '-n' in args or any(re.match(r'^-[A-Za-z]*n', a) for a in args):
                    shape = "sed -n %s" % (rng[0] if rng else '?')
                else:
                    shape = 'sed-script'
            elif cw in SLICERS:
                shape = cw
            piped_slice = None
            # a later pipeline segment that slices the stream
            j = si
            while j < len(segs) and segs[j]['pipe_next']:
                j += 1
                kk = cmdword(segs[j]['tokens'])
                ncw = os.path.basename(segs[j]['tokens'][kk]) if kk is not None else ''
                if ncw in SLICERS or (ncw == 'sed' and '-n' in segs[j]['tokens']):
                    piped_slice = ncw
                    pa = segs[j]['tokens'][kk + 1:]
                    if ncw in ('head', 'tail'):
                        nn = None
                        for ix, a in enumerate(pa):
                            mm = re.match(r'^-(\d+)$|^-n(\d+)$', a)
                            if mm: nn = mm.group(1) or mm.group(2)
                            if a == '-n' and ix + 1 < len(pa): nn = pa[ix + 1]
                            if a == '-c' and ix + 1 < len(pa): nn = pa[ix + 1] + 'c'
                        piped_slice = '%s -%s' % (ncw, nn if nn else '?')
            if shape is None and piped_slice:
                shape = 'cat|' + piped_slice
            chained = len(segs) > 1
            hit = {'kind': 'slice' if shape else 'whole', 'shape': shape, 'chained': chained, 'cmd': cw}
            break
        elif cw in SCRIPTERS:
            hit = hit or {'kind': 'script', 'shape': cw, 'chained': len(segs) > 1, 'cmd': cw}
        else:
            hit = hit or {'kind': 'other', 'detail': cw or '?', 'cmd': cw}
    return hit

# --------------------------------------------------------- file-changing calls
GIT_CHANGING = {'add', 'commit', 'checkout', 'switch', 'merge', 'rebase', 'reset', 'stash', 'worktree', 'cherry-pick',
                'apply', 'mv', 'rm', 'restore', 'pull', 'clone', 'init', 'am', 'revert', 'clean'}
SIMPLE_CHANGING = {'mkdir', 'touch', 'rm', 'rmdir', 'mv', 'cp', 'ln', 'tee', 'chmod', 'chown', 'install', 'truncate', 'dd',
                   'rsync', 'unzip', 'patch', 'mktemp'}
PYWRITE = re.compile(r"open\([^)]*['\"][wax]\+?b?['\"]|write_text|write_bytes|\.write\(|json\.dump\(|os\.makedirs|os\.mkdir|shutil\.|os\.rename|os\.remove|\.mkdir\(|\.touch\(")

def path_class(p, cwd):
    if p is None: return 'unknown'
    if p.startswith('~'): p = HOME + p[1:]
    if re.match(r'^\$\{?(TMPDIR|TMP|SCRATCH)', p): return 'scratch'
    if p.startswith('$') or '`' in p: return 'unknown'
    if not p.startswith('/'):
        p = os.path.normpath(os.path.join(cwd or '/', p))
    else:
        p = os.path.normpath(p)
    if p.startswith(('/tmp/', '/private/tmp/', '/var/folders/', '/private/var/folders/', '/dev/shm/')) or p in ('/tmp', '/private/tmp') or '/scratchpad' in p:
        return 'scratch'
    if '/' + CFG_NAME + '/' in p or '/.claude/' in p:
        return 'claude-state'
    if p.startswith(PARENT_DIR):
        return 'repo'
    if p.startswith('/dev/'):
        return 'devnull'
    return 'home-other'

def bash_change(cmd, cwd):
    """Return None if not file-changing, else (reason, [target classes])."""
    segs, bodies = lex(cmd)
    classes = []; reasons = []
    cur_cwd = cwd
    varmap = {}
    for s in segs:
        for t in s['tokens']:
            mv = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*)$', t)
            if mv: varmap[mv.group(1)] = mv.group(2)
    def subst(t):
        if t is None: return t
        for _ in range(3):
            t2 = re.sub(r'\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?', lambda m: varmap.get(m.group(1), m.group(0)), t)
            if t2 == t: break
            t = t2
        return t
    for s in segs:
        s = {'tokens': [subst(t) for t in s['tokens']], 'redirs': [(op, subst(t)) for op, t in s['redirs']], 'pipe_next': s['pipe_next']}
        toks = s['tokens']
        k = cmdword(toks)
        if k is not None:
            cw = os.path.basename(toks[k]); args = toks[k + 1:]
            nonopt = [a for a in args if not a.startswith('-')]
            if cw == 'cd' and nonopt:
                t = nonopt[0]
                if t.startswith('~'): t = HOME + t[1:]
                if not t.startswith('$'):
                    cur_cwd = os.path.normpath(os.path.join(cur_cwd or '/', t))
                continue
            if cw in SIMPLE_CHANGING:
                reasons.append(cw)
                if cw in ('cp', 'mv', 'ln', 'rsync') and len(nonopt) >= 1:
                    classes.append(path_class(nonopt[-1], cur_cwd))  # destination
                else:
                    for t in (nonopt or [None]): classes.append(path_class(t, cur_cwd))
            elif cw == 'git':
                sub = next((a for a in args if not a.startswith('-')), None)
                # skip "-C dir" forms
                if '-C' in args:
                    ci = args.index('-C'); rest = args[ci + 2:]
                    sub = next((a for a in rest if not a.startswith('-')), None)
                    base = args[ci + 1] if ci + 1 < len(args) else None
                    gcwd = os.path.normpath(os.path.join(cur_cwd or '/', base)) if base else cur_cwd
                else:
                    gcwd = cur_cwd
                if sub in GIT_CHANGING:
                    reasons.append('git ' + sub); classes.append(path_class('.', gcwd))
            elif cw == 'sed' and any(a == '-i' or re.match(r'^-i', a) for a in args):
                reasons.append('sed -i'); classes.append(path_class(nonopt[-1] if nonopt else None, cur_cwd))
            elif cw == 'perl' and any(re.match(r'^-[A-Za-z]*i', a) for a in args):
                reasons.append('perl -i'); classes.append(path_class(nonopt[-1] if nonopt else None, cur_cwd))
            elif cw in ('npm', 'pnpm', 'yarn', 'pip', 'pip3', 'brew', 'bun') and any(a in ('install', 'i', 'add') for a in args):
                reasons.append(cw + ' install'); classes.append(path_class('.', cur_cwd))
            elif cw in SCRIPTERS and any(PYWRITE.search(t) for t in args):
                reasons.append(cw + ' write'); classes.append('repo' if any(PARENT_DIR in t for t in args) and not any(re.search(r'/tmp/|scratchpad', t) for t in args) else path_class('.', cur_cwd))
            elif cw in ('curl', 'wget') and any(a in ('-o', '-O', '--output') for a in args):
                reasons.append(cw + ' -o'); classes.append('unknown')
            elif cw == 'tar' and any(re.match(r'^-?[A-Za-z]*x', a) for a in args[:1]):
                reasons.append('tar x'); classes.append(path_class('.', cur_cwd))
        for op, t in s['redirs']:
            if op == '>' and t and t != '/dev/null' and not t.startswith('&'):
                reasons.append('redirect'); classes.append(path_class(t, cur_cwd))
    for b in bodies:
        if PYWRITE.search(b):
            reasons.append('heredoc-write')
            classes.append('repo' if PARENT_DIR in b and not re.search(r'/tmp/|scratchpad', b) else path_class('.', cur_cwd))
    if not reasons: return None
    return reasons[0], classes

def change_class(classes):
    cl = [c for c in classes if c != 'devnull']
    if not cl: return 'scratch'
    if 'repo' in cl: return 'repo'
    if all(c == 'scratch' for c in cl): return 'scratch'
    if 'home-other' in cl: return 'home-other'
    if 'claude-state' in cl: return 'claude-state'
    return 'unknown'

# ---------------------------------------------------------------- per transcript
def result_text(b):
    c = b.get('content')
    if isinstance(c, str): return c
    if isinstance(c, list):
        return '\n'.join(x.get('text', '') for x in c if isinstance(x, dict) and x.get('type') == 'text')
    return ''

def scan(path):
    rec = {'accesses': [], 'first_change': None, 'tools': collections.Counter(), 'ts_first': None,
           'sig_results': [], 'cwds': set(), 'scratch_rq': False, 'fixture_tree': False, 'mention_only_cmds': [], 'attach_rules_file': False}
    seen_use = set(); uses = {}; seen_res = set(); allbrief = {}
    ntool = 0
    with open(path, 'r', errors='replace') as fh:
        for li, line in enumerate(fh):
            if '"tool_use"' not in line and '"tool_result"' not in line and '"timestamp"' not in line and '"attachment"' not in line:
                continue
            try: o = json.loads(line)
            except Exception: continue
            if rec['ts_first'] is None and o.get('timestamp'): rec['ts_first'] = o['timestamp']
            if o.get('cwd'): rec['cwds'].add(o['cwd'])
            a = o.get('attachment')
            if isinstance(a, dict) and a.get('type') == 'file' and RULES in json.dumps(a)[:4000]:
                rec['attach_rules_file'] = True
            m = o.get('message')
            if not isinstance(m, dict) or not isinstance(m.get('content'), list): continue
            cwd = o.get('cwd')
            for b in m['content']:
                if not isinstance(b, dict): continue
                if b.get('type') == 'tool_use':
                    tid = b.get('id')
                    if tid in seen_use: continue
                    seen_use.add(tid); ntool += 1
                    name = b.get('name') or ''; inp = b.get('input') or {}
                    allbrief[tid] = (name, str(inp.get('file_path') or inp.get('command') or inp.get('path') or '')[:200])
                    rec['tools'][name] += 1
                    if re.search(r'scratchpad/r\d+/q\d+', json.dumps(inp)[:6000]): rec['scratch_rq'] = True
                    if re.search(r'/scratchpad/(?:r\d+[a-z]*|exp\d+|probe\d+)/', json.dumps(inp)[:20000]): rec['fixture_tree'] = True
                    # rules access?
                    acc = None
                    if name == 'Read' and str(inp.get('file_path', '')).endswith(RULES):
                        sl = ('offset' in inp and inp.get('offset') not in (None, 0, 1)) or ('limit' in inp and inp.get('limit') is not None)
                        acc = {'tool': 'Read', 'kind': 'slice' if sl else 'whole',
                               'shape': ('Read offset=%s limit=%s' % (inp.get('offset'), inp.get('limit'))) if sl else None,
                               'chained': False, 'cmd': 'Read'}
                        acc['cmd200'] = str(inp.get('file_path'))[:200]
                    elif name in ('Grep', 'Glob') and RULES in json.dumps(inp):
                        acc = {'tool': name, 'kind': 'slice', 'shape': name, 'chained': False, 'cmd': name, 'cmd200': json.dumps(inp)[:200]}
                    elif name.lower() == 'bash' and RULES in str(inp.get('command', '')):
                        cmd = str(inp.get('command', ''))
                        h = classify_bash_access(cmd)
                        if h and h['kind'] in ('whole', 'slice', 'script'):
                            acc = dict(h); acc['tool'] = 'Bash'; acc['cmd200'] = cmd[:200]
                        else:
                            rec['mention_only_cmds'].append((h or {}).get('detail', 'nonpath-mention'))
                    if acc:
                        acc.update({'use_line': li, 'idx': ntool - 1, 'res_line': None, 'secs': [], 'cut': [], 'err': False})
                        uses[tid] = acc; rec['accesses'].append(acc)
                    # file-changing?
                    if rec['first_change'] is None:
                        ch = None
                        if name in ('Write', 'Edit', 'MultiEdit', 'NotebookEdit'):
                            p = inp.get('file_path') or inp.get('notebook_path')
                            ch = (name, [path_class(p, cwd)])
                        elif name.lower() == 'bash':
                            r = bash_change(str(inp.get('command', '')), cwd)
                            if r: ch = (r[0], r[1])
                        if ch:
                            rec['first_change'] = {'line': li, 'idx': ntool - 1, 'tool': name, 'reason': ch[0],
                                                   'class': change_class(ch[1]),
                                                   'fixture': bool(re.search(r'/scratchpad/(?:r\d+[a-z]*|exp\d+|probe\d+)/', json.dumps(inp)[:20000])),
                                                   'cmd200': (str(inp.get('command', ''))[:200] if name.lower() == 'bash' else str(inp.get('file_path', ''))[:200])}
                elif b.get('type') == 'tool_result':
                    tid = b.get('tool_use_id')
                    # content signature (any tool): which exact rules headings reached the agent
                    tt = result_text(b)
                    if '## ' in tt:
                        sg = sorted(n for n, ttl in TITLES.items() if ('## %d. %s' % (n, ttl)) in tt)
                        if sg: rec['sig_results'].append((li, sg, tid in uses, bool(b.get('is_error')), allbrief.get(tid, ('?', ''))))
                    if tid in uses and tid not in seen_res:
                        seen_res.add(tid)
                        t = result_text(b)
                        acc = uses[tid]
                        acc['res_line'] = li
                        acc['secs'] = sorted(set(int(x) for x in HEAD_RE.findall(t)))
                        acc['cut'] = [k for k, rx in CUT_RES.items() if rx.search(t)]
                        acc['err'] = bool(b.get('is_error'))
                        acc['res_len'] = len(t)
    return rec

def judge(rec):
    """Return dict with verdict fields; None if not accessed (no reading access)."""
    acc = rec['accesses']
    if not acc: return None
    fc = rec['first_change']
    lim = fc['line'] if fc else float('inf')
    pre = [a for a in acc if a['res_line'] is not None and a['res_line'] < lim]
    secs = set()
    for a in pre: secs |= set(a['secs'])
    allsecs = set()
    for a in acc:
        if a['res_line'] is not None: allsecs |= set(a['secs'])
    complete = set(range(1, 9)) <= secs
    gs = set()
    for a in pre:
        if re.search(r'grep|rg$|ag$|Grep', str(a.get('shape') or '')): continue
        gs |= set(a['secs'])
    sigpre = set()
    for (ln, sg, isacc, iserr, br) in rec['sig_results']:
        if ln < lim: sigpre |= set(sg)
    sigall = set()
    for (ln, sg, isacc, iserr, br) in rec['sig_results']: sigall |= set(sg)
    out = {'sig_pre': sorted(sigpre), 'sig_ever': sorted(sigall), 'complete_sig': set(range(1, 9)) <= sigpre, 'complete_no_grep': set(range(1, 9)) <= gs, 'complete': complete, 'had_change': bool(fc), 'pre_n': len(pre), 'secs_pre': sorted(secs), 'secs_ever': sorted(allsecs)}
    if complete:
        out['mode'] = None
    else:
        if not pre: out['mode'] = 'a'
        elif any(a['cut'] for a in pre): out['mode'] = 'c'
        elif any(a['kind'] == 'slice' for a in pre): out['mode'] = 'b'
        elif any(a['kind'] == 'script' for a in pre): out['mode'] = 'b'  # script slices are deliberate too; reported separately
        else: out['mode'] = 'd'
        out['has_cut'] = any(a['cut'] for a in pre)
        out['has_slice'] = any(a['kind'] == 'slice' for a in pre)
    return out


def is_main(s): return not s['is_subagent']

def fixture_first(s):
    fc = s['first_change']
    return fc['fixture'] if fc else s['fixture_tree']

def analyze(S, excluded, nfiles):
    T = {}
    A = [s for s in S if s['accessed']]
    dup = [s for s in S if s['basename'].startswith('<session-id>')]
    uniq = [s for s in S if not (s in dup[1:])]
    Au = [s for s in uniq if s['accessed']]
    T['totals_unique_by_content'] = {'scored': len(uniq), 'accessed': len(Au), 'complete': sum(s['complete'] for s in Au), 'incomplete': sum(not s['complete'] for s in Au)}
    T['totals'] = {'files_on_disk': nfiles, 'excluded': len(excluded), 'scored': len(S), 'accessed': len(A),
                   'not_accessed': len(S) - len(A), 'complete': sum(s['complete'] for s in A),
                   'incomplete': sum(not s['complete'] for s in A),
                   'byte_identical_duplicate_pairs': 1}
    na = [s for s in S if not s['accessed']]
    T['not_accessed_breakdown'] = {
        'n': len(na),
        'full_8_headings_by_title_before_first_change_via_other_tool_result': sum(1 for s in na if len(s['sig_pre_any']) == 8),
        'mention_only_nonreading_command': sum(1 for s in na if s['mention_only']),
        'rules_file_injected_by_file_attachment': sum(1 for s in na if s['attach_rules_file']),
    }
    # per kind
    pk = {}
    for k in ['repo-main', 'repo-subagent', 'arm', 'other', 'ALL']:
        X = [s for s in S if k == 'ALL' or s['kind'] == k]
        Ac = [s for s in X if s['accessed']]
        I = [s for s in Ac if not s['complete']]
        pk[k] = {'scanned': len(X), 'accessed': len(Ac), 'not_accessed': len(X) - len(Ac), 'complete': len(Ac) - len(I), 'incomplete': len(I),
                 'modes': dict(collections.Counter(s['mode'] for s in I)),
                 'complete_title_variant': sum(1 for s in Ac if s['complete_sig']),
                 'complete_if_chained_results_ignored': None}
    T['per_kind'] = pk
    # check 3: incomplete x kind x mode, with mode-a split
    def a_class(s):
        fc = s['first_change']
        if not fc: return 'no-change-in-session'
        return fc['class']
    t3 = {}
    for k in ['repo-main', 'repo-subagent', 'arm', 'other', 'ALL']:
        X = [s for s in S if (k == 'ALL' or s['kind'] == k) and s['accessed'] and not s['complete']]
        row = {'incomplete': len(X)}
        for m in 'abcd': row['mode_' + m] = sum(1 for s in X if s['mode'] == m)
        a = [s for s in X if s['mode'] == 'a']
        row['a_first_change_class'] = dict(collections.Counter(a_class(s) for s in a))
        row['a_first_change_reason'] = dict(collections.Counter((s['first_change'] or {}).get('reason', 'none') for s in a))
        row['a_but_full_8_headings_via_other_path_before_change'] = sum(1 for s in a if len(s['sig_pre_any']) == 8)
        row['a_scratch_and_no_other_path_headings'] = sum(1 for s in a if a_class(s) == 'scratch' and len(s['sig_pre_any']) < 8)
        for m in 'abc': row['mode_%s_complete_later_in_session' % m] = sum(1 for s in X if s['mode'] == m and set(range(1, 9)) <= set(s['secs_ever']))
        row['b_with_cut_marker_too'] = sum(1 for s in X if s['mode'] == 'b' and s.get('has_cut'))
        t3[k] = row
    T['check3_incomplete_by_kind_mode'] = t3
    # headline variants
    hv = {}
    for k in ['repo-main', 'repo-subagent', 'arm', 'other', 'ALL']:
        Ac = [s for s in S if (k == 'ALL' or s['kind'] == k) and s['accessed']]
        def frac(sub):
            c = sum(1 for s in sub if s['complete']); return {'complete': c, 'of': len(sub), 'incomplete': len(sub) - c}
        scratch_a = [s for s in Ac if (not s['complete']) and s['mode'] == 'a' and a_class(s) == 'scratch']
        all_a = [s for s in Ac if (not s['complete']) and s['mode'] == 'a']
        hv[k] = {'H0_as_defined': frac(Ac),
                 'H1_minus_mode_a_with_scratch_first_change': frac([s for s in Ac if s not in scratch_a]),
                 'H2_minus_all_mode_a': frac([s for s in Ac if s not in all_a]),
                 'H3_content_title_variant_complete_of_accessed': {'complete': sum(1 for s in Ac if s['complete_sig']), 'of': len(Ac)}}
    T['headline_variants'] = hv
    # check 4: other projects
    oth = collections.defaultdict(lambda: collections.Counter())
    for s in S:
        if s['kind'] == 'other':
            key = (s['project'], 'subagent' if s['is_subagent'] else 'main')
            oth[key]['scanned'] += 1
            if s['accessed']:
                oth[key]['complete' if s['complete'] else 'incomplete'] += 1
            else: oth[key]['not_accessed'] += 1
    T['check4_other_projects'] = {'%s | %s' % k: dict(v) for k, v in sorted(oth.items())}
    # repo-subagent split
    sp = {}
    RS = [s for s in S if s['kind'] == 'repo-subagent']
    for label, pred in [('arm-like (first file-changing call, or the whole session if none, inside a scratchpad fixture tree r*/exp*/probe*)', fixture_first),
                        ('work-like (all the others)', lambda s: not fixture_first(s))]:
        X = [s for s in RS if pred(s)]
        Ac = [s for s in X if s['accessed']]
        I = [s for s in Ac if not s['complete']]
        sp[label] = {'sessions': len(X), 'accessed': len(Ac), 'complete': len(Ac) - len(I), 'incomplete': len(I),
                     'modes': dict(collections.Counter(s['mode'] for s in I)),
                     'a_scratch': sum(1 for s in I if s['mode'] == 'a' and a_class(s) == 'scratch')}
    T['check4_repo_subagent_split'] = sp
    # sensitivity: any fixture touch
    X = [s for s in RS if s['fixture_tree']]
    Ac = [s for s in X if s['accessed']]
    T['check4_repo_subagent_split_sensitivity_any_fixture_touch'] = {'sessions': len(X), 'accessed': len(Ac), 'complete': sum(s['complete'] for s in Ac), 'incomplete': sum(not s['complete'] for s in Ac)}
    # check 5: main sessions
    def c5(M):
        Ac = [s for s in M if s['accessed']]
        I = [s for s in Ac if not s['complete']]
        return {'N': len(M), 'accessed': len(Ac), 'not_accessed': len(M) - len(Ac), 'complete': len(Ac) - len(I), 'incomplete': len(I),
                'modes': dict(collections.Counter(s['mode'] for s in I)),
                'a_first_change_class': dict(collections.Counter(a_class(s) for s in I if s['mode'] == 'a')),
                'incomplete_basenames': [(s['basename'][:13], s['kind'], s['mode'], a_class(s)) for s in I]}
    T['check5_main_unique_by_content'] = c5([s for s in uniq if is_main(s)])
    M = [s for s in S if is_main(s)]
    Ac = [s for s in M if s['accessed']]
    I = [s for s in Ac if not s['complete']]
    T['check5_main_sessions'] = {'N': len(M), 'by_kind': dict(collections.Counter(s['kind'] for s in M)), 'accessed': len(Ac), 'not_accessed': len(M) - len(Ac),
                                 'complete': len(Ac) - len(I), 'incomplete': len(I),
                                 'modes': dict(collections.Counter(s['mode'] for s in I)),
                                 'a_first_change_class': dict(collections.Counter(a_class(s) for s in I if s['mode'] == 'a'))}
    # check 6: slices
    sl = []
    for s in S:
        if s['accessed'] and not s['complete'] and s['mode'] == 'b':
            pre = [a for a in s['accesses'] if a['before_first_change']]
            shapes = [a['shape'] for a in pre if a['kind'] in ('slice', 'script')]
            missing = sorted(set(range(1, 9)) - set(s['secs_pre']))
            later_full = set(range(1, 9)) <= set(s['secs_ever'])
            later_access_after_change = any((not a['before_first_change']) and a['res_line'] is not None for a in s['accesses'])
            sl.append({'basename': s['basename'], 'kind': s['kind'], 'main': is_main(s), 'shapes': shapes, 'secs_pre': s['secs_pre'], 'missing': missing,
                       'completes_later_in_session': later_full, 'any_later_rules_access_after_first_change': later_access_after_change,
                       'first_change_class': a_class(s)})
    T['check6_slices'] = sl
    shape_ctr = collections.Counter()
    for r in sl:
        for sh in r['shapes']:
            shape_ctr[re.sub(r'(?<=,)\d+', 'B', re.sub(r'^(sed -n )\d+', r'\1A', sh)) if sh.startswith('sed') else sh] += 1
    T['check6_shape_counts'] = dict(shape_ctr)
    T['check6_missing_counts'] = dict(collections.Counter(m for r in sl for m in r['missing']))
    T['check6_complete_later'] = {'n': len(sl), 'completes_later': sum(r['completes_later_in_session'] for r in sl)}
    # cut markers on any rules-access result
    cm = collections.Counter(); cmb = collections.Counter()
    for s in S:
        for a in s.get('accesses', []):
            for c in a['cut']:
                cm[c] += 1
                if a['before_first_change']: cmb[c] += 1
    T['cut_markers_on_rules_access_results'] = {'all': dict(cm), 'before_first_change': dict(cmb)}
    # contamination check: complete only thanks to chained commands
    chained_only = 0; chained_only_title = 0
    for s in A:
        if not s['complete']: continue
        pre = [a for a in s['accesses'] if a['before_first_change']]
        ss = set()
        for a in pre:
            if not a['chained']: ss |= set(a['secs'])
        if not set(range(1, 9)) <= ss:
            chained_only += 1
            if s['complete_sig']: chained_only_title += 1
    T['complete_only_by_chained_command_results'] = {'n': chained_only, 'of_which_title_confirmed': chained_only_title}
    T['complete_vs_title_disagree'] = {'numeric_complete_title_not': sum(1 for s in A if s['complete'] and not s['complete_sig']),
                                       'title_complete_numeric_not': sum(1 for s in A if (not s['complete']) and s['complete_sig'])}
    T['no_change_in_session_among_accessed'] = sum(1 for s in A if not s['had_change'])
    return T

def compare(S, excluded):
    """Compare with the author's 03b_census.json (read only the aggregates and the incomplete list)."""
    a = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '03b_census.json')))
    A = collections.Counter(r['basename'] for r in a['incomplete_sessions'])
    mine = collections.Counter(s['basename'] for s in S if s['accessed'] and not s['complete'])
    out = {'author_incomplete_entries': sum(A.values()), 'author_incomplete_distinct': len(A), 'my_incomplete_entries': sum(mine.values()),
           'author_by_kind': {k: {x: a['by_kind'][k][x] for x in ('in_window', 'accessed', 'complete', 'incomplete')} for k in a['by_kind']},
           'author_totals_accessed': a['totals']['accessed'], 'author_excluded': a['excluded_basenames'], 'disagreements': []}
    byb = {s['basename']: s for s in S}
    ex = {e['basename']: e for e in excluded}
    for b in sorted(set(A) - set(mine)):
        r = [x for x in a['incomplete_sessions'] if x['basename'] == b][0]
        row = {'basename': b, 'author': 'incomplete (%s, first access %s, missing %s, had_write %s, reads_before_first_write %s)' % (r['cause'], r['first_access_kind'], r['missing'], r['had_write'], r['reads_before_first_write'])}
        if b in ex:
            row['mine'] = 'EXCLUDED (subagent of current session, born %s local); would score accessed=%s complete=%s mode=%s' % (ex[b]['birth_local'], ex[b]['would_be_accessed'], ex[b]['would_be_complete'], ex[b]['would_be_mode'])
        elif b in byb:
            x = byb[b]; row['mine'] = 'not accessed (only non-reading mentions of the path: %s)' % (x['mention_cmds'],)
        out['disagreements'].append(row)
    for b in sorted(set(mine) - set(A)):
        x = byb[b]
        out['disagreements'].append({'basename': b, 'author': 'not in incomplete list', 'mine': 'incomplete mode %s; accesses %s; first change %s %s' % (
            x['mode'], [(q['tool'], q['shape'], q['secs'], 'before' if q['before_first_change'] else 'after') for q in x['accesses']][:3], x['first_change']['reason'], x['first_change']['class'])})
    return out

def main():
    files = []
    for root, ds, fs in os.walk(ROOT):
        for f in sorted(fs):
            if f.endswith('.jsonl'): files.append(os.path.join(root, f))
    files.sort()
    sessions = []; excluded = []
    for p in files:
        rel = os.path.relpath(p, ROOT).split(os.sep)
        proj = rel[0]; base = rel[-1]
        sub = (len(rel) == 4 and rel[2] == 'subagents')
        rec = scan(p)
        birth = datetime.datetime.fromtimestamp(os.stat(p).st_birthtime).strftime('%Y-%m-%d %H:%M:%S')
        # exclusion: subagents of the current session created after 2026-11-12 00:30 local
        if proj == REPO_PROJECT and sub and rel[1] == CURRENT_SESSION and (rec['ts_first'] or '')[:19] >= CUTOFF_UTC:
            jx = judge(rec)
            excluded.append({'basename': base, 'birth_local': birth, 'first_ts_utc': rec['ts_first'], 'size': os.path.getsize(p),
                             'would_be_accessed': jx is not None, 'would_be_complete': (jx or {}).get('complete'),
                             'would_be_mode': (jx or {}).get('mode')})
            continue
        if proj.startswith('-private-tmp'): kind = 'arm'
        elif proj == REPO_PROJECT: kind = 'repo-subagent' if sub else 'repo-main'
        else: kind = 'other'
        j = judge(rec)
        fcl0 = rec['first_change']['line'] if rec['first_change'] else float('inf')
        sigp = set(); siga = set()
        for (ln, sg, isacc, iserr, br) in rec['sig_results']:
            siga |= set(sg)
            if ln < fcl0: sigp |= set(sg)
        s = {'sig_pre_any': sorted(sigp), 'sig_ever_any': sorted(siga), 'basename': base, 'project': proj, 'kind': kind, 'is_subagent': sub, 'ts_first': rec['ts_first'],
             'size': os.path.getsize(p), 'accessed': j is not None, 'attach_rules_file': rec['attach_rules_file'],
             'mention_only': (j is None and bool(rec['mention_only_cmds'])), 'scratch_rq': rec['scratch_rq'], 'fixture_tree': rec['fixture_tree'],
             'cwd_first_class': None, 'tools_top': dict(rec['tools'].most_common(6))}
        cw = sorted(rec['cwds'])
        s['cwd_scratch_rq'] = any(re.search(r'scratchpad/r\d+/q\d+', c) for c in cw)
        s['cwd_fixture_tree'] = any(re.search(r'/scratchpad/(?:r\d+[a-z]*|exp\d+|probe\d+)/', c + '/') for c in cw)
        s['cwd_repo'] = any(c.startswith(str(REPO_ROOT)) for c in cw)
        s['first_change'] = rec['first_change']
        s['sig_sources_pre'] = [{'line': ln, 'secs': sg, 'via_rules_access': isacc, 'tool': br[0], 'what200': br[1]} for (ln, sg, isacc, iserr, br) in rec['sig_results'] if ln < fcl0][:6]
        if j:
            s.update(j)
            s['accesses'] = [{k: a[k] for k in ('idx', 'tool', 'kind', 'shape', 'chained', 'cmd200', 'secs', 'cut', 'err', 'use_line', 'res_line')} for a in rec['accesses']]
            fcl = rec['first_change']['line'] if rec['first_change'] else float('inf')
            for a in s['accesses']: a['before_first_change'] = (a['res_line'] is not None and a['res_line'] < fcl)
        s['mention_cmds'] = collections.Counter(rec['mention_only_cmds']).most_common(5)
        sessions.append(s)
    tables = analyze(sessions, excluded, len(files))
    tables['comparison_with_03b'] = compare(sessions, excluded)
    json.dump({'tables': tables, 'sessions': sessions, 'excluded': excluded}, open(OUT, 'w'), indent=1, default=list)
    print('files', len(files), 'scored', len(sessions), 'excluded', len(excluded))
    print(json.dumps(tables, indent=1, default=list))

if __name__ == '__main__':
    main()
