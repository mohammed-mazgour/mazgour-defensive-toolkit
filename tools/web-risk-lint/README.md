# WebRiskLint

Flags selected HTML and JavaScript patterns for a developer to review: inline scripts and handlers, `innerHTML`, `document.write`, links opened in a new tab without `rel`, and plain-HTTP resource URLs.

```powershell
python main.py C:\path\to\web-project --json web-review.json
```

This is pattern matching, not a vulnerability scanner. It may miss issues or flag safe code. Review data flow, framework behavior, and browser policy. It does not execute or modify source code and makes no network requests.
