# Worlds Further changelog

## 0.1.1

Create × magic × homestead recipe addons, and a client crash fix.

- **Create: Sourceworks** — Create crushing/mixing/mechanical crafting for Ars Nouveau (magebloom fiber, Source Gems, parchment, mill recycles). Liquid Source stays StarbuncleMania; wheel/contraptions stay Ars Creo.
- **Create: Dragonworks** — Create processing for Ice and Fire (scales, skulls, silver, hunt drops, fire dragonforge bricks). Dragonsteel stays on the Dragon Forge.
- **Ars Draconis** — Ars Nouveau imbuement/apparatus using dragon blood, lilies, silver, and bone.
- **Create: Harvestworks** — Create mill/mix/compact for Pam’s HarvestCraft 2 Food Core (flour, dough, butter, salt, cheese, oil).
- **Create: Relicworks** — Create recycle for *broken* Relics only; optional Artifacts junk. Intact relics are not crushed.
- **Spark** is disabled on the client (async-profiler native crash on Apple Silicon after world load). Dedicated servers can still ship Spark.
- **Continuity** stays disabled (needs Fabric API + Connector). Do not re-enable it in the CurseForge app.
- Do not take Loot Journal 6.2.2 or FTB XMod Compat 21.1.12 — they require Fragmentum 5 and JEI 19.53. Pack stays Fragmentum 2.4.4 and JEI 19.51.0.418.
- Complementary Reimagined: Real-Time Shadows **OFF** (`SHADOW_QUALITY=-1`) and Light Shaft Quality **OFF** (`LIGHTSHAFT_QUALI_DEFINE=0`) to stop Create Aeronautics visual glitches. Ships in `shaderpacks/*.txt` — tick **shaderpacks/** on export.
- **Soaring Traders** (Create Aeronautics: Discovery): flyovers spawn at Y **280–310**, cruise with terrain/avoid autopilot, despawn after **4 minutes**. Datapack zip in **`datapacks/`** (CurseForge Data Packs path). Tick **`config/`** and **`datapacks/`**.

## 0.1.0

First public-shaped build. NeoForge 21.1.250 / Minecraft 1.21.1.

- All instance resource packs enabled by default (base textures under overlay/CEM; Cubic then Dramatic Skys last). Complementary Reimagined r5.9.3 LOW shaders forced on via `config/iris.properties`.
- `config/defaultoptions/options.txt` matches pack `options.txt`. Add **Default Options** in the CurseForge app so those options re-apply (Balm is already present).
- Quest book regenerated from `quest-tools` (~500 quests). Iron intro gate, no lottery trinket tasks, pack keybind quest, thicker aviation/mastery lines.
- Default key layout: N quests, M map, K skills, G Curios, C Ars book, R roll, Ctrl+R dragon fire.
- Title screen uses the Worlds Further key art; window title is Worlds Further.
- Continuity, Create Factory Benchmark, Just Enough Threads, and Inventory Profiles Next are in `mods-disabled/` (disable them in the CurseForge app or they come back).
- Almost Unified recipe-viewer hiding is on. JEI hides Pam’s tomato/onion/cabbage/rice so Farmer’s Delight owns those crops. Pam’s unique meals stay.
- ScalableLux dependency override removed (that mod is not in the pack).
