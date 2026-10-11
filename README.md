# Brick+Data – Scan-to-BIM / reality capture szolgáltatási portfólió

Vizuális értékesítési portfólió négy célcsoportnak (**színházak, rendezvényhelyszínek, szállodák, múzeumok**): mit tud a digitális térfelmérés, és melyik szolgáltatás melyik területhez illik a legjobban.

## Mit tartalmaz

| Fájl / mappa | Mire való |
|---|---|
| `portfolio/index.html` | **Webes portfólió**: a nyitóképen húzással váltható a fotószerű nézet és a pontfelhő; célcsoport-fejezetek; 4 × 3 pontos 360°-os virtuális túra; 3 bejárható pontfelhő (színház, múzeum, rendezvénytér a tervezett elrendezéssel); berepülő videó; szűrhető szolgáltatáskatalógus; illeszkedési mátrix |
| `portfolio/prezentacio.html` | **16:9-es prezentáció** élő ügyféltalálkozóhoz: ← → lapozás, `F` teljes képernyő |
| `pdf/BrickData_Portfolio_teljes.pdf` | A teljes portfólió PDF-ben (24 dia) |
| `pdf/BrickData_Portfolio_Szinhazak.pdf` stb. | Célcsoportonként egy-egy 14 diás változat, közvetlenül kiküldhető |
| `BELSO_ELLENORZES.md` | **Belső** ellenőrzőlista: mit kell jóváhagyatni vagy kitölteni küldés előtt, és szolgáltatásonkénti képanyag-terv |
| `forras/matrix/` | A mátrix kinyerése az Excel **cellaszíneiből** (`matrix_szinekbol.json`) |
| `forras/render/` | A 3D jelenetek, a virtuális szkennelés, a renderelés és a PDF-export forráskódja |

### Célcsoportra szabott változatok

Ugyanaz az oldal a `?csoport=` paraméterrel csak az adott célcsoport anyagát mutatja:

- `index.html?csoport=szinhaz` · `?csoport=rendezveny` · `?csoport=szalloda` · `?csoport=muzeum`
- ugyanez működik a prezentációnál: `prezentacio.html?csoport=szalloda`
- **belső nézet:** `index.html?belso=1`. Megjelennek az ellenőrzendő pontok és a mátrix forrása. Ezt ne küldje ügyfélnek.

## Megnyitás

- **Helyben:** az `index.html` dupla kattintással is megnyílik; a túrák és a pontfelhők szerver nélkül is működnek (a panorámák és a pontfelhők beágyazott adatfájlokból töltődnek).
- **Online:** a `portfolio/` mappa bármilyen statikus tárhelyre feltölthető (pl. GitHub Pages, Netlify, a cég saját tárhelye). Mérete kb. 50 MB, ennek nagy része a három pontfelhő és a 12 panoráma.

## Testreszabás

- **Kapcsolattartó:** `portfolio/assets/data.js` → `config` (név, e-mail, telefon, weboldal). Üresen hagyva a kapcsolati sor nem jelenik meg. **A kiküldés előtt kitöltendő.**
- **Szövegek és illeszkedés:** `portfolio/assets/data.js`. A `fit` mezők a mátrix színeiből jönnek (`fo` = zöld, `extra` = sárga), ezeket csak a mátrix frissítésével együtt érdemes módosítani.
- **PDF-ek újragenerálása** a módosítások után: nyissa meg a `prezentacio.html`-t (vagy pl. a `prezentacio.html?csoport=muzeum` címet) Chrome-ban, majd *Nyomtatás → Mentés PDF-be* (Háttérgrafika: be, Margók: nincs). Automatikusan a `forras/render/make_pdfs.sh` is elvégzi (Node + Playwright szükséges hozzá).

## A képanyagról

Minden vizuális elem **saját koncepcióvizualizáció**, procedurálisan felépített 3D jelenetekből Blender Cycles-szel renderelve: patkó alakú színházterem, kastélypark rendezvény-elrendezéssel és szállodai medencekerttel, szállodai lakosztály, felülvilágítós múzeumi kiállítóterem. A pontfelhők **virtuális lézerszkenneléssel** készültek: több álláspontból 360°-os szín- és mélységkép, ugyanúgy, ahogy egy földi lézerszkenner dolgozik. A mesh valódi felületrekonstrukció a pontfelhőből.

A képek nem valós ügyfélhelyszínek és nem referenciamunkák, ezért mindegyiken „Koncepcióvizualizáció” címke szerepel. A felhasznált nyílt licencű elemek (CC0 / CC BY 4.0) listája a `BELSO_ELLENORZES.md` 4. pontjában, a portfólió láblécében és a prezentáció utolsó diáján található.
