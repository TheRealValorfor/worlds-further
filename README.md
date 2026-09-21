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
manifest.json          CurseForge addon list (350 files)
modlist.html           Human-readable addon list
overrides/             What the CF app ticked: config, datapacks, shader .txt, README, CHANGELOG
server/                Dedicated start scripts, JVM args, SPC conf, datapack zip
profileImage/          Pack icon
```

`overrides/mods/create-relicworks-*.jar` is only here until Relicworks is added as a CurseForge addon in the instance. After that, remove the jar from overrides.

## Related projects (TheRealValorfor)

| GitHub | CurseForge |
|---|---|
| [create-sourceworks](https://github.com/TheRealValorfor/create-sourceworks) | [create-sourceworks](https://www.curseforge.com/minecraft/mc-mods/create-sourceworks) |
| [create-dragonworks](https://github.com/TheRealValorfor/create-dragonworks) | [create-dragonworks](https://www.curseforge.com/minecraft/mc-mods/create-dragonworks) |
| [ars-draconis](https://github.com/TheRealValorfor/ars-draconis) | [ars-draconis](https://www.curseforge.com/minecraft/mc-mods/ars-draconis) |
| [create-harvestworks](https://github.com/TheRealValorfor/create-harvestworks) | [create-harvestworks](https://www.curseforge.com/minecraft/mc-mods/create-harvestworks) |
| [create-relicworks](https://github.com/TheRealValorfor/create-relicworks) | [create-relicworks](https://www.curseforge.com/minecraft/mc-mods/create-relicworks) |
| [soaring-trader-flyovers](https://github.com/TheRealValorfor/soaring-trader-flyovers) | [soaring-trader-flyovers](https://www.curseforge.com/minecraft/data-packs/soaring-trader-flyovers) |
| [skill-progression-enhanced-ui](https://github.com/TheRealValorfor/skill-progression-enhanced-ui) | [skill-progression-enhanced-ui](https://www.curseforge.com/minecraft/mc-mods/skill-progression-enhanced-ui) |

## Apply git changes to a local CurseForge instance

After `git pull`, copy pack configs/datapacks/shader settings onto the instance **without** replacing CurseForge addons:

```bash
# macOS / Linux — Minecraft fully quit
chmod +x scripts/apply-to-instance.sh
./scripts/apply-to-instance.sh                  # auto-finds Worlds further / Ejomilishy
./scripts/apply-to-instance.sh --dry-run
./scripts/apply-to-instance.sh --instance "/path/to/Instances/Worlds further"
./scripts/apply-to-instance.sh --skip-options   # keep your keybinds
```

Windows (PowerShell): `.\scripts\apply-to-instance.ps1` (same flags: `-Instance`, `-DryRun`, `-SkipOptions`, `-SkipJars`).

Or set `WORLD_FURTHER_INSTANCE` to the instance folder. This does **not** install new mods from `manifest.json` — use the CurseForge app for addon updates.

## License

Pack configs and original addons are MIT unless a nested file says otherwise. Third-party mods stay under their own licenses via CurseForge.
