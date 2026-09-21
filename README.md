# Worlds Further

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

- [Create: Sourceworks](https://github.com/TheRealValorfor/create-sourceworks)
- [Create: Dragonworks](https://github.com/TheRealValorfor/create-dragonworks)
- [Ars Draconis](https://github.com/TheRealValorfor/ars-draconis)
- [Create: Harvestworks](https://github.com/TheRealValorfor/create-harvestworks)
- [Create: Relicworks](https://github.com/TheRealValorfor/create-relicworks)
- [Soaring Trader Flyovers](https://github.com/TheRealValorfor/soaring-trader-flyovers)
- [Skill Progression: Enhanced UI](https://github.com/TheRealValorfor/skill-progression-enhanced-ui)

## License

Pack configs and original addons are MIT unless a nested file says otherwise. Third-party mods stay under their own licenses via CurseForge.
