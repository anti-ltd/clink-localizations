#!/usr/bin/env python3
"""Read-only gate for the exact localization assets that will be published."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import pathlib


ROOT = pathlib.Path(__file__).resolve().parent.parent


def validate_release(root: pathlib.Path = ROOT) -> list[str]:
    catalog_path = root / "Catalog" / "Localizable.xcstrings"
    digest = hashlib.sha256(catalog_path.read_bytes()).hexdigest()
    fingerprint = root / "Localizations" / ".catalog-sha256"
    errors = []
    if not fingerprint.is_file() or fingerprint.read_text().strip() != digest:
        errors.append("Compiled localizations are stale. Run tools/export-localizations.sh in clink-localizations on a Mac.")
    released = (root / "release-locales.txt").read_text().split()
    if not released or released[0] != "en" or len(released) != len(set(released)):
        errors.append("release-locales.txt must contain unique locales with en first.")
    packs = sorted(pack for pack in (root / "Localizations").glob("*.lproj")
                   if not pack.name.startswith("._"))
    if {pack.name.removesuffix(".lproj") for pack in packs} != set(released):
        errors.append("Compiled packs must exactly match release-locales.txt.")
    spec = importlib.util.spec_from_file_location("localization_validator", ROOT / "tools" / "validate-localization.py")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    for pack in packs:
        errors.extend(f"{pack.name}: {error}" for error in validator.validate(pack, catalog))
    return errors


def main() -> None:
    errors = validate_release()
    if errors:
        preview = ["ERROR: " + error for error in errors[:30]]
        if len(errors) > 30:
            preview.append(f"ERROR: ... and {len(errors) - 30} more")
        raise SystemExit("\n".join(preview))
    count = len((ROOT / "release-locales.txt").read_text().split())
    print(f"All {count} release packs are current and match their catalog values.")


if __name__ == "__main__":
    main()
