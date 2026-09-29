import json, os, glob

BASE = os.path.dirname(os.path.abspath(__file__))
SPECS_DIR = os.path.join(BASE, "specs", "chapters")

with open(os.path.join(BASE, "verified_items.json")) as f:
    verified = json.load(f)
modded = {ns: set(items) for ns, items in verified["modded"].items()}
vanilla = set(verified["vanilla"])

def is_valid(item_id):
    if item_id.startswith("#"):
        return True  # tag reference — hand-verified separately, not in the item registry
    ns, name = item_id.split(":", 1)
    if ns == "minecraft":
        return name in vanilla
    return name in modded.get(ns, set())

specs = {}
for f in sorted(glob.glob(os.path.join(SPECS_DIR, "*.json"))):
    spec = json.load(open(f))
    specs[spec["key"]] = spec

# Global (chapter_key, quest_key) set, since a dependency may point at a quest in a
# different chapter — "other_chapter_key:quest_key" — now that chapters can be
# reorganized/merged without breaking cross-references.
quest_owner = {(key, q["key"]) for key, spec in specs.items() for q in spec["quests"]}

def dep_is_valid(current_key, dep):
    if ":" in dep:
        dep_chapter, dep_key = dep.split(":", 1)
    else:
        dep_chapter, dep_key = current_key, dep
    return (dep_chapter, dep_key) in quest_owner

total_bad = 0
for key, spec in specs.items():
    bad_here = []
    if not is_valid(spec["icon"]):
        bad_here.append(("chapter icon", spec["icon"]))
    for q in spec["quests"]:
        if not is_valid(q["icon"]):
            bad_here.append((f"quest '{q['key']}' icon", q["icon"]))
        for t in q.get("tasks", []):
            ttype = t.get("type", "item")
            if ttype == "item" and not is_valid(t["item"]):
                bad_here.append((f"quest '{q['key']}' task", t["item"]))
            elif ttype == "advancement" and not t.get("advancement"):
                bad_here.append((f"quest '{q['key']}' advancement task", "missing 'advancement' id"))
            elif ttype == "kill" and not t.get("entity"):
                bad_here.append((f"quest '{q['key']}' kill task", "missing 'entity' id"))
            elif ttype == "biome" and not t.get("biome"):
                bad_here.append((f"quest '{q['key']}' biome task", "missing 'biome' id"))
            elif ttype == "dimension" and not t.get("dimension"):
                bad_here.append((f"quest '{q['key']}' dimension task", "missing 'dimension' id"))
            elif ttype == "structure" and not t.get("structure"):
                bad_here.append((f"quest '{q['key']}' structure task", "missing 'structure' id"))
            elif ttype not in ("item", "advancement", "checkmark", "kill", "biome", "dimension", "structure"):
                bad_here.append((f"quest '{q['key']}' task", f"unknown type '{ttype}'"))
        for r in q.get("rewards", []):
            if not is_valid(r["item"]):
                bad_here.append((f"quest '{q['key']}' reward", r["item"]))
        for d in q.get("dependencies", []):
            if not dep_is_valid(key, d):
                bad_here.append((f"quest '{q['key']}' dependency", f"unknown key '{d}'"))
        if not q.get("tasks"):
            bad_here.append((f"quest '{q['key']}'", "has no tasks"))
    if bad_here:
        print(f"=== {key} ({len(bad_here)} bad) ===")
        for ctx, item_id in bad_here:
            print(f"  {ctx}: {item_id}")
        total_bad += len(bad_here)

print(f"\nTOTAL INVALID ITEM REFERENCES: {total_bad}")
