/* Brick+Data portfólió – oldal-logika (klasszikus script, file:// alól is működik) */
(function () {
  "use strict";
  var D = window.BD;
  var Q = new URLSearchParams(location.search);
  var SEG = Q.get("csoport");
  if (!D.segments.some(function (s) { return s.id === SEG; })) SEG = null;
  var INTERNAL = Q.get("belso") === "1";
  var FILE = location.protocol === "file:";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var el = function (tag, attrs, html) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (html != null) e.innerHTML = html;
    return e;
  };
  var seg = function (id) { return D.segments.filter(function (s) { return s.id === id; })[0]; };
  var svc = function (id) { return D.services.filter(function (s) { return s.id === id; })[0]; };
  var imgFor = function (s, segId) { return (segId && s.imgSeg && s.imgSeg[segId]) || s.img; };
  var esc = function (t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;"); };
  var TAG = '<span class="tag">Koncepcióvizualizáció</span>';

  if (INTERNAL) {
    document.body.classList.add("internal");
    document.body.appendChild(el("div", { class: "int-banner" }, "Belső nézet – ügyfélnek a <b>?belso=1</b> nélküli linket küldje"));
  }

  /* ---------- nav */
  var nav = $("#nav");
  var onScroll = function () { nav.classList.toggle("solid", window.scrollY > 40); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- hero */
  var HERO_ALT = {
    szinhaz: ["assets/img/hero-foto.jpg", "assets/img/hero-pontfelho.jpg", "Fotószerű nézet", "Pontfelhő"],
    muzeum: ["assets/img/muzeum-hero.jpg", "assets/img/muzeum-pontfelho.jpg", "Fotószerű nézet", "Pontfelhő"],
    rendezveny: ["assets/img/rendezveny-hero.jpg", "assets/img/rendezveny-terv.jpg", "Drónnézet", "3D elrendezésterv"],
    szalloda: ["assets/img/szalloda-hero.jpg", "assets/img/szalloda-bim.jpg", "Fotószerű nézet", "BIM-modell"]
  };
  if (SEG) {
    var s0 = seg(SEG), h = HERO_ALT[SEG];
    var imgs = document.querySelectorAll("#heroCmp img");
    imgs[0].src = h[0]; imgs[1].src = h[1];
    $("#heroCmp .lbl.l").textContent = h[2];
    $("#heroCmp .lbl.r").textContent = h[3];
    $("#heroKicker").textContent = s0.name + " · " + s0.kicker;
    $("#heroTitle").innerHTML = esc(s0.headline).replace(/\.\s/, ".<br><em>") + (/\.\s/.test(s0.headline) ? "</em>" : "");
    $("#heroLead").textContent = s0.message;
    $("#heroBtn").setAttribute("href", "#ch-" + SEG);
    $("#heroBtn").textContent = "Megoldások " + s0.name.toLowerCase() + " számára ↓";
    document.title = "Brick+Data – " + s0.name;
  } else {
    var chips = $("#heroChips");
    D.segments.forEach(function (s) { chips.appendChild(el("a", { href: "#ch-" + s.id }, s.name)); });
  }
  (function compare() {
    var box = $("#heroCmp"), dragging = false;
    var set = function (p) { box.style.setProperty("--split", Math.max(2, Math.min(98, p)) + "%"); };
    var fromEvent = function (e) {
      var r = box.getBoundingClientRect(), x = (e.touches ? e.touches[0].clientX : e.clientX) - r.left;
      set((x / r.width) * 100);
    };
    box.addEventListener("pointerdown", function (e) { if (e.target.closest(".handle") || e.pointerType !== "mouse") { dragging = true; fromEvent(e); } });
    window.addEventListener("pointermove", function (e) { if (dragging) fromEvent(e); });
    window.addEventListener("pointerup", function () { dragging = false; });
    box.addEventListener("mousemove", function (e) { if (!dragging && e.buttons === 0 && !matchMedia("(pointer:coarse)").matches) fromEvent(e); });
    var t0 = null;
    var intro = function (t) {
      if (t0 == null) t0 = t;
      var k = Math.min(1, (t - t0) / 2200), e = 1 - Math.pow(1 - k, 3);
      set(98 - 43 * e);
      if (k < 1) requestAnimationFrame(intro);
    };
    set(98);
    setTimeout(function () { requestAnimationFrame(intro); }, 500);
  })();

  /* ---------- process */
  var procImgs = ["assets/img/proc-rogzites.jpg", "assets/img/proc-feldolgozas.jpg", "assets/img/proc-kimenetek.jpg", "assets/img/proc-felhasznalas.jpg"];
  D.process.forEach(function (p, i) {
    $("#process").appendChild(el("div", { class: "step" },
      '<div class="media"><img src="' + procImgs[i] + '" alt="' + esc(p.t) + '" loading="lazy">' + TAG + "</div>" +
      '<span class="n">' + p.n + "</span><h3>" + esc(p.t) + "</h3><p>" + esc(p.d) + "</p>"));
  });

  /* ---------- same space */
  (function same() {
    var stage = $("#sameStage"), tabs = $("#sameTabs"), auto = true, cur = 0;
    D.sameSpace.forEach(function (v, i) {
      var im = el("img", { src: v.img, alt: v.name, loading: i ? "lazy" : "eager" });
      if (!i) im.className = "on";
      stage.appendChild(im);
      var b = el("button", { type: "button" }, '<span class="k">0' + (i + 1) + "</span><b>" + esc(v.name) + "</b><span>" + esc(v.txt) + "</span>");
      if (!i) b.className = "on";
      b.addEventListener("click", function () { auto = false; show(i); });
      tabs.appendChild(b);
    });
    function show(i) {
      cur = i;
      stage.querySelectorAll("img").forEach(function (im, k) { im.classList.toggle("on", k === i); });
      tabs.querySelectorAll("button").forEach(function (b, k) { b.classList.toggle("on", k === i); });
    }
    setInterval(function () { if (auto && isVisible(stage)) show((cur + 1) % D.sameSpace.length); }, 3800);
  })();
  function isVisible(e) { var r = e.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; }

  var ladder = [
    ["Nyers mérés", "Pontfelhő", "Pontok milliói, valós színnel. A meglévő állapot hű lenyomata.", "assets/img/svc-pontfelho.jpg"],
    ["Felület", "Mesh", "Összefüggő háromszögháló: könnyebb megjeleníteni és bejárni.", "assets/img/svc-mesh.jpg"],
    ["Térbeli modell", "3D modell", "Tisztított geometria prezentációhoz, elrendezéshez és látványtervhez.", "assets/img/svc-3dmodell.jpg"],
    ["Információ", "BIM-modell", "Objektumok saját adatokkal felújításhoz, üzemeltetéshez és dokumentációhoz.", "assets/img/svc-bim.jpg"]
  ];
  ladder.forEach(function (l) {
    $("#ladder").appendChild(el("div", null, '<div class="media"><img src="' + l[3] + '" alt="' + l[1] + '" loading="lazy"></div><span class="lv">' + l[0].toUpperCase() + "</span><h4>" + l[1] + "</h4><p>" + l[2] + "</p>"));
  });

  /* ---------- segment overview + chapters */
  var fitList = function (segId, level) {
    return D.services.filter(function (s) { return s.fit[segId] === level; });
  };
  D.segments.forEach(function (s, i) {
    if (SEG && SEG !== s.id) return;
    var nf = fitList(s.id, "fo").length, ne = fitList(s.id, "extra").length;
    var a = el("a", { class: "seg-card", href: "#ch-" + s.id },
      '<img src="' + s.hero + '" alt="' + esc(s.heroAlt) + '" loading="lazy"><div class="in"><span class="k">0' + (i + 1) + " · " + esc(s.kicker) + "</span><h3>" + esc(s.name) + "</h3><p>" + esc(s.message) + '</p><div class="fitcount"><span><i class="dot fo"></i>' + nf + ' fő illeszkedés</span><span><i class="dot extra"></i>' + ne + " kiegészítő</span></div></div>");
    $("#segCards").appendChild(a);
  });
  if (SEG) {
    $("#segCards").style.gridTemplateColumns = "1fr";
    $("#segCards .seg-card").style.minHeight = "520px";
  }

  var chapters = $("#chapters");
  D.segments.forEach(function (s, i) {
    if (SEG && SEG !== s.id) return;
    var fo = fitList(s.id, "fo"), ex = fitList(s.id, "extra");
    var wrap = el("section", { id: "ch-" + s.id, class: "chapter" });
    wrap.appendChild(el("div", { class: "chapter-hero" },
      '<img src="' + s.hero + '" alt="' + esc(s.heroAlt) + '" loading="lazy">' + TAG.replace('class="tag"', 'class="tag" style="position:absolute"') +
      '<div class="copy"><div class="wrap"><span class="num">0' + (i + 1) + " / " + esc(s.name.toUpperCase()) + "</span><h2>" + esc(s.headline) + '</h2><p class="lead">' + esc(s.message) + "</p></div></div>"));
    var body = el("div", { class: "light pad" });
    var w = el("div", { class: "wrap" });
    var story = el("div", { class: "story rv" });
    s.story.forEach(function (st) { story.appendChild(el("div", null, '<span class="k">' + esc(st[0]) + "</span><p>" + esc(st[1]) + "</p>")); });
    w.appendChild(story);
    w.appendChild(el("div", { class: "fit-head rv" }, '<h3>Legjobban illő szolgáltatások</h3><span class="pill fo">Fő illeszkedés · ' + fo.length + "</span>"));
    var cards = el("div", { class: "cards rv" + (fo.length === 4 ? " two" : "") });
    fo.forEach(function (sv) {
      cards.appendChild(el("article", { class: "card" },
        '<div class="media"><img src="' + imgFor(sv, s.id) + '" alt="' + esc(sv.name) + '" loading="lazy">' + TAG + "</div><h4>" + esc(sv.name) + "</h4><p>" + esc(sv.use[s.id]) + '</p><p class="what muted">' + esc(sv.mi) + "</p>"));
    });
    w.appendChild(cards);
    w.appendChild(el("div", { class: "fit-head rv", style: "margin-top:64px" }, '<h3>Kiegészítő érték</h3><span class="pill extra">Extra · ' + ex.length + "</span>"));
    var extras = el("div", { class: "extras rv" });
    ex.forEach(function (sv) {
      extras.appendChild(el("div", { class: "extra-row" }, '<div class="media"><img src="' + imgFor(sv, s.id) + '" alt="' + esc(sv.name) + '" loading="lazy"></div><div><h5>' + esc(sv.name) + "</h5><p>" + esc(sv.use[s.id]) + "</p></div>"));
    });
    w.appendChild(extras);
    if (s.note) w.appendChild(el("div", { class: "note rv" }, esc(s.note)));
    body.appendChild(w);
    wrap.appendChild(body);
    chapters.appendChild(wrap);
  });

  /* ---------- catalogue */
  (function catalogue() {
    var f = $("#filters"), cat = $("#catalog");
    var opts = [["all", "Mind a 14 szolgáltatás"]].concat(D.segments.map(function (s) { return [s.id, s.name]; }));
    var current = SEG || "all";
    opts.forEach(function (o) {
      var b = el("button", { type: "button", "data-f": o[0] }, o[1]);
      b.addEventListener("click", function () { apply(o[0]); });
      f.appendChild(b);
    });
    D.groups.forEach(function (g) {
      var list = D.services.filter(function (s) { return s.group === g.id; });
      var grp = el("div", { class: "cat-group", "data-g": g.id });
      grp.appendChild(el("h3", null, esc(g.name)));
      var grid = el("div", { class: "svc" });
      list.forEach(function (s) {
        var fits = D.segments.map(function (sg) {
          var lv = s.fit[sg.id];
          return lv ? '<span class="fitchip ' + lv + '">' + esc(sg.short) + (lv === "fo" ? " · fő" : " · extra") + "</span>" : "";
        }).join("");
        var c = el("article", { class: "svc-card", "data-id": s.id },
          '<div class="media"><img src="' + imgFor(s, SEG) + '" alt="' + esc(s.name) + '" loading="lazy">' + TAG + "</div><h4>" + esc(s.name) +
          "</h4><dl><dt>Mi ez?</dt><dd>" + esc(s.mi) + "</dd><dt>Mire jó?</dt><dd>" + esc(s.mire) + "</dd><dt>Miben más?</dt><dd>" + esc(s.kulonbseg) + '</dd></dl><div class="fits">' + fits + "</div>");
        grid.appendChild(c);
      });
      grp.appendChild(grid);
      cat.appendChild(grp);
    });
    function apply(id) {
      current = id;
      f.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-f") === id); });
      cat.querySelectorAll(".svc-card").forEach(function (c) {
        var s = svc(c.getAttribute("data-id"));
        c.classList.toggle("hidden", id !== "all" && !s.fit[id]);
      });
      cat.querySelectorAll(".cat-group").forEach(function (g) {
        g.style.display = g.querySelector(".svc-card:not(.hidden)") ? "" : "none";
      });
    }
    apply(current);
  })();

  /* ---------- matrix */
  (function matrix() {
    var t = $("#matrixTable");
    var head = "<thead><tr><th>Szolgáltatás</th>" + D.segments.map(function (s) {
      return '<th class="' + (SEG === s.id ? "hl" : "") + '">' + esc(s.name) + "</th>";
    }).join("") + "</tr></thead><tbody>";
    var rows = "";
    D.groups.forEach(function (g) {
      rows += '<tr class="grp"><td colspan="5">' + esc(g.name) + "</td></tr>";
      D.services.filter(function (s) { return s.group === g.id; }).forEach(function (s) {
        rows += "<tr><td>" + esc(s.name) + "</td>" + D.segments.map(function (sg) {
          var lv = s.fit[sg.id], cls = SEG === sg.id ? "hl" : "";
          var mk = lv === "fo" ? '<span class="mk fo" title="Legjobban illik"><i></i></span>' : lv === "extra" ? '<span class="mk extra" title="Kiegészítő érték"><i></i></span>' : '<span class="mk no">–</span>';
          return '<td class="' + cls + '">' + mk + "</td>";
        }).join("") + "</tr>";
      });
    });
    t.innerHTML = head + rows + "</tbody>";
  })();

  /* ---------- contact + internal list */
  (function contact() {
    var c = D.config, parts = [];
    if (c.contactName) parts.push("<b>" + esc(c.contactName) + "</b>");
    if (c.contactEmail) parts.push('<a href="mailto:' + esc(c.contactEmail) + '">' + esc(c.contactEmail) + "</a>");
    if (c.contactPhone) parts.push('<a href="tel:' + esc(c.contactPhone.replace(/\s/g, "")) + '">' + esc(c.contactPhone) + "</a>");
    if (c.website) parts.push('<a href="' + esc(c.website) + '">' + esc(c.website.replace(/^https?:\/\//, "")) + "</a>");
    var box = $("#contact");
    if (parts.length) {
      box.innerHTML = parts.join(" · ") + '<div class="btns"><a class="btn primary" href="' + (c.contactEmail ? "mailto:" + esc(c.contactEmail) + "?subject=" + encodeURIComponent("Digitális térfelmérés – egyeztetés") : "#") + '">Időpontot kérek</a></div>';
    } else {
      box.innerHTML = '<p class="muted">Kollégánk a megkeresés után felveszi Önnel a kapcsolatot.</p>' + (INTERNAL ? '<div class="int-note"><b>Kitöltendő</b>A kapcsolattartó neve, e-mail-címe és telefonszáma az <code>assets/data.js</code> fájl <code>config</code> részében adható meg.</div>' : "");
    }
    $("#internalList").innerHTML = "<b>Belső egyeztetést igényel, mielőtt ügyfélnek küldjük</b><ul>" + D.internal.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul>";
  })();

  /* ---------- lazy script loader (panos & clouds as data-URI scripts → works on file:// too) */
  var loaded = {};
  function loadScript(src) {
    if (loaded[src]) return loaded[src];
    loaded[src] = new Promise(function (res, rej) {
      var s = document.createElement("script");
      s.src = src; s.onload = res; s.onerror = rej;
      document.head.appendChild(s);
    });
    return loaded[src];
  }

  /* ---------- 360 tour */
  (function tour() {
    var T = window.BD_TOURS;
    if (!T) return;
    var box = $("#tourViewer"), tabs = $("#tourTabs"), viewer = null, current = null;
    var order = ["szinhaz", "rendezveny", "szalloda", "muzeum"].filter(function (k) { return T[k]; });
    if (SEG && T[SEG]) order = [SEG].concat(order.filter(function (k) { return k !== SEG; }));
    order.forEach(function (k) {
      var b = el("button", { type: "button", "data-k": k }, esc(T[k].label));
      b.addEventListener("click", function () { start(k); });
      tabs.appendChild(b);
    });
    function poster(k) {
      box.innerHTML = '<img class="poster" src="' + T[k].poster + '" alt="">' +
        '<button class="start" type="button"><span>▶ Virtuális túra indítása – ' + esc(T[k].label) + "</span></button>" + TAG;
      box.querySelector(".start").addEventListener("click", function () { start(k); });
      tabs.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-k") === k); });
    }
    function panoUrl(name) {
      if (!FILE) return Promise.resolve("assets/pano/" + name + ".jpg");
      return loadScript("assets/pano/" + name + ".js").then(function () { return window.BD_PANO[name]; });
    }
    function start(k) {
      tabs.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-k") === k); });
      var t = T[k];
      Promise.all(t.scenes.map(function (sc) { return panoUrl(sc.pano); })).then(function (urls) {
        if (viewer) { viewer.destroy(); viewer = null; }
        box.innerHTML = '<div id="pnlm"></div>' + TAG + '<span class="hint">Húzással körbenézhet · a pontokra kattintva továbbléphet</span>';
        var scenes = {};
        t.scenes.forEach(function (sc, i) {
          scenes[sc.id] = {
            title: sc.title, type: "equirectangular", panorama: urls[i], yaw: sc.yaw || 0, pitch: sc.pitch || -4, hfov: 105,
            hotSpots: sc.hotspots.map(function (h) {
              return { pitch: h.pitch, yaw: h.yaw, type: "scene", sceneId: h.scene, cssClass: "bd-hot", createTooltipFunc: function (div) { var sp = document.createElement("span"); sp.textContent = h.text; div.appendChild(sp); } };
            })
          };
        });
        viewer = pannellum.viewer("pnlm", {
          default: { firstScene: t.scenes[0].id, autoLoad: true, sceneFadeDuration: 900, showFullscreenCtrl: true, compass: false, autoRotate: -2, autoRotateInactivityDelay: 6000 },
          scenes: scenes
        });
        current = k;
      });
    }
    poster(order[0]);
  })();

  /* ---------- point cloud */
  (function clouds() {
    var C = window.BD_CLOUD_LIST;
    if (!C) return;
    var box = $("#cloudViewer"), tabs = $("#cloudTabs"), cv = null;
    var order = C.slice();
    if (SEG) order.sort(function (a, b) { return (b.seg.indexOf(SEG) >= 0) - (a.seg.indexOf(SEG) >= 0); });
    order.forEach(function (c) {
      var b = el("button", { type: "button", "data-k": c.id }, esc(c.label));
      b.addEventListener("click", function () { start(c); });
      tabs.appendChild(b);
    });
    function poster(c) {
      box.innerHTML = '<img class="poster" src="' + c.poster + '" alt="">' + '<button class="start" type="button"><span>▶ Pontfelhő betöltése – ' + esc(c.label) + "</span></button>" + TAG;
      box.querySelector(".start").addEventListener("click", function () { start(c); });
      tabs.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-k") === c.id); });
    }
    function start(c) {
      tabs.querySelectorAll("button").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-k") === c.id); });
      box.innerHTML = '<img class="poster" src="' + c.poster + '" alt=""><div class="start"><span>Betöltés…</span></div>';
      loadScript("assets/cloud/" + c.id + ".js").then(function () {
        if (cv) { cv.dispose(); cv = null; }
        box.innerHTML = '<div class="cv"></div>' + TAG + '<span class="hint">Bal egérgomb: forgatás · görgő: nagyítás · jobb gomb: mozgatás</span>';
        var hud = el("div", { class: "hud" });
        var data = window.BD_CLOUDS[c.id];
        cv = new window.BDCloudViewer(box.querySelector(".cv"));
        cv.load(data);
        var fly = el("button", { type: "button" }, "▶ Végigrepülés");
        fly.addEventListener("click", function () { cv.fly(); fly.classList.add("on"); });
        box.querySelector(".cv").addEventListener("flystop", function () { fly.classList.remove("on"); });
        hud.appendChild(fly);
        data.views.forEach(function (v, i) {
          var b = el("button", { type: "button" }, esc(v.name));
          b.addEventListener("click", function () { cv.view(i); });
          hud.appendChild(b);
        });
        hud.appendChild(el("span", { class: "sp" }));
        var mode = el("button", { type: "button" }, "Színezés: valós szín");
        var m = 0;
        mode.addEventListener("click", function () { m = 1 - m; cv.setMode(m); mode.textContent = m ? "Színezés: magasság" : "Színezés: valós szín"; });
        hud.appendChild(mode);
        box.appendChild(hud);
        setTimeout(function () { cv.fly(); fly.classList.add("on"); }, 600);
      }, function () { box.innerHTML = '<img class="poster" src="' + c.poster + '" alt="">'; });
    }
    poster(order[0]);
  })();

  /* ---------- reveal */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" }) : null;
  document.querySelectorAll(".rv").forEach(function (e) { io ? io.observe(e) : e.classList.add("in"); });
})();
