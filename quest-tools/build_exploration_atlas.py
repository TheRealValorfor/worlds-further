"""Build overworld / nether / end exploration chapters from installed jars + vanilla 1.21.1."""
from __future__ import annotations

import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
INSTANCE = BASE.parent
MODS = INSTANCE / "mods"
VANILLA_JAR = Path("/Users/joshie/Documents/curseforge/minecraft/Install/versions/1.21.1/1.21.1.jar")
OUT = BASE / "specs" / "chapters"

COLS = 10
STEP = 1.6
SECTION_GAP = 4.0
SKIP_BIOME_NS = {"terrablender", "blueprint"}
NETHER_STRUCT_NS = {"mns", "betterfortresses"}
END_STRUCT_NS = {"mes", "betterendisland"}
NETHER_BIOMES_MC = {
    "basalt_deltas", "crimson_forest", "nether_wastes", "soul_sand_valley", "warped_forest",
}
END_BIOMES_MC = {
    "the_end", "end_highlands", "end_midlands", "end_barrens", "small_end_islands",
}
NETHER_STRUCT_MC = {"fortress", "bastion_remnant", "nether_fossil", "ruined_portal_nether"}
END_STRUCT_MC = {"end_city"}

NS_TITLE = {
    "minecraft": "Vanilla",
    "regions_unexplored": "Regions Unexplored",
    "biomesoplenty": "Biomes O' Plenty",
    "natures_spirit": "Nature's Spirit",
    "hybrid_aquatic": "Hybrid Aquatic",
    "ars_nouveau": "Ars Nouveau",
    "quark": "Quark",
    "mvs": "Moog's Voyager",
    "mbs": "Moog's Bountiful",
    "mss": "Moog's Soaring",
    "mos": "Moog's Ocean",
    "mns": "Moog's Nether",
    "mes": "Moog's End",
    "mmv": "Moog's Missing Villages",
    "towns_and_towers": "Towns and Towers",
    "explorify": "Explorify",
    "bettermineshafts": "YUNG's Mineshafts",
    "betterdungeons": "YUNG's Dungeons",
    "betterwitchhuts": "YUNG's Witch Huts",
    "betterfortresses": "YUNG's Nether Fortresses",
    "betterdeserttemples": "YUNG's Desert Temples",
    "betterjungletemples": "YUNG's Jungle Temples",
    "betterstrongholds": "YUNG's Strongholds",
    "betteroceanmonuments": "YUNG's Ocean Monuments",
    "betterendisland": "YUNG's End Island",
    "iceandfire": "Ice and Fire",
    "sky_whale_ship": "Sky Whale",
    "friendsandfoes": "Friends and Foes",
    "supplementaries": "Supplementaries",
    "aeronauticsdiscovery": "Aeronautics Discovery",
    "oddities": "Bosses Oddities",
    "spider_overhaul": "Spider Overhaul",
    "ecologics": "Ecologics",
    "dungeon_echo": "Dungeon Echo",
}

CHAPTERS = {
    "overworld": {
        "order_index": 2,
        "title": "The Overworld Atlas",
        "icon": "minecraft:grass_block",
        "subtitle": "Every biome and structure under this sky",
        "dimension": "minecraft:overworld",
        "enter_title": "Stand in the Overworld",
        "enter_icon": "minecraft:grass_block",
        "biome_icon": "minecraft:oak_sapling",
        "structure_icon": "explorerscompass:explorerscompass",
        "source": "explore_overworld",
    },
    "nether": {
        "order_index": 3,
        "title": "The Nether Atlas",
        "icon": "minecraft:netherrack",
        "subtitle": "Every biome and structure in the deep heat",
        "dimension": "minecraft:the_nether",
        "enter_title": "Step into the Nether",
        "enter_icon": "minecraft:obsidian",
        "biome_icon": "minecraft:crimson_fungus",
        "structure_icon": "minecraft:nether_brick",
        "source": "explore_nether",
    },
    "end": {
        "order_index": 4,
        "title": "The End Atlas",
        "icon": "minecraft:end_stone",
        "subtitle": "Every biome and structure past the portal",
        "dimension": "minecraft:the_end",
        "enter_title": "Arrive in the End",
        "enter_icon": "minecraft:ender_eye",
        "biome_icon": "minecraft:chorus_fruit",
        "structure_icon": "minecraft:purpur_block",
        "source": "explore_end",
    },
}


def pretty_name(path: str) -> str:
    leaf = path.split("/")[-1]
    return leaf.replace("_", " ").title()


def key_id(prefix: str, ns: str, path: str) -> str:
    return f"{prefix}_{ns}_{path.replace('/', '_')}"[:80]


def read_zip_entries(jar: Path, kind: str) -> list[tuple[str, str]]:
    pat = re.compile(rf"^data/([^/]+)/worldgen/{kind}/(.+)\.json$")
    out = []
    try:
        z = zipfile.ZipFile(jar)
    except Exception:
        return out
    for name in z.namelist():
        m = pat.match(name)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def classify_biome(ns: str, path: str) -> str:
    if ns == "minecraft":
        if path in NETHER_BIOMES_MC:
            return "nether"
        if path in END_BIOMES_MC:
            return "end"
        return "overworld"
    return "overworld"


def classify_structure(ns: str, path: str) -> str:
    if ns in NETHER_STRUCT_NS:
        return "nether"
    if ns in END_STRUCT_NS:
        return "end"
    if ns == "minecraft":
        if path in NETHER_STRUCT_MC:
            return "nether"
        if path in END_STRUCT_MC:
            return "end"
        return "overworld"
    return "overworld"


def collect() -> dict:
    biomes = defaultdict(list)
    structs = defaultdict(list)
    if VANILLA_JAR.exists():
        for ns, path in read_zip_entries(VANILLA_JAR, "biome"):
            biomes[classify_biome(ns, path)].append((ns, path))
        for ns, path in read_zip_entries(VANILLA_JAR, "structure"):
            structs[classify_structure(ns, path)].append((ns, path))
    for jar in sorted(MODS.glob("*.jar")):
        for ns, path in read_zip_entries(jar, "biome"):
            if ns in SKIP_BIOME_NS:
                continue
            biomes[classify_biome(ns, path)].append((ns, path))
        for ns, path in read_zip_entries(jar, "structure"):
            structs[classify_structure(ns, path)].append((ns, path))
    for dim in biomes:
        biomes[dim] = sorted(set(biomes[dim]))
    for dim in structs:
        structs[dim] = sorted(set(structs[dim]))
    return {"biomes": biomes, "structs": structs}


def grid_quests(entries, *, prefix, task_field, task_type, icon, source, section, y0, dep, flavour):
    quests = []
    for i, (ns, path) in enumerate(entries):
        x = (i % COLS) * STEP
        y = y0 + (i // COLS) * STEP
        rid = f"{ns}:{path}"
        quests.append({
            "key": key_id(prefix, ns, path),
            "title": pretty_name(path),
            "icon": icon,
            "x": round(x, 2),
            "y": round(y, 2),
            "description": [
                f"{NS_TITLE.get(ns, ns.replace('_', ' ').title())}. {flavour}",
                rid,
            ],
            "tasks": [{"type": task_type, task_field: rid}],
            "rewards": [],
            "dependencies": [],
            "source": source,
            "section": section,
        })
    last_y = y0 if not entries else y0 + ((len(entries) - 1) // COLS) * STEP
    return quests, last_y


def build_chapter(dim: str, meta: dict, data: dict) -> dict:
    source = meta["source"]
    quests = [{
        "key": "enter_dimension",
        "title": meta["enter_title"],
        "icon": meta["enter_icon"],
        "x": 0.0,
        "y": 0.0,
        "description": [
            "Walk through the portal, or just be here. The atlas starts when you arrive.",
        ],
        "tasks": [{"type": "dimension", "dimension": meta["dimension"]}],
        "rewards": [{"item": "minecraft:map", "count": 1}],
        "dependencies": [],
        "source": source,
        "shape": "hexagon",
        "size": 1.4,
        "section": "arrival",
    }]
    biomes = data["biomes"].get(dim, [])
    b_quests, b_last = grid_quests(
        biomes,
        prefix="biome",
        task_field="biome",
        task_type="biome",
        icon=meta["biome_icon"],
        source=source,
        section="biomes",
        y0=SECTION_GAP,
        dep="enter_dimension",
        flavour="Stand in this biome until the task ticks.",
    )
    quests.extend(b_quests)
    s_y0 = (b_last if biomes else 0.0) + SECTION_GAP
    if biomes:
        s_y0 = b_last + SECTION_GAP
    structs = data["structs"].get(dim, [])
    s_quests, _ = grid_quests(
        structs,
        prefix="structure",
        task_field="structure",
        task_type="structure",
        icon=meta["structure_icon"],
        source=source,
        section="structures",
        y0=s_y0,
        dep="enter_dimension",
        flavour="Walk inside the structure until the task ticks.",
    )
    quests.extend(s_quests)
    images = [
        {"x": 0.0, "y": -1.6, "width": 12, "height": 0.8, "text": ["Arrive"]},
        {"x": 0.0, "y": 2.4, "width": 12, "height": 0.8, "text": ["Walk Every Biome"]},
        {"x": 0.0, "y": 8.0, "width": 12, "height": 0.8, "text": ["Find Every Structure"]},
    ]
    return {
        "key": f"explore_{dim}",
        "group": "exploration",
        "order_index": meta["order_index"],
        "title": meta["title"],
        "icon": meta["icon"],
        "subtitle": meta["subtitle"],
        "quests": quests,
        "images": images,
    }


def main():
    data = collect()
    for dim, meta in CHAPTERS.items():
        spec = build_chapter(dim, meta, data)
        path = OUT / f"explore_{dim}.json"
        path.write_text(json.dumps(spec, indent=2) + "\n")
        print(f"{path.name}: {len(spec['quests'])} quests "
              f"(biomes {len(data['biomes'].get(dim, []))} "
              f"structures {len(data['structs'].get(dim, []))})")


if __name__ == "__main__":
    main()
