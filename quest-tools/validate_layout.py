"""Check generated IDs, references, layout bounds and reproducible generation."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent / 'config' / 'ftbquests' / 'quests'
files = list(ROOT.rglob('*.snbt'))
ids = []
for path in files:
    if path.parent.name != 'lang':
        ids += re.findall(r'\bid: "([A-F0-9]{16})"', path.read_text())
assert len(ids) == len(set(ids)), 'Duplicate object IDs'
assert all(1 < int(i, 16) <= 0x7fffffffffffffff for i in ids), 'ID outside Java signed-long range'
saved = json.loads((BASE / 'specs/id_map.json').read_text())
assert set(saved.values()) <= set(ids), 'Previously saved IDs lost'
groups = set(re.findall(r'\bid: "([A-F0-9]{16})"', (ROOT / 'chapter_groups.snbt').read_text()))
for path in (ROOT / 'chapters').glob('*.snbt'):
    text = path.read_text()
    assert re.search(r'\bgroup: "(\w+)"', text).group(1) in groups, path
    for block in re.findall(r'dependencies: \[(.*?)\]', text, re.S):
        assert set(re.findall(r'"(\w+)"', block)) <= set(ids), path
for path in (BASE / 'specs/chapters').glob('*.json'):
    spec = json.loads(path.read_text())
    quests = spec['quests']
    for i, quest in enumerate(quests):
        for other in quests[i + 1:]:
            clearance = (quest.get('size', 1) + other.get('size', 1)) / 2
            assert max(abs(quest['x'] - other['x']), abs(quest['y'] - other['y'])) * 1.3 > clearance, (path, quest['key'], other['key'])
    for image in spec['images']:
        for quest in quests:
            assert (abs(image['y'] - quest['y']) * 1.3 > (image['height'] * 1.3 + quest.get('size', 1)) / 2
                    or abs(image['x'] - quest['x']) * 1.3 > (image['width'] * 1.3 + quest.get('size', 1)) / 2), (path, image, quest['key'])
before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
subprocess.run([sys.executable, str(BASE / 'generate_quests.py')], check=True, capture_output=True)
assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in before.items()), 'Regeneration changed output'
print(f'PASS: {len(ids)} valid unique IDs; {len(saved)} saved IDs preserved; references resolve; nodes and headings do not overlap; regeneration is byte-stable.')
