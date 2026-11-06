# PermissionLens

Inspects local file mode bits without changing permissions. On POSIX systems it flags world-writable files and selected script files marked executable. Windows ACLs are not evaluated by this first release.

```powershell
python main.py C:\path\to\folder --json permissions.json
```

An executable script is informational, not automatically unsafe. Review ownership, purpose, and intended access before changing permissions.
