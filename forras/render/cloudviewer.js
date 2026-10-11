// Brick+Data point-cloud viewer (bundled to a classic script so it also works from file://)
import {
  WebGLRenderer, Scene, PerspectiveCamera, BufferGeometry, BufferAttribute, Points, ShaderMaterial,
  Vector3, Color, CatmullRomCurve3, MathUtils
} from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

function b64ToBytes(b64) {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

const VERT = `
  uniform float uSize; uniform float uScale; uniform float uMode; uniform float uZmin; uniform float uZmax;
  attribute vec3 color;
  varying vec3 vCol; varying float vDepth;
  vec3 ramp(float t){
    vec3 a=vec3(0.08,0.16,0.47), b=vec3(0.0,0.67,0.86), c=vec3(0.47,0.9,0.78), d=vec3(1.0,0.78,0.35), e=vec3(1.0,0.43,0.24);
    if(t<0.25) return mix(a,b,t/0.25); if(t<0.5) return mix(b,c,(t-0.25)/0.25);
    if(t<0.75) return mix(c,d,(t-0.5)/0.25); return mix(d,e,(t-0.75)/0.25);
  }
  void main(){
    vec4 mv = modelViewMatrix * vec4(position,1.0);
    gl_Position = projectionMatrix * mv;
    float d = -mv.z; vDepth = d;
    gl_PointSize = clamp(uSize * uScale / max(d, 0.1), 1.5, 12.0);
    float t = clamp((position.z - uZmin)/(uZmax-uZmin), 0.0, 1.0);
    vCol = mix(color, ramp(t), uMode);
  }`;
const FRAG = `
  varying vec3 vCol; varying float vDepth; uniform float uFog; uniform float uGain;
  void main(){
    vec2 c = gl_PointCoord - 0.5; if(dot(c,c) > 0.25) discard;
    float f = exp(-vDepth * uFog);
    vec3 cc = pow(vCol * uGain, vec3(0.9));
    gl_FragColor = vec4(cc * (0.4 + 0.6*f), 1.0);
  }`;

export class CloudViewer {
  constructor(container, opts = {}) {
    this.el = container;
    this.renderer = new WebGLRenderer({ antialias: false, alpha: false, preserveDrawingBuffer: !!opts.preserve });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.setClearColor(new Color(opts.bg || "#07090d"));
    container.appendChild(this.renderer.domElement);
    this.scene = new Scene();
    this.camera = new PerspectiveCamera(55, 1, 0.05, 2000);
    this.camera.up.set(0, 0, 1);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.screenSpacePanning = true;
    this.uniforms = {
      uSize: { value: 0.022 }, uScale: { value: 800 }, uMode: { value: 0 }, uZmin: { value: 0 }, uZmax: { value: 10 },
      uFog: { value: 0.012 }, uGain: { value: 1.4 }
    };
    this.points = null;
    this.flying = null;
    this._onResize = () => this.resize();
    window.addEventListener("resize", this._onResize);
    this.controls.addEventListener("start", () => { this.flying = null; this.el.dispatchEvent(new CustomEvent("flystop")); });
    this.resize();
    const loop = (t) => { this._raf = requestAnimationFrame(loop); this.tick(t); };
    this._raf = requestAnimationFrame(loop);
  }
  resize() {
    const w = this.el.clientWidth || 800, h = this.el.clientHeight || 450;
    this.renderer.setSize(w, h, false);
    this.renderer.domElement.style.width = "100%";
    this.renderer.domElement.style.height = "100%";
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.uniforms.uScale.value = h / (2 * Math.tan(MathUtils.degToRad(this.camera.fov) / 2)) * this.renderer.getPixelRatio();
  }
  load(data) {
    if (this.points) { this.scene.remove(this.points); this.points.geometry.dispose(); }
    const q = new Uint16Array(b64ToBytes(data.pos).buffer);
    const col = b64ToBytes(data.col);
    const n = data.n, pos = new Float32Array(n * 3), c = new Float32Array(n * 3);
    const mn = data.min, mx = data.max;
    for (let i = 0; i < n; i++) {
      for (let k = 0; k < 3; k++) {
        pos[i * 3 + k] = mn[k] + (q[i * 3 + k] / 65535) * (mx[k] - mn[k]);
        const v = col[i * 3 + k] / 255;
        c[i * 3 + k] = v;
      }
    }
    const g = new BufferGeometry();
    g.setAttribute("position", new BufferAttribute(pos, 3));
    g.setAttribute("color", new BufferAttribute(c, 3));
    const m = new ShaderMaterial({ uniforms: this.uniforms, vertexShader: VERT, fragmentShader: FRAG });
    this.points = new Points(g, m);
    this.scene.add(this.points);
    this.uniforms.uZmin.value = data.zrange ? data.zrange[0] : mn[2];
    this.uniforms.uZmax.value = data.zrange ? data.zrange[1] : mx[2];
    this.uniforms.uSize.value = data.size || 0.022;
    this.uniforms.uFog.value = data.fog != null ? data.fog : 0.012;
    this.uniforms.uGain.value = data.gain || 1.4;
    this.data = data;
    this.view(0, false);
  }
  view(i, animate = true) {
    const v = this.data.views[i];
    if (!v) return;
    if (!animate) {
      this.camera.position.set(...v.pos);
      this.controls.target.set(...v.target);
      this.controls.update();
      return;
    }
    const p0 = this.camera.position.clone(), t0 = this.controls.target.clone();
    const p1 = new Vector3(...v.pos), t1 = new Vector3(...v.target);
    const start = performance.now(), dur = 1600;
    this.flying = { type: "lerp", f: (now) => {
      const k = Math.min(1, (now - start) / dur), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      this.camera.position.lerpVectors(p0, p1, e);
      this.controls.target.lerpVectors(t0, t1, e);
      return k < 1;
    } };
  }
  fly() {
    const path = this.data.path;
    if (!path) return;
    const pc = new CatmullRomCurve3(path.map((p) => new Vector3(...p.pos)));
    const tc = new CatmullRomCurve3(path.map((p) => new Vector3(...p.target)));
    const start = performance.now(), dur = (this.data.pathSeconds || 22) * 1000;
    this.flying = { type: "path", f: (now) => {
      const k = Math.min(1, (now - start) / dur), e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      this.camera.position.copy(pc.getPoint(e));
      this.controls.target.copy(tc.getPoint(e));
      return k < 1;
    } };
  }
  setMode(m) { this.uniforms.uMode.value = m; }
  setSize(s) { this.uniforms.uSize.value = s; }
  tick(now) {
    if (this.flying) {
      const going = this.flying.f(now);
      this.camera.lookAt(this.controls.target);
      if (!going) { this.flying = null; this.el.dispatchEvent(new CustomEvent("flystop")); }
    } else {
      this.controls.update();
    }
    this.renderer.render(this.scene, this.camera);
  }
  dispose() {
    cancelAnimationFrame(this._raf);
    window.removeEventListener("resize", this._onResize);
    this.renderer.dispose();
    this.el.removeChild(this.renderer.domElement);
  }
}
window.BDCloudViewer = CloudViewer;
