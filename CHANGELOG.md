# Changelog

## 1.0.1

- Fix `media_csp` template tag mangling absolute URLs (e.g. CDN URLs) by using
  `Media.absolute_path()` instead of `static()`.

## 1.0.0

- Add support for Django 6.0+ native CSP alongside existing django-csp support. The nonce
  source is detected automatically: Django's `ContentSecurityPolicyMiddleware` and context
  processor, or django-csp's middleware, both work without any configuration change.
