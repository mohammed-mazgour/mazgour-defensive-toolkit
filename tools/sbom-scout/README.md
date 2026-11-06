# SBOMScout

Builds an offline inventory from `requirements.txt`, `package-lock.json`, or `npm-shrinkwrap.json`. It reports dependency names and declared versions and highlights Python entries that are not pinned with `==`/`===`.

```powershell
python main.py C:\path\to\requirements.txt --json dependencies.json
python main.py C:\path\to\package-lock.json --json dependencies.json
```

It does not query registries, identify known vulnerabilities, or establish that a package is safe. Use an authoritative, current advisory source for vulnerability review.
