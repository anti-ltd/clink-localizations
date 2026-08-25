#!/usr/bin/env bash
set -euo pipefail

# Run on a Mac after editing Catalog/Localizable.xcstrings.
root="$(cd "$(dirname "$0")/.." && pwd)"
staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT
xcrun xcstringstool compile "$root/Catalog/Localizable.xcstrings" --output-directory "$staging" --serialization-format binary
find "$root/Localizations" -mindepth 1 -maxdepth 1 -type d -name '*.lproj' -exec rm -rf {} +
cp -R "$staging"/. "$root/Localizations/"
for pack in "$root"/Localizations/*.lproj; do
  python3 "$root/tools/validate-localization.py" "$pack"
done
