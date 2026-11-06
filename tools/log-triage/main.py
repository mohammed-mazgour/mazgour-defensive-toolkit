#!/usr/bin/env python3
"""LogTriage: summarize SSH/Linux authentication events in a local text log."""
import argparse,collections,json,re
from pathlib import Path

EVENTS=[("failed",re.compile(r"Failed password for (?:invalid user )?(\S+) from ([\dA-Fa-f:.]+)")),
        ("accepted",re.compile(r"Accepted (?:password|publickey) for (\S+) from ([\dA-Fa-f:.]+)")),
        ("invalid_user",re.compile(r"Invalid user (\S+) from ([\dA-Fa-f:.]+)"))]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("log",type=Path);p.add_argument("--json",dest="out",type=Path);a=p.parse_args()
 try: lines=a.log.read_text(encoding="utf-8",errors="replace").splitlines()
 except OSError as e:p.error(str(e))
 counts=collections.Counter();users=collections.Counter();sources=collections.Counter();events=[]
 for n,line in enumerate(lines,1):
  for kind,rx in EVENTS:
   m=rx.search(line)
   if m:
    user,ip=m.groups();counts[kind]+=1;users[user]+=1;sources[ip]+=1
    if len(events)<10000:events.append({"line":n,"event":kind,"user":user,"source":ip})
    break
 report={"tool":"LogTriage","lines":len(lines),"event_counts":dict(counts),"top_users":users.most_common(20),"top_sources":sources.most_common(20),"events_truncated":sum(counts.values())>len(events),"events":events}
 print(json.dumps(report,indent=2));
 if a.out:a.out.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
 return 0
if __name__=="__main__":raise SystemExit(main())
