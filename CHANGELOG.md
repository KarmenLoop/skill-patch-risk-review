# Changelog

## 0.2.0 - 2026-10-20

- Parse real Git paths containing spaces or quoted UTF-8 names and reject incomplete hunks.
- Accept JSON from standard input with `--input -` and report the installed version with `--version`.
- Report deeply nested JSON as an input error without a traceback.
- Exercise pipeline input, output preservation, installation, and examples in the test suite.

## 0.1.0 — 2026-10-19

- Initial release of Patch Risk Review.
- Added the local helper, examples, regression tests, and non-overwriting installer.
- Documented input contracts, provenance, and unverified integrations.
