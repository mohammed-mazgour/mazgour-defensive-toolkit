#!/usr/bin/env python3
"""ConfigGuardian: conservative static checks for common local config files."""
import argparse,json,re
from pathlib import Path

RULES=[
 ("ssh-root-login","sshd_config",r"(?im)^\s*PermitRootLogin\s+yes\b","SSH permits direct root login"),
 ("ssh-password-auth","sshd_config",r"(?im)^\s*PasswordAuthentication\s+yes\b","SSH password authentication is enabled"),
 ("nginx-plain-http","nginx",r"(?i)listen\s+80\s*;","Nginx listens on plain HTTP; verify TLS redirect policy"),
 ("nginx-server-tokens","nginx",r"(?im)^\s*server_tokens\s+on\s*;","Nginx version tokens are enabled"),
 ("docker-root-user","Dockerfile",r"(?im)^\s*USER\s+root\s*$","Container explicitly runs as root"),
 ("compose-public-bind","compose",r"(?m)['\"]?0\.0\.0\.0:\d+:[^\n]+","Compose port appears bound on all interfaces"),
 ("compose-privileged","compose",r"(?im)^\s*privileged\s*:\s*true\b","Compose service is privileged"),
]
def category(path):
 n=path.name.lower()
 if n=="sshd_config" or "ssh" in n: return "sshd_config"
 if n.startswith("dockerfile"): return "Dockerfile"
 if n.endswith((".yml",".yaml")) and ("compose" in n or "docker" in n): return "compose"
 if "nginx" in n or n.endswith(".conf"): return "nginx"
 return ""
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("paths",nargs="+",type=Path);p.add_argument("--json",dest="out",type=Path);a=p.parse_args()
 findings=[]
 for input_path in a.paths:
  files=[input_path] if input_path.is_file() else input_path.rglob("*") if input_path.is_dir() else []
  for f in files:
   if not f.is_file():continue
   cat=category(f)
   if not cat:continue
   try: lines=f.read_text(encoding="utf-8",errors="replace").splitlines()
   except OSError:continue
   for rule,target,rx,msg in RULES:
    if target!=cat:continue
    for i,line in enumerate(lines,1):
     if re.search(rx,line): findings.append({"file":str(f),"line":i,"rule":rule,"finding":msg})
 report={"tool":"ConfigGuardian","findings":findings,"note":"Review context before changing settings; disabled or commented directives may need manual interpretation."}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 1 if findings else 0
if __name__=="__main__":raise SystemExit(main())
