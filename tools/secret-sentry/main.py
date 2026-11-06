#!/usr/bin/env python3
"""SecretSentry: local heuristic credential scanner. Never prints matched values."""
import argparse, json, re
from pathlib import Path

RULES = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github-token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "slack-token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "generic-assignment": re.compile(r"(?i)\b(api[_-]?key|secret|password|token)\b\s*[:=]\s*['\"]?([^\s'\";,]{8,})"),
}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}
MAX_BYTES = 1_000_000

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", type=Path, help="Local directory to inspect")
    p.add_argument("--json", dest="output", type=Path, help="Optional JSON report path")
    args = p.parse_args()
    root = args.root.resolve()
    if not root.is_dir(): p.error("root must be an existing directory")
    findings, scanned, skipped = [], 0, 0
    for f in root.rglob("*"):
        if not f.is_file() or any(part in SKIP_DIRS for part in f.relative_to(root).parts): continue
        try:
            if f.stat().st_size > MAX_BYTES: skipped += 1; continue
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError: skipped += 1; continue
        scanned += 1
        for n, line in enumerate(text.splitlines(), 1):
            for kind, rx in RULES.items():
                if rx.search(line): findings.append({"file": f.relative_to(root).as_posix(), "line": n, "rule": kind})
    report = {"tool":"SecretSentry", "scanned_files":scanned, "skipped_files":skipped, "findings":findings,
              "note":"Heuristic only. Matched values are intentionally omitted; inspect locally and rotate any real exposed credential."}
    print(json.dumps(report, indent=2))
    if args.output: args.output.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    return 1 if findings else 0
if __name__ == "__main__": raise SystemExit(main())
