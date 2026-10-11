# Renderelési folyamat (referencia)

A portfólió képanyaga ezekkel a szkriptekkel készült. A szkriptek az eredeti munkakönyvtár útvonalaira hivatkoznak, ezért újrafuttatás előtt ezeket át kell írni.

| Fájl | Szerep |
|---|---|
| `lib.py` | Közös Blender-segédfüggvények: anyagok, geometria, fények, kamera, panorámakamera |
| `theater.py`, `estate.py`, `hotel.py`, `museum.py` | A négy procedurális jelenet: színházterem, kastélypark, szállodai lakosztály, múzeumi kiállítóterem |
| `scan.py` | Virtuális lézerszkenner: 360°-os szín- és mélységkép álláspontonként → színes pontfelhő (`cloud.npz`) |
| `modes.py` | Alternatív nézetek: BIM-kategóriaszínezés, hőkép, mesh-rekonstrukció a pontfelhőből, pontfelhő-renderelés |
| `q_*.py` | Renderelési sorok jelenetenként (`... q_theater.py -- photo` stb.) |
| `gen_art.py` | A múzeumi jelenet saját generálású festményei |
| `make_assets.py`, `make_clouds.py` | Webes képek, panorámák, túrapontok és pontfelhő-adatfájlok előállítása |
| `cloudviewer.js` | A böngészős pontfelhő-néző forrása (three.js, esbuild-del csomagolva) |
| `shoot.js`, `make_pdfs.sh` | Képernyőképek és a PDF-ek generálása Playwrighttal |

Futtatáshoz szükséges: Blender Python-modul (`pip install bpy`, Python 3.13), numpy, Pillow, Node.js + Playwright, ffmpeg.
