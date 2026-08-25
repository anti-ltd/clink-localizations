# Verify this Clink localization repository

Read `README.md`, `PROMPT.md`, the validators, and every file in
`Localizations/`. Audit without editing unless asked to fix a finding.

Run `python3 tools/validate-localization.py Localizations/<locale>.lproj` for
every pack. Confirm every locale has an editorial review, all source-catalog
keys are represented, placeholders and plural rules are preserved, and the
compiled resources came from `Catalog/Localizable.xcstrings`. Confirm release
tooling is unchanged and no manifest has been fabricated. Do not publish.
