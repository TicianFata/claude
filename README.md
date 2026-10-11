# Brick+Data – Scan-to-BIM / reality capture szolgáltatási portfólió

Vizuális értékesítési portfólió négy célcsoportnak (**színházak, rendezvényhelyszínek, szállodák, múzeumok**): mit tud a digitális térfelmérés, és melyik szolgáltatás melyik területhez illik a legjobban.

## Mit tartalmaz

| Fájl | Mire való |
|---|---|
| `portfolio/index.html` | **Webes portfólió**: interaktív nyitókép (fotószerű nézet és pontfelhő húzással váltva), célcsoport-fejezetek, 360°-os virtuális túrák, bejárható pontfelhők, berepülő videó, szolgáltatáskatalógus szűrővel, illeszkedési mátrix |
| `portfolio/prezentacio.html` | **16:9-es prezentáció** élő ügyféltalálkozóhoz: ← → lapozás, `F` teljes képernyő |
| `pdf/` | Kész PDF-ek: a teljes portfólió és célcsoportonként egy-egy rövidebb változat |
| `BELSO_ELLENORZES.md` | **Belső** ellenőrzőlista: mit kell jóváhagyatni vagy kitölteni küldés előtt |
| `forras/` | A mátrix kinyerése a színekből, valamint a 3D jelenetek és a renderelés forráskódja |

### Célcsoportra szabott változatok

Ugyanaz az oldal a `?csoport=` paraméterrel csak az adott célcsoport anyagát mutatja:

- `index.html?csoport=szinhaz` · `?csoport=rendezveny` · `?csoport=szalloda` · `?csoport=muzeum`
- ugyanez működik a prezentációnál: `prezentacio.html?csoport=szalloda`
- **belső nézet:** `index.html?belso=1`. Megjelennek az ellenőrzendő pontok és a mátrix forrása. Ezt ne küldje ügyfélnek.

## Megnyitás

- **Helyben:** az `index.html` dupla kattintással is megnyílik; a túrák és a pontfelhők szerver nélkül is működnek.
- **Online:** a `portfolio/` mappa bármilyen statikus tárhelyre feltölthető (pl. GitHub Pages, Netlify, a cég saját tárhelye).

## Testreszabás

- **Kapcsolattartó:** `portfolio/assets/data.js` → `config` (név, e-mail, telefon, weboldal). Üresen hagyva a kapcsolati sor nem jelenik meg.
- **Szövegek és illeszkedés:** `portfolio/assets/data.js`. A `fit` mezők a mátrix színeiből jönnek (`fo` = zöld, `extra` = sárga), ezeket csak a mátrix frissítésével együtt érdemes módosítani.
- **PDF-ek újragenerálása** a módosítások után: nyissa meg a `prezentacio.html`-t Chrome-ban, majd *Nyomtatás → Mentés PDF-be* (Háttérgrafika: be, Margó: nincs), vagy futtassa a `forras/render/shoot.js deck` parancsot (lásd a fájl elejét).

## A képanyagról

Minden vizuális elem **saját koncepcióvizualizáció**. Procedurálisan felépített 3D jelenetekből készült Blender Cycles-szel: patkó alakú színházterem, kastélypark rendezvény-elrendezéssel és szállodai medencekerttel, szállodai lakosztály, felülvilágítós múzeumi kiállítóterem. A pontfelhők virtuális lézerszkenneléssel készültek: több álláspontból 360°-os szín- és mélységkép, ugyanúgy, ahogy egy földi lézerszkenner dolgozik. A mesh valódi felületrekonstrukció a pontfelhőből.

A képek nem valós ügyfélhelyszínek és nem referenciamunkák, ezért mindegyiken „Koncepcióvizualizáció” címke szerepel. A felhasznált nyílt licencű elemek (CC0 / CC BY 4.0) listája a `BELSO_ELLENORZES.md` 4. pontjában és a portfólió láblécében található.
