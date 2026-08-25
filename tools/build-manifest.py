#!/usr/bin/env python3
"""Validate compiled resources and generate the immutable release manifest."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent.parent
packs = sorted(pack for pack in (root / "Localizations").glob("*.lproj") if not pack.name.startswith("._"))
if not packs:
    raise SystemExit("No localization packs found in Localizations/.")
validator = root / "tools" / "validate-localization.py"
for pack in packs:
    subprocess.run([sys.executable, str(validator), str(pack)], check=True)
try:
    version = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
except subprocess.CalledProcessError:
    # Lets a newly scaffolded repository verify its manifest before its first
    # commit. GitHub Actions always has HEAD, so releases never use this value.
    version = "development"
repository = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], cwd=root, text=True).strip()
if repository.startswith("git@github.com:"):
    repository = repository.removeprefix("git@github.com:").removesuffix(".git")
elif repository.startswith("https://github.com/"):
    repository = repository.removeprefix("https://github.com/").removesuffix(".git")
else:
    raise SystemExit("origin must be a GitHub repository URL.")
output = root / "out"
shutil.rmtree(output, ignore_errors=True)
assets_dir = output / "assets"
assets_dir.mkdir(parents=True)
manifest_packs = []
for pack in packs:
    locale = pack.name.removesuffix(".lproj")
    assets = []
    for resource in sorted(resource for resource in pack.iterdir() if not resource.name.startswith("._")):
        data = resource.read_bytes()
        name = f"{locale}--{resource.name}"
        (assets_dir / name).write_bytes(data)
        assets.append({"path": resource.name, "url": f"https://github.com/{repository}/releases/download/latest/{name}", "sha256": hashlib.sha256(data).hexdigest(), "byteCount": len(data)})
    manifest_packs.append({"locale": locale, "sourceRevision": "v1", "version": version, "assets": assets})
(output / "manifest.json").write_text(json.dumps({"version": version, "packs": manifest_packs}, indent=2) + "\n", encoding="utf-8")
print(f"Wrote manifest.json for {len(manifest_packs)} localization pack(s).")
