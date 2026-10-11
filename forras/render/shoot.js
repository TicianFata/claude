// Screenshots + PDF export for the portfolio. Usage: node shoot.js <mode> [args]
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");
const http = require("http");

const ROOT = "/home/user/claude/portfolio";
const OUT = path.join(__dirname, "shots");
fs.mkdirSync(OUT, { recursive: true });
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css", ".jpg": "image/jpeg",
  ".png": "image/png", ".woff2": "font/woff2", ".mp4": "video/mp4", ".json": "application/json" };

function serve(port) {
  return new Promise((res) => {
    const srv = http.createServer((req, rsp) => {
      const u = decodeURIComponent(req.url.split("?")[0].split("#")[0]);
      const f = path.join(ROOT, u === "/" ? "index.html" : u);
      fs.readFile(f, (err, buf) => {
        if (err) { rsp.writeHead(404); rsp.end(); return; }
        rsp.writeHead(200, { "Content-Type": TYPES[path.extname(f)] || "application/octet-stream" });
        rsp.end(buf);
      });
    }).listen(port, () => res(srv));
  });
}

(async () => {
  const mode = process.argv[2] || "page";
  const srv = await serve(8765);
  const browser = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
  const base = "http://127.0.0.1:8765/";
  try {
    if (mode === "page") {
      const q = process.argv[3] || "";
      const w = parseInt(process.argv[4] || "1440", 10);
      const ctx = await browser.newContext({ viewport: { width: w, height: w < 600 ? 844 : 900 }, deviceScaleFactor: 1 });
      const p = await ctx.newPage();
      const errs = [];
      p.on("pageerror", (e) => errs.push(String(e)));
      p.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
      await p.goto(base + "index.html" + q, { waitUntil: "networkidle" });
      await p.evaluate(async () => {
        document.querySelectorAll(".rv").forEach((e) => e.classList.add("in"));
        document.querySelectorAll("img[loading=lazy]").forEach((i) => i.removeAttribute("loading"));
        for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); }
        window.scrollTo(0, 0);
      });
      await p.waitForTimeout(3500);
      const tag = (q.replace(/[^a-z0-9]/gi, "_") || "full") + "_" + w;
      await p.screenshot({ path: path.join(OUT, "page_" + tag + ".png"), fullPage: true });
      const ow = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
      console.log("errors:", JSON.stringify(errs), "horizontal-overflow:", ow);
    } else if (mode === "viewers") {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const p = await ctx.newPage();
      const errs = [];
      p.on("pageerror", (e) => errs.push(String(e)));
      p.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
      await p.goto(base + "index.html", { waitUntil: "networkidle" });
      await p.evaluate(() => document.querySelectorAll(".rv").forEach((e) => e.classList.add("in")));
      const tour = process.argv[3] || "szinhaz";
      await p.locator("#tourTabs button[data-k=" + tour + "]").click();
      await p.waitForTimeout(6000);
      await p.locator("#tourViewer").screenshot({ path: path.join(OUT, "tour_" + tour + ".png") });
      const cl = process.argv[4] || "muzeum";
      await p.locator("#cloudTabs button[data-k=" + cl + "]").click();
      await p.waitForTimeout(9000);
      await p.locator("#cloudViewer").screenshot({ path: path.join(OUT, "cloud_" + cl + ".png") });
      console.log("errors:", JSON.stringify(errs));
    } else if (mode === "deck") {
      const q = process.argv[3] || "";
      const name = process.argv[4] || "deck";
      const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
      const p = await ctx.newPage();
      const errs = [];
      p.on("pageerror", (e) => errs.push(String(e)));
      await p.emulateMedia({ media: "print" });
      await p.goto(base + "prezentacio.html" + q, { waitUntil: "networkidle" });
      await p.waitForFunction(() => window.BD_DECK_READY === true);
      await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; }))); });
      await p.waitForTimeout(800);
      const pdf = process.argv[5];
      if (pdf) {
        await p.pdf({ path: pdf, width: "1920px", height: "1080px", printBackground: true, preferCSSPageSize: true });
        console.log("pdf", pdf);
      }
      // also slide thumbnails for review
      const n = await p.evaluate(() => document.querySelectorAll(".slide").length);
      if (process.argv[6] !== "nothumbs") {
        for (let i = 0; i < n; i++) {
          await p.locator(".slide").nth(i).screenshot({ path: path.join(OUT, name + "_" + String(i + 1).padStart(2, "0") + ".png") });
        }
      }
      console.log("slides", n, "errors:", JSON.stringify(errs));
    }
  } finally {
    await browser.close();
    srv.close();
  }
})();
