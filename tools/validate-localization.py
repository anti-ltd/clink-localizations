#!/usr/bin/env python3
"""Validate compiled pack coverage and values against the source catalog.

This is a structural/content check, not an editorial approval. Run on macOS or
Linux; binary Apple property lists can be read without invoking Xcode.
"""
from __future__ import annotations

import json
import pathlib
import plistlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parent.parent
RESOURCES = {"Localizable.strings", "Localizable.stringsdict"}
PLURAL_CATEGORIES = {"zero", "one", "two", "few", "many", "other"}


def validate(path: pathlib.Path, catalog: dict) -> list[str]:
    errors = []
    locale = path.name.removesuffix(".lproj")
    if not path.is_dir() or not path.name.endswith(".lproj"):
        return ["pack must be a <locale>.lproj directory."]
    if not re.fullmatch(r"[a-z]{2,3}(?:-[A-Z][a-z]{3}|-[A-Z]{2}|-[0-9]{3})*", locale):
        errors.append("directory must use a canonical BCP-47 locale (for example fr, pt-BR, zh-Hans).")

    tables = {}
    for name in sorted(RESOURCES):
        resource = path / name
        if not resource.is_file():
            if name == "Localizable.strings":
                errors.append(f"missing {name}.")
            tables[name] = {}
            continue
        try:
            content = plistlib.loads(resource.read_bytes())
            if not isinstance(content, dict) or (name == "Localizable.strings" and not content):
                errors.append(f"{name} must be a non-empty property-list dictionary.")
                content = {}
            tables[name] = content
        except (OSError, ValueError, plistlib.InvalidFileException) as error:
            errors.append(f"{name} is not a valid property list: {error}")
            tables[name] = {}

    unexpected = sorted(child.name for child in path.iterdir()
                        if not child.name.startswith("._") and child.name not in RESOURCES)
    if unexpected:
        errors.append("unexpected resource(s): " + ", ".join(unexpected))

    strings = tables["Localizable.strings"]
    plurals = tables["Localizable.stringsdict"]
    entries = catalog.get("strings", {})
    compiled_keys = set(strings) | set(plurals)
    if set(strings) & set(plurals):
        errors.append("keys must not be duplicated across strings and stringsdict resources.")
    unknown = compiled_keys - set(entries)
    if unknown:
        errors.append(f"compiled resources contain {len(unknown)} unknown catalog key(s).")

    for key, entry in entries.items():
        localization = entry.get("localizations", {}).get(locale, {})
        if locale != "en" and entry.get("shouldTranslate") is not False and key not in compiled_keys:
            errors.append(f"missing translated catalog key {key!r}.")
            continue
        if key not in compiled_keys:
            # Xcode omits some source-language entries. Looking up the English
            # source key already supplies its exact fallback value.
            continue
        unit = localization.get("stringUnit")
        variations = localization.get("variations", {})
        if unit is not None or (locale == "en" and not variations):
            expected = unit.get("value", "") if unit is not None else key
            if strings.get(key) != expected:
                errors.append(f"compiled value differs from catalog for {key!r}.")
        elif variations:
            if set(variations) != {"plural"}:
                errors.append(f"unsupported variation structure for {key!r}; extend validation before release.")
                continue
            value = plurals.get(key, {})
            if not isinstance(value, dict):
                errors.append(f"invalid compiled plural for {key!r}.")
                continue
            format_key = value.get("NSStringLocalizedFormatKey", "")
            match = re.fullmatch(r"%#@([^@]+)@", format_key) if isinstance(format_key, str) else None
            rule = value.get(match.group(1), {}) if match else {}
            if not isinstance(rule, dict) or rule.get("NSStringFormatSpecTypeKey") != "NSStringPluralRuleType":
                errors.append(f"missing compiled plural rule for {key!r}.")
                continue
            source_forms = variations["plural"]
            expected = {category: form.get("stringUnit", {}).get("value")
                        for category, form in source_forms.items()}
            actual = {category: rule[category] for category in PLURAL_CATEGORIES if category in rule}
            if actual != expected:
                errors.append(f"compiled plural values differ from catalog for {key!r}.")
            # The released catalog currently uses integer count variations.
            # Matching text alone cannot catch an edited variadic argument type.
            source_types = re.findall(r"%(?:\d+\$)?(lld|ld|d|llu|lu|u|f)", key)
            if len(source_types) != 1 or rule.get("NSStringFormatValueTypeKey") != source_types[0]:
                errors.append(f"compiled plural argument type differs for {key!r}.")
        elif entry.get("shouldTranslate") is not False:
            errors.append(f"no catalog translation for compiled key {key!r}.")
    return errors


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 tools/validate-localization.py Localizations/<locale>.lproj")
    path = pathlib.Path(sys.argv[1])
    catalog = json.loads((ROOT / "Catalog" / "Localizable.xcstrings").read_text(encoding="utf-8"))
    errors = validate(path, catalog)
    if errors:
        raise SystemExit("\n".join("ERROR: " + error for error in errors))
    print(f"{path.name}: compiled coverage and values match the catalog.")


if __name__ == "__main__":
    main()
