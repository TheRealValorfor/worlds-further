# Worlds Further changelog

## 0.1.2 (unreleased)

Pack default is an **8 GB** Java heap (`recommendedRam` **8192**). Needs ~**16 GB** of machine RAM. 8 GB total PCs are not a target.

Configs (not just Distant Horizons):

- **DH** 48 chunks, FOUR_BLOCKS / MEDIUM (was 72 / BLOCK / HIGH)
- **Every Compat** assets **CACHED_ZIPPED** (was always held in RAM)
- **JEI** low-memory search
- **Quantified API / Sable / Aeronautics** left on stock GPU settings (`enableGpuAcceleration`, `VULKAN_PREFERRED`, default thread pools)
- **Ice and Fire** smaller dragon pathing / target range, smaller bird flocks, siren post-shader off
- **Health Bars** crosshair-only, no 3D GUI preview, 24-block world bars (also cuts the Sable AABB spam)
- **Create FPS Optimizer** shorter BE/contraption/particle distances; lower fan particle density
- **FTB Chunks** releases map regions sooner; 3×3 biome blend
- **Particle Rain / Particular / Visuality** lower particle budgets
- **Sound Physics** shorter clone range and fewer occlusion rays
- **Flywheel** 2 workers; Sodium 1 frame of render-ahead; mipmaps 2; entity distance 80%
- FerriteCore compact maps, AllTheLeaks ingredient dedupe, Legendary Tooltips no 3D item models

Vanilla render distance stays **4**. Raise DH / particles locally if you allocate 10–12 GB.

New performance addons: **Structure Layout Optimizer** 1.0.12, **Noisium** 2.3.0 (Modrinth; CF project is archived), **Particle Core** 0.3.3. **Let Me Despawn** was dropped — **Performance Tweaks** already injects the same despawn mixin (bootstrap crash).

**FTB Obsidian** 21.1.0 — CurseForge Data Packs loader. Auto-loads instance `datapacks/` (no extra config). Moonlight `global_datapacks_folder` is empty so Soaring Traders is not loaded twice. Replaces Global Packs.

Safe CurseForge updates taken (1.21.1 NeoForge patches): Sodium 0.8.13 + Sodium Extra 0.9.4, Entity Culling 1.11.1, Central Kitchen 2.6.1, Dragons Plus 1.11.9, Create Advanced Optimization 1.5, Polytone 4.5.0, Redomesticate 1.11.0, MOS 1.1.1, MMV 2.2.0, MSS 2.2.0, Naturalist 2.0.4, Lootr 1.11.38.126, Collective 8.40, Moonlight 3.6.7, Ice and Fire CE 2.1.3, Slice & Dice 4.3.4.

**Not taken:** Fragmentum 5, Loot Journal 6.2.2, FTB XMod Compat 21.1.12 (JEI/Fragmentum break). **Create Aeronautics Discovery 2.2.0** (soaring-trader datapack is built on 2.1.4).

**Furtherworks** — pack trophy. Mechanical-craft four hearts then **The Further**; spend it on Creative Motor / Fluid Tank / Blaze Cake / Physics Staff. GitHub [v1.0.3](https://github.com/TheRealValorfor/furtherworks/releases/tag/v1.0.3). Not a CurseForge addon yet (cannot go in `manifest.json` until a CF project exists). Mastery ends on The Further.

Resource packs: **Create Style Sophisticated Storages** (Luna), **Tom's Create Style** (ogabasferr), **ANBICS** (Fr_z_n), **SolidSails Soft** (speedbuiz), **Aeronautics Hot Air Shader Fix** (Tr0nCrafts), **Low Fire** (Oculie). **Dramatic Skys** and **Better Ores 3D** removed. **Create: Relicworks** is a CurseForge addon (no `overrides/mods/` jar). **Soaring Trader Flyovers** is a CurseForge datapack addon as well as `datapacks/`.

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
