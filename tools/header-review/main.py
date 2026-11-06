#!/usr/bin/env python3
"""HeaderReview: review headers copied to a local text file; makes no network requests."""
import argparse,json
from pathlib import Path

CHECKS={"strict-transport-security":("Strict-Transport-Security",True),"content-security-policy":("Content-Security-Policy",True),"x-content-type-options":("X-Content-Type-Options",True),"referrer-policy":("Referrer-Policy",True),"permissions-policy":("Permissions-Policy",False),"x-frame-options":("X-Frame-Options",False)}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("headers",type=Path,help="Text export with one Name: value per line");p.add_argument("--json",dest="out",type=Path);a=p.parse_args()
 try: raw=a.headers.read_text(encoding="utf-8",errors="replace").splitlines()
 except OSError as e:p.error(str(e))
 headers={}
 for line in raw:
  if ":" in line:
   k,v=line.split(":",1);headers[k.strip().lower()]=v.strip()
 findings=[]
 for key,(label,required) in CHECKS.items():
  if key not in headers: findings.append({"header":label,"status":"missing","severity":"recommended" if required else "consider"})
 if "x-content-type-options" in headers and headers["x-content-type-options"].lower()!="nosniff":findings.append({"header":"X-Content-Type-Options","status":"unexpected-value","value":headers["x-content-type-options"]})
 if "strict-transport-security" in headers and "max-age=" not in headers["strict-transport-security"].lower():findings.append({"header":"Strict-Transport-Security","status":"review-value","value":headers["strict-transport-security"]})
 report={"tool":"HeaderReview","headers_found":sorted(headers),"findings":findings,"note":"Offline checklist only. HSTS and CSP values depend on deployment; validate carefully before applying."}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 1 if findings else 0
if __name__=="__main__":raise SystemExit(main())
