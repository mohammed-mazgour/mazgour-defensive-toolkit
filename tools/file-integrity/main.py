#!/usr/bin/env python3
"""FileIntegrity: create or verify a local SHA-256 file manifest."""
import argparse, hashlib, json
from pathlib import Path

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()
def collect(root):
    out={}
    for p in root.rglob("*"):
        if p.is_file() and not p.is_symlink():
            try: out[p.relative_to(root).as_posix()]=digest(p)
            except OSError: pass
    return out
def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest="action",required=True)
    for name in ("create","verify"):
        q=sub.add_parser(name); q.add_argument("root",type=Path); q.add_argument("manifest",type=Path)
    a=p.parse_args(); root=a.root.resolve()
    if not root.is_dir(): p.error("root must be an existing directory")
    if a.action=="create":
        entries=collect(root); data={"format":1,"algorithm":"sha256","root_label":root.name,"files":entries}
        a.manifest.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
        print(f"Created manifest for {len(entries)} files: {a.manifest}"); return 0
    try: old=json.loads(a.manifest.read_text(encoding="utf-8"))["files"]
    except (OSError,ValueError,KeyError) as e: p.error(f"cannot read valid manifest: {e}")
    now=collect(root); missing=sorted(set(old)-set(now)); added=sorted(set(now)-set(old))
    changed=sorted(k for k in set(old)&set(now) if old[k]!=now[k])
    print(json.dumps({"unchanged":len(set(now)&set(old))-len(changed),"changed":changed,"missing":missing,"added":added},indent=2))
    return 1 if missing or added or changed else 0
if __name__=="__main__": raise SystemExit(main())
