"""21.1 B1 check: certificate.py's per-call reader on 20.11's six REAL transcripts (read-only), numbers only.
Protocol arms (q94-q96) and bare arms (q97-q99) must all come out clean; a copy of q94's transcript with an
instruction file from OUTSIDE the arm appended (the verifier's p2_instr-style stub) must NOT."""
import json, os, pathlib, shutil, sys, tempfile
OLD = str(pathlib.Path(os.environ["BMA_SCRATCH"]) / "r2011")      # 20.11's round folder: BMA_SCRATCH must point at the scratch directory that round ran in
os.environ["R211_ROOT"] = OLD
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import certificate as C
KEYS = ("transcripts", "instruction_records", "override_header", "tool_calls_naming_apparatus", "tool_calls_dotdot",
        "attachments_naming_foreign_paths", "parent_repo_tool_calls", "clean", "first_user_equals_prompt_t1")
bad = []
for arm in ("q94", "q95", "q96", "q97", "q98", "q99"):
    sid = json.load(open(f"{OLD}/{arm}.json"))["session_id"]
    r = C.call_row(arm, "t1", f"{OLD}/{arm}", sid)
    r["outside_arm_dir"] = len(r["outside_arm_dir"])
    print(arm, "protocol" if arm in ("q94", "q95", "q96") else "bare    ", {k: r.get(k) for k in KEYS}, "outside_arm_dir", r["outside_arm_dir"])
    if not r["clean"]: bad.append(arm)
print("unclean among the six:", bad)
# p2_instr-style stub: q94's transcript + an instruction attachment from outside the arm, in a scratch config dir
tmp = pathlib.Path(tempfile.mkdtemp(prefix="cert2011_", dir=os.environ["BMA_SCRATCH"]))
sid = json.load(open(f"{OLD}/q94.json"))["session_id"]
src = next((pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude") / "projects").glob(f"*/{sid}.jsonl"))
dst = tmp / "projects" / src.parent.name; dst.mkdir(parents=True)
shutil.copy(src, dst / src.name)
with open(dst / src.name, "a") as f:
    f.write(json.dumps({"type": "attachment", "attachment": {"type": "instructions", "files": [
        {"type": "project", "path": str(pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4])) + "/AGENTS.md", "content": "x"}]}}) + "\n")
C.CFG = tmp / "projects"
r = C.call_row("q94", "t1", f"{OLD}/q94", sid)
print("stub q94 + outside instruction file:", {"clean": r["clean"], "outside_arm_dir": len(r["outside_arm_dir"]), "instruction_records": r["instruction_records"]})
shutil.rmtree(tmp)
sys.exit(1 if bad or r["clean"] else 0)
