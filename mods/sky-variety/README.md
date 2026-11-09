# Sky Variety

Eleven photographic skies assigned across 37 track variants in Takedawn. Version **1.2.1** replaces 17 sky sheets and recolours 20 sky-gradient atlases. Each sky uses its own cloud shapes instead of the original game's cloud mask.

[Download Sky Variety 1.2.0](https://github.com/rigerc/takedawn-mods/releases/download/sky-variety-v1.2.0/sky-variety-1.2.0.zip) (1.2.1, described below, is not released yet: copy this folder from the repository to use it)

## Installation

Extract `sky-variety/` from the ZIP into your [Takedawn mods folder](../../README.md#install-a-mod), enable **Sky Variety** in Settings → Mods, then restart. Alternatively, copy this folder directly from the repository.

Disable **Industrial Sunset Skies** and other sky texture packs first: they replace the same hashes. To restore the original skies, disable Sky Variety and restart.

Requires a Takedawn build with PNG texture-pack support. Texture keys were identified from the NTSC-U disc data, manifest `81dc20fd647fb0b1`.

## Included skies

- Belfast Sunset
- Kloppenheim 06 sunrise
- Qwantani Sunrise
- Rosendal Park Sunset
- Overcast Soil
- Sunflowers daylight
- Kloofendal 48d Partly Cloudy
- Industrial Sunset
- Qwantani Dusk 2
- Kloofendal Overcast
- Qwantani Night

Each track has a fixed assignment; there is no random selection or in-game sky selector. Tracks sharing the same original texture hash share a replacement. See [coverage.tsv](coverage.tsv) for sky assignments and [gradient-coverage.tsv](gradient-coverage.tsv) for the corresponding gradients. Track variants include forward and reverse routes; they are not 37 unique locations.

## In-game comparison

Captured in game at the race start (the GO frame), same track and car, one run with the mod disabled and one enabled. Takedawn 0.3.1, Linux, NVIDIA RTX 3070, Vulkan, headless, native 640×448 crop of the 640×480 frame. Rival positions and traffic differ slightly between runs. These are gameplay screenshots, not game textures; sky assignments per track are in [coverage.tsv](coverage.tsv).

| Track | Stock | Sky Variety 1.2.1 |
| --- | --- | --- |
| US/C1_V1<br>Sunflowers daylight | ![US/C1_V1 stock](screenshots/us-c1-v1-stock.jpg) | ![US/C1_V1 with Sky Variety](screenshots/us-c1-v1-sky-variety.jpg) |
| US/C3_V1<br>Industrial Sunset | ![US/C3_V1 stock](screenshots/us-c3-v1-stock.jpg) | ![US/C3_V1 with Sky Variety](screenshots/us-c3-v1-sky-variety.jpg) |
| EU/C1_V2<br>Sunflowers daylight | ![EU/C1_V2 stock](screenshots/eu-c1-v2-stock.jpg) | ![EU/C1_V2 with Sky Variety](screenshots/eu-c1-v2-sky-variety.jpg) |
| EU/M1_V1<br>Overcast Soil | ![EU/M1_V1 stock](screenshots/eu-m1-v1-stock.jpg) | ![EU/M1_V1 with Sky Variety](screenshots/eu-m1-v1-sky-variety.jpg) |
| EU/C2_V1<br>daylight sky | ![EU/C2_V1 stock](screenshots/eu-c2-v1-stock.jpg) | ![EU/C2_V1 with Sky Variety](screenshots/eu-c2-v1-sky-variety.jpg) |
| AS/C1_V2<br>daylight sky | ![AS/C1_V2 stock](screenshots/as-c1-v2-stock.jpg) | ![AS/C1_V2 with Sky Variety](screenshots/as-c1-v2-sky-variety.jpg) |

## Changes in 1.2.1

EU/C1 (a clear blue sky in the original) had been given Overcast Soil, which clashed with the track's sunny lighting; it now uses Sunflowers daylight. Overcast Soil moved to EU/M1, whose original sky is already stormy. Only four textures changed: the EU/C1 and EU/M1 sheets and gradients.

## Appearance and compatibility

Sky sheets are 4096×512 or 4096×1024 RGBA PNGs with an authored fade at the zenith. Matching 128×128 RGB gradient atlases use colours sampled from their source panoramas. `alpha = "auto"` reads the new sheet alpha while retaining the original gradient atlas alpha at runtime.

Fog, vertex tint, sun/moon effects, track lighting and reflection textures remain controlled by the game. This is a sky-art replacement, not a complete time-of-day conversion: a night sky does not darken the road. Night artwork is reduced to 55% brightness.

Tested with Takedawn 0.3.1, Linux, NVIDIA RTX 3070 and Vulkan in headless daylight and night races. Other track variants, HDR and other platforms have not been visually verified. Both modded races and the no-mod control completed their scenes, then encountered the same executable shutdown crash. See [VALIDATION.txt](VALIDATION.txt) for the checks and limitations.

## Rebuild the artwork

The generated PNGs are committed, so rebuilding is optional. From the repository root:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-build.txt
python tools/build_sky_variety.py --sources /path/to/source-jpgs
```

Download the **8K Tonemapped JPG** for each of the eleven assets linked in [CREDITS.txt](CREDITS.txt), keeping its original filename, such as `sunflowers_puresky.jpg`. The sources folder must contain all eleven JPGs. The builder checks their SHA-256 hashes before processing; the expected sources and exposure settings are in [tools/sky-variety-sources.json](../../tools/sky-variety-sources.json).

Output is `dist/sky-variety/` and `dist/sky-variety.zip`. No retail game files are needed to rebuild the pack. Source panoramas and build output are not committed.

## Credits and licence

Artwork comes from Poly Haven contributors under [CC0 1.0 Universal](LICENSE.txt). Full authors, source URLs and checksums are in [CREDITS.txt](CREDITS.txt). Replacement textures and source-derived gradient colours are provided under CC0; repository tools and documentation use the root MIT licence. No original game textures or masks are bundled.
