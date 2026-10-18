#!/usr/bin/env python3
"""Sync the allowlisted skill bundle and build offline, deterministic plugin ZIPs."""
import argparse
import json
from pathlib import Path
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
SKILL_FILES = (
    "SKILL.md", "LICENSE", "agents/openai.yaml", "scripts/calculate_coverage.py",
    "references/local-setup.md", "references/pitfalls.md",
    "references/role-prompts.md", "references/rule-inventory.md",
    "references/runtime-separation.md",
)
BUNDLE = "skills/blackbox-web-recon"


def safe_path(relative):
    path = ROOT / relative
    if not path.resolve().is_relative_to(ROOT):
        raise ValueError(f"Path escapes repository: {relative}")
    for part in (path, *path.parents):
        if part == ROOT:
            break
        if part.is_symlink():
            raise ValueError(f"Symlinks are not package inputs or destinations: {relative}")
    return path


def read(relative):
    return safe_path(relative).read_bytes()


def validate_manifests():
    portable = json.loads(read("plugin.json"))
    claude = json.loads(read(".claude-plugin/plugin.json"))
    for key in ("name", "version", "description", "author", "homepage", "repository", "license"):
        if portable[key] != claude[key]:
            raise ValueError(f"Plugin metadata differs: {key}")
    if portable["name"] != "blackbox-web-recon" or portable["license"] != "MIT":
        raise ValueError("Unexpected plugin identity or license")
    catalog = json.loads(read(".claude-plugin/marketplace.json"))
    local = json.loads(read(".agents/plugins/marketplace.json"))
    if catalog["name"] != "web-rea" or local["name"] != catalog["name"]:
        raise ValueError("Marketplace identity differs")
    if len(catalog["plugins"]) != 1 or len(local["plugins"]) != 1:
        raise ValueError("Expected exactly one plugin in each marketplace")
    a, b = catalog["plugins"][0], local["plugins"][0]
    if a["name"] != portable["name"] or b["name"] != portable["name"]:
        raise ValueError("Marketplace plugin identity differs")
    if a["source"] != "./" or b["source"] != {"source": "local", "path": "./"}:
        raise ValueError("Marketplace must reference only this plugin root")


def sync_bundle(check):
    folder = safe_path(BUNDLE)
    if folder.exists():
        existing = {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file() or p.is_symlink()}
        extra = existing - set(SKILL_FILES)
        if extra:
            raise ValueError(f"Unexpected bundled files; inspect before packaging: {sorted(extra)}")
    for name in SKILL_FILES:
        source = read(name)
        destination = safe_path(f"{BUNDLE}/{name}")
        if check:
            if not destination.is_file() or destination.read_bytes() != source:
                raise ValueError(f"Bundled skill is stale: {name}; rerun build_packages.py")
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source)


def write_zip(name, files):
    path = safe_path(f"dist/{name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for destination, source in sorted(files.items()):
            info = ZipInfo(destination, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, read(source))
    print(f"Built dist/{name} ({len(files)} allowlisted files)")


def build():
    docs = {"LICENSE": "LICENSE", "README.md": "README.md", "docs/installation.md": "docs/installation.md"}
    skill = {f"blackbox-web-recon/{name}": name for name in SKILL_FILES}
    skill.update({f"blackbox-web-recon/{name}": source for name, source in docs.items()})
    write_zip("blackbox-web-recon-skill.zip", skill)
    bundled = {f"{BUNDLE}/{name}": f"{BUNDLE}/{name}" for name in SKILL_FILES}
    write_zip("blackbox-web-recon-claude-code.zip", {
        **docs, **bundled, ".claude-plugin/plugin.json": ".claude-plugin/plugin.json",
    })
    write_zip("blackbox-web-recon-openai.zip", {**docs, **bundled, "plugin.json": "plugin.json"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check manifests and bundle parity without writes")
    args = parser.parse_args()
    try:
        validate_manifests()
        sync_bundle(args.check)
        if args.check:
            print("Plugin identities, local marketplace paths and bundled skill parity verified.")
        else:
            build()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Package error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
