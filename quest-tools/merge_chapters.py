import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
CHAPTERS_DIR = os.path.join(BASE, "specs", "chapters")

BAND_MARGIN = 3  # gap (in x/y grid units, pre-SPACING) between stacked source bands

NEW_GROUPS = [
    {"key": "begin_your_journey", "title": "Begin Your Journey", "order_index": 0},
    {"key": "build_and_create", "title": "Build & Create", "order_index": 1},
    {"key": "magic_and_discovery", "title": "Magic & Discovery", "order_index": 2},
    {"key": "conquer_the_skies", "title": "Conquer the Skies", "order_index": 3},
    {"key": "greater_challenges", "title": "Greater Challenges", "order_index": 4},
]

# (new_key, group, order_index, title, subtitle, icon, [source old chapter keys in band order])
NEW_CHAPTERS = [
    ("welcome_adventurer", "begin_your_journey", 0, "Welcome, Adventurer!",
     "Everything you need before the real journey begins",
     "skillprogression:skill_book",
     ["getting_started", "first_steps"]),

    ("adventure_awaits", "begin_your_journey", 1, "Adventure Awaits",
     "Waystones, relics, ruins, and reasons to leave home",
     "waystones:waystone",
     ["adventurer_rpg", "waystones", "artifacts", "guard_villagers", "relics"]),

    ("home_sweet_home", "begin_your_journey", 2, "Home Sweet Home",
     "Furnish it, light it, and make it feel like yours",
     "minecraft:chest",
     ["handcrafted", "supplementaries", "quark"]),

    ("from_farm_to_feast", "build_and_create", 0, "From Farm to Feast",
     "A proper kitchen, a proper farm, and a proper meal",
     "farmersdelight:cutting_board",
     ["farmers_delight", "pams_harvestcraft", "aquaculture", "homestead_milestones", "create_culinary"]),

    ("engineers_workshop", "build_and_create", 1, "The Engineer's Workshop",
     "From andesite alloy to a factory that runs itself",
     "create:andesite_alloy",
     ["create_core", "create_stuff_additions", "create_electric", "create_connected",
      "create_decor", "create_enchantment_industry", "create_aquatic_engineering", "railways"]),

    ("storage_and_logistics", "build_and_create", 2, "Storage & Logistics",
     "From a single drawer to a warehouse that sorts itself",
     "storagedrawers:controller",
     ["storage_drawers", "functional_storage", "sophisticated_storage", "toms_storage"]),

    ("arcane_arts", "magic_and_discovery", 0, "The Arcane Arts",
     "Simple experiments become real spellcraft",
     "ars_nouveau:source_gem",
     ["ars_nouveau", "arcane_abilities", "mystical_agriculture"]),

    ("beyond_the_horizon", "magic_and_discovery", 1, "Beyond the Horizon",
     "The map is bigger than you think",
     "naturescompass:naturescompass",
     ["the_explorer"]),

    ("taking_to_the_skies", "conquer_the_skies", 0, "Taking to the Skies",
     "Learn to fly before you learn to live up here",
     "aeronautics:wooden_propeller",
     ["aeronautics_fundamentals"]),

    ("captain_of_the_skies", "conquer_the_skies", 1, "Captain of the Skies",
     "A ship of your own, and everything it takes to keep it in the air",
     "create_aeronautics_ftb_chunks:contraption_claim_block",
     ["airship_mastery"]),

    ("here_be_dragons", "greater_challenges", 0, "Here Be Dragons",
     "Rumours first. Then proof",
     "iceandfire:dragonegg",
     ["ice_and_fire"]),

    ("bounty_board", "greater_challenges", 1, "Bounty Board",
     "Someone's always paying for a thinner mob population",
     "minecraft:crossbow",
     ["bounties"]),

    ("mastery", "greater_challenges", 2, "Mastery",
     "What you've become, spread across everything you've touched",
     "minecraft:nether_star",
     ["mastery"]),
]

def load(old_key):
    with open(os.path.join(CHAPTERS_DIR, f"{old_key}.json")) as f:
        return json.load(f)

def band_quests(spec, y_offset):
    """Return (quests, height) with every quest's y shifted by y_offset and
    tagged with its source chapter for id-seeding, height = span to stack next band."""
    quests = spec["quests"]
    ys = [q.get("y", 0) for q in quests]
    min_y, max_y = (min(ys), max(ys)) if ys else (0, 0)
    out = []
    for q in quests:
        nq = dict(q)
        nq["source"] = spec["key"]
        nq["y"] = q.get("y", 0) - min_y + y_offset
        out.append(nq)
    height = (max_y - min_y) + BAND_MARGIN
    return out, height

def merge_one(new_key, group, order_index, title, subtitle, icon, source_keys):
    all_quests = []
    seen_keys = set()
    y_cursor = 0
    for old_key in source_keys:
        spec = load(old_key)
        quests, height = band_quests(spec, y_cursor)
        y_cursor += height
        for q in quests:
            if q["key"] in seen_keys:
                # collision across merged sources — disambiguate the merged-file key,
                # but keep source/source_key so id-seeding is unaffected.
                q["source_key"] = q["key"]
                q["key"] = f"{old_key}__{q['key']}"
                # fix up any same-source dependency references to the old plain key
                # (only needed among this source's own quests, already appended)
            seen_keys.add(q["key"])
            all_quests.append(q)
    # second pass: rewrite dependencies for any renamed keys, per source
    rename_map = {}
    for q in all_quests:
        if "source_key" in q and q["source_key"] != q["key"]:
            rename_map[(q["source"], q["source_key"])] = q["key"]
    for q in all_quests:
        deps = q.get("dependencies", [])
        new_deps = []
        for d in deps:
            new_deps.append(rename_map.get((q["source"], d), d))
        q["dependencies"] = new_deps

    return {
        "key": new_key,
        "group": group,
        "order_index": order_index,
        "title": title,
        "icon": icon,
        "subtitle": subtitle,
        "quests": all_quests,
    }

def main():
    with open(os.path.join(BASE, "specs", "groups.json"), "w") as f:
        json.dump(NEW_GROUPS, f, indent=2)
        f.write("\n")

    old_keys_used = set()
    new_specs = {}
    for new_key, group, order_index, title, subtitle, icon, sources in NEW_CHAPTERS:
        spec = merge_one(new_key, group, order_index, title, subtitle, icon, sources)
        new_specs[new_key] = spec
        old_keys_used.update(sources)
        print(f"{new_key}: merged {sources} -> {len(spec['quests'])} quests")

    # retire every old chapter file that got folded into a new one
    for fname in os.listdir(CHAPTERS_DIR):
        if not fname.endswith(".json"):
            continue
        key = fname[:-5]
        if key in old_keys_used:
            os.remove(os.path.join(CHAPTERS_DIR, fname))

    # write new merged files
    for new_key, spec in new_specs.items():
        with open(os.path.join(CHAPTERS_DIR, f"{new_key}.json"), "w") as f:
            json.dump(spec, f, indent=2)
            f.write("\n")

    print(f"\n{len(new_specs)} new chapters written, {len(old_keys_used)} old chapters retired.")

if __name__ == "__main__":
    main()
