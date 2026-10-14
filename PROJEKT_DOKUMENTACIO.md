# Brick+Data Scan-to-BIM portfólió – projektdokumentáció

> A projekt céljai, kiinduló anyagai, a meghozott döntések és a teljes elkészítési folyamat egy helyen. Belső dokumentum, nem az ügyfélnek szól.

---

## 1. A projekt célja

**Fő cél:** a Brick+Data Scan-to-BIM / reality capture képességéből olyan vizuális, értékesítésre kész portfóliót építeni, amely megmutatja a potenciális ügyfeleknek:

1. **milyen szolgáltatásokat** tud nyújtani a cég a digitális térfelmérésből,
2. **melyik szolgáltatás melyik célcsoporthoz illik a legjobban**,
3. és mindezt **látványosan, esztétikusan, marketingre alkalmasan** teszi.

**Alapgondolat:** nem „pontfelhőt” vagy „szkennelést” adunk el, hanem azt, amit lehetővé tesz. *„Egy felmérés. Sokféle digitális érték.”*

**A négy célcsoport és a fő üzenetük:**

| Célcsoport | Fő érték | Főcím a portfólióban |
|---|---|---|
| Színházak | A díszlettervező távolról is megismeri a színpadot és a teret | „A színpad ott van, ahol a tervező.” |
| Rendezvényhelyszínek | Elrendezés-tervezés (színpad, sátrak, asztalok, mosdók) helyszíni bejárás nélkül | „Az elrendezés a digitális térben kezdődik.” |
| Szállodák | Újrahasznosítható marketingtartalom és webes vendégélmény | „Mutassa meg a szállodát, mielőtt a vendég megérkezik.” |
| Múzeumok | Időszakos kiállítások archiválása és online bejárása | „A kiállítás bezár. A digitális tere nyitva marad.” |

**Értékesítési sorrend** (a mesteranyag szerint): Marketing → Ügyfélélmény → Értékesítés → Tér- és eseménytervezés → Műszaki alap (másodlagos, de releváns).

---

## 2. Kiinduló anyagok

| Anyag | Tartalom | Hogyan használtuk |
|---|---|---|
| `BrickData_Scan_to_BIM_Portfolio_Mesteranyag.docx` | Projektháttér, a 4 célcsoport, a 18 szolgáltatás leírása, a kommunikációs alapelvek, a nyitott kérdések | Szövegek, struktúra, alapelvek forrása |
| `grading_javitott_elso4_leirasokkal.xlsx` | Szolgáltatás × célcsoport mátrix színkódokkal és cellaszövegekkel | **Csak a cellaszíneket** használtuk (lásd 3.1) |

**Alapelvek a mesteranyagból, amelyeket végig betartottunk:**
- Nem állítunk árat, pontosságot, eszközspecifikációt, határidőt vagy referenciát, amíg a cég nem igazolta.
- Külső anyagot nem tüntetünk fel Brick+Data-munkaként; a licenceket ellenőrizni kell.
- Az ügyfél eredményével kezdünk, nem a technológiával.
- A pontfelhő, a mesh, a 3D modell és a BIM nem ugyanaz; ezt a portfólió külön meg is mutatja.
- A piros (nem releváns) kombinációkat nem erőltetjük.

---

## 3. Kulcsdöntések

### 3.1. A mátrix a színekből, nem a szövegből

A felhasználó jelezte, hogy az Excel szövege nem teljesen megbízható, a színek igen. Ezért a cellák kitöltőszínét programmal olvastuk ki:

- zöld `#D9EAD3` → **fő illeszkedés**
- sárga `#FFF2CC` → **kiegészítő érték**
- piros `#F4CCCC` → **nem jelenik meg** az adott célcsoportnál

Eredmény: `forras/matrix/matrix_szinekbol.json`. A végleges illeszkedés (● = fő, ○ = kiegészítő, – = nem javasolt):

| Szolgáltatás | Színház | Rendezvény | Szálloda | Múzeum |
|---|:-:|:-:|:-:|:-:|
| 360°-os panorámakép | ● | ● | ● | ● |
| Virtuális túra panorámapontokkal | ● | ○ | ● | ● |
| Berepülhető 3D túra | – | ● | – | ● |
| 360°-os videó | ○ | ○ | ● | ● |
| Virtuális berepülő videó | ○ | ● | ○ | ○ |
| VR / MR / AR bemutató | ○ | ○ | ○ | ○ |
| Drónfotó | – | – | ○ | ○ |
| Drónvideó | – | ○ | ● | ○ |
| Környezeti és megközelítési túra | ● | ○ | ● | ● |
| Pontfelhő | ○ | ○ | ○ | ● |
| Mesh (felületmodell) | ○ | ○ | ○ | ○ |
| 3D modell | ● | ● | ○ | ○ |
| BIM-modell (Revit / Archicad) | ○ | ○ | ● | ● |
| Hőtérképezés | – | – | – | ○ |

**Kimaradt négy szolgáltatás**, mert mind a négy célcsoportnál piros volt: benapozásvizsgálat, kivitelezés nyomon követése, megvalósulási hiba / deformáció elemzése, vegyes (modell + valós) berepülő videó. Így 18 helyett **14 szolgáltatás** szerepel.

Ahol a cellaszöveg ellentmond a színnek (pl. színház – berepülhető túra), a színt követtük, és az eltéréseket a `BELSO_ELLENORZES.md` listázza.

### 3.2. Saját koncepcióvizualizációk külső fotók helyett

- A munkakörnyezet hálózati szabályai blokkolták a nagy képoldalakat (Wikimedia Commons, Unsplash, Pexels, Poly Haven CDN, Pixabay).
- Csak a GitHub és az npm volt elérhető. Innen nyílt licencű textúrákat (CC0) és bútor-/tárgymodelleket (CC0, CC BY 4.0) töltöttünk le.
- **Döntés:** minden képet saját, procedurálisan felépített 3D jelenetekből renderelünk. Ennek előnyei:
  - nincs licenckockázat,
  - egységes, prémium vizuális nyelv,
  - ugyanabból a térből minden kimenet (fotó, pontfelhő, mesh, BIM, panoráma) előállítható. Pontosan ezt kérte a mesteranyag: *„ugyanazt a helyszínt többféle kimenetben mutatjuk be”*.
- Minden kép **„Koncepcióvizualizáció”** címkét kapott, hogy ne lehessen referenciamunkának nézni.

### 3.3. Három formátum ugyanabból az adatból

Minden szöveg és illeszkedési adat egyetlen fájlban (`portfolio/assets/data.js`) van, és ebből épül fel:
1. a **webes portfólió** (interaktív, online vagy helyben),
2. a **16:9-es prezentáció** (élő ügyféltalálkozóhoz),
3. a **PDF-ek** (kiküldéshez: teljes + 4 célcsoportos).

Így egy módosítás mindhárom formátumban megjelenik.

---

## 4. A folyamat lépésről lépésre

### 4.1. Elemzés
- A mesteranyag feldolgozása: célcsoportok, 18 szolgáltatás, alapelvek, nyitott kérdések.
- A mátrix színeinek gépi kiolvasása (3.1).
- A portfólió szerkezetének megtervezése a mesteranyag 8.2 pontja alapján: nyitóoldal → folyamat → célcsoportok → szolgáltatások → bemutatók → következő lépés.

### 4.2. Tartalom
- A 14 szolgáltatás mindegyikéhez: **Mi ez? / Mire jó? / Miben más?** (a mesteranyag 6. fejezete alapján, rövidítve).
- Célcsoportonként és szolgáltatásonként egy-egy ügyfélközpontú mondat (csak a zöld és sárga kombinációkhoz).
- Célcsoportonkénti történet: **Kihívás → Digitális megoldás → Kézzelfogható előny → Amit kézbe kap**.
- Célcsoport-specifikus megjegyzések, pl. a rendezvényhelyszínnél a méretre tervezés pontossága, a múzeumnál a műtárgyak rögzítési feltételei.

### 4.3. A négy 3D jelenet (Blender, procedurálisan)

| Jelenet | Tartalom | Mire használtuk |
|---|---|---|
| **Színházterem** | Patkó alakú nézőtér, 3 páholysor, ~1350 szék, proszcénium aranykerettel, bársonyfüggöny, csillár, díszlet ciklorámával | Nyitókép, „ugyanaz a tér” sorozat, színházi fejezet, VR |
| **Kastélypark** | Barokk kastély, park, fák; elöl rendezvény-elrendezés (színpad, 10 sátor, 25 asztal, fényfüzérek, mosdók, büfék), hátul szállodai medencekert | Rendezvényes fejezet, drónképek, térkép, elrendezésterv, hőkép, videó |
| **Szállodai lakosztály** | Kék órás esti hangulat, ágy, lounge, panorámaablak városképpel | Szállodai fejezet, túra, BIM |
| **Múzeumi kiállítóterem** | Felülvilágítós galéria, saját generálású festmények, szobrok, vitrinek, időszakos kiállítás molinóval | Múzeumi fejezet, túra, pontfelhő, hőkép |

Renderelés: Blender Cycles, Full HD felbontás, zajszűréssel.

### 4.4. Virtuális lézerszkennelés → valódi pontfelhők
A szkenner működését modelleztük: minden álláspontból **360°-os színkép + mélységkép**, majd ezekből számoltuk vissza a 3D pontokat. A pontok színét a panorámakép adja, ahogy egy valódi földi lézerszkennernél.

| Helyszín | Álláspontok | Nyers pontszám | Ritkítás után |
|---|:-:|:-:|:-:|
| Színházterem | 8 | 10,7 millió | 6,7 millió (1,2 cm-es rács) |
| Múzeumi terem | 6 | 4,9 millió | 4,3 millió (1 cm-es rács) |
| Kastélypark (üres helyszín) | 8 | 8,5 millió | 2,9 millió (5 cm-es rács) |

### 4.5. Származtatott nézetek ugyanabból a térből
- **Pontfelhő:** valós színnel és magasság szerinti színezéssel.
- **Mesh:** valódi felületrekonstrukció a pontfelhőből, a pontok színével és dróthálós nézettel.
- **BIM-nézet:** az elemek kategóriánként színezve (fal, födém, mellvéd, ülés, színpad, díszlet, világítás…).
- **3D modell:** metszeti, „babaház” nézet, levett mennyezettel.
- **Hőkép:** szimulált hőkamerás nézet (homlokzat és kiállítótér).
- **360°-os panorámák:** helyszínenként 3, összesen 12 nézőpont.
- **Elrendezésterv:** a rendezvény-elrendezés építészeti diagramként, valamint a felmért helyszín pontfelhőjére rárajzolva.
- **VR-nézet:** sztereó képpár a színpadról.
- **Berepülő videó:** 150 képkocka, 6 másodperc, 1280×720.

### 4.6. Webes portfólió
- Interaktív nyitókép: húzással váltható a fotószerű nézet és a pontfelhő.
- „Ugyanaz a tér, öt kimenet” bemutató: fotó, pontfelhő, magasság, mesh, BIM.
- Négy célcsoport-fejezet, csak a zöld és sárga szolgáltatásokkal.
- **360°-os virtuális túra** (Pannellum) 4 helyszínen, Street View-szerű továbblépési pontokkal.
- **Bejárható pontfelhő** (saját three.js-nézegető): nézőpontok, automatikus végigrepülés, színezésváltás.
- Szűrhető szolgáltatáskatalógus, illeszkedési mátrix, kapcsolati blokk.
- `?csoport=…` célcsoport-nézet, `?belso=1` belső nézet.
- **Szerver nélkül is működik:** a panorámák és a pontfelhők beágyazott adatfájlokból töltődnek.

### 4.7. Prezentáció és PDF-ek
- A 16:9-es diasor ugyanabból az adatból épül: nyilakkal lapozható, `F`-fel teljes képernyős.
- A PDF-eket automatikusan generáltuk: egy teljeset (24 dia) és célcsoportonként egyet (14-14 dia).

### 4.8. Minőségellenőrzés és javítások
Minden renderelt képet és minden képernyőt átnéztünk; a hibákat javítottuk és újrarendereltük. A fontosabbak:
- A színházi padló túlnyúlt a patkó alaprajzon, ezért alaprajzhoz igazítottuk.
- A BIM-nézet zárt teremben túl sötét volt, ezért belső modellvilágítást kapott.
- A rendezvényes szkennelésnél fák álltak a tervezett asztalok helyén; a fasort áthelyeztük és újraszkenneltünk.
- Egy rendezvényes panoráma kamerája egy asztal közepére esett, ezért áthelyeztük.
- A szállodai falsarkoknál rés látszott a panorámán; lezártuk.
- A múzeumi túra továbblépési pontjai a szoborra estek; a nézőpontot és a pontok elhelyezését módosítottuk.
- A mesh-nézet színtelen volt, mert az anyag nem került rá a rekonstruált hálóra; javítottuk.
- A hőkép túl egyszínű volt, ezért szélesebb hőmérséklet-tartományt kapott.
- Weboldal: kép-elrendezési hiba az „ugyanaz a tér” résznél, mobilnézet, hosszú szavak tördelése, mátrixdia túlcsordulása.
- Végül ellenőriztük, hogy minden hivatkozott fájl létezik, nincs JavaScript-hiba, és nincs vízszintes kilógás mobilon.

---

## 5. Elkészült anyagok

| Fájl | Leírás |
|---|---|
| `portfolio/index.html` | Webes portfólió (≈ 52 MB a képekkel, panorámákkal, pontfelhőkkel együtt) |
| `portfolio/prezentacio.html` | 16:9-es élő prezentáció |
| `pdf/BrickData_Portfolio_teljes.pdf` | Teljes portfólió, 24 dia |
| `pdf/BrickData_Portfolio_Szinhazak.pdf` | Színházaknak, 14 dia |
| `pdf/BrickData_Portfolio_Rendezvenyhelyszinek.pdf` | Rendezvényhelyszíneknek, 14 dia |
| `pdf/BrickData_Portfolio_Szallodak.pdf` | Szállodáknak, 14 dia |
| `pdf/BrickData_Portfolio_Muzeumok.pdf` | Múzeumoknak, 14 dia |
| `BELSO_ELLENORZES.md` | Belső ellenőrzőlista és szolgáltatásonkénti képanyag-terv |
| `README.md` | Rövid használati útmutató |
| `forras/` | A mátrix kinyerése, valamint a jelenetek, a szkennelés és a renderelés forráskódja |

**Számokban:** 14 szolgáltatás, 4 célcsoport, 4 3D jelenet, 60 kép, 12 db 360°-os panoráma, 3 bejárható pontfelhő, 1 berepülő videó, 5 PDF.

---

## 6. Használat

1. **Megnyitás:** töltsd le a repót ZIP-ként a GitHubról (`claude/architecture-portfolio-clients-1fcjzf` ág), csomagold ki, és kattints duplán a `portfolio/index.html` fájlra (Chrome vagy Edge).
2. **Célcsoport-link:** `index.html?csoport=szinhaz` / `rendezveny` / `szalloda` / `muzeum`.
3. **Élő bemutató:** `prezentacio.html` (← → lapozás, `F` teljes képernyő), célcsoportra szűrve is.
4. **Kiküldés:** a `pdf/` mappából a megfelelő célcsoportos PDF.
5. **Belső nézet** (ezt ne küldd ügyfélnek): `index.html?belso=1`.

---

## 7. Teendők a kiküldés előtt

- [ ] **Kapcsolattartó adatai:** `portfolio/assets/data.js` → `config`, utána a PDF-ek újragenerálása. Jelenleg egyik anyagon sincs elérhetőség.
- [ ] **Hivatalos logó és arculat** (most egy egyszerű „BRICK+DATA” felirat szerepel).
- [ ] **Belső jóváhagyás** a technikai és kereskedelmi állításokra (ki hagyja jóvá?).
- [ ] A `BELSO_ELLENORZES.md` kérdéseinek tisztázása: szkennertípusok, saját és partneri szolgáltatások, formátumok, pontosság, árazás, drónengedélyek, hőkamera.
- [ ] A szín–szöveg ellentmondások átnézése a mátrix gazdájával.

## 8. Javasolt következő lépések

1. **Saját felmérésekkel cserélni a koncepcióképeket**, a legerősebbekkel kezdve. A `BELSO_ELLENORZES.md` 6. pontja szolgáltatásonként leírja, mit érdemes pótolni.
2. **Online közzététel:** a `portfolio/` mappa feltöltése statikus tárhelyre, hogy linkként is küldhető legyen.
3. **Leadlista és e-mail-sablonok összekötése** a célcsoportos PDF-ekkel vagy linkekkel.
4. **Visszajelzés gyűjtése** az első ügyféltalálkozókról: mely szolgáltatások érdeklik leginkább az egyes célcsoportokat, és ennek alapján a mátrix finomítása.
