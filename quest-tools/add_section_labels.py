"""Refresh section-heading bounds without discarding authored section names."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent


def main():
    for path in sorted((BASE / 'specs' / 'chapters').glob('*.json')):
        spec = json.loads(path.read_text())
        sections = {}
        for quest in spec['quests']:
            sections.setdefault(quest['section'], []).append(quest)
        sections = sorted(sections.values(), key=lambda qs: min(q['y'] for q in qs))
        images = spec['images']
        if len(images) != len(sections):
            raise ValueError(f'{path.name}: provide one named heading per section')
        width = max(12, max(q['x'] for q in spec['quests']) + 2)
        for image, quests in zip(images, sections):
            image.update(x=round((min(q['x'] for q in quests) + max(q['x'] for q in quests)) / 2, 2),
                         y=round(min(q['y'] for q in quests) - 1.6, 2),
                         width=width, height=0.8)
        path.write_text(json.dumps(spec, indent=2) + '\n')
        print(f'{path.stem}: {len(images)} section headings')


if __name__ == '__main__':
    main()
