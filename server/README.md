# Worlds Further dedicated server

Nested in the pack repo on purpose: same version as the client, same configs, one changelog.

Minecraft **1.21.1** / NeoForge **21.1.250**. Java **21**. Default port **25565**. Heap **8 GB** + ZGC in `variables.txt`.

## What this folder is

Start scripts, `server.properties`, `eula.txt`, ServerPackCreator config (`worlds-further.conf`), and `datapacks/SoaringTraderFlyovers-1.0.0.zip`.

**Mods are not committed.** Generate them from the CurseForge instance:

```bash
# From the Ejomilishy instance root (Minecraft closed)
./scripts/export-server.sh
```

That writes `server-pack/` locally. For PebbleHost you can still upload `export/WorldsFurther-0.1.2-server.zip` from the instance (CurseForge **Server Pack** file, same version as the client).

If you only need the trader fix on an existing host, upload:

1. `config/aeronauticsdiscovery-common.toml` (from `overrides/config/` in this repo)
2. `config/moonlight-common.toml` (`global_datapacks_folder = ""`; FTB Obsidian loads instance `datapacks/`)
3. `datapacks/SoaringTraderFlyovers-1.0.0.zip` (this folder or `overrides/datapacks/`)

Then delete any leftover `moonlight-global-datapacks/` on the host.

## Run

Set `eula=true` in `eula.txt`. Then:

| OS | Command |
|---|---|
| Windows | `start.bat` |
| macOS | `start.command` |
| Linux | `chmod +x start.sh && ./start.sh` |

First start downloads NeoForge ServerStarterJar. Do not add a second `-Xmx` if the host already sets RAM.

## Do not

- Make a separate GitHub repo for the server pack
- Commit `mods/` or `libraries/`
- Tick `server-pack/` when exporting the **client** CurseForge zip
