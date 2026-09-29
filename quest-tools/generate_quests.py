import json, os, hashlib, sys, re

BASE = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.dirname(BASE)
SPECS_DIR = os.path.join(BASE, "specs")
CHAPTERS_SPEC_DIR = os.path.join(SPECS_DIR, "chapters")
LANG_DIR = os.path.join(BASE, "lang")
VERIFIED_ITEMS_PATH = os.path.join(BASE, "verified_items.json")
OUT_DIR = os.path.join(INSTANCE_DIR, "config", "ftbquests", "quests")
SPACING = 1.3  # grid units are multiplied by this; smaller = quests packed tighter on screen

# Keep the IDs already saved by FTB, including IDs it repaired on earlier loads.
with open(os.path.join(SPECS_DIR, "id_map.json")) as f:
    _saved_ids = json.load(f)
_used_ids = set()
_localized_titles = {}
_reserved_ids = set(_saved_ids.values())

def gen_id(seed):
    if seed in _saved_ids:
        cid = _saved_ids[seed]
        if cid in _used_ids:
            raise ValueError(f"Duplicate ID seed: {seed}")
    else:
        n = 0
        while True:
            value = seed if n == 0 else f"{seed}#{n}"
            # FTB reads hex strings with Java Long.parseLong, not unsigned parsing.
            number = int(hashlib.sha256(value.encode("utf-8")).hexdigest()[:16], 16) & 0x7FFFFFFFFFFFFFFF
            cid = f"{number:016X}"
            if number > 1 and cid not in _used_ids and cid not in _reserved_ids:
                break
            n += 1
    _used_ids.add(cid)
    return cid

def load_valid_items():
    # Prefer the strong item-model-based registry (verified_items.json, built by
    # audit_items.py from real assets/<ns>/models/item/*.json files) over the
    # weaker lang-key-based check, since lang files can contain translation
    # entries for things that were never actually registered as real items.
    if os.path.exists(VERIFIED_ITEMS_PATH):
        with open(VERIFIED_ITEMS_PATH) as f:
            data = json.load(f)
        valid = set(f"minecraft:{n}" for n in data["vanilla"])
        per_mod = {"minecraft": set(data["vanilla"])}
        for ns, names in data["modded"].items():
            per_mod[ns] = set(names)
            valid |= set(f"{ns}:{n}" for n in names)
        return valid, per_mod

    valid = set()
    per_mod = {}
    for fname in os.listdir(LANG_DIR):
        if not fname.endswith(".json"):
            continue
        mod = fname[:-5]
        with open(os.path.join(LANG_DIR, fname)) as f:
            data = json.load(f)
        ids = set(data.keys())
        valid |= ids
        per_mod[mod] = ids
    return valid, per_mod

def snbt_str(s):
    # Double any literal backslashes first (standard SNBT string escaping).
    s = s.replace("\\", "\\\\")
    # FTB Quests reads "&" as a formatting-code trigger (e.g. "&c" = color).
    # To get a literal "&" past FTB's own parser, the parsed string must contain
    # the two characters \& — which means the SNBT file must contain \\& (the
    # \\ decodes to one backslash during SNBT parsing, leaving \& for FTB).
    s = s.replace("&", "\\\\&")
    s = s.replace('"', '\\"')
    return f'"{s}"'

def snbt_list_str(items, indent):
    if not items:
        return "[ ]"
    pad = "\t" * indent
    inner_pad = "\t" * (indent + 1)
    lines = [f"{inner_pad}{snbt_str(i)}" for i in items]
    return "[\n" + "\n".join(lines) + f"\n{pad}]"

def write_task(task, indent, seed_prefix, idx):
    pad = "\t" * indent
    inner = "\t" * (indent + 1)
    tid = gen_id(f"{seed_prefix}:task:{idx}")
    ttype = task.get("type", "item")
    lines = [f"{pad}{{"]
    lines.append(f"{inner}id: {snbt_str(tid)}")
    lines.append(f"{inner}type: {snbt_str(ttype)}")
    if ttype == "item":
        count = task.get("count", 1)
        lines.append(f"{inner}item: {snbt_str(task['item'])}")
        if count != 1:
            lines.append(f"{inner}count: {count}")
    elif ttype == "advancement":
        lines.append(f"{inner}advancement: {snbt_str(task['advancement'])}")
    elif ttype == "checkmark":
        pass  # no extra fields — purely manual, player-clicked
    elif ttype == "kill":
        # Real FTB Quests KillTask fields, confirmed by decompiling KillTask.class:
        # "entity" (a ResourceLocation string, e.g. "minecraft:creeper") and "value" (long).
        lines.append(f"{inner}entity: {snbt_str(task['entity'])}")
        lines.append(f"{inner}value: {task.get('value', 1)}L")
    elif ttype == "biome":
        # BiomeTask writes a "biome" string: registry id or #tag.
        lines.append(f"{inner}biome: {snbt_str(task['biome'])}")
    elif ttype == "dimension":
        # DimensionTask writes "dimension" as a resource location.
        lines.append(f"{inner}dimension: {snbt_str(task['dimension'])}")
    elif ttype == "structure":
        # StructureTask writes "structure": registry id or #tag.
        lines.append(f"{inner}structure: {snbt_str(task['structure'])}")
    else:
        raise ValueError(f"unknown task type '{ttype}'")
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def write_reward(reward, indent, seed_prefix, idx):
    pad = "\t" * indent
    inner = "\t" * (indent + 1)
    rid = gen_id(f"{seed_prefix}:reward:{idx}")
    rtype = reward.get("type", "item")
    count = reward.get("count", 1)
    lines = [f"{pad}{{"]
    lines.append(f"{inner}id: {snbt_str(rid)}")
    lines.append(f"{inner}type: {snbt_str(rtype)}")
    enchant = reward.get("enchant")
    if enchant:
        # Real ItemReward field, confirmed by decompiling ItemReward.class: "item" is a
        # full saved ItemStack (id/count/components), the same vanilla 1.20.5+ format
        # used everywhere in Minecraft — not an FTB-specific guess. stored_enchantments
        # is the standard vanilla component for a pre-enchanted book.
        lines.append(f"{inner}item: {{")
        lines.append(f"{inner}\tid: {snbt_str(reward['item'])}")
        lines.append(f"{inner}\tcount: {count}")
        lines.append(f"{inner}\tcomponents: {{")
        lines.append(f'{inner}\t\t"minecraft:stored_enchantments": {{')
        lines.append(f"{inner}\t\t\tlevels: {{")
        lines.append(f'{inner}\t\t\t\t"{enchant["id"]}": {enchant["level"]}')
        lines.append(f"{inner}\t\t\t}}")
        lines.append(f"{inner}\t\t}}")
        lines.append(f"{inner}\t}}")
        lines.append(f"{inner}}}")
    else:
        lines.append(f"{inner}item: {snbt_str(reward['item'])}")
        if count != 1:
            lines.append(f"{inner}count: {count}")
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def write_quest(q, key_to_id, indent, chapter_key, resolve_dep):
    pad = "\t" * indent
    inner = "\t" * (indent + 1)
    qid = key_to_id[q["key"]]
    # "source" lets a quest keep the id-seed of the chapter it originally belonged
    # to even after being merged into a new chapter file — see main() below.
    seed_prefix = f"quest:{q.get('source', chapter_key)}:{q.get('source_key', q['key'])}"
    x = q.get("x", 0) * SPACING
    y = q.get("y", 0) * SPACING
    lines = [f"{pad}{{"]
    lines.append(f"{inner}id: {snbt_str(qid)}")
    lines.append(f"{inner}x: {x:.1f}d")
    lines.append(f"{inner}y: {y:.1f}d")
    lines.append(f"{inner}title: {snbt_str(q['title'])}")
    lines.append(f"{inner}icon: {snbt_str(q['icon'])}")
    # Real Quest fields (confirmed via decompiled Quest.class): "shape" (e.g.
    # "hexagon") and "size" (a double multiplier) — used to visually emphasize
    # major achievement/capstone quests, matching FTB's own built-in "goal" preset
    # (hexagon, size 2.0) seen in a freshly-saved data.snbt.
    if q.get("shape"):
        lines.append(f"{inner}shape: {snbt_str(q['shape'])}")
    if q.get("size"):
        lines.append(f"{inner}size: {q['size']:.1f}d")
    desc = q.get("description") or []
    if desc:
        lines.append(f"{inner}description: {snbt_list_str(desc, indent+1)}")
    if q.get("hidden"):
        lines.append(f"{inner}hide_details_until_startable: true")
    tasks = q.get("tasks", [])
    if tasks:
        task_lines = ",\n".join(write_task(t, indent+2, seed_prefix, i) for i, t in enumerate(tasks))
        lines.append(f"{inner}tasks: [\n{task_lines}\n{inner}]")
    rewards = q.get("rewards", [])
    if rewards:
        reward_lines = ",\n".join(write_reward(r, indent+2, seed_prefix, i) for i, r in enumerate(rewards))
        lines.append(f"{inner}rewards: [\n{reward_lines}\n{inner}]")
    deps = q.get("dependencies", [])
    if deps:
        dep_ids = [resolve_dep(chapter_key, d) for d in deps]
        lines.append(f"{inner}dependencies: {snbt_list_str(dep_ids, indent+1)}")
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def check_chapter_items(spec, valid_items, errors):
    key = spec["key"]
    quests = spec["quests"]

    # A leading "#" marks an item TAG reference (e.g. "#relics:relic"), which isn't a
    # single registry id and so isn't checked against verified_items.json — tag
    # references must be hand-verified against the real mod data before use.
    def check_item(item_id, ctx):
        if item_id.startswith("#"):
            return
        if item_id not in valid_items:
            errors.append(f"[{key}] {ctx}: unknown item id '{item_id}'")

    check_item(spec["icon"], "chapter icon")
    for q in quests:
        check_item(q["icon"], f"quest '{q['key']}' icon")
        for t in q.get("tasks", []):
            ttype = t.get("type", "item")
            if ttype == "item":
                check_item(t["item"], f"quest '{q['key']}' task item")
            elif ttype == "advancement":
                if not t.get("advancement"):
                    errors.append(f"[{key}] quest '{q['key']}' advancement task missing 'advancement' id")
            elif ttype == "checkmark":
                pass
            elif ttype == "kill":
                if not t.get("entity"):
                    errors.append(f"[{key}] quest '{q['key']}' kill task missing 'entity' id")
            elif ttype == "biome":
                if not t.get("biome"):
                    errors.append(f"[{key}] quest '{q['key']}' biome task missing 'biome' id")
            elif ttype == "dimension":
                if not t.get("dimension"):
                    errors.append(f"[{key}] quest '{q['key']}' dimension task missing 'dimension' id")
            elif ttype == "structure":
                if not t.get("structure"):
                    errors.append(f"[{key}] quest '{q['key']}' structure task missing 'structure' id")
            else:
                errors.append(f"[{key}] quest '{q['key']}' unknown task type '{ttype}'")
        for r in q.get("rewards", []):
            check_item(r["item"], f"quest '{q['key']}' reward item")
        if not q.get("tasks"):
            errors.append(f"[{key}] quest '{q['key']}' has no tasks")

def write_image(img, indent, seed_prefix, idx):
    # Real ChapterImage fields, confirmed by decompiling ChapterImage.class AND by
    # observing a live FTB-Quests round-trip: an earlier attempt wrote "text_on_image"
    # as a list of strings (the actual label text) and FTB silently discarded it on
    # load — only x/y/width/height/rotation/image/id survived the resave. Re-checking
    # the class confirms why: ChapterImage inherits a plain "title" field from
    # QuestObjectBase (same as every chapter/group/quest), and "text_on_image" is
    # really a BOOLEAN toggle (backing method: shouldDrawTextOnImage()) for whether
    # that title renders on top of the image — not the text itself.
    pad = "\t" * indent
    inner = "\t" * (indent + 1)
    iid = gen_id(f"{seed_prefix}:image:{idx}")
    x = img["x"] * SPACING
    y = img["y"] * SPACING
    label = img["text"][0] if isinstance(img["text"], list) else img["text"]
    _localized_titles[f"image.{iid}.title"] = label
    lines = [f"{pad}{{"]
    lines.append(f"{inner}id: {snbt_str(iid)}")
    lines.append(f"{inner}title: {snbt_str(label)}")
    lines.append(f"{inner}x: {x:.1f}d")
    lines.append(f"{inner}y: {y:.1f}d")
    lines.append(f"{inner}width: {img.get('width', 6) * SPACING:.1f}d")
    lines.append(f"{inner}height: {img.get('height', 1) * SPACING:.1f}d")
    lines.append(f"{inner}text_on_image: true")
    lines.append(f"{inner}text_h_align: {snbt_str('MIDDLE')}")
    lines.append(f"{inner}text_v_align: {snbt_str('MIDDLE')}")
    lines.append(f"{pad}}}")
    return "\n".join(lines)

def write_chapter(spec, group_id, key_to_id, resolve_dep):
    key = spec["key"]
    quests = spec["quests"]
    chapter_id = key_to_id["__chapter__"]
    _localized_titles[f"chapter.{chapter_id}.title"] = spec["title"]

    quest_blocks = ",\n".join(write_quest(q, key_to_id, 2, key, resolve_dep) for q in quests)

    subtitle = spec.get("subtitle", "")
    lines = []
    lines.append("{")
    lines.append(f'\tid: {snbt_str(chapter_id)}')
    lines.append(f'\tgroup: {snbt_str(group_id)}')
    lines.append(f'\torder_index: {spec.get("order_index", 0)}')
    lines.append(f'\tfilename: {snbt_str(key)}')
    lines.append(f'\ttitle: {snbt_str(spec["title"])}')
    if subtitle:
        lines.append(f'\tsubtitle: {snbt_str(subtitle)}')
    lines.append(f'\ticon: {snbt_str(spec["icon"])}')
    lines.append('\tdefault_quest_shape: "square"')
    lines.append('\tdefault_hide_dependency_lines: false')
    images = spec.get("images", [])
    if images:
        image_blocks = ",\n".join(write_image(img, 2, f"chapter:{key}", i) for i, img in enumerate(images))
        lines.append(f'\timages: [\n{image_blocks}\n\t]')
    lines.append(f'\tquests: [\n{quest_blocks}\n\t]')
    lines.append("}")
    return key, "\n".join(lines) + "\n"

def main():
    _used_ids.clear()
    _localized_titles.clear()
    valid_items, per_mod = load_valid_items()
    print(f"Loaded {len(valid_items)} valid item ids across {len(per_mod)} namespaces")

    with open(os.path.join(SPECS_DIR, "groups.json")) as f:
        groups = json.load(f)

    group_ids = {g["key"]: gen_id(f"group:{g['key']}") for g in groups}

    errors = []
    chapter_files = {}
    order = []

    chapter_specs = []
    for fname in sorted(os.listdir(CHAPTERS_SPEC_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(CHAPTERS_SPEC_DIR, fname)) as f:
            try:
                spec = json.load(f)
            except Exception as e:
                errors.append(f"[{fname}] JSON parse error: {e}")
                continue
        chapter_specs.append((fname, spec))

    # sort by (group order_index, chapter order_index) for stable global order
    def sort_key(item):
        fname, spec = item
        g = next((g for g in groups if g["key"] == spec.get("group")), None)
        return (g["order_index"] if g else 999, spec.get("order_index", 0))
    chapter_specs.sort(key=sort_key)

    for fname, spec in chapter_specs:
        check_chapter_items(spec, valid_items, errors)
        gkey = spec.get("group")
        if gkey not in group_ids:
            errors.append(f"[{fname}] unknown group '{gkey}'")

    # Pass 1: assign every chapter's and quest's id up front, across ALL chapters,
    # before writing anything out. This lets dependencies reference quests in a
    # different chapter (e.g. "taking_to_the_skies:first_flight") — FTB dependencies
    # are just global quest-id references, so this is a real, supported pattern, not
    # a workaround. A quest's id is seeded on its "source" chapter key when present
    # (the chapter it originally lived in, before a reorg merged chapters together)
    # so moving quests between chapter files never changes their id.
    all_key_to_id = {}  # chapter_key -> {"__chapter__": id, quest_key: id, ...}
    quest_owner = {}    # (chapter_key, quest_key) -> True, for dependency validation
    for fname, spec in chapter_specs:
        key = spec["key"]
        mapping = {"__chapter__": gen_id(f"chapter:{key}")}
        for q in spec["quests"]:
            mapping[q["key"]] = gen_id(f"quest:{q.get('source', key)}:{q.get('source_key', q['key'])}")
            quest_owner[(key, q["key"])] = True
        all_key_to_id[key] = mapping

    def resolve_dep(current_chapter_key, dep):
        if ":" in dep:
            dep_chapter, dep_key = dep.split(":", 1)
        else:
            dep_chapter, dep_key = current_chapter_key, dep
        if (dep_chapter, dep_key) not in quest_owner:
            errors.append(f"[{current_chapter_key}] dependency '{dep}' does not resolve to any known quest")
            return "0000000000000000"
        return all_key_to_id[dep_chapter][dep_key]

    # Now that every id is known, validate dependencies (deferred until after pass 1
    # since a cross-chapter dependency can't be checked until all chapters are loaded).
    for fname, spec in chapter_specs:
        key = spec["key"]
        for q in spec["quests"]:
            for d in q.get("dependencies", []):
                resolve_dep(key, d)

    if errors:
        print(f"\n{len(errors)} VALIDATION ERRORS — no files written:\n")
        for e in errors:
            print(" -", e)
        sys.exit(1)

    # Pass 2: write every chapter out using the ids already assigned in pass 1.
    for fname, spec in chapter_specs:
        gkey = spec.get("group")
        key, content = write_chapter(spec, group_ids[gkey], all_key_to_id[spec["key"]], resolve_dep)
        chapter_files[key] = content
        order.append(key)

    chapters_dir = os.path.join(OUT_DIR, "chapters")
    os.makedirs(chapters_dir, exist_ok=True)
    # Remove stale chapter files left over from specs that were renamed/deleted —
    # otherwise a retired chapter (e.g. the old create_aeronautics.json) keeps
    # showing up in-game forever even after its spec is gone.
    for fname in os.listdir(chapters_dir):
        if fname.endswith(".snbt") and fname[:-5] not in chapter_files:
            os.remove(os.path.join(chapters_dir, fname))
            print(f"Removed stale chapter file: {fname}")
    for key, content in chapter_files.items():
        with open(os.path.join(chapters_dir, f"{key}.snbt"), "w") as f:
            f.write(content)

    # FTB loads groups in array order. Chapter order_index is read by the
    # quest-file loader's comparator; groups do not have a chapters field.
    cg_lines = ["{", "\tchapter_groups: ["]
    for g in sorted(groups, key=lambda g: g["order_index"]):
        _localized_titles[f"chapter_group.{group_ids[g['key']]}.title"] = g["title"]
        cg_lines.append("\t\t{")
        cg_lines.append(f'\t\t\tid: {snbt_str(group_ids[g["key"]])}')
        cg_lines.append(f'\t\t\ttitle: {snbt_str(g["title"])}')
        cg_lines.append("\t\t}")
    cg_lines.append("\t]")
    cg_lines.append("}")
    with open(os.path.join(OUT_DIR, "chapter_groups.snbt"), "w") as f:
        f.write("\n".join(cg_lines) + "\n")

    # data.snbt — real field set, confirmed by decompiling BaseQuestFile.class and by
    # reading back a genuinely FTB-Quests-resaved data.snbt (the schema this project
    # assumed at first — chapter_groups/order/reward_tables/title_icon/etc — turned out
    # to not exist at all; FTB just silently ignores unrecognized fields and applies its
    # own defaults, which is why nothing broke, but nothing we wrote there ever took
    # effect either). These are exactly FTB's own defaults, so this is a no-op vs not
    # writing the file at all, kept here so the file is honest about what really exists.
    data_content = """{
\tdefault_autoclaim_rewards: "disabled"
\tdefault_consume_items: false
\tdefault_quest_disable_jei: false
\tdefault_quest_shape: ""
\tdefault_reward_team: false
\tdetection_delay: 20
\tdisable_gui: false
\tdrop_book_on_death: false
\tdrop_loot_crates: false
\temergency_items_cooldown: 0
\tfallback_locale: ""
\tgrid_scale: 0.5d
\thide_excluded_quests: false
\tlock_message: ""
\tloot_crate_no_drop: {
\t\tboss: 0
\t\tmonster: 600
\t\tpassive: 4000
\t}
\tpause_game: false
\tpresets: {
\t\tgoal: {
\t\t\tshape: "hexagon"
\t\t\tsize: 2.0d
\t\t}
\t\tinfo: {
\t\t\tshape: "gear"
\t\t\tsize: 1.0d
\t\t}
\t\tnormal: {
\t\t\tshape: "square"
\t\t\tsize: 1.0d
\t\t}
\t}
\tprogression_mode: "linear"
\tshow_lock_icons: true
\tverify_on_load: false
\tversion: 13
}
"""
    with open(os.path.join(OUT_DIR, "data.snbt"), "w") as f:
        f.write(data_content)

    # FTB moves inline titles into its language file when saving. Keep existing
    # translations in sync so old section names cannot override regenerated ones.
    lang_path = os.path.join(OUT_DIR, "lang", "en_us.snbt")
    if os.path.exists(lang_path):
        with open(lang_path) as f:
            language = f.read()
        for key, title in _localized_titles.items():
            line = f"\t{key}: {snbt_str(title)}"
            pattern = r"(?m)^\t" + re.escape(key) + r":.*$"
            if re.search(pattern, language):
                language = re.sub(pattern, lambda _: line, language)
            else:
                end = language.rfind("}")
                language = language[:end] + line + "\n" + language[end:]
        with open(lang_path, "w") as f:
            f.write(language)

    print(f"\nWrote {len(chapter_files)} chapters, {len(groups)} groups.")
    print(f"Output: {OUT_DIR}")

if __name__ == "__main__":
    main()
