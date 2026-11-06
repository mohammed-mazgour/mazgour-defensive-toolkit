#!/usr/bin/env python3
"""WebRiskLint: flag selected source patterns for human review; does not execute code."""
import argparse,json,re
from pathlib import Path

RULES=[("inline-script","<script\\b(?![^>]*\\bsrc=)[^>]*>","Inline script; consider a restrictive CSP and external script."),
       ("inline-handler",r"\bon[a-z]+\s*=\s*['\"]","Inline event handler; consider addEventListener and CSP."),
       ("unsafe-innerhtml",r"\.innerHTML\s*=","Review whether untrusted content can reach innerHTML."),
       ("document-write",r"\bdocument\.write\s*\(","document.write can introduce unsafe HTML injection."),
       ("target-blank-noopener",r"<a\b(?![^>]*\brel\s*=)[^>]*\btarget\s*=\s*['\"]_blank['\"]","target=_blank lacks an explicit rel attribute."),
       ("http-resource",r"(?:src|href)\s*=\s*['\"]http://","Resource uses plain HTTP; check mixed-content and transport policy.")]
EXT={".html",".htm",".js",".jsx",".ts",".tsx"}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("paths",nargs="+",type=Path);p.add_argument("--json",dest="out",type=Path);a=p.parse_args();findings=[]
 for path in a.paths:
  files=[path] if path.is_file() else path.rglob("*") if path.is_dir() else []
  for f in files:
   if not f.is_file() or f.suffix.lower() not in EXT:continue
   try:lines=f.read_text(encoding="utf-8",errors="replace").splitlines()
   except OSError:continue
   for line_no,line in enumerate(lines,1):
    for rule,pattern,message in RULES:
     if re.search(pattern,line,re.I):findings.append({"file":str(f),"line":line_no,"rule":rule,"finding":message})
 report={"tool":"WebRiskLint","findings":findings,"note":"Pattern checks can produce false positives and miss real issues. Review data flow and framework context manually."}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 1 if findings else 0
if __name__=="__main__":raise SystemExit(main())
