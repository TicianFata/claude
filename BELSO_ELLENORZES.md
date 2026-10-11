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

## 6. Szolgáltatásonkénti képanyag-terv

Jelölés: Sz = színház, R = rendezvényhelyszín, H = szálloda (hotel), M = múzeum; ● = fő illeszkedés (zöld), ○ = kiegészítő (sárga).

| Szolgáltatás | Célcsoport | Most a portfólióban (koncepció) | Érdemes pótolni saját anyaggal | Belső kérdés |
|---|---|---|---|---|
| 360°-os panorámakép | Sz● R● H● M● | 4 helyszín 360°-os panorámái, körbenézhetően | Saját 360°-os felvétel egy valós színpadról vagy szállodai szobáról | Melyik kamerával, milyen felbontásban? Fényképezés vagy szkennerpanoráma? |
| Virtuális túra panorámapontokkal | Sz● R○ H● M● | Működő túra 3×3 ponttal (színház, rendezvénytér, szálloda, múzeum) | Egy valós helyszín 5–10 pontos túrája, weboldalba ágyazva | Milyen platformon adjuk át (saját, Matterport, Kuula stb.)? Ki tárolja, és mennyiért? |
| Berepülhető 3D túra | R● M● | Böngészőben bejárható pontfelhő (múzeum, rendezvénytér a tervvel) | Saját szkenből készült bejárható modell | Milyen nézőt használunk (Potree, Matterport, saját)? Mekkora fájlt kezel az ügyfél gépe? |
| 360°-os videó | Sz○ R○ H● M● | Panorámakép lejátszófelülettel (illusztráció) | Rövid saját 360°-os videó | Van-e 360°-os videókamera? Utómunka és stabilizálás? |
| Virtuális berepülő videó | Sz○ R● H○ M○ | Renderelt berepülés a kastélyparkról, tervezett elrendezéssel | Saját modellből renderelt 20–40 mp-es videó | Melyik szoftverrel rendereljük, és mennyi idő egy videó? |
| VR / MR / AR bemutató | Sz○ R○ H○ M○ | Sztereó VR-nézet a színházból (illusztráció) | Rövid VR-demó headsettel (pl. Quest) | Van-e eszköz, és ki fejleszti? Ez gyakran partnert igényel. |
| Drónfotó | H○ M○ | Szállodai medencekert alkonyatkor | Saját drónfotó egy referenciahelyszínről | Drónengedély, kategória, biztosítás, repülési tilalmak |
| Drónvideó | R○ H● M○ | Drónnézet lejátszófelülettel, kastélypark | Saját drónvideó | Ugyanaz, mint a drónfotónál, valamint a vágás és a zene jogai |
| Környezeti és megközelítési túra | Sz● R○ H● M● | Felülnézeti térkép útvonallal és panorámapontokkal | Megközelítési útvonal valós panorámapontokkal | A „Google Earth” és a „Street View” név használata; feltöltsük-e a Google-re? |
| Pontfelhő | Sz○ R○ H○ M● | Színház (6,7 M pont) és múzeum (4,3 M pont) szimulált szkenje | Saját TLS-szkenből készült képek és bejárás | Szkennertípus, pontosság, regisztrációs hiba, formátum (E57/LAS/RCP) |
| Mesh (felületmodell) | Sz○ R○ H○ M○ | A pontfelhőből rekonstruált háló, dróthálós nézettel | Saját mesh textúrával | Melyik szoftverrel készül, és mekkora a fájlméret és a részletesség? |
| 3D modell | Sz● R● H○ M○ | Metszeti modellek (színház, szálloda, múzeum, rendezvény-elrendezés) | Saját egyszerűsített modell egy valós helyszínről | Milyen részletességet vállalunk, és milyen formátumban adjuk át? |
| BIM-modell (Revit / Archicad) | Sz○ R○ H● M● | Kategóriánként színezett BIM-nézetek | Képernyőkép valós Revit/Archicad modellből (elemlista, tulajdonságpanel) | LOD-szint, átadási formátum (RVT/PLN/IFC), modellezési idő |
| Hőtérképezés | M○ | Szimulált hőkép (homlokzat, kiállítótér) | Valós hőkamerás felvétel | Van-e hőkamera és minősített kiértékelő? Diagnózist nem ígérünk. |
