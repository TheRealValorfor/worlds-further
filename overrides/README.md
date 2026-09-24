# Worlds Further — CurseForge export checklist

**CurseForge pack:** [worlds-further](https://www.curseforge.com/minecraft/modpacks/worlds-further)

Minecraft **1.21.1** / NeoForge **21.1.250**. **Do not bump mod versions** for this export. **Do not** drop CurseForge-hosted jars into `overrides/mods/` — those must stay instance addons.

This page is the **single source of truth** for what to tick in the CurseForge app. RAM / Additional Java Arguments **do not ship** in the export zip.

## Do this in the CurseForge app before Export

1. **Disable these in the instance content list** (or they reappear on refresh / get listed in the zip). Jars already live in `mods-disabled/` so the game does not load them — the UI toggle is what keeps them out of the pack:
   - **Continuity** (must **not** export as an enabled addon)
   - **Just Enough Threads**
   - **Create Factory Benchmark**
   - **Inventory Profiles Next** (disabling this is enough for **libIPN**)
2. Resource packs are CurseForge texture-pack addons (not `overrides/resourcepacks/`). Do not re-enable **Dramatic Skys** or **Better Ores 3D**.
3. **Add Default Options** via **Add More Content → Mods** (search **Default Options**). **Balm is already installed.** Do **not** pirate a jar into `mods/`. `config/defaultoptions/options.txt` is already wired to match live options. Without the mod, `options.txt` only applies on **first install**.
4. Complementary Shaders - Reimagined **r5.9.3** is already a shader addon. Do not bump. Do not add Euphoria Patcher.
5. **Soaring Trader Flyovers** is a CurseForge Data Packs addon **and** the zip in `datapacks/` (FTB Obsidian). Same filename — do not add a second copy.
6. **Fully quit Minecraft** (not just disconnect). Relaunch this instance once so configs rewrite in final form. Confirm: title screen key art, window title **Worlds Further**, shaders **on** / Complementary LOW, resource packs selected.

## CurseForge Export Profile — tick these

Profile options → **Export Profile**. Ticked paths become `overrides/` in the zip. That is how other players get configs.

| Tick | Why |
|---|---|
| **`config/`** | Sodium, Iris (`iris.properties`: shaders forced on), Distant Horizons, FancyMenu assets (`config/fancymenu/`, including title art), HUD tweaks, Shoulder Surfing, `config/defaultoptions/`, FTB Quests (`config/ftbquests/` — **this pack does not use `kubejs/`**). **Skip this and shaders will not be on.** |
| **`shaderpacks/`** | Official Complementary zip **and** the settings `.txt` files (Real-Time Shadows **OFF**, light shafts **OFF**). Does **not** create the shader addon entry (Complementary is already added via **Add More Content → Shaders**). |
| **`resourcepacks/`** | Not used. Resource packs are CurseForge addons in `manifest.json` (ROP, Luna backpacks/storage, Tom's Create Style, ANBICS, SolidSails, Hot Air Fix, Low Fire, Fresh Animations, etc.). |
| **`options.txt`** | If the exporter lists it: vanilla defaults + **all resource packs enabled** + pack keybinds. First install only unless Default Options is in the pack. |
| **`defaultconfigs/`** | Copied into **new worlds** as `serverconfig/` (not used by Iris). Tick it; this pack uses it. |
| **`datapacks/`** | CurseForge Data Packs folder (`SoaringTraderFlyovers-1.0.0.zip`). **FTB Obsidian** loads this for every world (no extra config). Moonlight's global folder is off so packs are not applied twice. **Skip this and trader planes stay on the mod defaults (Y 220, no avoid).** |
| **`README.md`** | Players see RAM + JVM instructions (those settings never auto-apply). |
| **`CHANGELOG.md`** | Listing history. |

If the exporter shows **`kubejs/`**, tick it **only if that folder exists**. It does **not** exist in this instance today. Quests ship with **`config/`**.

### Do **not** tick

| Path | Why |
|---|---|
| **`mods-disabled/`** | Disabled jars. Ticking this would stuff them into `overrides/mods/` and risk review rejection / loading them again. |
| **`saves/`** | Your worlds (tick only if you *want* to ship a world). |
| **`logs/`**, **`crash-reports/`**, **`hs_err_*.log`**, **`replay_*.log`** | Noise. |
| **`.cursor/`**, **`.nitro/`**, **`.mixin.out/`**, **`.cache/`**, **`.sable/`** | Local / generated. |
| **`local/`** | Your FTB Chunks map data. |
| **`Distant_Horizons_server_data/`** | Your LOD cache. |
| **`dynamic-data-pack-cache/`**, **`dynamic-resource-pack-cache/`**, **`particular_cache/`** | Regenerated on launch. |
| **`server-pack/`** | Dedicated NeoForge tree from ServerPackCreator. Use `scripts/export-server.sh` to regenerate. Do not tick for the **client** export. |
| **`quest-tools/`** | Python quest pipeline, not the game. Do **not** run `merge_chapters.py`. |
| **`downloads/`**, **`screenshots/`**, **`schematics/`**, **`pack-art/`** | Personal / source art (in-game title art is already under `config/fancymenu/assets/`). |
| **`fancymenu_data/`** | Last-world cache, not the layout. Layouts/assets are in `config/fancymenu/`. |
| **`usercache.json`**, **`usernamecache.json`**, **`command_history.txt`** | Machine-specific. |
| **`minecraftinstance.json`** | CurseForge regenerates this. |
| **`user_jvm_args.txt`**, **`ADDITIONAL_JVM_ARGS.txt`** | Harmless if ticked, but they **do not** set player RAM or Java args in the CurseForge app. |

`mods/` is **not** an override folder in a normal export. CurseForge writes mods into `manifest.json` from the instance addon list. Only put a jar in `overrides/mods/` if it is on the [approved third-party list](https://support.curseforge.com/en/support/solutions/articles/9000198500-exporting-a-modpack-for-curseforge-project-submission) **and** is **not** on CurseForge.

## After export — unzip and check

- `manifest.json` + `overrides/` at the **root** of the zip (not nested in an extra folder)
- `overrides/config/iris.properties` → `enableShaders=true`, `shaderPack=ComplementaryReimagined_r5.9.3.zip`, `maxShadowRenderDistance=10`
- `overrides/shaderpacks/ComplementaryReimagined_r5.9.3.zip` **and** `ComplementaryReimagined_r5.9.3.zip.txt` (Real-Time Shadows **OFF**, light shafts **OFF**). No unpacked shader folder. No old `+ EuphoriaPatches` combined zip
- `manifest.json` lists **Complementary Shaders - Reimagined** (shader addon)
- `overrides/config/DistantHorizons.toml` exists (`maxHorizontalResolution = "BLOCK"`, `horizontalQuality = "HIGH"`, `lodChunkRenderDistanceRadius = 72`)
- `overrides/config/fancymenu/assets/worlds_further_title.png` exists
- `overrides/config/ftbquests/` exists
- `overrides/config/aeronauticsdiscovery-common.toml` has `maxLifetimeTicks = 4800`, `obstacleCheck = true`, `raycastPrecision = "HIGH"`
- `overrides/datapacks/SoaringTraderFlyovers-1.0.0.zip` exists
- `overrides/config/moonlight-common.toml` has `global_datapacks_folder = ""` (FTB Obsidian owns instance `datapacks/`)
- `overrides/config/defaultoptions/options.txt` has the same `resourcePacks` list as `overrides/options.txt`
- `overrides/mods/` is empty or only approved non-CurseForge jars
- **Continuity / JET / Factory Benchmark / IPN** are **not** enabled addons in `manifest.json`

Then install that zip into a **clean** test instance. **Full quit and relaunch** before you judge shaders, packs, or DH.

## Default Options (missing as an addon)

**Default Options is not in this instance.** `config/defaultoptions/options.txt` is already a copy of the pack `options.txt` (resource packs, Fancy graphics, keybinds, render **4** / simulation **8**). Add the mod in the CurseForge app so those defaults **re-apply** for every new install and pack update. Balm is already present.

| Setting | How players get it |
|---|---|
| Shaders on, Complementary r5.9.3, shadows and light shafts off | **`config/iris.properties`** + **`shaderpacks/*.txt`**. Ships whenever **`config/`** and **`shaderpacks/`** are ticked. Does **not** need Default Options. |
| Distant Horizons, FancyMenu, HUD, Shoulder Surfing, quests | **`config/`**. Same as above. |
| Resource packs selected, vanilla options, pack keybinds | **`options.txt`** on **first install only**. **Default Options** is what reapplies them after that. |

## Shaders (Complementary, forced on)

`config/iris.properties`: `enableShaders=true`, `shaderPack=ComplementaryReimagined_r5.9.3.zip`, `maxShadowRenderDistance=10`.

Shader defaults in `shaderpacks/ComplementaryReimagined_r5.9.3.zip.txt` **and** `shaderpacks/ComplementaryReimagined_r5.9.3.txt`: `SHADOW_QUALITY=-1` (Real-Time Shadows **OFF**), `LIGHTSHAFT_QUALI_DEFINE=0` (Light Shaft Quality **OFF**), FXAA off. Required for Create Aeronautics (Sable) visual glitches. Iris loads `shaderpacks/<shaderPackName>.txt`.

Official zip: CurseForge shader addon **Complementary Shaders - Reimagined** r5.9.3. Pin **r5.9.3**. [Euphoria Patches](https://www.curseforge.com/minecraft/mc-mods/euphoria-patches) is **not** in the pack; do not add it for this export.

## Resource packs (all selected)

Last in the `resourcePacks` list wins. Create restyles sit on the base packs. SolidSails, Hot Air Fix, then **Low Fire** last.

Bottom → top: ROP → CreateSophBackpacks → CreateSophiStorage → Tom's Create Style → ANBICS → Boss Refreshed → Fresh Animations → Freshly Modded → Torrezx-Glowy → Cubic Sun & Moon → SolidSails Soft → Aeronautics Hot Air Fix → Low Fire.

Dramatic Skys, 3D Ores, and Better Ores 3D are **not** in the pack. Continuity is **not** enabled. Do not turn it back on.

## JVM arguments (does **not** ship)

`manifest.json` `recommendedRam` is **8192**, so a CurseForge install should default the Memory slider to **8 GB**. Extra JVM flags still do **not** ship with the app — paste this in the project description:

> Allocate **8 GB RAM** (instance settings → Memory). Then Additional Java Arguments:

```
-XX:+UnlockExperimentalVMOptions -XX:+UseZGC -XX:+ZGenerational -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:MaxMetaspaceSize=1g -Dfile.encoding=UTF-8 -Dstdout.encoding=UTF-8 -Dstderr.encoding=UTF-8 -Dlog4j2.formatMsgNoLookups=true
```

That string is in `ADDITIONAL_JVM_ARGS.txt`. Do **not** also paste `-Xmx`; the memory slider already adds it. ZGC needs **Java 21** (CurseForge bundled runtime). Do **not** add Nitro’s `-javaagent:.../.nitro/...`.

**8 GB heap** is the pack default. Distant Horizons is only one of the knobs: Every Compat caches to disk, JEI uses low-memory search, Ice and Fire pathing is smaller, Health Bars are crosshair-only, Create/particle/sound budgets are lower. Complementary shadows stay off. Quantified / Sable / Aeronautics GPU settings are **unchanged** (Vulkan preferred). That still needs a machine with **about 16 GB physical RAM**. A PC with only 8 GB total RAM cannot run this pack. Raise the slider to 10–12 GB if you bump DH or particle quality back up.

## What `config/` already forces (if ticked)

- Complementary **LOW**, shaders **on**, Iris shadow distance **10**
- DH ~**48** chunks, **FOUR_BLOCKS** / **MEDIUM**, surface-only distant gen, 2 worker threads
- Every Compat **CACHED_ZIPPED**; JEI low-memory search
- Ice and Fire pathing/target/flock reduced; Health Bars picked-entity only
- Create FPS Optimizer shorter render/particle distances; Particle Rain/Particular/Visuality lower density
- Vanilla render **4**, simulation **8**, graphics **Fancy**, mipmaps **2**, entity distance **0.8**
- Mac Retina resolution reduction on; Flywheel lighting **TRI_LINEAR**, 2 worker threads
- Dynamic Render Distance HUD **off**; Inventory HUD empty arrows **hidden**; Combat Roll prompt **left of hotbar**; FTB sidebar **top_left**; Shoulder Surfing **over-shoulder** default
- Pack keybinds: quests **N**, map **M**, skills **K**, Curios **G**, Ars book **C**, roll **R**, backpack **Shift+E**, Tom's terminal **B**, shaders **F6**, configs **`**

## After upload

1. Create/update the CurseForge project (logo ≥ 400×400, real description).
2. Upload the export zip as a new file.
3. Paste RAM + JVM instructions in the description.
4. Install into a **clean** test instance, **full restart**, then confirm: shaders on (Complementary LOW), all resource packs on, DH LODs, quests, title art, no Continuity/JET/IPN/Factory Benchmark.

## Local launch (this folder)

CurseForge profile **Worlds further**: memory override **on**, **8 GB**; Additional Java Arguments = contents of `ADDITIONAL_JVM_ARGS.txt`. That lives in `minecraftinstance.json` on this machine only.

## Pack review leftovers (not version bumps)

- **Continuity / JET / Factory Benchmark / IPN + libIPN** → `mods-disabled/`. Disable in the CurseForge UI or they return. Do not add Connector / Forgified Fabric API to “fix” Continuity.
- Do not bring back **ScalableLux**, **Better Third Person**, **GPUTape**, or **zfastnoise**.
- FTB Quests live in **`config/ftbquests/`** (generated from `quest-tools/`). Do **not** rerun `merge_chapters.py`. Minecraft must be closed when regenerating.
- Dynamic Trees + Every Compat still log broken bioshroom/snowblossom assets (visual/log noise, not a boot crash).
- `server-pack/` is the dedicated NeoForge tree (not a CurseForge client override). Regenerate with `./scripts/export-server.sh`. Start with **`start.bat`** (Windows), **`start.command`** (macOS), or **`start.sh`** (Linux) after setting `eula=true`. First start downloads ServerStarterJar; the generator does not run Minecraft.
