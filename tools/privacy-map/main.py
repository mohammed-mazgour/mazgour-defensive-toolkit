#!/usr/bin/env python3
"""PrivacyMap: inventory filenames and flag path names that may expose personal data."""
import argparse,json,re
from pathlib import Path

PATTERNS={"email-like":re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),"phone-like":re.compile(r"(?<!\w)(?:\+?\d[\d .()/-]{7,}\d)(?!\w)"),"identity-keyword":re.compile(r"(?i)(passport|national.?id|cni|social.?security|birth.?certificate)")}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("root",type=Path);p.add_argument("--json",dest="out",type=Path);a=p.parse_args();root=a.root.resolve()
 if not root.is_dir():p.error("root must be an existing directory")
 files=[];flags=[]
 for f in root.rglob("*"):
  if not f.is_file():continue
  rel=f.relative_to(root).as_posix()
  try:size=f.stat().st_size
  except OSError:continue
  files.append({"path":rel,"bytes":size,"extension":f.suffix.lower()})
  for label,rx in PATTERNS.items():
   if rx.search(rel):flags.append({"path":rel,"reason":label})
 report={"tool":"PrivacyMap","file_count":len(files),"total_bytes":sum(x["bytes"] for x in files),"name_flags":flags,"inventory":files,"note":"Only names and file sizes are inspected; file contents are not read. Review before sharing the report."}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 0
if __name__=="__main__":raise SystemExit(main())
