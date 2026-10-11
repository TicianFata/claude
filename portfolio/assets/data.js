/* Brick+Data – Scan-to-BIM / reality capture portfólió: tartalom és illeszkedési mátrix.
 *
 * Az illeszkedési szinteket (fo / extra) a "grading_javitott_elso4_leirasokkal.xlsx" cellaszíneiből
 * olvastuk ki géppel (zöld = fo, sárga = extra, piros = nem jelenik meg). A cellák szövegét
 * szándékosan nem használjuk forrásként. Lásd: forras/matrix_szinekbol.json
 */
window.BD = {
  config: {
    // Kitöltendő a kiküldés előtt. Üresen hagyva a kapcsolati sor nem jelenik meg.
    contactName: "",
    contactEmail: "",
    contactPhone: "",
    website: ""
  },

  segments: [
    {
      id: "szinhaz",
      name: "Színházak",
      short: "Színház",
      kicker: "Díszlet- és látványtervezőknek",
      headline: "A színpad ott van, ahol a tervező.",
      message: "A díszlettervező a színpadot és a teret távolról is megismerheti, így kevesebb helyszíni felmérésre lehet szükség.",
      hero: "assets/img/szinhaz-hero.jpg",
      heroAlt: "Patkó alakú színházterem, a színpad felé nézve – fotószerű nézet és pontfelhő egymás mellett",
      story: [
        ["Kihívás", "Minden új produkció előtt meg kell ismerni a színpad arányait, a beépíthető tereket, a hozzáféréseket és a korlátokat. Ez gyakran ismételt helyszíni bejárást jelent."],
        ["Digitális megoldás", "Digitálisan rögzítjük a színpadot, a színpadtechnikai környezetet és a nézőteret."],
        ["Kézzelfogható előny", "A tervezők a digitális térből indulhatnak ki, így kevesebb személyes felmérésre van szükség."],
        ["Amit kézbe kap", "Bejárható 360°-os nézetek és 3D modell, igény szerint pontfelhő, mesh vagy BIM-modell."]
      ]
    },
    {
      id: "rendezveny",
      name: "Rendezvényhelyszínek",
      short: "Rendezvény",
      kicker: "Rendezvényszervezőknek és látványtervezőknek",
      headline: "Az elrendezés a digitális térben kezdődik.",
      message: "A rendezvénytervező távolról is megismerheti a helyszínt, és a digitális térből indulva készítheti elő az elrendezést.",
      hero: "assets/img/rendezveny-hero.jpg",
      heroAlt: "Kastélypark légi nézetben, tervezett színpaddal, sátrakkal és asztalokkal",
      story: [
        ["Kihívás", "Színpad, sátrak, mosdók, asztalok, standok és közlekedési útvonalak: minden rendezvény előkészítéséhez alaposan ismerni kell a helyszínt, ami gyakran több bejárást jelent."],
        ["Digitális megoldás", "A helyszínt 3D-ben rögzítjük, így a tervezők és a kivitelező partnerek ugyanabból a digitális térből dolgozhatnak."],
        ["Kézzelfogható előny", "Kevesebb utazás és gördülékenyebb egyeztetés, a megrendelő pedig előre láthatja a tervezett elrendezést."],
        ["Amit kézbe kap", "3D modell, berepülhető virtuális túra, 360°-os panorámák és berepülő videó a tervezett elrendezésről."]
      ],
      note: "Ha méretre kell tervezni, előre egyeztetjük, melyik kimenet alkalmas erre, és milyen pontossági szinten."
    },
    {
      id: "szalloda",
      name: "Szállodák",
      short: "Szálloda",
      kicker: "Marketing- és értékesítési csapatoknak",
      headline: "Mutassa meg a szállodát, mielőtt a vendég megérkezik.",
      message: "Egyetlen felmérésből többféle digitális bemutató és hosszabb távon is újrahasznosítható marketingtartalom készülhet.",
      hero: "assets/img/szalloda-hero.jpg",
      heroAlt: "Elegáns szállodai lakosztály esti fényekkel",
      story: [
        ["Kihívás", "A vendégek a foglalás előtt online döntenek. A szobákat, a közösségi tereket és a környezetet a hagyományos fotók csak részben adják vissza."],
        ["Digitális megoldás", "Egy átgondolt felmérésből virtuális túra, 360°-os képek és videók, valamint légi felvételek készülnek."],
        ["Kézzelfogható előny", "Személyesebb online élmény a weboldalon, és újrahasznosítható tartalom a marketingcsatornákra."],
        ["Amit kézbe kap", "Weboldalba illeszthető virtuális túra, 360°-os tartalmak és drónvideó, felújításhoz pedig BIM-alap."]
      ]
    },
    {
      id: "muzeum",
      name: "Múzeumok",
      short: "Múzeum",
      kicker: "Kurátoroknak és gyűjteménykezelőknek",
      headline: "A kiállítás bezár. A digitális tere nyitva marad.",
      message: "A kiállítás digitálisan akkor is tovább élhet, amikor a fizikai installáció már nincs a helyén.",
      hero: "assets/img/muzeum-hero.jpg",
      heroAlt: "Felülvilágítós kiállítóterem festményekkel és szobrokkal",
      story: [
        ["Kihívás", "Az időszakos kiállítások a bontással eltűnnek, a tér, az installáció és a látogatói élmény pedig nehezen dokumentálható."],
        ["Digitális megoldás", "A kiállítóteret 360°-os panorámákkal, pontfelhővel és bejárható digitális térrel rögzítjük."],
        ["Kézzelfogható előny", "A kiállítás a bontás után is megőrizhető és online bejárható: távoli látogatóknak, oktatási célra és az archívumnak."],
        ["Amit kézbe kap", "Virtuális túra, 360°-os kép és videó, pontfelhő-archívum és BIM-alapú épületdokumentáció."]
      ],
      note: "A műtárgyak és az érzékeny terek rögzítésének feltételeit (fényviszonyok, hozzáférés, adatkezelés) előre egyeztetjük."
    }
  ],

  groups: [
    { id: "elmeny", name: "Bejárás és élmény" },
    { id: "legi", name: "Légi és környezeti nézet" },
    { id: "modell", name: "3D adat és modell" },
    { id: "diag", name: "Állapotvizsgálat" }
  ],

  /* fit: "fo" = zöld (legjobban illik), "extra" = sárga (kiegészítő érték); a piros kombinációk hiányoznak */
  services: [
    {
      id: "pano360", group: "elmeny", name: "360°-os panorámakép", excel: "360 panoráma képek",
      img: "assets/img/svc-pano360.jpg", imgSeg: { szinhaz: "assets/img/szinhaz-pano360.jpg", rendezveny: "assets/img/rendezveny-pano360.jpg", muzeum: "assets/img/muzeum-pano360.jpg" }, pano: "assets/pano/szalloda-lakosztaly.jpg",
      mi: "Egyetlen álláspontból készült, minden irányba körbenézhető kép.",
      mire: "Helyiségek, vendégterek, kiállítások és helyszínek látványos bemutatására, webes és közösségi tartalomként.",
      kulonbseg: "Állókép egy adott pontról. Nem videó, és nem szabadon bejárható 3D tér.",
      fit: { szinhaz: "fo", rendezveny: "fo", szalloda: "fo", muzeum: "fo" },
      use: {
        szinhaz: "A színpad és a nézőtér a próbák között is körbejárható nézetben áll a tervezők rendelkezésére.",
        rendezveny: "A szervezők körbenézhetnek a helyszínen, mielőtt egyetlen bejárást is szerveznének.",
        szalloda: "A szobák és a közösségi terek körbenézhető képei a weboldalon és a közösségi médiában is működnek.",
        muzeum: "A kiállítóterek állapota egy-egy pillanatképben megőrizhető és online megmutatható."
      }
    },
    {
      id: "tura", group: "elmeny", name: "Virtuális túra panorámapontokkal", excel: "Street view szerű virtuális túra",
      img: "assets/img/svc-tura.jpg", imgSeg: { szalloda: "assets/img/szalloda-tura.jpg", muzeum: "assets/img/muzeum-tura.jpg", rendezveny: "assets/img/rendezveny-tura.jpg" },
      mi: "Egymáshoz kapcsolt 360°-os panorámapontok, amelyek között a látogató egy kattintással lép tovább, ahogy a Street View-ban.",
      mire: "Egyszerű, böngészőben futó online helyszínbejárás vendégeknek, látogatóknak és érdeklődőknek.",
      kulonbseg: "A felhasználó a rögzített pontok között mozog, a teljes 3D teret nem járhatja be tetszőlegesen.",
      fit: { szinhaz: "fo", rendezveny: "extra", szalloda: "fo", muzeum: "fo" },
      use: {
        szinhaz: "A díszlettervezők és a produkciós csapatok távolról is végigjárhatják a színpadot, a takarásokat és a nézőteret.",
        rendezveny: "Az ügyfelek és a partnerek előzetesen végigjárhatják a helyszín fő pontjait.",
        szalloda: "A weboldalba illesztett túrán a vendég már a foglalás előtt körbejárhatja a szobát.",
        muzeum: "Az időszakos kiállítás a zárás után is online végigjárható marad."
      }
    },
    {
      id: "repulheto", group: "elmeny", name: "Berepülhető 3D túra", excel: "Berepülhető virtuális túra (Mesh / Pontfelhő)",
      img: "assets/img/svc-repulheto.jpg", imgSeg: { rendezveny: "assets/img/rendezveny-pontfelho-terv.jpg" },
      mi: "Szabad mozgás a digitálisan rögzített térben, nemcsak előre kijelölt panorámapontok között.",
      mire: "A tér részletes távoli megismerésére és a térbeli elrendezés előzetes megértésére.",
      kulonbseg: "Szabadabb mozgást és jobb térérzetet ad, de a navigáció minősége a feldolgozott modelltől és a megjelenítőtől függ.",
      fit: { rendezveny: "fo", muzeum: "fo" },
      use: {
        rendezveny: "A tervezők bármely nézőpontból megvizsgálhatják a helyszínt, és erre építhetik a teljes elrendezést.",
        muzeum: "A kiállítás digitálisan bejárható és később is elérhető, a szezonális tárlatoké is."
      }
    },
    {
      id: "pano360video", group: "elmeny", name: "360°-os videó", excel: "360 panoráma videó",
      img: "assets/img/svc-video360.jpg", imgSeg: { szinhaz: "assets/img/szinhaz-video360.jpg", rendezveny: "assets/img/rendezveny-video360.jpg", szalloda: "assets/img/szalloda-video360.jpg" },
      mi: "Mozgóképes 360°-os felvétel, amelyben a néző lejátszás közben bármerre körbenézhet.",
      mire: "Élményalapú helyszínbemutatásra, turisztikai és eseménymarketingre.",
      kulonbseg: "A kamera útvonala és a felvétel idővonala előre rögzített, így ez nem azonos a szabadon bejárható túrával.",
      fit: { szinhaz: "extra", rendezveny: "extra", szalloda: "fo", muzeum: "fo" },
      use: {
        szinhaz: "A színpad és a nézőtér térélménye mozgóképen is átadható a produkciós csapatnak.",
        rendezveny: "A helyszín hangulata és térbeli adottságai mozgásban is bemutathatók.",
        szalloda: "Hangulatos, magával ragadó tartalom a weboldalra és a közösségi felületekre.",
        muzeum: "A kiállítás hangulata és térbeli kialakítása mozgóképen is megőrizhető."
      }
    },
    {
      id: "berepulo", group: "elmeny", name: "Virtuális berepülő videó", excel: "Virtuális berepülő videó",
      img: "assets/img/svc-berepulo.jpg", imgSeg: { szinhaz: "assets/img/szinhaz-berepulo.jpg", szalloda: "assets/img/szalloda-berepulo.jpg", muzeum: "assets/img/muzeum-berepulo.jpg" }, video: "assets/video/szinhaz-berepulo.mp4",
      mi: "A digitális modellből előre megtervezett kameraúttal renderelt videó.",
      mire: "Látványos marketingre, bemutatókra és vezetett térbemutatásra.",
      kulonbseg: "A néző egy előre megszerkesztett kameraútvonalat követ. A minőséget a modell, a textúrák, a fények és az utómunka határozzák meg.",
      fit: { szinhaz: "extra", rendezveny: "fo", szalloda: "extra", muzeum: "extra" },
      use: {
        szinhaz: "A színpad és a tér egy filmszerű bejárásban jelenik meg a produkciós egyeztetéseken.",
        rendezveny: "A helyszín és a tervezett elrendezés egyetlen látványos videóban mutatható be a megrendelőnek és a partnereknek.",
        szalloda: "Prémium, többször felhasználható videós tartalom a szállodáról.",
        muzeum: "A kiállítás vagy az épület filmszerű digitális bemutatása, főleg online kommunikációhoz."
      }
    },
    {
      id: "xr", group: "elmeny", name: "VR / MR / AR bemutató", excel: "VR/MR/AR prezentáció",
      img: "assets/img/svc-xr.jpg",
      mi: "Immerzív bemutató: a VR virtuális térbe helyezi a nézőt, az AR digitális elemeket illeszt a valós környezetbe, az MR pedig a kettőt térben összekapcsolja.",
      mire: "Látványos ügyfélélményre, térbeli koncepciók megértésére, díszlet-, rendezvény- és kiállítási tervek bemutatására.",
      kulonbseg: "Ez nem fájlformátum, hanem megjelenítési réteg, amelyhez megfelelő modell, eszköz és fejlesztés kell.",
      fit: { szinhaz: "extra", rendezveny: "extra", szalloda: "extra", muzeum: "extra" },
      use: {
        szinhaz: "A díszletterv már a megvalósítás előtt bejárható és egyeztethető.",
        rendezveny: "A tervezett térbeli kialakítás virtuálisan bemutatható a tervezőknek és a megrendelőnek.",
        szalloda: "Interaktív, prémium élmény a leendő vendégeknek, például a szobák virtuális bemutatására.",
        muzeum: "Digitális kiállítások és kiegészítő élmények, amelyek a helyszíni látogatást is gazdagíthatják."
      }
    },
    {
      id: "dronfoto", group: "legi", name: "Drónfotó", excel: "Drón felvétel kép",
      img: "assets/img/svc-dronfoto.jpg", imgSeg: { muzeum: "assets/img/muzeum-dron.jpg" },
      mi: "Drónról készített légi állókép.",
      mire: "Az épület, a környezet, a megközelítés és a nagyobb területek bemutatására.",
      kulonbseg: "Légi nézetet ad, de nem helyettesíti a belső térfelmérést vagy a műszaki modellt.",
      fit: { szalloda: "extra", muzeum: "extra" },
      use: {
        szalloda: "Prémium külső képek a weboldalra, a foglalási oldalakra és a közösségi médiába.",
        muzeum: "Az épület és környezete látványosan dokumentálható, különösen ha az építészeti érték kívül van."
      }
    },
    {
      id: "dronvideo", group: "legi", name: "Drónvideó", excel: "Drón felvétel videó",
      img: "assets/img/svc-dronvideo.jpg", imgSeg: { rendezveny: "assets/img/rendezveny-dronvideo.jpg", szalloda: "assets/img/szalloda-dronvideo.jpg" }, video: "assets/video/kastely-dron.mp4",
      mi: "Drónnal készített mozgóképes légi felvétel.",
      mire: "Szállodák, rendezvényhelyszínek és épületek dinamikus bemutatására, a környezet és a megközelítés érzékeltetésére.",
      kulonbseg: "Mozgóképes narratívát ad, míg a drónfotó egy-egy pillanatot rögzít. A repülési feltételeket minden helyszínen ellenőrizni kell.",
      fit: { rendezveny: "extra", szalloda: "fo", muzeum: "extra" },
      use: {
        rendezveny: "A helyszín és a rendezvény léptéke látványos promóciós tartalomként mutatható be.",
        szalloda: "Prémium videós tartalom a szállodáról és környezetéről, amely több csatornán is felhasználható.",
        muzeum: "Az épület és a külső terek mozgóképes bemutatása és dokumentálása."
      }
    },
    {
      id: "kornyezet", group: "legi", name: "Környezeti és megközelítési túra", excel: "Google Earth street-view túra",
      img: "assets/img/svc-kornyezet.jpg",
      mi: "A környezet, az odavezető út és a külső megközelítés navigálható, panorámás bemutatása (Google Earth / Street View jellegű).",
      mire: "Megmutatja, hogyan közelíthető meg a helyszín, mi van a környékén, és milyen a környezete.",
      kulonbseg: "A külső környezetre és az útvonalra koncentrál, nem a belső tér részletes modellezésére.",
      fit: { szinhaz: "fo", rendezveny: "extra", szalloda: "fo", muzeum: "fo" },
      use: {
        szinhaz: "A helyszín, a beszállítási útvonal és a környezet előre megmutatható a produkciós csapatnak.",
        rendezveny: "A megközelítés és a környezet előre bemutatható a szervezőknek és a tervezőknek.",
        szalloda: "A vendégek már foglalás előtt megismerhetik a szálloda környezetét és megközelítését.",
        muzeum: "A múzeum és környezete online felfedezhető, ami kiegészíti a digitális látogatást."
      }
    },
    {
      id: "pontfelho", group: "modell", name: "Pontfelhő", excel: "Pontfelhő",
      img: "assets/img/svc-pontfelho.jpg", imgSeg: { muzeum: "assets/img/muzeum-pontfelho-felul.jpg", rendezveny: "assets/img/rendezveny-pontfelho.jpg" },
      mi: "A szkennelés nyers eredménye: térbeli koordinátákkal rendelkező mérési pontok milliói, amelyek leírják a rögzített felületeket.",
      mire: "A meglévő állapot dokumentálására, méretek levételére és a további modellezés alapjául, a mérés minőségétől függően.",
      kulonbseg: "Nyers vagy részben feldolgozott mérési adat. Nem textúrázott mesh és nem strukturált BIM-modell.",
      fit: { szinhaz: "extra", rendezveny: "extra", szalloda: "extra", muzeum: "fo" },
      use: {
        szinhaz: "Digitális alap a színpad és a terek díszlettervezéséhez, kevesebb helyszíni felméréssel.",
        rendezveny: "Téradat a színpadok, sátrak, asztalok, mosdók és más elemek megtervezéséhez.",
        szalloda: "A felújításokhoz és átalakításokhoz ad digitális állapotfelmérést.",
        muzeum: "Digitális állapotdokumentáció a kiállítóterek archiválásához, felújításához és későbbi feldolgozásához."
      }
    },
    {
      id: "mesh", group: "modell", name: "Mesh (felületmodell)", excel: "Mesh pontfelhőből",
      img: "assets/img/svc-mesh.jpg",
      mi: "A pontfelhőből létrehozott, összefüggő háromszögháló, amely textúrával is ellátható.",
      mire: "A tér vizuális megjelenítésére, bejárható digitális tér és prezentációk készítésére.",
      kulonbseg: "Folytonos felületként mutatja a geometriát, de nem azonos a pontfelhővel, és automatikusan nem BIM.",
      fit: { szinhaz: "extra", rendezveny: "extra", szalloda: "extra", muzeum: "extra" },
      use: {
        szinhaz: "A színpad és a terek könnyen kezelhető 3D változata a díszlet- és tértervezéshez.",
        rendezveny: "A helyszín 3D-ben feldolgozható, így az elrendezésen távolról is lehet dolgozni.",
        szalloda: "A valós térből látványos 3D tartalom készülhet online bemutatóhoz.",
        muzeum: "A kiállítások 3D-ben archiválhatók, és később digitális bejáráshoz is felhasználhatók."
      }
    },
    {
      id: "modell3d", group: "modell", name: "3D modell", excel: "3D modell",
      img: "assets/img/svc-3dmodell.jpg", imgSeg: { rendezveny: "assets/img/rendezveny-3dmodell.jpg", szalloda: "assets/img/szalloda-3dmodell.jpg", muzeum: "assets/img/muzeum-3dmodell.jpg" },
      mi: "A tér vagy egy tárgy háromdimenziós digitális mása, amelynek részletessége a felhasználási céltól függ.",
      mire: "Térbeli megértésre, koncepciók és elrendezések szemléltetésére, prezentációra és tervezési alapként.",
      kulonbseg: "Tág kategória: nem feltétlenül tartalmaz BIM-adatokat, és nem minden esetben szerkeszthető műszaki modell.",
      fit: { szinhaz: "fo", rendezveny: "fo", szalloda: "extra", muzeum: "extra" },
      use: {
        szinhaz: "A színpad és a teljes tér modellje a díszlettervezés és az új előadások tervezésének kiindulópontja.",
        rendezveny: "A helyszín modelljén a tervezők távolról helyezhetik el a színpadot, a sátrakat, az asztalokat és a többi elemet.",
        szalloda: "A szálloda modelljéből látványos marketingtartalom és online térbemutató készülhet.",
        muzeum: "A kiállítóterek modellje online bemutatásra és az időszakos kiállítások archiválására használható."
      }
    },
    {
      id: "bim", group: "modell", name: "BIM-modell (Revit / Archicad)", excel: "BIM modell (Revit, Archicad)",
      img: "assets/img/svc-bim.jpg", imgSeg: { szalloda: "assets/img/szalloda-bim-metszet.jpg", muzeum: "assets/img/muzeum-bim.jpg" },
      mi: "Objektumalapú épületmodell, amelynek elemeihez a geometria mellett tulajdonságok és rendszerezett információk is tartoznak.",
      mire: "Felújításhoz, átalakításhoz, üzemeltetéshez és dokumentációhoz, valamint más BIM-alapú munkafolyamatokhoz.",
      kulonbseg: "Ez nem csupán látványos 3D modell vagy pontfelhő. Részletességét a megrendelő igényei határozzák meg.",
      fit: { szinhaz: "extra", rendezveny: "extra", szalloda: "fo", muzeum: "fo" },
      use: {
        szinhaz: "A pontos épületmodell a későbbi átalakítások és a tértervezési feladatok alapja lehet.",
        rendezveny: "Részletes helyszíntervezéshez és állandó beépítésekhez ad megbízható alapot.",
        szalloda: "Felújítások és átalakítások digitális alapja, amely a marketingcélú felmérésből is kiindulhat.",
        muzeum: "Az épület digitális dokumentációja felújításhoz, átalakításhoz és hosszú távú archiváláshoz."
      }
    },
    {
      id: "hoterkep", group: "diag", name: "Hőtérképezés", excel: "Hőtérképezés",
      img: "assets/img/svc-hoterkep.jpg", imgSeg: { muzeum: "assets/img/muzeum-hokep.jpg" },
      mi: "Hőkamerás felvétel, amely a felületi hőmérséklet-különbségeket színekkel jeleníti meg.",
      mire: "Megfelelő körülmények és szakértelem mellett az épület és a kiállítási környezet állapotának vizsgálatára.",
      kulonbseg: "Nem marketinganyag: az eredmények értelmezése a mérési körülményektől és a módszertantól függ.",
      fit: { muzeum: "extra" },
      use: {
        muzeum: "Segíthet feltárni a kiállítási környezet hőtechnikai sajátosságait, például az érzékeny műtárgyak közelében."
      }
    }
  ],

  /* "Ugyanaz a tér – több kimenet" összehasonlító nézetek (azonos kameraállásból) */
  sameSpace: [
    { id: "latvany", name: "Fotószerű nézet", img: "assets/img/same-latvany.jpg", txt: "A rögzített tér, ahogy a szem látja. Ebből készülnek a 360°-os képek és a látványanyagok." },
    { id: "pontfelho", name: "Pontfelhő", img: "assets/img/same-pontfelho.jpg", txt: "Mérési pontok milliói, valós színekkel. Ez a nyers digitális lenyomat." },
    { id: "magassag", name: "Pontfelhő (magasság)", img: "assets/img/same-magassag.jpg", txt: "Ugyanazok a pontok magasság szerint színezve: így jobban kiolvashatók a szintek és a lejtések." },
    { id: "mesh", name: "Mesh", img: "assets/img/same-mesh.jpg", txt: "A pontokból összefüggő háromszögháló lesz, amely könnyebben kezelhető és megjeleníthető." },
    { id: "bim", name: "BIM-modell", img: "assets/img/same-bim.jpg", txt: "Az elemek (fal, födém, mellvéd, ülés, színpad) külön objektumok, saját adatokkal." }
  ],

  process: [
    { n: "01", t: "Rögzítés", d: "Lézerszkenner és 360°-os kamera több álláspontból, a helyszín és a cél szerint megtervezve." },
    { n: "02", t: "Feldolgozás", d: "Az állásokat egyetlen koordináta-rendszerbe illesztjük, és színezett pontfelhőt hozunk létre." },
    { n: "03", t: "Kimenetek", d: "A célhoz illő termékek: panoráma, túra, videó, mesh, 3D modell vagy BIM." },
    { n: "04", t: "Felhasználás", d: "Marketing, ügyfélélmény, tér- és díszlettervezés, és ahol szükséges, műszaki munka." }
  ],

  /* belső nézet (?belso=1): ellenőrzendő pontok */
  internal: [
    "Mely szkennerek és kamerák tartoznak az egyes szolgáltatásokhoz? A pontos típus, a korlátok és a pontosság még nincs rögzítve.",
    "Mely szolgáltatásokat nyújtjuk házon belül, és melyekhez kell partner, külön szoftver vagy fejlesztés (pl. VR/MR/AR, 360°-os videó, hőtérképezés)?",
    "Átadási formátumok szolgáltatásonként (webes túra, videó, képfájl, E57/LAS, OBJ/FBX, RVT/PLN/IFC). Csak a ténylegesen támogatottakat szabad feltüntetni.",
    "Pontosság, részletesség, lefedettség, elkészítési idő, árazási logika: belső iránymutatás szükséges.",
    "Saját referenciák és demóanyagok (Berci anyagai?), valamint engedély az ügyfél vagy a helyszín megnevezésére.",
    "Drónrepülési engedélyek és helyszíni feltételek; a „Google Earth” és a „Street View” márkanév használata.",
    "A technikai és kereskedelmi állításokat jóváhagyó kolléga neve."
  ]
};
