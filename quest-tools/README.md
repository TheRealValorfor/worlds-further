# Quest generation

Edit `specs/groups.json` and `specs/chapters/*.json`, then run:

```sh
python3 quest-tools/add_section_labels.py
python3 quest-tools/generate_quests.py
python3 quest-tools/audit_specs.py
python3 quest-tools/validate_layout.py
```

Run from the instance directory with Minecraft closed so an in-game save cannot overwrite the generated files. Launch the instance to review the book.

The sidebar is organised by activity: Home and Homestead, Engineering and Storage, Magic and Spellcraft, Travel and Exploration, Airships and Aviation, and Combat and Mastery. Each quest has a `section` key; each section has one authored heading in the chapter's `images` list, in vertical order. Keep 1.6 grid units between normal nodes and 4 units between the last row of a section and the first row of the next. The heading helper refreshes bounds while retaining authored names.

`specs/id_map.json` preserves the IDs in the saved quest book before this reorganisation. Do not remove it or change a quest's `source` / `source_key` when moving quests: those identify existing progress. New IDs are deterministic positive 63-bit numbers because this FTB version parses them using Java's signed `Long.parseLong`. The earlier generator emitted out-of-range IDs, which FTB replaced on loading, breaking group assignments and dependencies.

The generator also synchronises section, chapter and group titles with `lang/en_us.snbt`. Item tasks, rewards and progression requirements remain defined in the chapter specs. The validator checks saved IDs, reference resolution, node/heading clearance and byte-stable regeneration. In-game visual rendering is a separate manual check.

`merge_chapters.py` is a historical migration from the original per-mod chapters, not part of the current generation workflow. Do not rerun it on the reorganised specs.

The pre-change quest files, specs and generator are backed up under `backups/20260918-095536/`. This work updates the local instance's `config/ftbquests/quests`; the server-pack directories are separate.
