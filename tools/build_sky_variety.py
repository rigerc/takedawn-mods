#!/usr/bin/env python3
"""Rebuild Sky Variety from locally downloaded, checksum-verified CC0 JPGs."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import zipfile

from PIL import Image, ImageDraw, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'mods/sky-variety'


def read_coverage(name):
    return [line.split('\t') for line in (TEMPLATE / name).read_text().splitlines()[1:]]


def build(sources_dir, output):
    sources = json.loads((ROOT / 'tools/sky-variety-sources.json').read_text())
    clouds = read_coverage('coverage.tsv')
    gradients = read_coverage('gradient-coverage.tsv')
    # Check inputs before writing output. Hashes identify the exact tonemapped JPGs.
    for source in sources.values():
        path = sources_dir / (source['asset'] + '.jpg')
        if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError(f'Source checksum mismatch: {path}')
    for row in clouds + gradients:
        if row[5] not in sources:
            raise ValueError(f'Unknown sky assignment: {row[5]}')
    output.mkdir(parents=True, exist_ok=True)
    for path in TEMPLATE.iterdir():
        if path.is_file():
            shutil.copy2(path, output / path.name)
    textures = output / 'textures'
    textures.mkdir(exist_ok=True)
    shutil.copy2(TEMPLATE / 'textures/pack.toml', textures / 'pack.toml')
    expected = {row[0] + '.png' for row in clouds + gradients}
    unexpected = {p.name for p in textures.iterdir()} - expected - {'pack.toml'}
    if unexpected:
        raise ValueError(f'Unexpected output files; use a fresh output directory: {unexpected}')
    for style, source in sources.items():
        with Image.open(sources_dir / (source['asset'] + '.jpg')) as im:
            if im.size != (8192, 4096):
                raise ValueError(f'Expected 8192x4096 source: {source["asset"]}')
            sky = im.convert('RGB').crop((0, 0, im.width, im.height // 2))
        if source['brightness'] != 1:
            sky = ImageEnhance.Brightness(sky).enhance(source['brightness'])
        cache = {}
        for row in (row for row in clouds if row[5] == style):
            if row[2] not in cache:
                width, height = (int(value) * 4 for value in row[2].split('x'))
                replacement = sky.resize((width, height), Image.Resampling.LANCZOS)
                pixels = replacement.load()
                for y in range(height):
                    edge = tuple(round((a + b) / 2) for a, b in
                                 zip(pixels[0, y], pixels[width - 1, y]))
                    pixels[0, y] = pixels[width - 1, y] = edge
                replacement = replacement.convert('RGBA')
                alpha = Image.new('L', (width, height), 255)
                draw = ImageDraw.Draw(alpha)
                for y in range(round(height * 0.08)):
                    draw.line((0, y, width - 1, y), fill=round(255 * y / (height * 0.08)))
                replacement.putalpha(alpha)
                buffer = io.BytesIO()
                replacement.save(buffer, format='PNG')
                cache[row[2]] = buffer.getvalue()
            (textures / (row[0] + '.png')).write_bytes(cache[row[2]])
        profile = sky.resize((1, 128), Image.Resampling.BOX).resize((128, 128))
        for row in (row for row in gradients if row[5] == style):
            profile.save(textures / (row[0] + '.png'))
    archive = output.parent / (output.name + '.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(output.rglob('*')):
            if path.is_file():
                z.write(path, path.relative_to(output.parent))
    print(f'Built {len(clouds)} sky sheets and {len(gradients)} gradients: {archive}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', required=True, type=Path, help='Folder with the 11 source JPGs')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/sky-variety')
    args = parser.parse_args()
    output = args.output.resolve()
    if output == TEMPLATE or output in TEMPLATE.parents or TEMPLATE in output.parents:
        parser.error('--output must be outside the committed mod folder and its parents')
    build(args.sources.resolve(), output)


if __name__ == '__main__':
    main()
