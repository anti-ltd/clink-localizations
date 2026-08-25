#!/usr/bin/env python3
"""Validate one compiled Clink UI-localization resource directory."""
import pathlib
import plistlib
import re
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 tools/validate-localization.py Localizations/<locale>.lproj")

path = pathlib.Path(sys.argv[1])
errors = []
locale_re = re.compile(r"^[a-z]{2,3}(?:-[A-Z][a-z]{3}|-[A-Z]{2}|-[0-9]{3})*$")
if not path.is_dir() or not path.name.endswith(".lproj"):
    errors.append("pack must be a <locale>.lproj directory.")
locale = path.name.removesuffix(".lproj")
if not locale_re.fullmatch(locale):
    errors.append("directory must use a canonical BCP-47 locale (for example fr, pt-BR, zh-Hans).")

for name, required in (("Localizable.strings", True), ("Localizable.stringsdict", False)):
    resource = path / name
    if required and not resource.is_file():
        errors.append(f"missing {name}.")
    elif resource.exists():
        try:
            content = plistlib.loads(resource.read_bytes())
            if not isinstance(content, dict) or (required and not content):
                errors.append(f"{name} must be a non-empty property-list dictionary.")
        except (OSError, plistlib.InvalidFileException) as error:
            errors.append(f"{name} is not a valid property list: {error}")

if path.is_dir():
    unexpected = [child.name for child in path.iterdir() if not child.name.startswith("._") and child.name not in {"Localizable.strings", "Localizable.stringsdict"}]
    if unexpected:
        errors.append("unexpected resource(s): " + ", ".join(sorted(unexpected)))
if errors:
    raise SystemExit("\n".join("ERROR: " + error for error in errors))
print(f"{path}: looks ready for source-key coverage review.")
