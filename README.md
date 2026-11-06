# Mazgour Defensive Toolkit

Ten independent, offline-first Python tools for reviewing files and configurations you own or are authorized to assess. They are designed for learning and defensive maintenance: no exploit code, credential harvesting, brute forcing, stealth, persistence, or remote scanning.

## Requirements

- Python 3.10 or newer
- Standard library only; no package installation required
- Windows, macOS, and Linux (some filesystem permission details are platform-specific)

## Tools

| Tool | Purpose |
|---|---|
| [SecretSentry](tools/secret-sentry/README.md) | Find likely hard-coded credentials in a local source tree without printing secret values |
| [FileIntegrity](tools/file-integrity/README.md) | Create and verify SHA-256 manifests for files you select |
| [ConfigGuardian](tools/config-guardian/README.md) | Review common risky settings in local SSH, Nginx, Dockerfile, and Compose configs |
| [LogTriage](tools/log-triage/README.md) | Summarize authentication events from a local log export |
| [HeaderReview](tools/header-review/README.md) | Review saved HTTP response headers offline against a practical baseline |
| [SBOMScout](tools/sbom-scout/README.md) | Inventory dependencies and flag unpinned Python/npm entries from local manifests |
| [BackupVerifier](tools/backup-verifier/README.md) | Compare a source tree with its backup by relative path and SHA-256 |
| [PermissionLens](tools/permission-lens/README.md) | Identify broad POSIX permissions and inspect executable files |
| [PrivacyMap](tools/privacy-map/README.md) | Inventory filenames and flag names that may contain personal data |
| [WebRiskLint](tools/web-risk-lint/README.md) | Flag selected risky patterns in local HTML/JS source for human review |

Each tool has its own directory, detailed guide, examples, and a runnable `main.py`. Start with the individual README before using it. Reports are written only when you provide an output path; tools do not transmit data.

## Responsible use

Run these tools only on your own files and systems, or where you have permission. Findings are heuristics, not proof of a vulnerability or a substitute for a professional review. Check that reports do not contain information you do not intend to share before publishing them.

## Project status

This is an educational first release. Review issues and false positives, then improve the rules with documented examples. No claim is made that these tools have undergone independent security review.
