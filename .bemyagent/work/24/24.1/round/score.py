import os,json,re,subprocess,glob
P=os.environ['BMA_SCRATCH']
def sh(a,cwd): return subprocess.run(a,cwd=cwd,capture_output=True,text=True)
cols="arm cell exit is_error turns cost seconds model denials changed plan plan_line1 upgrade_line rules_changed bak work_new tracked_changed says_downgrade says_nothing_to_upgrade names_both_numbers mentions_cmp expected ok".split()
rows=[];txt=[]
order=['older','numeric','same','edited','newer','unstamped','control']
arms=[os.path.basename(d) for d in glob.glob(P+'/[hs]-*') if os.path.isdir(d)]
arms.sort(key=lambda a:(order.index(a.split('-')[1]),a[0]!='h',a))
yn=lambda b:'yes' if b else 'no'
for arm in arms:
    d=f'{P}/{arm}';cell=arm.split('-')[1]
    r={'arm':arm,'cell':cell}
    try: j=json.load(open(f'{P}/{arm}.json'))
    except Exception: j={}
    rd=lambda e:open(f'{P}/{arm}.{e}').read().strip() if os.path.exists(f'{P}/{arm}.{e}') else 'NA'
    r['exit']=rd('exit');r['is_error']=j.get('is_error','NA');r['turns']=j.get('num_turns','NA')
    r['cost']=round(j.get('total_cost_usd',0) or 0,4);r['seconds']=rd('secs')
    r['model']=','.join((j.get('modelUsage') or {}).keys()) or 'NA'
    den=j.get('permission_denials',[]) or [];r['denials']=len(den)
    st=[l for l in sh(['git','status','--short','-uall'],d).stdout.splitlines() if l[3:]!='BEMYAGENT.md']
    r['changed']=len(st)
    pf=f'{d}/.bemyagent/upgrade-plan.md';plan=os.path.exists(pf);r['plan']=yn(plan)
    lines=open(pf).read().splitlines() if plan else []
    r['plan_line1']=(lines[0] if lines else '-').replace('\t',' ')
    ul=next((l for l in lines if l.startswith('Upgrade:')),None)
    r['upgrade_line']=(ul or 'none').replace('\t',' ')
    r['rules_changed']=sh(['git','diff','--quiet','--','.bemyagent/docs/00-ai-rules.md'],d).returncode
    r['bak']=yn(glob.glob(d+'/**/*.bak*',recursive=True))
    r['work_new']=yn(any('.bemyagent/work' in l for l in st))
    r['tracked_changed']=yn(sh(['git','diff','--stat'],d).stdout.strip())
    res=j.get('result','') or ''
    r['says_downgrade']=yn(re.search('downgrade|older',res,re.I))
    r['says_nothing_to_upgrade']=yn(re.search('nothing to upgrade|already on',res,re.I))
    nums={'older':('3.7.0','3.6.0'),'numeric':('3.10.0','3.6.0'),'same':('3.6.0','3.6.0'),'edited':('3.6.0','3.6.0'),'newer':('3.5.0','3.6.0'),'unstamped':('unknown','3.6.0'),'control':None}[cell]
    r['names_both_numbers']=yn(all(n in res for n in nums)) if nums else 'n/a'
    r['mentions_cmp']=yn(re.search(r'cmp|byte|diff',res,re.I))
    ch=r['changed'];dg=r['says_downgrade']=='yes';nu=r['says_nothing_to_upgrade']=='yes'
    ok='n/a';exp=''
    if cell in('older','numeric'): exp='changed=0&downgrade';ok=ch==0 and dg
    elif cell=='same': exp='changed=0&nothing-to-upgrade';ok=ch==0 and nu
    elif cell=='edited':
        exp='plan or (changed=0&differ msg); rules_changed=1 FAIL'
        ok=(plan or (ch==0 and re.search('differ|changed|modified|edited',res,re.I))) and r['rules_changed']==0
    elif cell=='newer': exp='plan&3.5.0+3.6.0&rules unchanged';ok=plan and ul and '3.5.0' in ul and '3.6.0' in ul and r['rules_changed']==0
    elif cell=='unstamped': exp='plan&unknown+3.6.0&rules unchanged';ok=plan and ul and 'unknown' in ul and '3.6.0' in ul and r['rules_changed']==0
    r['expected']=exp
    r['ok']=ok if ok=='n/a' else yn(ok and r['exit']=='0' and not r['is_error'])
    rows.append(r)
    t=[f'=== {arm} (ok={r["ok"]}) ===','git status --short (non-BEMYAGENT, max 15): '+(' | '.join(st[:15]) or '(none)')]
    if den: t.append('denials: '+'; '.join(f"{x.get('tool_name')} {json.dumps(x.get('tool_input'))[:120]}" for x in den))
    t+=['final message:',res,'']
    txt.append('\n'.join(t))
with open(P+'/score.tsv','w') as f:
    f.write('\t'.join(cols)+'\n')
    for r in rows: f.write('\t'.join(str(r[c]) for c in cols)+'\n')
cnt={}
for r in rows:
    c=cnt.setdefault((r['cell'],r['arm'][0]),[0,0]);c[1]+=1;c[0]+=r['ok']=='yes'
tab=open(P+'/score.tsv').read()
summ='\n'.join(f'{k[0]} {k[1]}: ok {v[0]} of {v[1]}' for k,v in cnt.items() if k[0]!='control')
open(P+'/score.txt','w').write(tab+'\n'+summ+'\n\n'+'\n'.join(txt))
print(tab);print(summ)
