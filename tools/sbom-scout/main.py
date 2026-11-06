#!/usr/bin/env python3
"""SBOMScout: offline dependency inventory for requirements.txt and npm lockfiles."""
import argparse,json,re
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("manifest",type=Path);p.add_argument("--json",dest="out",type=Path);a=p.parse_args()
 f=a.manifest
 try: text=f.read_text(encoding="utf-8",errors="replace")
 except OSError as e:p.error(str(e))
 deps=[]
 if f.name=="package-lock.json" or f.name=="npm-shrinkwrap.json":
  try:
   obj=json.loads(text); packages=obj.get("packages",{})
   for name,item in packages.items():
    if name and "node_modules/" in name:deps.append({"name":name.split("node_modules/")[-1],"version":item.get("version","unknown"),"pinned":bool(item.get("version"))})
  except ValueError:p.error("invalid npm lockfile JSON")
 else:
  for line in text.splitlines():
   s=line.strip()
   if not s or s.startswith(("#","-","--")):continue
   m=re.match(r"^([A-Za-z0-9_.-]+)\s*(==|===|~=|>=|<=|!=|>|<)?\s*([^;\s]+)?",s)
   if m:deps.append({"name":m.group(1),"operator":m.group(2) or "","version":m.group(3) or "unspecified","pinned":m.group(2) in ("==","===")})
 report={"tool":"SBOMScout","manifest":f.name,"dependency_count":len(deps),"unpinned":[d["name"] for d in deps if not d["pinned"]],"dependencies":deps,"note":"Inventory only. No registry lookup or vulnerability verdict is performed."}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 0
if __name__=="__main__":raise SystemExit(main())
