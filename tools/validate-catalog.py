#!/usr/bin/env python3
"""Validate that every released locale is complete and format-safe."""
from __future__ import annotations

import collections
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "Catalog" / "Localizable.xcstrings"
RELEASE_LOCALES = ROOT / "release-locales.txt"
FORMAT = re.compile(
    r"(?<![0-9])%(?:\d+\$)?(?:\{(?:public|private)\})?"
    r"[-+#0]*(?:\d+|\*)?(?:\.\d+|\.\*)?"
    r"(?:@|(?:hh|h|ll|l|q|z|t|j)?[diuoxXfFeEgGaAcCsSp])"
)


def signature(value: str) -> collections.Counter[str]:
    value = value.replace("%%", "")
    return collections.Counter(re.sub(r"^%\d+\$", "%", token) for token in FORMAT.findall(value))


def units(localization: dict) -> list[dict]:
    result = []
    if "stringUnit" in localization:
        result.append(localization["stringUnit"])
    for variation in localization.get("variations", {}).values():
        result.extend(form.get("stringUnit", {}) for form in variation.values())
    return result


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if catalog.get("sourceLanguage") != "en":
        raise SystemExit("ERROR: sourceLanguage must be en.")
    locales = [line.strip() for line in RELEASE_LOCALES.read_text().splitlines() if line.strip()]
    if not locales or locales[0] != "en" or len(locales) != len(set(locales)):
        raise SystemExit("ERROR: release-locales.txt must contain unique locales with en first.")

    errors = []
    for key, entry in catalog.get("strings", {}).items():
        if entry.get("shouldTranslate") is False:
            continue
        source_signature = signature(key)
        for locale in locales[1:]:
            localization = entry.get("localizations", {}).get(locale)
            localized_units = units(localization or {})
            if not localized_units:
                errors.append(f"{locale}: missing {key!r}")
                continue
            for unit in localized_units:
                value = unit.get("value", "")
                if unit.get("state") != "translated" or not value:
                    errors.append(f"{locale}: unreviewed or empty {key!r}")
                elif signature(value) != source_signature:
                    errors.append(f"{locale}: placeholders differ for {key!r}: {value!r}")

    if errors:
        preview = "\n".join("ERROR: " + error for error in errors[:100])
        remainder = len(errors) - 100
        if remainder > 0:
            preview += f"\nERROR: ... and {remainder} more"
        raise SystemExit(preview)
    print(f"Catalog is complete for {len(locales) - 1} translated release locale(s).")


if __name__ == "__main__":
    main()
