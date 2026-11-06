#!/usr/bin/env python3
"""PermissionLens: inspect local filesystem mode bits; no permissions are changed."""
import argparse,json,os,stat
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("root",type=Path);p.add_argument("--json",dest="out",type=Path);a=p.parse_args();root=a.root.resolve()
 if not root.is_dir():p.error("root must be an existing directory")
 findings=[];count=0
 for f in root.rglob("*"):
  if not f.is_file() or f.is_symlink():continue
  count+=1
  try:mode=stat.S_IMODE(f.stat().st_mode)
  except OSError:continue
  if os.name!="nt":
   if mode & stat.S_IWOTH: findings.append({"path":f.relative_to(root).as_posix(),"mode":oct(mode),"issue":"world-writable"})
   elif mode & stat.S_IROTH and mode & stat.S_IWGRP: findings.append({"path":f.relative_to(root).as_posix(),"mode":oct(mode),"issue":"group-writable and world-readable"})
  if mode & stat.S_IXUSR and f.suffix.lower() in (".py",".sh",".bat",".cmd",".ps1"): findings.append({"path":f.relative_to(root).as_posix(),"mode":oct(mode),"issue":"executable-script-review"})
 report={"tool":"PermissionLens","files_seen":count,"platform":os.name,"findings":findings,"note":"Windows ACLs are not evaluated; POSIX mode-bit results are indicators for review."}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 1 if any(x["issue"]=="world-writable" for x in findings) else 0
if __name__=="__main__":raise SystemExit(main())
