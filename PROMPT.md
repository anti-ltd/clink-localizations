# Clink localization-pack authoring

Read `README.md`, `Catalog/Localizable.xcstrings`, and the validation tools
before editing. Translate a complete locale only; do not fabricate or omit
keys, alter placeholders, or use machine translation without native-speaker
editorial review. Preserve Clink, URLs, Markdown, and official iOS setting
names. Run `./tools/export-localizations.sh`, then validate every `.lproj`.
Do not edit generated release output, commit, tag, or publish unless asked.
