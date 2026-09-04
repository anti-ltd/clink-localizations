#!/usr/bin/env bash
set -euo pipefail

# Run on a Mac after editing Catalog/Localizable.xcstrings.
root="$(cd "$(dirname "$0")/.." && pwd)"
staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT
python3 "$root/tools/validate-catalog.py"
xcrun xcstringstool compile "$root/Catalog/Localizable.xcstrings" --output-directory "$staging" --serialization-format binary
find "$root/Localizations" -mindepth 1 -maxdepth 1 -type d -name '*.lproj' -exec rm -rf {} +
while IFS= read -r locale; do
  [ -z "$locale" ] && continue
  test -d "$staging/$locale.lproj" || { echo "Missing compiled locale: $locale" >&2; exit 1; }
  cp -R "$staging/$locale.lproj" "$root/Localizations/"
done < "$root/release-locales.txt"
shasum -a 256 "$root/Catalog/Localizable.xcstrings" | awk '{print $1}' > "$root/Localizations/.catalog-sha256"
for pack in "$root"/Localizations/*.lproj; do
  python3 "$root/tools/validate-localization.py" "$pack"
done
