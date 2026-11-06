# ConfigGuardian

Checks local `sshd_config`, Nginx `.conf`, Dockerfiles, and Docker Compose YAML for a small set of common settings that deserve review.

```powershell
python main.py C:\path\to\configs --json config-review.json
```

The checks are deliberately conservative and may flag comments or context-dependent settings. Confirm the active configuration and deployment needs before making any change. No configuration is edited, and no service is contacted.
