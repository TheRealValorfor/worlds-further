import zipfile, json, os, re, glob, io

BASE = os.path.dirname(os.path.abspath(__file__))
INSTANCE = os.path.dirname(BASE)
MODS_DIR = os.path.join(INSTANCE, "mods")
QUESTS_DIR = os.path.join(INSTANCE, "config", "ftbquests", "quests", "chapters")
LANG_DIR = os.path.join(BASE, "lang")

# namespace -> jar path (best effort: match by namespace name substring in lang dir already built)
# We instead just scan every mod jar + nested jarjar jars once, building ns -> set(valid item ids)
#
# "Valid" requires BOTH a real item model file AND a real lang display name — a model alone
# isn't enough (some mods ship WIP/removed items with a model but no lang entry, or with a
# lang entry literally saying "[WIP]"/"[Removed ...]"; those slipped through as false-positives
# for the Relics mod and must not be usable in quest content).
def collect_valid_items():
    models = {}       # ns -> set of registry names that have a real item model
    names = {}        # ns -> {registry name: display name}
    recipe_outputs = {}  # ns -> set of registry names produced/converted by a real recipe

    def scan_zip(zf):
        namelist = zf.namelist()
        for name in namelist:
            m = re.match(r"assets/([^/]+)/models/item/(.+)\.json$", name)
            if m:
                ns, item = m.group(1), m.group(2)
                models.setdefault(ns, set()).add(item)
        for name in namelist:
            m = re.match(r"assets/([^/]+)/lang/en_us\.json$", name)
            if m:
                ns = m.group(1)
                try:
                    data = json.loads(zf.read(name).decode("utf-8"))
                except Exception:
                    continue
                for k, v in data.items():
                    parts = k.split(".")
                    if len(parts) == 3 and parts[0] in ("item", "block") and parts[1] == ns:
                        names.setdefault(ns, {})[parts[2]] = v
        # Recipe outputs are strong independent proof an item is real and obtainable,
        # even when (as happens for a few untranslated/ported items) no lang key exists.
        for name in namelist:
            m = re.match(r"data/([^/]+)/recipes?/.+\.json$", name)
            if not m:
                continue
            try:
                recipe = json.loads(zf.read(name).decode("utf-8"))
            except Exception:
                continue
            results = recipe.get("results")
            if results is None:
                results = [recipe["result"]] if "result" in recipe else []
            for r in results:
                if not isinstance(r, dict):
                    continue
                rid = r.get("id") or r.get("item")
                if isinstance(rid, str) and ":" in rid:
                    rns, rname = rid.split(":", 1)
                    recipe_outputs.setdefault(rns, set()).add(rname)

    for jarpath in glob.glob(os.path.join(MODS_DIR, "*.jar")):
        try:
            with zipfile.ZipFile(jarpath) as zf:
                scan_zip(zf)
                for n in zf.namelist():
                    if n.startswith("META-INF/jarjar/") and n.endswith(".jar"):
                        try:
                            with zipfile.ZipFile(io.BytesIO(zf.read(n))) as nzf:
                                scan_zip(nzf)
                        except Exception:
                            pass
        except Exception as e:
            print("WARN failed to open", jarpath, e)

    def looks_like_placeholder(display_name):
        low = display_name.lower()
        return "[wip]" in low or "[removed" in low or display_name.strip() == ""

    # Valid = has a real, non-placeholder lang name (regardless of whether it also has a
    # standalone item model — some real items, e.g. bred/dropped-only items, never get one)
    # OR is a genuine recipe output/conversion result (proves obtainability even when a
    # translation is missing, which happens for a few untranslated/ported items).
    # A model file alone, with neither a real name nor any recipe producing it, is exactly
    # the leftover/WIP-asset pattern that caused real bugs earlier — that alone is NOT enough.
    valid = {}
    all_ns = set(models) | set(names) | set(recipe_outputs)
    for ns in all_ns:
        ns_names = names.get(ns, {})
        recipe_made = recipe_outputs.get(ns, set())
        candidates = set(models.get(ns, set())) | set(ns_names) | recipe_made
        kept = set()
        for item in candidates:
            has_name = item in ns_names and not looks_like_placeholder(ns_names[item])
            has_recipe = item in recipe_made
            if has_name or has_recipe:
                kept.add(item)
        if kept:
            valid[ns] = kept
    return valid

# vanilla items: derive from the client jar too, same method
def collect_vanilla():
    vjar = "/Users/joshie/Documents/curseforge/minecraft/Install/versions/1.21.1/1.21.1.jar"
    valid = set()
    with zipfile.ZipFile(vjar) as zf:
        for name in zf.namelist():
            m = re.match(r"assets/minecraft/models/item/(.+)\.json$", name)
            if m:
                valid.add(m.group(1))
    return valid

def main():
    print("Scanning mod jars for real item models (this proves an item actually exists)...")
    valid = collect_valid_items()
    vanilla = collect_vanilla()
    print(f"Found {sum(len(v) for v in valid.values())} modded items across {len(valid)} namespaces, {len(vanilla)} vanilla items")

    all_refs = {}  # (ns:item) -> list of (chapter_file, quest_key, context)
    for f in sorted(glob.glob(os.path.join(QUESTS_DIR, "*.snbt"))):
        text = open(f).read()
        chapter = os.path.basename(f)[:-5]
        # crude parse: walk quest blocks by title/id order isn't necessary; just find all item: "..." occurrences with nearest preceding quest title/key context
        for m in re.finditer(r'item: "([a-z0-9_.\-]+:[a-z0-9_./\-]+)"', text):
            item_id = m.group(1)
            # find nearest preceding title for context
            pre = text[:m.start()]
            title_matches = re.findall(r'title: "([^"]*)"', pre)
            ctx = title_matches[-1] if title_matches else "?"
            all_refs.setdefault(item_id, []).append((chapter, ctx))

    bad = []
    for item_id, refs in sorted(all_refs.items()):
        ns, name = item_id.split(":", 1)
        if ns == "minecraft":
            ok = name in vanilla
        else:
            ok = name in valid.get(ns, set())
        if not ok:
            bad.append((item_id, refs))

    print(f"\nChecked {len(all_refs)} distinct item ids across all chapters.")
    print(f"INVALID: {len(bad)}\n")
    for item_id, refs in bad:
        locs = ", ".join(f"{c}:{q}" for c, q in refs[:4])
        more = f" (+{len(refs)-4} more)" if len(refs) > 4 else ""
        print(f"  {item_id}  <-  {locs}{more}")

    # dump valid sets for reuse by a repair pass
    out = {"modded": {ns: sorted(v) for ns, v in valid.items()}, "vanilla": sorted(vanilla)}
    with open(os.path.join(BASE, "verified_items.json"), "w") as fo:
        json.dump(out, fo, indent=1)
    print(f"\nWrote full verified item registry to {os.path.join(BASE, 'verified_items.json')}")

if __name__ == "__main__":
    main()
