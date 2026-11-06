# LogTriage

Summarizes common SSH authentication success, failure, and invalid-user lines from a local Linux authentication log export.

```powershell
python main.py C:\reports\auth.log --json auth-summary.json
```

It reports the top usernames and source addresses present in the file. Logs may contain personal or operational information; keep input and reports private. This tool only reads a text file and does not block addresses, connect to hosts, or infer attribution.
