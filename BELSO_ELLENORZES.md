# Belső ellenőrzőlista – Brick+Data Scan-to-BIM portfólió

> Belső dokumentum, nem az ügyfélnek szól. A portfólió (web + PDF) kiküldése előtt ezeket kell tisztázni vagy jóváhagyatni.

## 1. Mire épül a portfólió

- **Illeszkedési mátrix:** a `grading_javitott_elso4_leirasokkal.xlsx` **cellaszíneiből** készült, géppel kiolvasva (zöld `#D9EAD3` = fő illeszkedés, sárga `#FFF2CC` = kiegészítő érték, piros `#F4CCCC` = nem jelenik meg). A cellák szövegét és a cellamegjegyzéseket szándékosan nem használtuk forrásként, mert nem teljesen megbízhatók. Az eredmény: `forras/matrix_szinekbol.json`.
- **Szolgáltatásleírások:** a „Mesteranyag” 6. fejezete (mi ez / mire jó / miben más) alapján, rövidítve. A célcsoportonkénti mondatokat (`use`) a mesteranyag célcsoport-prioritásaihoz igazítva újraírtuk.
- **Kimaradt szolgáltatások** (mind a 4 célcsoportnál pirosak): benapozásvizsgálat, kivitelezés nyomon követése, megvalósulási hiba / deformáció elemzése, vegyes (modell + valós) berepülő videó. Ha ezeket mégis szerepeltetni kell (pl. „műszaki szolgáltatások kérésre” blokkban), azt külön kell eldönteni.

### Figyelmeztetés: ahol a színek és a cellaszövegek ellentmondanak

A portfólió a színeket követi. Néhány cellában a szöveg mást sugall, ezeket érdemes a mátrix gazdájával átnézni:

| Szolgáltatás | Célcsoport | Szín (ezt követjük) | A cella szövege / megjegyzése |
|---|---|---|---|
| Berepülhető virtuális túra | Színház | piros (kimarad) | a szöveg szerint díszlettervezéshez hasznos, a megjegyzés szerint „közvetlenül támogatja a látványt” |
| Berepülhető virtuális túra | Szálloda | piros (kimarad) | a szöveg szerint a vendégek bejárhatják a szállodát |
| Vegyes berepülő videó | Szálloda | piros (kimarad) | a szöveg szerint „erős prémium marketingtartalom” |
| Drónfotó | Színház | piros | a megjegyzés szerint „értékes extra lehet” |

## 2. Ügyfélnek küldés előtt kötelező

- [ ] **Kapcsolattartó adatai:** `portfolio/assets/data.js` → `config` (név, e-mail, telefon, weboldal). Utána újra kell generálni a PDF-eket (lásd README).
- [ ] **Hivatalos logó és arculat:** a portfólióban most egy egyszerű „BRICK+DATA” szóvédjegy szerepel. Ha van hivatalos logó vagy színpaletta, azzal kell cserélni.
- [ ] **Jóváhagyás:** a technikai és kereskedelmi állításokat jóváhagyó kolléga neve: ____________

## 3. Belső egyeztetést igényel (a portfólió jelenleg nem állít ilyet)

- [ ] Mely szkennerek és kamerák tartoznak az egyes szolgáltatásokhoz (a három szkennerkategória pontos típusa, korlátai, pontossága)?
- [ ] Mely szolgáltatásokat nyújtjuk házon belül, és melyekhez kell partner, külön szoftver vagy fejlesztés (különösen: VR/MR/AR, 360°-os videó, hőtérképezés, drón)?
- [ ] Átadási formátumok szolgáltatásonként (webes túra, MP4, JPG, E57/LAS/RCP, OBJ/FBX, RVT/PLN/IFC). Csak a ténylegesen támogatottakat szabad feltüntetni.
- [ ] Pontosság, részletesség (LOD), lefedettség, elkészítési idő, árazási logika. A portfólió szándékosan nem tartalmaz számokat.
- [ ] Drónrepülési engedélyek, helyszíni feltételek, biztosítás.
- [ ] A „Google Earth” és a „Street View” név használata: a szövegben csak „jellegű” összehasonlításként szerepel, integrációt nem ígér.
- [ ] Hőtérképezés: van-e minősített szakember és módszertan? A portfólió diagnózist nem ígér.
- [ ] Saját referenciák és demóanyagok (Berci anyagai?), valamint engedély az ügyfél vagy a helyszín megnevezésére. Ha van saját felmérés, azzal érdemes a koncepcióképeket fokozatosan lecserélni.

## 4. A képanyagról

- Minden kép, panoráma, pontfelhő és videó **saját koncepcióvizualizáció**: Blenderben procedurálisan felépített jelenetekből (színházterem, rendezvényhelyszín egy kastélyparkban, szállodai lakosztály, múzeumi kiállítóterem) renderelve. A pontfelhők **virtuális lézerszkenneléssel** készültek: több álláspontból 360°-os szín- és mélységképet rendereltünk, és ezekből raktuk össze a pontokat, ugyanúgy, ahogy egy valódi földi lézerszkenner dolgozik.
- A képeken a „Koncepcióvizualizáció” címke jelzi, hogy nem referenciamunkáról van szó (a mesteranyag 8.4 és 8.5 pontja szerint).
- Felhasznált külső elemek (mind kereskedelmi célra is használható, a forrásmegjelölés a portfólió láblécében és a prezentáció utolsó diáján szerepel):
  - textúrák: ambientCG, Poly Haven (CC0)
  - modellek: Khronos glTF Sample Assets – SheenChair, GlassVaseFlowers, AntiqueCamera (CC0); GlamVelvetSofa (© Wayfair, CC BY 4.0); DiffuseTransmissionPlant (CC BY 4.0); ABeautifulGame (© ASWF / MaterialX Project, CC BY 4.0); MosquitoInAmber (© Loïc Norgeot / Sketchfab, CC BY 4.0)
  - a festmények a múzeumi jelenetben saját, programmal generált képek
  - szoftverek: three.js (MIT), Pannellum (MIT), betűtípusok: Fraunces, Inter, JetBrains Mono (SIL OFL)
- A munkakörnyezet hálózati szabályai miatt a nagy fotóoldalak (Wikimedia Commons, Unsplash, Pexels, Poly Haven CDN) nem voltak elérhetők. Ezért nem használtunk külső fotókat, ami egyben a licencproblémákat is elkerüli.

## 5. Külső inspirációk (csak belső használatra, nem a portfólióba)

A mesteranyag 8.5 pontja szerint külső példákat csak ötletként használunk, Brick+Data-munkaként soha nem tüntetjük fel. Érdemes megnézni (licencellenőrzés nélkül nem ágyazható be):
- Matterport-túrák szállodákról és múzeumokról (pl. a Matterport saját „Discover” galériája),
- múzeumi virtuális túrák (Google Arts & Culture),
- színházi digitális ikrek és BIM-folyamatvideók a szoftvergyártóktól (Autodesk, Graphisoft, Leica, NavVis, Faro).
