# Security Ledger

| Check ID | Result | Files/sections covered | Last checked (date) | Open issues |
|---|---|---|---|---|
| SC-01 | Pass | `blog/models.py` (`PostQuerySet`), `blog/views.py` — ORM only, no raw SQL | 2026-10-17 | 0 |
| SC-02 | Pass | `templates/base.html`, `blog/templates/blog/*.html` — autoescaping on, no `|safe`; covered by `test_post_text_is_escaped` | 2026-10-17 | 0 |
| SC-03 | Pass | `mysite/settings.py` `MIDDLEWARE` (`CsrfViewMiddleware`), `CSRF_COOKIE_SECURE`; only POST routes are Django admin | 2026-10-17 | 0 |
| SC-05 | Pass | `blog/views.py` `PostDetailView.get_queryset` — drafts/scheduled posts return 404; covered by tests | 2026-10-17 | 0 |
| SC-06 | Fail | `mysite/urls.py` route `admin/` login has no rate limiting | 2026-10-17 | 1 (Medium) |
| SC-08 | Pass (resolved) | `mysite/settings.py` `SECRET_KEY` read from env; old key remains in git history and must be treated as leaked | 2026-10-17 | 0 |
| SC-09 | Pass | Django default PBKDF2 hasher, `AUTH_PASSWORD_VALIDATORS` | 2026-10-17 | 0 |
| SC-10 | Fail | `admin/` login has no MFA | 2026-10-17 | 1 (Medium) |
| SC-13 | Pass | `blog/admin.py` — Django admin enforces `is_staff` and model permissions server-side | 2026-10-17 | 0 |
| SC-18 | Pass (resolved) | `db.sqlite3` with superuser removed from tracking and ignored; `.env.example` has placeholders only. Admin password must still be changed (see README/notes) | 2026-10-17 | 0 |
| SC-20 | Pass (resolved) | `requirements.txt` — Django 5.0.6 → 5.2.18, python-dotenv 1.2.2; `pip-audit` clean | 2026-10-17 | 0 |
