#!/usr/bin/env python3
"""Copy Worlds Further git overrides onto a local CurseForge instance.

Works on Windows, macOS, and Linux. Does not install CurseForge addons
(use the CurseForge app / manifest.json for that). Does not touch saves/,
logs/, or minecraftinstance.json.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def is_instance(path: Path) -> bool:
    return (path / "mods").is_dir() and (path / "config").is_dir()


def instance_profile_name(path: Path) -> str:
    meta = path / "minecraftinstance.json"
    if not meta.is_file():
        return ""
    try:
        data = json.loads(meta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str(data.get("name") or "")


def name_matches_pack(text: str) -> bool:
    key = "".join(text.lower().split())
    return key in {"worldsfurther"} or text.lower().strip() == "worlds further"


def is_worlds_further_instance(path: Path) -> bool:
    if not is_instance(path):
        return False
    return name_matches_pack(path.name) or name_matches_pack(instance_profile_name(path))


def instance_roots() -> list[Path]:
    home = Path.home()
    extra = os.environ.get("WORLD_FURTHER_INSTANCES_ROOT", "").strip()
    roots: list[Path] = []
    if extra:
        roots.append(Path(extra).expanduser())
    roots.extend(
        [
            home / "Documents" / "curseforge" / "minecraft" / "Instances",
            home / "curseforge" / "minecraft" / "Instances",
            home / ".curseforge" / "minecraft" / "Instances",
        ]
    )
    # Deduplicate while keeping order
    seen: set[Path] = set()
    out: list[Path] = []
    for r in roots:
        try:
            r = r.resolve()
        except OSError:
            continue
        if r in seen or not r.is_dir():
            continue
        seen.add(r)
        out.append(r)
    return out


def detect_instance() -> Path:
    hits: list[Path] = []
    searched = instance_roots()
    for root in searched:
        for child in root.iterdir():
            if child.is_dir() and is_worlds_further_instance(child):
                hits.append(child)
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        listed = "\n".join(f"  {h}" for h in hits)
        raise SystemExit(f"Multiple Worlds Further instances:\n{listed}\nPass --instance PATH")
    searched_txt = "\n".join(f"  searched: {r}" for r in searched) or "  searched: (none found)"
    raise SystemExit(
        "No Worlds Further instance found. Pass --instance PATH\n"
        "Look for a CurseForge profile named Worlds further / Worlds Further / WorldsFurther.\n"
        f"{searched_txt}"
    )


def copy_tree(src: Path, dst: Path, dry_run: bool, *, skip_file=None, skip_dir_prefixes=None) -> None:
    skip_file = {s.lower() for s in (skip_file or set())}
    skip_dir_prefixes = tuple(skip_dir_prefixes or ())
    if not src.is_dir():
        return
    for root, dirs, files in os.walk(src):
        rel_root = Path(root).relative_to(src)
        rel_posix = "." if str(rel_root) == "." else rel_root.as_posix()

        def keep_dir(name: str) -> bool:
            child = name if rel_posix == "." else f"{rel_posix}/{name}"
            return not any(child == p or child.startswith(p + "/") for p in skip_dir_prefixes)

        dirs[:] = [d for d in dirs if keep_dir(d)]
        dest_dir = dst if rel_posix == "." else dst / rel_root
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
        for name in files:
            if name.lower() in skip_file or name.endswith(".bak"):
                continue
            from_path = Path(root) / name
            to_path = dest_dir / name
            if dry_run:
                print(f"  {from_path.relative_to(src)} -> {to_path}")
            else:
                shutil.copy2(from_path, to_path)


def copy_file(src: Path, dst: Path, dry_run: bool) -> None:
    if not src.is_file():
        return
    if dry_run:
        print(f"  {src.name} -> {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply this public worlds-further repo onto a local CurseForge instance (Windows, macOS, Linux)."
    )
    parser.add_argument("--instance", help="CurseForge instance folder (contains mods/ and config/)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be copied")
    parser.add_argument("--skip-options", action="store_true", help="Do not overwrite options.txt")
    parser.add_argument("--skip-jars", action="store_true", help="Do not copy overrides/mods/*.jar")
    args = parser.parse_args()

    overrides = repo_root() / "overrides"
    if not (overrides / "config").is_dir():
        print(f"Missing {overrides / 'config'} — clone TheRealValorfor/worlds-further first.", file=sys.stderr)
        return 1

    instance_s = args.instance or os.environ.get("WORLD_FURTHER_INSTANCE", "").strip()
    instance = Path(instance_s).expanduser() if instance_s else detect_instance()
    instance = instance.resolve()
    if not is_instance(instance):
        print(f"Not a CurseForge instance (need mods/ and config/): {instance}", file=sys.stderr)
        return 1

    print(f"Repo:     {repo_root()}")
    print(f"Instance: {instance}")
    if args.dry_run:
        print("Mode:     dry-run")

    skip_dirs = {"jei/world", "spark/tmp", "spark/tmp-client"}
    skip_files = {".ds_store", "sodium-fingerprint.json", "user_variables.db"}

    copy_tree(
        overrides / "config",
        instance / "config",
        args.dry_run,
        skip_file=skip_files,
        skip_dir_prefixes=skip_dirs,
    )
    copy_tree(overrides / "datapacks", instance / "datapacks", args.dry_run)
    copy_tree(overrides / "defaultconfigs", instance / "defaultconfigs", args.dry_run)

    shader_src = overrides / "shaderpacks"
    shader_dst = instance / "shaderpacks"
    if shader_src.is_dir():
        if not args.dry_run:
            shader_dst.mkdir(parents=True, exist_ok=True)
        for txt in shader_src.glob("*.txt"):
            copy_file(txt, shader_dst / txt.name, args.dry_run)

    if not args.skip_options:
        copy_file(overrides / "options.txt", instance / "options.txt", args.dry_run)
    for name in ("README.md", "CHANGELOG.md"):
        copy_file(overrides / name, instance / name, args.dry_run)

    mods_src = overrides / "mods"
    if not args.skip_jars and mods_src.is_dir():
        if not args.dry_run:
            (instance / "mods").mkdir(parents=True, exist_ok=True)
        for jar in mods_src.glob("*.jar"):
            copy_file(jar, instance / "mods" / jar.name, args.dry_run)

    print("Done. Fully quit and relaunch CurseForge Minecraft so configs reload.")
    print("Addon list (manifest.json) is not applied — update mods in the CurseForge app.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
