#!/usr/bin/env bash
# Copy Worlds Further git overrides onto a local CurseForge instance.
# Does not install/update CurseForge addons (that stays in the CF app / manifest.json).
# Does not touch saves/, logs/, or minecraftinstance.json.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OVERRIDES="$REPO_ROOT/overrides"
DRY_RUN=0
COPY_OPTIONS=1
COPY_OVERRIDE_JARS=1
INSTANCE=""

usage() {
  cat <<'EOF'
Usage: scripts/apply-to-instance.sh [options]

Applies this repo's overrides/ onto a CurseForge Minecraft instance
(config, datapacks, shader .txt, defaultconfigs, README).

  --instance PATH   CurseForge instance folder (contains mods/ and config/)
  --dry-run         Print rsync plan; do not write
  --skip-options    Do not overwrite options.txt (keeps the player's keybinds)
  --skip-jars       Do not copy overrides/mods/*.jar (e.g. Relicworks until it is a CF addon)
  -h, --help        This help

Instance detection (first match wins):
  1. --instance
  2. WORLD_FURTHER_INSTANCE
  3. A folder named Worlds further / Worlds Further / WorldsFurther / Ejomilishy
     under ~/Documents/curseforge/minecraft/Instances or ~/curseforge/minecraft/Instances

Quit Minecraft before applying. Configs written while the game is open can be overwritten on exit.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --instance) INSTANCE="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --skip-options) COPY_OPTIONS=0; shift ;;
    --skip-jars) COPY_OVERRIDE_JARS=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ ! -d "$OVERRIDES/config" ]]; then
  echo "Missing $OVERRIDES/config — run this from a clone of worlds-further." >&2
  exit 1
fi

instance_roots() {
  local r
  for r in \
    "${WORLD_FURTHER_INSTANCES_ROOT:-}" \
    "$HOME/Documents/curseforge/minecraft/Instances" \
    "$HOME/curseforge/minecraft/Instances"
  do
    [[ -n "$r" && -d "$r" ]] && printf '%s\n' "$r"
  done
}

looks_like_instance() {
  [[ -d "$1/mods" && -d "$1/config" ]]
}

instance_display_name() {
  python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("name",""))' "$1/minecraftinstance.json" 2>/dev/null || true
}

is_worlds_further_instance() {
  local dir="$1" base name
  looks_like_instance "$dir" || return 1
  base="$(basename "$dir")"
  case "$base" in
    "Worlds further"|"Worlds Further"|"WorldsFurther"|"Ejomilishy") return 0 ;;
  esac
  name="$(instance_display_name "$dir")"
  [[ "$name" == "Worlds further" || "$name" == "Worlds Further" || "$name" == "WorldsFurther" ]]
}

detect_instance() {
  local root dir hits=()
  local glob
  while IFS= read -r root; do
    [[ -z "$root" ]] && continue
    shopt -s nullglob
    for dir in "$root"/*; do
      [[ -d "$dir" ]] || continue
      if is_worlds_further_instance "$dir"; then
        hits+=("$dir")
      fi
    done
    shopt -u nullglob
  done < <(instance_roots)
  if [[ ${#hits[@]} -eq 1 ]]; then
    printf '%s\n' "${hits[0]}"
    return 0
  fi
  if [[ ${#hits[@]} -gt 1 ]]; then
    echo "Multiple matching instances:" >&2
    printf '  %s\n' "${hits[@]}" >&2
    echo "Pass --instance PATH" >&2
    return 1
  fi
  echo "No Worlds Further instance found. Pass --instance PATH" >&2
  instance_roots | sed 's/^/  searched: /' >&2 || true
  return 1
}

if [[ -z "$INSTANCE" && -n "${WORLD_FURTHER_INSTANCE:-}" ]]; then
  INSTANCE="$WORLD_FURTHER_INSTANCE"
fi
if [[ -z "$INSTANCE" ]]; then
  INSTANCE="$(detect_instance)"
fi
INSTANCE="$(cd "$INSTANCE" && pwd)"

if ! looks_like_instance "$INSTANCE"; then
  echo "Not a CurseForge instance (need mods/ and config/): $INSTANCE" >&2
  exit 1
fi

if pgrep -fil 'minecraft|curseforge' >/dev/null 2>&1; then
  echo "Warning: Minecraft or CurseForge looks running. Quit the game first or configs may be overwritten on exit." >&2
fi

RSYNC=(rsync -a)
if [[ "$DRY_RUN" -eq 1 ]]; then
  RSYNC+=(-n -v --itemize-changes)
fi

RSYNC_EXCLUDES=(
  --exclude '.DS_Store'
  --exclude '*.bak'
  --exclude 'jei/world/'
  --exclude 'spark/tmp/'
  --exclude 'spark/tmp-client/'
  --exclude 'sodium-fingerprint.json'
  --exclude 'fancymenu/user_variables.db'
)

echo "Repo:     $REPO_ROOT"
echo "Instance: $INSTANCE"
[[ "$DRY_RUN" -eq 1 ]] && echo "Mode:     dry-run"

"${RSYNC[@]}" "${RSYNC_EXCLUDES[@]}" "$OVERRIDES/config/" "$INSTANCE/config/"

if [[ -d "$OVERRIDES/datapacks" ]]; then
  mkdir -p "$INSTANCE/datapacks"
  "${RSYNC[@]}" "$OVERRIDES/datapacks/" "$INSTANCE/datapacks/"
fi

if [[ -d "$OVERRIDES/defaultconfigs" ]]; then
  mkdir -p "$INSTANCE/defaultconfigs"
  "${RSYNC[@]}" "$OVERRIDES/defaultconfigs/" "$INSTANCE/defaultconfigs/"
fi

if [[ -d "$OVERRIDES/shaderpacks" ]]; then
  mkdir -p "$INSTANCE/shaderpacks"
  # Settings only — Complementary zip is a CurseForge shader addon.
  if [[ "$DRY_RUN" -eq 1 ]]; then
    rsync -n -v --itemize-changes --include '*/' --include '*.txt' --exclude '*' "$OVERRIDES/shaderpacks/" "$INSTANCE/shaderpacks/" || true
  else
    rsync -a --include '*/' --include '*.txt' --exclude '*' "$OVERRIDES/shaderpacks/" "$INSTANCE/shaderpacks/"
  fi
fi

if [[ "$COPY_OPTIONS" -eq 1 && -f "$OVERRIDES/options.txt" ]]; then
  "${RSYNC[@]}" "$OVERRIDES/options.txt" "$INSTANCE/options.txt"
fi

for f in README.md CHANGELOG.md; do
  [[ -f "$OVERRIDES/$f" ]] && "${RSYNC[@]}" "$OVERRIDES/$f" "$INSTANCE/$f"
done

if [[ "$COPY_OVERRIDE_JARS" -eq 1 && -d "$OVERRIDES/mods" ]]; then
  mkdir -p "$INSTANCE/mods"
  "${RSYNC[@]}" --include '*.jar' --exclude '*' "$OVERRIDES/mods/" "$INSTANCE/mods/"
fi

echo "Done. Fully quit and relaunch CurseForge Minecraft so configs reload."
echo "Addon list (manifest.json) is not applied — update mods in the CurseForge app."
