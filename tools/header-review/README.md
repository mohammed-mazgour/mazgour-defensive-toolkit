# HeaderReview

Reviews a text file containing copied HTTP response headers. It makes no HTTP requests, so use it with a response from a site you own or are authorized to assess.

Example `headers.txt`:

```text
Content-Type: text/html; charset=utf-8
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

```powershell
python main.py headers.txt --json header-review.json
```

Policies such as CSP depend on the application. Treat results as a review checklist, not a one-click configuration recipe.
