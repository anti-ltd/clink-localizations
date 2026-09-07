#!/usr/bin/env bash
set -euo pipefail

# Run on a Mac after editing Catalog/Localizable.xcstrings.
root="$(cd "$(dirname "$0")/.." && pwd)"
staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT
python3 "$root/tools/validate-catalog.py"
languages=()
while IFS= read -r locale; do
  [ -z "$locale" ] && continue
  languages+=(--language "$locale")
done < "$root/release-locales.txt"
xcrun xcstringstool compile "$root/Catalog/Localizable.xcstrings" --output-directory "$staging" --serialization-format binary "${languages[@]}"
# Verify every staged pack before replacing any existing release resource.
while IFS= read -r locale; do
  [ -z "$locale" ] && continue
  test -d "$staging/$locale.lproj" || { echo "Missing compiled locale: $locale" >&2; exit 1; }
  python3 "$root/tools/validate-localization.py" "$staging/$locale.lproj"
done < "$root/release-locales.txt"
mkdir -p "$root/Localizations"
find "$root/Localizations" -mindepth 1 -maxdepth 1 -type d -name '*.lproj' ! -name '._*' -exec rm -rf {} +
while IFS= read -r locale; do
  [ -z "$locale" ] && continue
  cp -R "$staging/$locale.lproj" "$root/Localizations/"
done < "$root/release-locales.txt"
shasum -a 256 "$root/Catalog/Localizable.xcstrings" | awk '{print $1}' > "$root/Localizations/.catalog-sha256"
python3 "$root/tools/validate-release.py"
