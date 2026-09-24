# Worlds Further

**CurseForge:** [worlds-further](https://www.curseforge.com/minecraft/modpacks/worlds-further)

Minecraft **1.21.1** / NeoForge **21.1.250** modpack. Git tracks the CurseForge **client export** (`manifest.json` + `overrides/`) plus a slim **`server/`** tree for dedicated hosts.

This is **not** a dump of every mod jar. CurseForge installs those from `manifest.json`. Do not add CurseForge-hosted jars to `overrides/mods/` once they are project addons.

## CurseForge vs this repo

| | CurseForge export zip | This git repo |
|---|---|---|
| Players | Install the pack file in the CurseForge app | Source of truth for configs, quests, shader settings, datapack zip |
| Mods | Downloaded as addons | Listed in `manifest.json` only |
| Dedicated server | Optional extra file on the same version | Nested `server/` (scripts + generator). **Not** a second GitHub repo |

## Server: nested, not a separate repo

Keep the dedicated server **inside this repository** (`server/`). Client and server share one version (currently **0.1.1**), the same configs, and the same Soaring Trader datapack. A second repo would drift.

What is **not** in git: `server/mods/` (~400 MB of jars). Generate those with ServerPackCreator from the instance, or ship `export/WorldsFurther-0.1.1-server.zip` as the CurseForge **Server Pack** file. See [`server/README.md`](server/README.md).

## Layout

```
manifest.json          CurseForge addon list
modlist.html           Human-readable addon list
overrides/             What the CF app ticked: config, datapacks, shader .txt, README, CHANGELOG
server/                Dedicated start scripts, JVM args, SPC conf, datapack zip
profileImage/          Pack icon
```

`overrides/mods/` should stay empty except archived **Noisium** (`noisium-neoforge-2.3.0+mc1.21-1.21.1.jar`). **Furtherworks** and **Create: Relicworks** are CurseForge addons.

## Related projects (TheRealValorfor)

| GitHub | CurseForge |
|---|---|
| [furtherworks](https://github.com/TheRealValorfor/furtherworks) | [furtherworks](https://www.curseforge.com/minecraft/mc-mods/furtherworks) |
| [create-sourceworks](https://github.com/TheRealValorfor/create-sourceworks) | [create-sourceworks](https://www.curseforge.com/minecraft/mc-mods/create-sourceworks) |
| [create-dragonworks](https://github.com/TheRealValorfor/create-dragonworks) | [create-dragonworks](https://www.curseforge.com/minecraft/mc-mods/create-dragonworks) |
| [ars-draconis](https://github.com/TheRealValorfor/ars-draconis) | [ars-draconis](https://www.curseforge.com/minecraft/mc-mods/ars-draconis) |
| [create-harvestworks](https://github.com/TheRealValorfor/create-harvestworks) | [create-harvestworks](https://www.curseforge.com/minecraft/mc-mods/create-harvestworks) |
| [create-relicworks](https://github.com/TheRealValorfor/create-relicworks) | [create-relicworks](https://www.curseforge.com/minecraft/mc-mods/create-relicworks) |
| [soaring-trader-flyovers](https://github.com/TheRealValorfor/soaring-trader-flyovers) | [soaring-trader-flyovers](https://www.curseforge.com/minecraft/data-packs/soaring-trader-flyovers) |
| [skill-progression-enhanced-ui](https://github.com/TheRealValorfor/skill-progression-enhanced-ui) | [skill-progression-enhanced-ui](https://www.curseforge.com/minecraft/mc-mods/skill-progression-enhanced-ui) |

## Apply git changes to a local CurseForge instance

This repository is **public**. After `git pull`, anyone on **Windows, macOS, or Linux** can copy pack configs, datapacks, and shader settings onto their CurseForge instance **without** replacing addons.

You need **Python 3** (stdlib only). Minecraft must be fully quit.

```bash
# macOS / Linux / Git Bash
python3 scripts/apply-to-instance.py
# or
./scripts/apply-to-instance.sh
```

```powershell
# Windows PowerShell
py scripts\apply-to-instance.py
# or
.\scripts\apply-to-instance.ps1
```

Useful flags (same on every OS):

| Flag | Meaning |
|---|---|
| `--dry-run` | Print copies; write nothing |
| `--instance PATH` | CurseForge instance folder (`mods/` + `config/`) |
| `--skip-options` | Keep the player's `options.txt` / keybinds |
| `--skip-jars` | Do not copy `overrides/mods/*.jar` |

Auto-detect looks for a profile or folder named **Worlds further** / **Worlds Further** / **WorldsFurther** under the usual CurseForge `Instances` directories (`~/Documents/curseforge/minecraft/Instances`, `~/curseforge/minecraft/Instances`, `~/.curseforge/minecraft/Instances`, and `%USERPROFILE%\curseforge\minecraft\Instances` on Windows). If detection fails, pass `--instance` or set `WORLD_FURTHER_INSTANCE`.

This does **not** install new mods from `manifest.json` — use the CurseForge app for addon updates.

## License

Pack configs and original addons are MIT unless a nested file says otherwise. Third-party mods stay under their own licenses via CurseForge.
