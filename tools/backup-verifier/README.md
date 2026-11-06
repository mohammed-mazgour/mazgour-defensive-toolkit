# BackupVerifier

Compares source and backup trees by relative path and SHA-256. Both directories must already exist and should be separate; do not put the backup inside the source tree.

```powershell
python main.py C:\data\source C:\data\backup --json backup-check.json
```

Reports missing, changed, and extra files. It never deletes or repairs files. A matching result verifies the compared files at that moment; it does not prove a backup can be restored as a working system. Periodically perform a controlled restore drill.
