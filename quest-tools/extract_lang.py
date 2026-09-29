import zipfile, json, os, sys, io

BASE = os.path.dirname(os.path.abspath(__file__))
INSTANCE = os.path.dirname(BASE)
MODS = os.path.join(INSTANCE, "mods")
OUT = os.path.join(BASE, "lang")
os.makedirs(OUT, exist_ok=True)

# jar filename -> list of (namespace, out_name) we care about; None namespace = "all found"
TARGETS = {
    "create-1.21.1-6.0.10.jar": None,
    "create-stuff-additions1.21.1_v2.1.4b.jar": None,
    "createaddition-1.6.0.jar": None,
    "create-central-kitchen-2.6.0.jar": None,
    "create-confectionery1.21.1_v1.1.3b.jar": None,
    "create-enchantment-industry-2.4.2.jar": None,
    "create_aquatic_ambitions-1.21.1-2.0.4.jar": None,
    "create_connected-1.3.3-mc1.21.1.jar": None,
    "create_hypertube-0.6.0-NEOFORGE.jar": None,
    "createdeco-2.1.3.jar": None,
    "railways-0.2.1+neoforge-mc1.21.1.jar": None,
    "CreateOPlenty-NeoForge-Create+6.0.7-3.0.jar": None,
    "MysticalAgriculture-1.21.1-8.0.28.jar": None,
    "MysticalAgradditions-1.21.1-8.0.14.jar": None,
    "ars_nouveau-1.21.1-5.13.1.jar": None,
    "ars_creo-1.21.1-5.4.0.jar": None,
    "SnowRealMagic-1.21.1-NeoForge-12.2.2.jar": None,
    "gemsrealm-1.21-2.11.3-neoforge.jar": None,
    "FarmersDelight-1.21.1-1.3.4.jar": None,
    "aquaculturedelight-1.2.0-neoforge-1.21.1.jar": None,
    "delightfulcreators-1.2.1.jar": None,
    "pamhc2crops-NEOFORGE-1.21.1-1.0.9.jar": None,
    "pamhc2fantasy-NEOFORGE-1.21.0-1.0.3.jar": None,
    "pamhc2foodcore-NEOFORGE-1.21.1-1.0.4.jar": None,
    "pamhc2foodextended-NEOFORGE-1.21.1-1.0.0.jar": None,
    "pamhc2trees-NEOFORGE-1.21.1-1.0.9.jar": None,
    "Aquaculture-1.21.1-2.7.21.jar": None,
    "StorageDrawers-neoforge-1.21.1-13.11.4.jar": None,
    "functionalstorage-1.21.1-1.5.8.jar": None,
    "sophisticatedbackpacks-1.21.1-3.26.3.2158.jar": None,
    "sophisticatedcore-1.21.1-1.5.1.2341.jar": None,
    "toms_storage-1.21-2.4.2.jar": None,
    "supplementaries-1.21.1-3.9.9-neoforge.jar": None,
    "waystones-neoforge-1.21.1-21.1.45.jar": None,
    "artifacts-neoforge-13.2.5.jar": None,
    "Quark-4.1-484.jar": None,
    "handcrafted-neoforge-1.21.1-4.0.3.jar": None,
    "guardvillagers-2.4.12-1.21.1.jar": None,
    "iceandfire-2.1.2.jar": None,
}

def process_zip(zf, jarname, results):
    for name in zf.namelist():
        if name.startswith("assets/") and name.endswith("lang/en_us.json"):
            ns = name.split("/")[1]
            try:
                data = json.loads(zf.read(name).decode("utf-8"))
            except Exception as e:
                print(f"  WARN failed to parse {name} in {jarname}: {e}")
                continue
            items = {}
            for k, v in data.items():
                if k.startswith("item.") or k.startswith("block."):
                    parts = k.split(".")
                    # must be exactly item.<ns>.<name> or block.<ns>.<name> (name has no further dots)
                    if len(parts) == 3 and parts[1] == ns:
                        items[f"{ns}:{parts[2]}"] = v
            if items:
                results.setdefault(ns, {}).update(items)

for jarname in TARGETS:
    path = os.path.join(MODS, jarname)
    if not os.path.exists(path):
        print(f"MISSING JAR: {jarname}")
        continue
    results = {}
    with zipfile.ZipFile(path) as zf:
        process_zip(zf, jarname, results)
        # handle nested jarjar jars
        for name in zf.namelist():
            if name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
                nested_bytes = zf.read(name)
                try:
                    with zipfile.ZipFile(io.BytesIO(nested_bytes)) as nzf:
                        process_zip(nzf, jarname + "!" + name, results)
                except Exception as e:
                    print(f"  WARN nested jar failed {name}: {e}")
    if not results:
        print(f"NO LANG FOUND: {jarname}")
        continue
    for ns, items in results.items():
        outpath = os.path.join(OUT, f"{ns}.json")
        with open(outpath, "w") as f:
            json.dump(items, f, indent=1, sort_keys=True)
        print(f"{jarname} -> {ns}: {len(items)} items")

# Also handle the aeronautics bundle (jarjar of jarjar)
bundle = os.path.join(MODS, "create-aeronautics-bundled-1.21.1-1.3.2.jar")
if os.path.exists(bundle):
    results = {}
    with zipfile.ZipFile(bundle) as zf:
        for name in zf.namelist():
            if name.startswith("META-INF/jarjar/") and name.endswith(".jar"):
                nested_bytes = zf.read(name)
                with zipfile.ZipFile(io.BytesIO(nested_bytes)) as nzf:
                    process_zip(nzf, name, results)
    for ns, items in results.items():
        outpath = os.path.join(OUT, f"{ns}.json")
        with open(outpath, "w") as f:
            json.dump(items, f, indent=1, sort_keys=True)
        print(f"aeronautics-bundle -> {ns}: {len(items)} items")

print("DONE")
