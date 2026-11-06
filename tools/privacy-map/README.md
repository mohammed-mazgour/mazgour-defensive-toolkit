# PrivacyMap

Creates a local file inventory with relative names, extensions, and sizes. It scans filenames only for email-like strings, phone-like strings, and identity-document keywords; it never opens file contents.

```powershell
python main.py C:\path\to\folder --json privacy-inventory.json
```

The inventory may itself reveal sensitive names and folder structure. Store it carefully and review it before sharing. Flags are approximate and may include false positives.
