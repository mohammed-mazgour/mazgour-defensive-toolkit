#!/usr/bin/env python3
"""BackupVerifier: compare local source and backup trees without modifying either."""
import argparse,hashlib,json
from pathlib import Path

def snapshot(root):
 result={}
 for f in root.rglob("*"):
  if f.is_file() and not f.is_symlink():
   try:
    h=hashlib.sha256()
    with f.open("rb") as stream:
     for chunk in iter(lambda:stream.read(1024*1024),b""):h.update(chunk)
    result[f.relative_to(root).as_posix()]=h.hexdigest()
   except OSError:pass
 return result
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("source",type=Path);p.add_argument("backup",type=Path);p.add_argument("--json",dest="out",type=Path);a=p.parse_args()
 s,b=a.source.resolve(),a.backup.resolve()
 if not s.is_dir() or not b.is_dir():p.error("source and backup must be existing directories")
 src,dst=snapshot(s),snapshot(b);missing=sorted(set(src)-set(dst));extra=sorted(set(dst)-set(src));changed=sorted(k for k in set(src)&set(dst) if src[k]!=dst[k])
 report={"tool":"BackupVerifier","source_files":len(src),"backup_files":len(dst),"missing_from_backup":missing,"content_mismatch":changed,"extra_in_backup":extra,"status":"match" if not missing and not changed else "review"}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 1 if missing or changed else 0
if __name__=="__main__":raise SystemExit(main())
