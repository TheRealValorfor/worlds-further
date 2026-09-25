# Worlds Further dedicated server

Generated with **ServerPackCreator 8.1.2**. Minecraft **1.21.1** / NeoForge **21.1.250**. Client-only mods (Sodium, Iris, FancyMenu, Distant Horizons, …) are omitted.

This tree matches pack **0.1.2** (Furtherworks 1.0.4, Relicworks 1.0.1, no Chunky, 8 GB + ZGC + 1g metaspace). CurseForge datapacks sit in `datapacks/` next to `mods/` — Moonlight loads that folder for every world.

## EULA (all platforms)

Read [Mojang’s EULA](https://aka.ms/MinecraftEULA). In `eula.txt` set `eula=true` before the first start (or type `I agree` when the script asks).

Java **21** is required. If `JAVA=java` in `variables.txt` and a suitable JDK is missing, `install_java.sh` / `install_java.ps1` can fetch Temurin.

## Start — pick your OS

| OS | What to run |
|---|---|
| **Windows** | Double-click **`start.bat`**. Do not delete `start.ps1`. |
| **macOS** | Double-click **`start.command`**, or in Terminal: `chmod +x start.sh start.command && ./start.command` |
| **Linux** | `chmod +x start.sh && ./start.sh` |

Do not use `run.sh` / `run.bat` if NeoForge creates them later — keep using **`start.*`**.

First start downloads NeoForge **ServerStarterJar** (`server.jar`) and libraries. Default port **25565**. RAM **8 GB** + ZGC: edit **`variables.txt`** (`JAVA_ARGS`). `start.sh` / `start.ps1` overwrite `user_jvm_args.txt` from that file.

Do not tick this folder in a CurseForge **client** export.

## Regenerate

From the instance root (Minecraft closed):

```bash
./scripts/export-server.sh
```

Config: `tools/ServerPackCreator/worlds-further.conf`. Extra OS helpers: `tools/ServerPackCreator/start-scripts/`.
