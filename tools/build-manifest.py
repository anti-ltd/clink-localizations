#!/usr/bin/env python3
"""Validate compiled resources and generate the immutable release manifest."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

# BEGIN repository platform policy (Tools/sync_repository_platforms.py)
def apply_platforms(root, manifest):
    """Annotate every pack; absent policy preserves legacy cross-platform packs."""
    path = root / "platforms.json"
    policy = json.loads(path.read_text()) if path.exists() else {}
    if not isinstance(policy, dict) or set(policy) - {"default", "overrides"}:
        raise ValueError("platforms.json must contain default and overrides only")
    default = policy.get("default", "both")
    overrides = policy.get("overrides", {})
    allowed = ("ios", "android", "both")
    if default not in allowed or not isinstance(overrides, dict):
        raise ValueError("Invalid repository platform policy")
    if any(value not in allowed for value in overrides.values()):
        raise ValueError("Platforms must be ios, android or both")
    entries = [entry for key, value in manifest.items() if isinstance(value, list)
               for entry in value]
    identifiers = {entry.get("id", entry.get("code", entry.get("locale"))) for entry in entries}
    if set(overrides) - identifiers:
        raise ValueError("Platform overrides name missing packs: " + str(sorted(set(overrides) - identifiers)))
    for entry in entries:
        identifier = entry.get("id", entry.get("code", entry.get("locale")))
        entry["platform"] = overrides.get(identifier, default)
    return manifest
# END repository platform policy


root = pathlib.Path(__file__).resolve().parent.parent
subprocess.run([sys.executable, str(root / "tools" / "validate-catalog.py")], check=True)
subprocess.run([sys.executable, str(root / "tools" / "validate-release.py")], check=True)
packs = sorted(pack for pack in (root / "Localizations").glob("*.lproj") if not pack.name.startswith("._"))
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
(output / "manifest.json").write_text(json.dumps(apply_platforms(root, {"version": version, "packs": manifest_packs}), indent=2) + "\n", encoding="utf-8")
print(f"Wrote manifest.json for {len(manifest_packs)} localization pack(s).")
