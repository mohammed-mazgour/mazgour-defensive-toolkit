# SecretSentry

Finds likely secrets in a local source directory. It reports rule, relative path, and line number, but never includes matched text in the output. It skips common generated folders and files larger than 1 MB.

```powershell
python main.py C:\path\to\your\project --json report.json
```

Exit code `1` means one or more heuristic matches were found; `0` means none were found. A match is not proof of a valid credential. Review privately, remove real credentials from source history where appropriate, and rotate exposed credentials. This tool does not modify files or contact a service.
