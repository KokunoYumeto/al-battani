"""S16 - replay S01's own read-only technical audit (scripts/audit_v003_readonly.py) on the complete S01 v003
package. The repository's S01 folder holds 563 of the package's files: it leaves out the package's QA renders and
the recovered evidence of the interrupted reread (history/interrupted_reread, qa/), which that audit needs. The
complete package is the zip _intake/AB01_S01_v003.zip (local, not in the repository). This script
  1. extracts the zip into a temporary folder and compares every file that the repository also holds, byte for byte;
  2. places the master scan beside the package under its packet name, where the audit looks for it;
  3. runs the audit in Python's UTF-8 mode (it reads its JSON with the platform's default encoding and was written
     on a UTF-8 platform) and saves its JSON as s01_technical_audit_replay.json.
Nothing in the repository is changed. python replay_s01_audit.py"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

AB = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ZIP = AB / "_intake" / "AB01_S01_v003.zip"
MASTER = Path(r"F:\user\Documents\CLAUDE PLEASE DONT DELETE WINDOWS 32\grind\nallino_pars123.pdf")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    tmp = Path(tempfile.mkdtemp(prefix="s16_s01audit_"))
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(tmp)
    pkg = tmp / "AB01_S01_v003"
    repo = subprocess.run(["git", "-C", str(AB), "ls-files", "--", "S01"], capture_output=True, text=True,
                          encoding="utf-8").stdout.split("\n")
    same, differ, only_repo = 0, [], []
    for f in filter(None, repo):
        q = pkg / Path(f).relative_to("S01")
        if not q.exists():
            only_repo.append(f)
        elif sha(q) == sha(AB / f):
            same += 1
        else:
            differ.append(f)
    n_pkg = sum(1 for p in pkg.rglob("*") if p.is_file())
    shutil.copy2(MASTER, tmp / "30_NALLINO_PARS_I_II_III_MASTER_1162P.pdf")
    r = subprocess.run([sys.executable, "scripts/audit_v003_readonly.py"], cwd=pkg, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=3600,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"})
    try:
        rep = json.loads(r.stdout)
    except ValueError:
        rep = {"error": "no JSON on stdout", "stdout_tail": r.stdout[-2000:], "stderr_tail": r.stderr[-2000:]}
    rep["_replay"] = {"exit_code": r.returncode, "package": str(ZIP.relative_to(AB)), "package_sha256": sha(ZIP),
                      "package_files": n_pkg, "repository_files": len([f for f in repo if f]),
                      "repository_files_identical_in_package": same, "repository_files_differing": differ,
                      "repository_files_not_in_package": only_repo, "master": str(MASTER),
                      "python": "UTF-8 mode (PYTHONUTF8=1)"}
    (OUT / "s01_technical_audit_replay.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                                                         encoding="utf-8", newline="\n")
    checks = rep.get("checks", [])
    fails = [c for c in checks if not c.get("pass")]
    print(f"package {n_pkg} files; repository {len([f for f in repo if f])} files, {same} identical in the package, "
          f"{len(differ)} differ, {len(only_repo)} not in the package")
    print(f"audit exit {r.returncode}; {len(checks)} checks, {len(fails)} fail")
    for c in fails:
        print("  FAIL", c.get("check"), str(c.get("detail"))[:300])
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
