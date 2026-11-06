# FileIntegrity

Creates and verifies SHA-256 manifests for ordinary files. It ignores symbolic links and unreadable files. Keep the manifest outside the tree being measured so the manifest does not become part of its own inventory.

```powershell
python main.py create C:\important\folder C:\reports\folder-baseline.json
python main.py verify C:\important\folder C:\reports\folder-baseline.json
```

Exit code `1` indicates added, missing, or changed files. Store a trusted baseline separately: a manifest kept beside files an attacker can alter is not an independent trust anchor. The tool never changes the inspected folder.
