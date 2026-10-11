/* Brick+Data – 16:9 prezentáció (élő bemutatás: nyilak / kattintás; PDF: nyomtatás) */
(function () {
  "use strict";
  var D = window.BD, Q = new URLSearchParams(location.search);
  var SEG = Q.get("csoport");
  if (!D.segments.some(function (s) { return s.id === SEG; })) SEG = null;
  var deck = document.getElementById("deck");
  var esc = function (t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;"); };
  var TAG = '<span class="tag">Koncepcióvizualizáció</span>';
  var seg = function (id) { return D.segments.filter(function (s) { return s.id === id; })[0]; };
  var imgFor = function (s, segId) { return (segId && s.imgSeg && s.imgSeg[segId]) || s.img; };
  var fit = function (segId, lv) { return D.services.filter(function (s) { return s.fit[segId] === lv; }); };
  var slides = [];
  var label = SEG ? seg(SEG).name : "Szolgáltatási portfólió";
  function add(cls, html) { slides.push('<section class="slide ' + cls + '">' + html + "</section>"); }
  function foot(light) { return '<div class="foot"><span><b>BRICK+DATA</b> · ' + esc(label) + "</span><span>{{n}}</span></div>"; }
  function media(src, alt, style, tag) {
    return '<div class="media"' + (style ? ' style="' + style + '"' : "") + '><img src="' + src + '" alt="' + esc(alt || "") + '">' + (tag === false ? "" : TAG) + "</div>";
  }

  /* 1 – cover */
  var COVER = {
    szinhaz: ["assets/img/hero-foto.jpg", "assets/img/hero-pontfelho.jpg", "Fotószerű nézet", "Pontfelhő"],
    muzeum: ["assets/img/muzeum-hero.jpg", "assets/img/muzeum-pontfelho.jpg", "Fotószerű nézet", "Pontfelhő"],
    rendezveny: ["assets/img/rendezveny-hero.jpg", "assets/img/rendezveny-terv.jpg", "Drónnézet", "3D elrendezésterv"],
    szalloda: ["assets/img/szalloda-hero.jpg", "assets/img/szalloda-bim.jpg", "Fotószerű nézet", "BIM-modell"]
  };
  var cv = COVER[SEG || "szinhaz"];
  var s0 = SEG ? seg(SEG) : null;
  var title = SEG ? esc(s0.headline).replace(/\.\s/, ".<br><em>") + (/\.\s/.test(s0.headline) ? "</em>" : "") : "Egy felmérés.<br><em>Sokféle digitális érték.</em>";
  add("cover", '<div class="split"><img src="' + cv[0] + '" alt=""><img class="r" src="' + cv[1] + '" alt=""><div class="line"></div></div>' +
    '<div class="lbls"><span style="left:120px">' + cv[2] + '</span><span style="left:calc(58% + 24px);color:var(--scan)">' + cv[3] + "</span></div>" +
    '<div class="shade-l"></div><div class="shade-b" style="opacity:.6"></div>' +
    '<div class="top"><div class="brand">BRICK<i>+</i>DATA</div><span>Reality capture · Scan-to-BIM · 2026</span></div>' +
    '<div class="copy"><div class="eyebrow">' + (SEG ? esc(s0.name) + " · " + esc(s0.kicker) : "3D térfelmérés · Szolgáltatási portfólió") + "</div><h1>" + title + '</h1><p class="lead">' +
    (SEG ? esc(s0.message) : "Digitálisan rögzítjük a teret, és a célhoz illő formában adjuk át színházaknak, rendezvényhelyszíneknek, szállodáknak és múzeumoknak.") + "</p></div>" +
    '<span class="tag" style="left:auto;right:120px;bottom:60px">Koncepcióvizualizáció</span>');

  /* 2 – idea */
  add("light", '<div class="pad"><div class="two"><div><div class="eyebrow">Az alapgondolat</div><h2 style="margin-top:28px">Nem pontfelhőt kínálunk.<br><em>Hanem azt, amit lehetővé tesz.</em></h2></div>' +
    '<p class="lead">Egyetlen átgondolt felmérésből olyan digitális anyag készül, amely a marketingben, az értékesítésben és a tervezésben is hasznos, és ahol szükséges, később műszaki alapként is szolgál.</p></div>' +
    '<div class="values"><div><span class="n">01</span><h4>Marketing</h4><p>Több és változatosabb látványtartalom a digitális csatornákra.</p></div><div><span class="n">02</span><h4>Ügyfélélmény</h4><p>A helyszín távolról is felfedezhető.</p></div><div><span class="n">03</span><h4>Értékesítés</h4><p>A helyszín könnyebben bemutatható és előre megérthető.</p></div><div><span class="n">04</span><h4>Tér- és eseménytervezés</h4><p>A tervező a digitális térből indulhat ki, utazás nélkül.</p></div><div style="opacity:.8"><span class="n">05</span><h4>Műszaki alap</h4><p>Dokumentáció, felújítás, BIM, megfelelő felméréssel.</p></div></div></div>' + foot(true));

  /* 3 – process */
  var procImgs = ["assets/img/proc-rogzites.jpg", "assets/img/proc-feldolgozas.jpg", "assets/img/proc-kimenetek.jpg", "assets/img/proc-felhasznalas.jpg"];
  add("", '<div class="pad"><div class="eyebrow">Így készül</div><h2 style="margin-top:24px">A helyszíntől a <em>kész digitális anyagig</em></h2><div class="process">' +
    D.process.map(function (p, i) { return "<div>" + media(procImgs[i], p.t) + '<span class="n">' + p.n + "</span><h3>" + esc(p.t) + "</h3><p>" + esc(p.d) + "</p></div>"; }).join("") +
    "</div></div>" + foot());

  /* 4 – same space */
  var ss = D.sameSpace;
  add("", '<div class="pad"><div class="two" style="align-items:end"><div><div class="eyebrow">Ugyanaz a tér, több kimenet</div><h2 style="margin-top:24px">Nem minden 3D <em>ugyanaz.</em></h2></div><p class="lead" style="font-size:25px">Ugyanaz a színházterem, ugyanabból a nézőpontból, ötféle formában. A pontfelhő, a mesh, a 3D modell és a BIM más-más célra való.</p></div>' +
    '<div class="same">' + [0, 1, 3, 4, 2].map(function (i) {
      var v = ss[i];
      return '<div class="media"><img src="' + v.img + '" alt=""><div class="lab">' + esc(v.name) + (i === 0 || i === 1 ? "<small>" + esc(v.txt) + "</small>" : "") + "</div>" + (i === 0 ? TAG : "") + "</div>";
    }).join("") + "</div></div>" + foot());

  /* 5 – ladder */
  var ladder = [
    ["NYERS MÉRÉS", "Pontfelhő", "Pontok milliói, valós színnel. A meglévő állapot hű lenyomata.", "assets/img/svc-pontfelho.jpg"],
    ["FELÜLET", "Mesh", "Összefüggő háromszögháló: könnyebb megjeleníteni és bejárni.", "assets/img/svc-mesh.jpg"],
    ["TÉRBELI MODELL", "3D modell", "Tisztított geometria prezentációhoz, elrendezéshez és látványtervhez.", "assets/img/svc-3dmodell.jpg"],
    ["INFORMÁCIÓ", "BIM-modell", "Objektumok saját adatokkal felújításhoz, üzemeltetéshez és dokumentációhoz.", "assets/img/svc-bim.jpg"]
  ];
  add("", '<div class="pad"><div class="eyebrow">Mi a különbség?</div><h2 style="margin-top:24px">A nyers méréstől <em>az információs modellig</em></h2><div class="ladder">' +
    ladder.map(function (l) { return "<div>" + media(l[3], l[1]) + '<span class="lv">' + l[0] + "</span><h4>" + l[1] + "</h4><p>" + l[2] + "</p></div>"; }).join("") +
    '</div><p class="small" style="margin-top:40px">Bejárás és élmény: a <b style="color:#ece7df">360°-os kép</b> egy pontból körbenéz; a <b style="color:#ece7df">virtuális túra</b> panorámapontok között lép; a <b style="color:#ece7df">berepülhető 3D túra</b> szabad mozgást ad; a <b style="color:#ece7df">berepülő videó</b> előre megtervezett kameraút; a <b style="color:#ece7df">360°-os videó</b> mozgókép, amelyben körbe lehet nézni.</p></div>' + foot());

  /* 6 – segments overview (full deck only) */
  if (!SEG) {
    add("light", '<div class="pad"><div class="two"><div><div class="eyebrow">Célcsoportok</div><h2 style="margin-top:24px">Mindenkinek <em>mást jelent</em> ugyanaz a felmérés</h2></div><p class="lead">Zöld: legjobban illő megoldás. Borostyán: kiegészítő érték. Amit egy területnek nem javaslunk, azt nem erőltetjük.</p></div><div class="segs">' +
      D.segments.map(function (s, i) {
        return '<div class="seg"><img src="' + s.hero + '" alt=""><div class="in"><span class="k">0' + (i + 1) + " · " + esc(s.kicker) + "</span><h3>" + esc(s.name) + "</h3><p>" + esc(s.message) + '</p><div class="cnt"><span><i class="dot fo"></i>' + fit(s.id, "fo").length + ' fő</span><span><i class="dot extra"></i>' + fit(s.id, "extra").length + " kiegészítő</span></div></div></div>";
      }).join("") + "</div></div>" + foot(true));
  }

  /* segment chapters */
  D.segments.forEach(function (s, i) {
    if (SEG && SEG !== s.id) return;
    add("opener", '<img class="fill" src="' + s.hero + '" alt=""><div class="shade-b"></div><span class="tag" style="left:auto;right:120px;top:70px;bottom:auto">Koncepcióvizualizáció</span>' +
      '<div class="copy"><div class="eyebrow" style="color:var(--brass-2)">0' + (i + 1) + " / " + esc(s.name) + "</div><h2>" + esc(s.headline) + '</h2><p class="lead">' + esc(s.message) + "</p></div>" +
      '<div class="story">' + s.story.map(function (st) { return '<div><span class="k">' + esc(st[0]) + "</span><p>" + esc(st[1]) + "</p></div>"; }).join("") + "</div>" + foot());
    var fo = fit(s.id, "fo"), ex = fit(s.id, "extra");
    add("light", '<div class="pad"><div class="head-row"><div><div class="eyebrow">' + esc(s.name) + '</div><h2 style="margin-top:20px;font-size:64px">Legjobban illő szolgáltatások</h2></div><span class="pill fo">Fő illeszkedés · ' + fo.length + "</span></div>" +
      '<div class="grid-fo n' + (fo.length <= 4 ? 4 : fo.length <= 6 ? 6 : 7) + '">' + fo.map(function (sv) {
        return "<div>" + media(imgFor(sv, s.id), sv.name) + "<h4>" + esc(sv.name) + "</h4><p>" + esc(sv.use[s.id]) + "</p></div>";
      }).join("") + "</div></div>" + foot(true));
    add("light", '<div class="pad"><div class="head-row"><div><div class="eyebrow">' + esc(s.name) + '</div><h2 style="margin-top:20px;font-size:64px">Kiegészítő érték</h2></div><span class="pill extra">Extra · ' + ex.length + "</span></div>" +
      '<div class="extras">' + ex.map(function (sv) {
        return '<div class="row">' + media(imgFor(sv, s.id), sv.name, "", false) + "<div><h5>" + esc(sv.name) + "</h5><p>" + esc(sv.use[s.id]) + "</p></div></div>";
      }).join("") + "</div>" + (s.note ? '<div class="note">' + esc(s.note) + "</div>" : "") + "</div>" + foot(true));
  });

  /* demos */
  add("", '<div class="pad"><div class="two"><div><div class="eyebrow">Interaktív bemutatók</div><h2 style="margin-top:24px">Böngészőben, <em>telepítés nélkül.</em></h2></div><p class="lead" style="font-size:25px">A portfólió webes változatában a túrák és a pontfelhők élőben bejárhatók. Ilyen formában kapja meg az ügyfél is.</p></div>' +
    '<div class="demos">' +
    '<div class="media"><img src="' + (SEG === "szalloda" ? "assets/img/szalloda-tura.jpg" : SEG === "muzeum" ? "assets/img/muzeum-tura.jpg" : SEG === "rendezveny" ? "assets/img/rendezveny-tura.jpg" : "assets/img/svc-tura.jpg") + '" alt="">' + TAG + '<div class="cap"><b>Virtuális túra panorámapontokkal</b><span>Körbenézés húzással, továbblépés a pontokra kattintva</span></div></div>' +
    '<div class="media"><img src="' + (SEG === "rendezveny" ? "assets/img/rendezveny-pontfelho-terv.jpg" : "assets/img/svc-repulheto.jpg") + '" alt="">' + TAG + '<div class="cap"><b>Berepülhető pontfelhő</b><span>Szabad bejárás, nézőpontok, végigrepülés</span></div></div>' +
    '<div class="media"><img src="assets/img/svc-berepulo.jpg" alt="">' + TAG + '<div class="cap"><b>Virtuális berepülő videó</b><span>Előre megtervezett kameraút a 3D modellből</span></div></div>' +
    "</div></div>" + foot());

  /* catalogue */
  var list = D.services.filter(function (s) { return !SEG || s.fit[SEG]; });
  var chunks = [];
  for (var k = 0; k < list.length; k += 8) chunks.push(list.slice(k, k + 8));
  chunks.forEach(function (ch, ci) {
    add("light", '<div class="pad"><div class="head-row"><div><div class="eyebrow">Szolgáltatások' + (chunks.length > 1 ? " · " + (ci + 1) + "/" + chunks.length : "") + '</div><h2 style="margin-top:20px;font-size:62px">Mi ez, <em>és mire jó?</em></h2></div></div><div class="cat">' +
      ch.map(function (s) {
        var fits = D.segments.map(function (sg) { var lv = s.fit[sg.id]; return lv ? '<span class="fitchip ' + lv + '">' + esc(sg.short) + "</span>" : ""; }).join("");
        return '<div class="c">' + media(imgFor(s, SEG), s.name, "", false) + "<h4>" + esc(s.name) + "</h4><p>" + esc(s.mi) + '</p><div class="fits">' + fits + "</div></div>";
      }).join("") + "</div></div>" + foot(true));
  });

  /* matrix */
  var rows = "";
  D.groups.forEach(function (g) {
    rows += '<tr class="grp"><td colspan="5">' + esc(g.name) + "</td></tr>";
    D.services.filter(function (s) { return s.group === g.id; }).forEach(function (s) {
      rows += "<tr><td>" + esc(s.name) + "</td>" + D.segments.map(function (sg) {
        var lv = s.fit[sg.id];
        return '<td class="' + (SEG === sg.id ? "hl" : "") + '">' + (lv ? '<span class="mk ' + lv + '"></span>' : '<span class="mk no">–</span>') + "</td>";
      }).join("") + "</tr>";
    });
  });
  add("", '<div class="pad" style="top:70px"><div class="eyebrow">Illeszkedési mátrix</div><h2 style="margin-top:14px;font-size:54px">Egy pillantással: <em>mit kinek ajánlunk</em></h2>' +
    '<table class="mx" style="font-size:18px;margin-top:26px"><thead><tr><th>Szolgáltatás</th>' + D.segments.map(function (s) { return '<th class="' + (SEG === s.id ? "hl" : "") + '">' + esc(s.name) + "</th>"; }).join("") + "</tr></thead><tbody>" + rows + "</tbody></table>" +
    '<div class="legend"><span><span class="mk fo"></span>&nbsp; Legjobban illik</span><span><span class="mk extra"></span>&nbsp; Kiegészítő érték</span><span>– Nem javasolt fókusz</span></div></div>' + foot());

  /* next step */
  var c = D.config, parts = [];
  if (c.contactName) parts.push("<b>" + esc(c.contactName) + "</b>");
  if (c.contactEmail) parts.push(esc(c.contactEmail));
  if (c.contactPhone) parts.push(esc(c.contactPhone));
  if (c.website) parts.push(esc(c.website.replace(/^https?:\/\//, "")));
  add("light", '<div class="pad"><div class="two" style="align-items:start;grid-template-columns:1.1fr 1fr"><div><div class="eyebrow">Következő lépés</div><h2 style="margin-top:24px">Beszéljük meg, <em>mire használná</em> a terét.</h2><p class="lead" style="margin-top:30px">Nem csomagot adunk el, hanem a helyszínhez és a célhoz illő kimeneteket ajánlunk. Egy rövid egyeztetés után személyre szabott javaslatot küldünk.</p>' +
    (parts.length ? '<div class="contact">' + parts.join(" · ") + "</div>" : "") + '</div><div class="steps3">' +
    '<div><span class="n">1</span><div><h4>Helyszín és cél</h4><p>Milyen tereket rögzítenénk, és mire használná az eredményt: marketingre, ügyfélélményre, tervezésre vagy műszaki munkára?</p></div></div>' +
    '<div><span class="n">2</span><div><h4>Személyre szabott javaslat</h4><p>Kimenetek, formátumok és a felmérés módja, a korlátokkal együtt.</p></div></div>' +
    '<div><span class="n">3</span><div><h4>Felmérés és átadás</h4><p>Rögzítés, feldolgozás és átadás, a weboldalba illeszthető formában is.</p></div></div></div></div></div>' + foot(true));

  /* credits */
  add("", '<div class="pad"><div class="eyebrow">A képekről</div><h2 style="margin-top:24px;font-size:58px">Koncepcióvizualizációk</h2><div class="two" style="margin-top:50px;align-items:start"><p class="small" style="font-size:22px">A portfólió képei, panorámái és videói a Brick+Data számára készült koncepcióvizualizációk: procedurálisan felépített 3D jelenetekből renderelt és virtuális lézerszkenneléssel szimulált anyagok. Nem valós ügyfélhelyszínek és nem referenciamunkák. A bemutatott kimenetek a szolgáltatások jellegét szemléltetik; a pontos tartalom, formátum és pontosság a felmérés céljától függ, és egyedi egyeztetés tárgya.</p>' +
    '<p class="small">Felhasznált nyílt licencű elemek: textúrák – ambientCG, Poly Haven (CC0). Bútor- és tárgymodellek – Khronos glTF Sample Assets: SheenChair, GlassVaseFlowers, AntiqueCamera (CC0); GlamVelvetSofa (© Wayfair, CC BY 4.0); DiffuseTransmissionPlant (CC BY 4.0); ABeautifulGame (© ASWF / MaterialX Project, CC BY 4.0); MosquitoInAmber (© Loïc Norgeot / Sketchfab, CC BY 4.0). Renderelés: Blender Cycles. Webes megjelenítés: three.js, Pannellum (MIT).</p></div></div>' + foot());

  deck.innerHTML = slides.map(function (h, i) { return h.replace("{{n}}", String(i + 1).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0")); }).join("");
  document.title = "Brick+Data – " + label + " (prezentáció)";

  /* screen presenting */
  var all = Array.prototype.slice.call(document.querySelectorAll(".slide"));
  var mode = Q.get("nezet") === "gorgetes" ? "scroll" : "present";
  if (window.matchMedia && window.matchMedia("print").matches) mode = "print";
  document.body.classList.add(mode);
  var cur = Math.max(0, Math.min(all.length - 1, (parseInt(location.hash.slice(1), 10) || 1) - 1));
  var hud = document.createElement("div");
  hud.className = "hud";
  document.body.appendChild(hud);
  function fit() {
    var s = Math.min(innerWidth / 1920, innerHeight / 1080);
    all.forEach(function (sl) {
      if (mode === "present") sl.style.transform = "translate(" + (-960 * s) + "px," + (-540 * s) + "px) scale(" + s + ")";
      else if (mode === "scroll") { var k = Math.min(1, (innerWidth - 32) / 1920); sl.style.transform = "scale(" + k + ")"; sl.style.marginBottom = (24 - 1080 * (1 - k)) + "px"; }
    });
  }
  function show(i) {
    cur = Math.max(0, Math.min(all.length - 1, i));
    all.forEach(function (sl, k) { sl.classList.toggle("on", k === cur); });
    hud.textContent = (cur + 1) + " / " + all.length + "  ·  ← → lapozás  ·  F teljes képernyő";
    history.replaceState(null, "", "#" + (cur + 1));
  }
  if (mode === "present") {
    show(cur);
    addEventListener("keydown", function (e) {
      if (["ArrowRight", "PageDown", " ", "Enter"].indexOf(e.key) >= 0) show(cur + 1);
      if (["ArrowLeft", "PageUp", "Backspace"].indexOf(e.key) >= 0) show(cur - 1);
      if (e.key === "Home") show(0);
      if (e.key === "End") show(all.length - 1);
      if (e.key === "f" || e.key === "F") { if (!document.fullscreenElement) document.documentElement.requestFullscreen(); else document.exitFullscreen(); }
    });
    addEventListener("click", function (e) { if (e.clientX > innerWidth / 3) show(cur + 1); else show(cur - 1); });
  } else hud.style.display = "none";
  addEventListener("resize", fit);
  fit();
  window.BD_DECK_READY = true;
})();
