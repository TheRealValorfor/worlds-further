import json, glob
from pathlib import Path

BASE = str(Path(__file__).resolve().parent)

def compute_depths(quests):
    by_key = {q["key"]: q for q in quests}
    depth = {}

    def get_depth(key, seen):
        if key in depth:
            return depth[key]
        if key in seen:
            return 0  # guard against any accidental cycle
        seen.add(key)
        deps = [d for d in by_key[key].get("dependencies", []) if d in by_key]
        d = 0 if not deps else 1 + max(get_depth(dep, seen) for dep in deps)
        depth[key] = d
        return d

    for q in quests:
        get_depth(q["key"], set())
    return depth

def find_capstone(quests):
    """The terminal quest (nothing depends on it) with the greatest depth —
    i.e. the deepest point actually reached by following real progression,
    not just whichever dead-end happens to have the most immediate deps."""
    depended_on = set()
    for q in quests:
        depended_on.update(q.get("dependencies", []))
    terminals = [q for q in quests if q["key"] not in depended_on and q.get("dependencies")]
    if not terminals:
        return None
    depths = compute_depths(quests)
    terminals.sort(key=lambda q: depths.get(q["key"], 0), reverse=True)
    return terminals[0]

def main():
    changed = {}
    for path in sorted(glob.glob(f"{BASE}/specs/chapters/*.json")):
        spec = json.load(open(path))
        quests = spec["quests"]
        touched = []

        capstone = find_capstone(quests)
        if capstone:
            capstone["shape"] = "hexagon"
            capstone["size"] = 1.4
            touched.append((capstone["key"], capstone["shape"], capstone["size"]))

        for q in quests:
            if q.get("shape"):
                continue
            if any(t.get("type") == "advancement" for t in q.get("tasks", [])):
                q["shape"] = "diamond"
                q["size"] = 1.2
                touched.append((q["key"], q["shape"], q["size"]))

        if spec["key"] in ("bounty_board", "here_be_dragons"):
            for q in quests:
                if q.get("shape"):
                    continue
                key = q["key"]
                if key.startswith("boss_") or "master" in key or "dragon_steel" in key:
                    q["shape"] = "diamond"
                    q["size"] = 1.2
                    touched.append((q["key"], q["shape"], q["size"]))

        if touched:
            with open(path, "w") as f:
                json.dump(spec, f, indent=2)
                f.write("\n")
            changed[spec["key"]] = touched

    for key, touched in changed.items():
        print(key, "->", touched)

if __name__ == "__main__":
    main()
