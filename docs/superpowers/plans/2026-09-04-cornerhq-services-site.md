# CornerHQ Services Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the app-only landing page at cornerhq.com.au with a reel-first services site (videos, marketing, websites, apps for combat sports gyms and fight promotions), per the approved spec `docs/superpowers/specs/2026-09-04-cornerhq-services-site-design.md`.

**Architecture:** Static site, no build step. `index.html` holds the markup, `css/site.css` the design tokens and layout, `js/site.js` the four behaviours (nav switch, lightbox, form submit, reduced-motion). Media (reel clips, stills, logos, fonts) is committed to the repo and served by Vercel. A Python check script is the test suite: it fails on banned characters, missing assets, oversized media and rule violations.

**Tech Stack:** HTML, CSS (custom properties, scroll-driven animations), vanilla JS, ffmpeg, Python 3 + Pillow (already installed), Web3Forms (existing key), Vercel auto-deploy from `main` on `github.com/ttd909/CornerHQWeb`.

**Working directory for every command:** `C:/Users/Thien/Desktop/CornerHQWeb` (Git Bash paths).

**Visual reference:** `.superpowers/brainstorm/958-1788486281/content/reel-first-v2.html` (not committed, git-ignored). The code below is derived from it with the spec's changes applied. Do not copy the mockup file verbatim: it links Google Fonts and uses `/files/` asset paths.

---

## File structure

| File | Responsibility |
|---|---|
| `index.html` | Page markup only. Nine sections in spec order. No inline styles or scripts. |
| `css/site.css` | Tokens, `@font-face`, layout for every section, motion, responsive collapse. |
| `js/site.js` | Nav colour switch, lightbox, form submit + inline states, reduced-motion handling, iframe reveal. |
| `scripts/check.py` | The test suite. Run before every commit. |
| `scripts/make-assets.sh` | Reproducible asset pipeline (ffmpeg + Pillow). Run once; re-run if the reel changes. |
| `images/logo-light.png`, `images/logo-dark.png` | Cropped logo, tagline removed, for dark and light surfaces. |
| `images/reel/poster.jpg`, `images/reel/f03.jpg` ... `f70.jpg` | Stills extracted from the reel. |
| `images/sing-site.png` | Static screenshot of singmuaythai.com.au, fallback under the iframe. |
| `images/dashboard-preview.png` | Already exists. App screenshot. |
| `video/reel-loop.mp4` | Muted 30s 720p loop for hero and phone. |
| `video/reel-full.mp4` | Full 73s reel with audio for the lightbox. |
| `fonts/bricolage-grotesque.woff2`, `fonts/jetbrains-mono.woff2` | Self-hosted variable fonts. |

Deleted: nothing else. `preview/` (dashboard preview) and `images/logo.png` (original logo) stay.

---

### Task 1: Check script (the test suite)

**Files:**
- Create: `scripts/check.py`

- [ ] **Step 1: Write the check script**

```python
#!/usr/bin/env python3
"""Pre-flight checks for the CornerHQ site. Exit 1 on any failure.

Rules come from docs/superpowers/specs/2026-09-04-cornerhq-services-site-design.md
section 8 and the taste-skill pre-flight list.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
failures = []


def fail(msg):
    failures.append(msg)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def check_dashes(path, text):
    for i, line in enumerate(text.splitlines(), 1):
        if "\u2014" in line or "\u2013" in line:
            fail(f"{path}:{i}: em/en dash found: {line.strip()[:80]}")


def check_assets(html):
    refs = re.findall(r'(?:src|href|poster)="([^"]+)"', html)
    for ref in refs:
        if ref.startswith(("http", "#", "mailto:", "data:")):
            continue
        if not os.path.exists(os.path.join(ROOT, ref)):
            fail(f"index.html references missing asset: {ref}")
    css = read("css/site.css")
    for ref in re.findall(r'url\("?\.\./([^")]+)"?\)', css):
        if not os.path.exists(os.path.join(ROOT, ref)):
            fail(f"site.css references missing asset: {ref}")


def check_sizes():
    limits = {
        "video/reel-loop.mp4": 2_000_000,
        "video/reel-full.mp4": 14_000_000,
        "images/logo-light.png": 400_000,
        "images/logo-dark.png": 400_000,
        "images/sing-site.png": 1_500_000,
    }
    for path, limit in limits.items():
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            fail(f"missing media: {path}")
            continue
        size = os.path.getsize(full)
        if size > limit:
            fail(f"{path} is {size:,} bytes, limit {limit:,}")
    stills = os.path.join(ROOT, "images", "reel")
    if os.path.isdir(stills):
        for name in os.listdir(stills):
            size = os.path.getsize(os.path.join(stills, name))
            if size > 400_000:
                fail(f"images/reel/{name} is {size:,} bytes, limit 400,000")


def check_rules(html):
    # One CTA label per intent.
    labels = re.findall(r'class="btn[^"]*"[^>]*>([^<]+)<', html)
    contact_like = {l.strip() for l in labels if re.search(r"contact|touch|talk|enquir|start", l, re.I)}
    if contact_like:
        fail(f"contact-intent CTA labels other than 'Book a call': {contact_like}")
    # Eyebrow ration: uppercase tracking labels above headings.
    eyebrows = len(re.findall(r'class="[^"]*\beyebrow\b', html))
    if eyebrows > 0:
        fail(f"{eyebrows} eyebrow labels found, spec allows none")
    # No step labels, scroll cues, version tags.
    for pat, why in [
        (r"Step\s*[123]\b", "step label"),
        (r"\bScroll\b(?!bar)", "scroll cue"),
        (r"\bv\d+\.\d+", "version label"),
        (r"Quietly", "AI social-proof phrasing"),
        (r"\bSeamless|Elevate|Unleash|Next-Gen", "filler verb"),
    ]:
        if re.search(pat, html):
            fail(f"banned copy pattern: {why} ({pat})")
    # Middle-dot chains.
    if re.search(r"·[^·\n]*·", html):
        fail("middle-dot separator chain found")
    # No inline styles or scripts.
    if re.search(r'\sstyle="', html):
        fail("inline style attribute found; put it in css/site.css")
    if re.search(r"<script>[^<]", html):
        fail("inline script found; put it in js/site.js")
    # Google Fonts must not be linked.
    if "fonts.googleapis.com" in html:
        fail("Google Fonts linked; fonts must be self-hosted")


def check_js():
    js = read("js/site.js")
    if "addEventListener('scroll'" in js or 'addEventListener("scroll"' in js:
        fail("scroll listener found in site.js; use IntersectionObserver")


def main():
    html = read("index.html")
    check_dashes("index.html", html)
    check_dashes("css/site.css", read("css/site.css"))
    check_dashes("js/site.js", read("js/site.js"))
    check_assets(html)
    check_sizes()
    check_rules(html)
    check_js()
    if failures:
        print("FAIL")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("OK: all checks passed")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it against the current site to confirm it fails**

Run: `python scripts/check.py`
Expected: `FAIL` with at least "css/site.css" not found (FileNotFoundError is acceptable at this stage; the script will run cleanly once Task 3 creates the file). If it raises `FileNotFoundError`, that counts as the expected failure.

- [ ] **Step 3: Commit**

```bash
git add scripts/check.py
git commit -m "Add pre-flight check script for the site rebuild

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Assets (logos, stills, video, fonts, screenshot)

**Files:**
- Create: `scripts/make-assets.sh`
- Create: `images/logo-light.png`, `images/logo-dark.png`
- Create: `images/reel/poster.jpg`, `images/reel/f03.jpg`, `f10.jpg`, `f18.jpg`, `f27.jpg`, `f36.jpg`, `f45.jpg`, `f54.jpg`, `f63.jpg`, `f70.jpg`
- Create: `video/reel-loop.mp4`, `video/reel-full.mp4`
- Create: `fonts/bricolage-grotesque.woff2`, `fonts/jetbrains-mono.woff2`
- Create: `images/sing-site.png`

- [ ] **Step 1: Write the asset pipeline script**

```bash
#!/usr/bin/env bash
# Rebuilds every derived asset from the source reel and the original logo.
# Run from the repo root in Git Bash. Needs ffmpeg, python3 + Pillow, curl.
set -euo pipefail

REEL="C:/Users/Thien/Downloads/Muay Thai Fighter Promo — IG Reel 1080p (1).mp4"
mkdir -p images/reel video fonts

echo "== logos"
python - <<'PY'
from PIL import Image

def make(src, dst, text_rgb):
    im = Image.open(src).convert("RGBA")
    px = im.load()
    w, h = im.size
    # Erase the "GYM MANAGEMENT SOFTWARE" tagline: it sits right of the ring
    # (x > 395) in the band y 388..440 of the 1200x630 original.
    for y in range(388, 441):
        for x in range(395, w):
            px[x, y] = (0, 0, 0, 0)
    # Recolour the white wordmark for the light-surface version.
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0 and r > 180 and g > 180 and b > 180 and abs(r - b) < 40:
                px[x, y] = text_rgb + (a,)
    bbox = im.getbbox()
    pad = 24
    im = im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                  min(w, bbox[2] + pad), min(h, bbox[3] + pad)))
    im.save(dst, optimize=True)
    print(dst, im.size)

make("images/logo.png", "images/logo-light.png", (255, 255, 255))
make("images/logo.png", "images/logo-dark.png", (28, 28, 30))
PY

echo "== stills"
for t in 3 10 18 27 36 45 54 63 70; do
  n=$(printf "%02d" "$t")
  ffmpeg -v error -y -ss "$t" -i "$REEL" -frames:v 1 -vf "scale=900:-2" -q:v 4 "images/reel/f$n.jpg"
done
ffmpeg -v error -y -ss 27 -i "$REEL" -frames:v 1 -vf "scale=720:-2" -q:v 4 images/reel/poster.jpg

echo "== video"
# Loop: skip the black fade-in, 30 seconds, muted, 720 wide.
ffmpeg -v error -y -ss 1.5 -t 30 -i "$REEL" -an -vf "scale=720:-2" \
  -c:v libx264 -preset slow -crf 26 -movflags +faststart video/reel-loop.mp4
# Full: whole reel, with audio, capped bitrate so it stays near 8 MB.
ffmpeg -v error -y -i "$REEL" -vf "scale=1080:-2" \
  -c:v libx264 -preset slow -crf 25 -maxrate 900k -bufsize 1800k \
  -c:a aac -b:a 96k -movflags +faststart video/reel-full.mp4

echo "== fonts"
curl -fsSL -o fonts/bricolage-grotesque.woff2 \
  "https://cdn.jsdelivr.net/npm/@fontsource-variable/bricolage-grotesque/files/bricolage-grotesque-latin-wght-normal.woff2"
curl -fsSL -o fonts/jetbrains-mono.woff2 \
  "https://cdn.jsdelivr.net/npm/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2"

echo "== screenshot of singmuaythai.com.au (fallback under the iframe)"
CHROME="C:/Program Files/Google/Chrome/Application/chrome.exe"
EDGE="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
BIN="$CHROME"; [ -x "$BIN" ] || BIN="$EDGE"
"$BIN" --headless=new --disable-gpu --hide-scrollbars --window-size=1280,900 \
  --screenshot="$(pwd)/images/sing-site.png" "https://singmuaythai.com.au" 2>/dev/null || true

ls -la images/logo-*.png images/reel video fonts images/sing-site.png
```

- [ ] **Step 2: Run it**

Run: `bash scripts/make-assets.sh`
Expected: prints the two logo sizes, then a listing showing nine `fNN.jpg` stills plus `poster.jpg`, `reel-loop.mp4` around 1.2 MB, `reel-full.mp4` between 6 and 12 MB, two `.woff2` files each larger than 20 KB, and `sing-site.png`.

If either font download returns 404, try the `full` variant name (`bricolage-grotesque-latin-full-normal.woff2`) and update the script. If neither Chrome nor Edge produces `sing-site.png`, take a screenshot of the live site by hand at 1280 wide and save it to `images/sing-site.png`; the check script requires the file.

- [ ] **Step 3: Eyeball the logos**

Open `images/logo-light.png` and `images/logo-dark.png` (Read tool). Expected: gold ring and "CornerHQ" wordmark, no tagline underneath, no stray pixels where the tagline was. If a sliver of tagline remains, widen the erase band in the script (`y` range) and re-run.

- [ ] **Step 4: Commit**

```bash
git add scripts/make-assets.sh images/logo-light.png images/logo-dark.png images/reel video fonts images/sing-site.png
git commit -m "Add site assets: cropped logos, reel clips, stills, fonts

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 3: Stylesheet

**Files:**
- Create: `css/site.css`

- [ ] **Step 1: Write the stylesheet**

```css
/* CornerHQ site styles.
   Locked rules (spec section 7): light paper page, dark surfaces only where media
   lives (hero, "who" blocks, closing band). One accent (gold). Bricolage Grotesque
   for everything, JetBrains Mono for numbers only. Radius rule: 6px buttons and
   thumbnails, 10px browser frames, 28px phone frame. */

@font-face {
  font-family: "Bricolage Grotesque";
  src: url("../fonts/bricolage-grotesque.woff2") format("woff2");
  font-weight: 200 800;
  font-display: swap;
}
@font-face {
  font-family: "JetBrains Mono";
  src: url("../fonts/jetbrains-mono.woff2") format("woff2");
  font-weight: 100 800;
  font-display: swap;
}

:root {
  --paper: #F3F3F1;
  --paper-2: #E9E9E6;
  --ink: #1C1C1E;
  --ink-2: #6B6B70;
  --line: #D9D9D5;
  --dark: #0E0E10;
  --dark-2: #151517;
  --dark-line: #26262A;
  --bone: #EDE8DD;
  --bone-2: #9B968C;
  --gold: #B8891F;
  --gold-dark: #D4A83A;
  --gold-hover: #E2B84C;
  --r: 6px;
  --r-frame: 10px;
  --r-phone: 28px;
  --font: "Bricolage Grotesque", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "Cascadia Code", monospace;
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --nav-h: 72px;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--font);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
img, video { display: block; max-width: 100%; }
a { color: inherit; text-decoration: none; }
h1, h2, h3 { margin: 0; }
p { margin: 0; }
:focus-visible { outline: 2px solid var(--gold-dark); outline-offset: 3px; }
.wrap { max-width: 1280px; margin: 0 auto; padding: 0 clamp(20px, 4vw, 56px); }
.visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }

/* Buttons */
.btn {
  display: inline-flex; align-items: center; gap: 10px;
  padding: 14px 22px; border: 0; border-radius: var(--r); cursor: pointer;
  font: inherit; font-weight: 700; font-size: 15px; line-height: 1;
  background: var(--gold-dark); color: #171205;
  transition: transform .25s var(--ease), background .2s;
}
.btn:hover { transform: translateY(-2px); background: var(--gold-hover); }
.btn:active { transform: scale(.98); }
.btn-ghost { background: transparent; color: var(--bone); border: 1px solid rgba(237, 232, 221, .3); }
.btn-ghost:hover { background: rgba(255, 255, 255, .06); }
.link { color: var(--gold); font-weight: 600; }
.link:hover { text-decoration: underline; }
.on-dark .link { color: var(--gold-dark); }

/* Nav: dark over the hero, paper once the hero has scrolled away */
.nav {
  position: fixed; inset: 0 0 auto 0; z-index: 20; height: var(--nav-h);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 clamp(20px, 4vw, 56px);
  color: var(--bone);
  background: linear-gradient(180deg, rgba(14, 14, 16, .85), transparent);
  transition: background .35s, color .35s, box-shadow .35s;
}
.nav-logo img { height: 40px; width: auto; }
.nav-logo .logo-dark { display: none; }
.nav-links { display: flex; gap: 32px; font-size: 15px; opacity: .85; }
.nav-links a:hover { opacity: 1; }
.nav .btn { padding: 10px 16px; font-size: 14px; }
.nav.is-light { color: var(--ink); background: rgba(243, 243, 241, .88); backdrop-filter: blur(12px); box-shadow: 0 1px 0 var(--line); }
.nav.is-light .logo-light { display: none; }
.nav.is-light .logo-dark { display: block; }

/* Hero: dark triptych of the reel */
.hero { position: relative; min-height: 100dvh; display: grid; grid-template-rows: 1fr auto; background: var(--dark); color: var(--bone); }
.hero-strip { position: absolute; inset: 0; display: grid; grid-template-columns: 1fr 1.25fr 1fr; gap: 2px; background: var(--dark); }
.hero-strip > div { position: relative; overflow: hidden; }
.hero-strip img, .hero-strip video { width: 100%; height: 100%; object-fit: cover; filter: saturate(.9); }
.hero-still img { opacity: .55; }
.hero-strip::after {
  content: ""; position: absolute; inset: 0; pointer-events: none;
  background: linear-gradient(180deg, rgba(14, 14, 16, .25) 0%, rgba(14, 14, 16, 0) 35%, rgba(14, 14, 16, .2) 60%, rgba(14, 14, 16, .96) 100%);
}
.hero-copy { position: relative; z-index: 2; grid-row: 2; padding-bottom: clamp(40px, 7vh, 80px); }
.hero h1 { font-size: clamp(2.6rem, 6.2vw, 5.6rem); line-height: .96; letter-spacing: -.03em; font-weight: 800; max-width: 14ch; margin-bottom: 20px; }
.hero h1 em { font-style: italic; color: var(--gold-dark); }
.hero-sub { font-size: clamp(1.05rem, 1.4vw, 1.3rem); color: var(--bone-2); max-width: 42ch; margin-bottom: 28px; line-height: 1.5; }
.hero-ctas { display: flex; gap: 12px; flex-wrap: wrap; }
.rise { animation: rise .9s var(--ease) both; }
.rise:nth-child(2) { animation-delay: .1s; }
.rise:nth-child(3) { animation-delay: .2s; }
@keyframes rise { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }

/* Opinion line */
.opinion { padding: clamp(72px, 11vh, 130px) 0 0; }
.opinion p { font-size: clamp(1.5rem, 2.6vw, 2.3rem); line-height: 1.25; letter-spacing: -.02em; font-weight: 500; max-width: 30ch; }
.opinion em { font-style: italic; color: var(--gold); }

/* The work */
.work { padding: clamp(72px, 11vh, 130px) 0 0; }
.section-title { font-size: clamp(2rem, 4vw, 3.4rem); letter-spacing: -.03em; font-weight: 700; line-height: 1; margin-bottom: 12px; }
.section-lead { color: var(--ink-2); font-size: 1.1rem; max-width: 55ch; line-height: 1.5; }
.work .section-lead { margin-bottom: 56px; }
.piece { display: grid; grid-template-columns: 5fr 7fr; gap: clamp(28px, 5vw, 80px); align-items: center; padding: clamp(48px, 8vh, 96px) 0; border-top: 1px solid var(--line); }
.piece-flip { grid-template-columns: 7fr 5fr; }
.piece-flip .piece-text { order: 2; }
.piece-wide { display: block; }
.piece-wide .piece-text { max-width: 60ch; margin-bottom: 40px; }
.piece-kind { color: var(--gold); font-weight: 600; font-size: 15px; margin-bottom: 10px; }
.piece h3 { font-size: clamp(1.7rem, 3vw, 2.6rem); letter-spacing: -.025em; font-weight: 700; line-height: 1.05; margin-bottom: 14px; }
.piece-text p:not(.piece-kind) { color: var(--ink-2); line-height: 1.55; max-width: 48ch; margin-bottom: 22px; font-size: 1.05rem; }
.facts { display: flex; gap: 28px; font-family: var(--mono); font-size: 13px; color: var(--ink-2); }
.facts b { display: block; color: var(--ink); font-size: 22px; font-weight: 500; margin-bottom: 4px; }
.piece .link { display: inline-block; margin-top: 18px; }
.phone {
  position: relative; width: min(100%, 360px); aspect-ratio: 9 / 16; margin: 0 auto;
  border-radius: var(--r-phone); overflow: hidden; background: #000;
  border: 1px solid #2C2C31; box-shadow: 0 30px 80px rgba(28, 28, 30, .28), 0 0 0 6px #111114;
}
.phone video { width: 100%; height: 100%; object-fit: cover; }
.phone-open { position: absolute; inset: 0; width: 100%; border: 0; background: transparent; cursor: pointer; color: var(--bone); font: inherit; }
.phone-open span { position: absolute; inset: auto 0 20px 0; text-align: center; font-family: var(--mono); font-size: 13px; color: var(--bone-2); }
.phone-open:hover span { color: var(--bone); }
.browser { border-radius: var(--r-frame); overflow: hidden; border: 1px solid var(--dark-line); background: var(--dark-2); box-shadow: 0 30px 80px rgba(28, 28, 30, .25); transition: transform .3s var(--ease); }
.browser:hover { transform: translateY(-4px); }
.browser-bar { height: 36px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid var(--dark-line); font-family: var(--mono); font-size: 12px; color: var(--bone-2); }
.browser-body { position: relative; height: 520px; background: #000; }
.browser-body img { width: 100%; height: 100%; object-fit: cover; object-position: top; }
.browser-body iframe { position: absolute; inset: 0; width: 100%; height: 100%; border: 0; pointer-events: none; opacity: 0; transition: opacity .4s; }
.browser-body iframe.is-loaded { opacity: 1; }
.piece-wide .browser-body { height: auto; }
.piece-wide .browser-body img { max-height: 640px; }

/* Who it's for: the one mid-page dark media block */
.who { display: grid; grid-template-columns: 1fr 1fr; gap: 2px; background: var(--paper); margin-top: clamp(48px, 8vh, 96px); }
.who a { position: relative; min-height: 460px; overflow: hidden; display: flex; align-items: flex-end; padding: 40px; color: var(--bone); background: var(--dark); }
.who img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .5; transition: transform .8s var(--ease), opacity .4s; }
.who a:hover img { transform: scale(1.04); opacity: .65; }
.who-text { position: relative; z-index: 1; }
.who h3 { font-size: clamp(1.8rem, 3vw, 2.6rem); letter-spacing: -.025em; font-weight: 700; margin-bottom: 10px; }
.who p { opacity: .85; max-width: 40ch; line-height: 1.5; }
.who .link { display: inline-block; margin-top: 18px; color: var(--gold-dark); }

/* What we do */
.services { padding: clamp(80px, 12vh, 140px) 0; }
.services-grid { display: grid; grid-template-columns: 4fr 8fr; gap: clamp(28px, 5vw, 80px); }
.services .section-title { position: sticky; top: 100px; margin-bottom: 16px; }
.services .section-lead { max-width: 30ch; }
.svc { display: grid; grid-template-columns: 1fr 140px; gap: 24px; align-items: center; padding: 28px 0; border-bottom: 1px solid var(--line); }
.svc:first-child { border-top: 1px solid var(--line); }
.svc h3 { font-size: 1.6rem; letter-spacing: -.02em; font-weight: 700; margin-bottom: 8px; }
.svc p { color: var(--ink-2); max-width: 52ch; line-height: 1.5; }
.svc img { width: 140px; aspect-ratio: 4 / 5; object-fit: cover; border-radius: var(--r); transition: transform .3s var(--ease); }
.svc:hover img { transform: scale(1.03); }

/* App pricing */
.app { padding: 0 0 clamp(80px, 12vh, 140px); }
.app-box { background: var(--paper-2); border-radius: 12px; padding: clamp(32px, 5vw, 64px); display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px; align-items: end; }
.app h2 { font-size: clamp(1.8rem, 3.2vw, 2.8rem); letter-spacing: -.03em; font-weight: 700; line-height: 1.05; max-width: 22ch; margin-bottom: 10px; }
.app-box > div > p { color: var(--ink-2); max-width: 55ch; line-height: 1.5; }
.tiers { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; font-family: var(--mono); font-size: 13px; color: var(--ink-2); }
.tiers b { display: block; font-size: 32px; color: var(--ink); font-weight: 500; letter-spacing: -.02em; margin-bottom: 6px; }
.app .link { display: inline-block; margin-top: 20px; }

/* Closing band: heading + enquiry form, the single dark band */
.book { position: relative; overflow: hidden; background: var(--dark); color: var(--bone); padding: clamp(80px, 12vh, 140px) 0; }
.book-bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .22; }
.book .wrap { position: relative; z-index: 1; display: grid; grid-template-columns: 1fr 1fr; gap: clamp(40px, 6vw, 96px); align-items: start; }
.book h2 { font-size: clamp(2.6rem, 6vw, 5.2rem); letter-spacing: -.03em; font-weight: 800; line-height: .96; max-width: 12ch; margin-bottom: 20px; }
.book-intro p { color: var(--bone-2); font-size: 1.15rem; max-width: 40ch; line-height: 1.5; }
.form { display: grid; gap: 22px; }
.field { display: grid; gap: 8px; }
.field label, .field .label { font-size: 14px; font-weight: 600; color: var(--bone); }
.pills { display: flex; gap: 10px; flex-wrap: wrap; }
.pills input { position: absolute; opacity: 0; width: 0; height: 0; }
.pills span { display: inline-block; padding: 10px 16px; border-radius: var(--r); border: 1px solid var(--dark-line); background: var(--dark-2); color: var(--bone); font-size: 14px; cursor: pointer; transition: border-color .2s, background .2s; }
.pills input:checked + span { border-color: var(--gold-dark); background: rgba(212, 168, 58, .12); }
.pills input:focus-visible + span { outline: 2px solid var(--gold-dark); outline-offset: 2px; }
.field input, .field textarea {
  width: 100%; padding: 13px 14px; border-radius: var(--r);
  border: 1px solid var(--dark-line); background: var(--dark-2); color: var(--bone);
  font: inherit; font-size: 15px;
}
.field input::placeholder, .field textarea::placeholder { color: #7A7570; }
.field input:focus, .field textarea:focus { outline: 2px solid var(--gold-dark); outline-offset: 0; border-color: var(--gold-dark); }
.field textarea { min-height: 120px; resize: vertical; }
.form-error { display: none; color: #F0A38B; font-size: 14px; }
.form-error.is-visible { display: block; }
.form-success { display: none; padding: 24px; border-radius: var(--r); border: 1px solid var(--gold-dark); background: rgba(212, 168, 58, .1); font-size: 1.05rem; line-height: 1.5; }
.form-success.is-visible { display: block; }
.form-fallback { font-size: 14px; color: var(--bone-2); }
.form-fallback a { color: var(--gold-dark); }
.form-fallback a:hover { text-decoration: underline; }

footer { background: var(--dark); color: var(--bone-2); border-top: 1px solid var(--dark-line); padding: 32px 0; }
footer .wrap { display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; font-size: 14px; }
footer img { height: 32px; width: auto; }
footer a:hover { color: var(--bone); }

/* Lightbox for the full reel */
.lightbox { border: 0; padding: 0; background: transparent; max-width: none; max-height: none; width: 100vw; height: 100dvh; }
.lightbox::backdrop { background: rgba(14, 14, 16, .92); }
.lightbox-inner { position: relative; width: 100%; height: 100%; display: grid; place-items: center; }
.lightbox video { height: min(90dvh, 960px); max-width: 100%; aspect-ratio: 9 / 16; border-radius: var(--r-frame); background: #000; }
.lightbox-close { position: absolute; top: 20px; right: 20px; padding: 12px 16px; border: 1px solid rgba(237, 232, 221, .3); border-radius: var(--r); background: rgba(14, 14, 16, .6); color: var(--bone); font: inherit; font-size: 14px; cursor: pointer; }
.lightbox-close:hover { background: rgba(14, 14, 16, .9); }

/* Scroll reveal: CSS scroll-driven, no JS, progressive enhancement */
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) {
    .reveal { animation: reveal both; animation-timeline: view(); animation-range: entry 0% entry 45%; }
    @keyframes reveal { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: none; } }
  }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .rise { animation: none; }
  .btn, .browser, .who img, .svc img, .nav { transition: none; }
  .btn:hover, .browser:hover, .who a:hover img, .svc:hover img { transform: none; }
}

/* Mobile collapse */
@media (max-width: 860px) {
  .nav-links { display: none; }
  .hero-strip { grid-template-columns: 1fr; }
  .hero-still { display: none; }
  .piece, .piece-flip { grid-template-columns: 1fr; }
  .piece-flip .piece-text { order: 0; }
  .browser-body { height: 380px; }
  .who { grid-template-columns: 1fr; }
  .who a { min-height: 340px; padding: 28px; }
  .services-grid { grid-template-columns: 1fr; }
  .services .section-title { position: static; }
  .svc { grid-template-columns: 1fr 96px; }
  .svc img { width: 96px; }
  .app-box { grid-template-columns: 1fr; }
  .tiers { grid-template-columns: 1fr; gap: 14px; }
  .book .wrap { grid-template-columns: 1fr; }
  .facts { flex-wrap: wrap; gap: 18px; }
}
```

- [ ] **Step 2: Dash check on the stylesheet**

Run: `grep -nP "[\x{2014}\x{2013}]" css/site.css || echo "no dashes"`
Expected: `no dashes`

- [ ] **Step 3: Commit**

```bash
git add css/site.css
git commit -m "Add stylesheet for the services site

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 4: Page markup

**Files:**
- Replace: `index.html` (entire file)

- [ ] **Step 1: Replace `index.html` with the new page**

Overwrite the whole file with this. The old markup is preserved in git history.

```html
<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CornerHQ: videos, websites and apps for the fight game</title>
  <meta name="description" content="CornerHQ makes promo videos, marketing, websites and apps for combat sports gyms and fight promotions across Australia.">
  <meta property="og:title" content="CornerHQ: videos, websites and apps for the fight game">
  <meta property="og:description" content="Promo videos, marketing, websites and apps for combat sports gyms and fight promotions across Australia.">
  <meta property="og:image" content="https://www.cornerhq.com.au/images/reel/f27.jpg">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.cornerhq.com.au/">
  <meta name="theme-color" content="#0E0E10">
  <link rel="preload" href="fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="images/reel/poster.jpg" as="image">
  <link rel="stylesheet" href="css/site.css">
</head>
<body>

  <header class="nav" id="nav">
    <a class="nav-logo" href="#top" aria-label="CornerHQ home">
      <img class="logo-light" src="images/logo-light.png" alt="CornerHQ" width="220" height="80">
      <img class="logo-dark" src="images/logo-dark.png" alt="CornerHQ" width="220" height="80">
    </a>
    <nav class="nav-links" aria-label="Main">
      <a href="#work">Work</a>
      <a href="#services">Services</a>
      <a href="#app">The app</a>
    </nav>
    <a class="btn" href="#book">Book a call</a>
  </header>

  <main id="top">

    <section class="hero" id="hero">
      <div class="hero-strip" aria-hidden="true">
        <div class="hero-still"><img src="images/reel/f54.jpg" alt="" loading="eager"></div>
        <div>
          <video class="hero-video" src="video/reel-loop.mp4" poster="images/reel/poster.jpg" autoplay muted loop playsinline preload="metadata"></video>
        </div>
        <div class="hero-still"><img src="images/reel/f63.jpg" alt="" loading="eager"></div>
      </div>
      <div class="wrap hero-copy">
        <h1 class="rise">Videos, websites and apps for the <em>fight game.</em></h1>
        <p class="hero-sub rise">CornerHQ works with combat sports gyms and fight promotions across Australia. One partner for the whole picture.</p>
        <div class="hero-ctas rise">
          <a class="btn" href="#book">Book a call</a>
          <a class="btn btn-ghost" href="#work">See the work</a>
        </div>
      </div>
    </section>

    <section class="opinion">
      <div class="wrap">
        <p class="reveal">Most gym sites are a template with a logo dropped in. Most fight promos are phone footage with a beat under it. <em>We do the other thing.</em></p>
      </div>
    </section>

    <section class="work" id="work">
      <div class="wrap">
        <h2 class="section-title reveal">The work</h2>
        <p class="section-lead reveal">Everything below is real, live and made by CornerHQ.</p>

        <article class="piece reveal">
          <div class="piece-text">
            <p class="piece-kind">Fighter promo</p>
            <h3>Sing Muay Thai</h3>
            <p>A 73-second promo cut for Instagram. Shot dark, cut to the fighter's own words, built to stop the scroll and sell the gym.</p>
            <div class="facts">
              <div><b>73s</b>runtime</div>
              <div><b>9:16</b>cut for Reels</div>
              <div><b>1080p</b>delivered</div>
            </div>
            <button class="link btn-watch" type="button">Watch with sound</button>
          </div>
          <div class="phone">
            <video class="loop-video" src="video/reel-loop.mp4" poster="images/reel/f10.jpg" autoplay muted loop playsinline preload="metadata"></video>
            <button class="phone-open btn-watch" type="button" aria-label="Watch the full promo with sound"><span>tap for sound</span></button>
          </div>
        </article>

        <article class="piece piece-flip reveal">
          <div class="piece-text">
            <p class="piece-kind">Gym website</p>
            <h3>singmuaythai.com.au</h3>
            <p>Sydney Muay Thai gym with four world champions on the floor. Classes, trainers, membership and trial bookings, all on one fast site.</p>
            <div class="facts">
              <div><b>5</b>membership tiers</div>
              <div><b>4</b>trainer profiles</div>
              <div><b>1</b>trial booking flow</div>
            </div>
            <a class="link" href="https://singmuaythai.com.au" target="_blank" rel="noopener">Open the live site</a>
          </div>
          <div class="browser">
            <div class="browser-bar">singmuaythai.com.au</div>
            <div class="browser-body">
              <img src="images/sing-site.png" alt="Screenshot of the Sing Muay Thai website" loading="lazy" width="1280" height="900">
              <iframe class="site-frame" data-src="https://singmuaythai.com.au" title="Sing Muay Thai website, live" tabindex="-1"></iframe>
            </div>
          </div>
        </article>

        <article class="piece piece-wide reveal">
          <div class="piece-text">
            <p class="piece-kind">Gym app</p>
            <h3>The CornerHQ app</h3>
            <p>Class management, member profiles, payments and messaging, built from scratch for combat sports gyms. Your members get a branded app on their phone.</p>
            <div class="facts">
              <div><b>$0</b>up to 20 members</div>
              <div><b>All</b>features on every plan</div>
            </div>
            <a class="link" href="#app">See app pricing</a>
          </div>
          <div class="browser">
            <div class="browser-bar">app.cornerhq.com.au</div>
            <div class="browser-body">
              <img src="images/dashboard-preview.png" alt="CornerHQ dashboard showing members, attendance and revenue" loading="lazy" width="1547" height="1058">
            </div>
          </div>
        </article>
      </div>

      <div class="who">
        <a href="#book">
          <img src="images/reel/f10.jpg" alt="" loading="lazy">
          <div class="who-text">
            <h3>Gyms</h3>
            <p>Muay Thai, boxing, kickboxing, MMA, BJJ. From one room to multi-site.</p>
            <span class="link">Book a call</span>
          </div>
        </a>
        <a href="#book">
          <img src="images/reel/f27.jpg" alt="" loading="lazy">
          <div class="who-text">
            <h3>Fight promotions</h3>
            <p>Event trailers, fighter promos, ticket pushes, fight card sites and apps.</p>
            <span class="link">Book a call</span>
          </div>
        </a>
      </div>
    </section>

    <section class="services" id="services">
      <div class="wrap services-grid">
        <div>
          <h2 class="section-title reveal">What we do</h2>
          <p class="section-lead reveal">Four things, done for one industry. Buy one or all of them.</p>
        </div>
        <div>
          <div class="svc reveal">
            <div>
              <h3>Promo videos</h3>
              <p>Fighter promos, fight night trailers, gym reels. Shot and cut for Instagram, TikTok and the big screen at the venue.</p>
            </div>
            <img src="images/reel/f54.jpg" alt="" loading="lazy">
          </div>
          <div class="svc reveal">
            <div>
              <h3>Marketing</h3>
              <p>Trial offers, fight ticket pushes, member campaigns. Ads and content that speak the language of the gym floor.</p>
            </div>
            <img src="images/reel/f45.jpg" alt="" loading="lazy">
          </div>
          <div class="svc reveal">
            <div>
              <h3>Websites</h3>
              <p>Fast, custom built, yours to own. Classes, timetable, trainers, membership and trial bookings that actually convert.</p>
            </div>
            <img src="images/reel/f70.jpg" alt="" loading="lazy">
          </div>
          <div class="svc reveal">
            <div>
              <h3>Apps</h3>
              <p>The CornerHQ gym app, plus custom builds: fight card apps, ticketing, member portals.</p>
            </div>
            <img src="images/reel/f27.jpg" alt="" loading="lazy">
          </div>
        </div>
      </div>
    </section>

    <section class="app" id="app">
      <div class="wrap">
        <div class="app-box reveal">
          <div>
            <h2>The gym app is priced by members, not features.</h2>
            <p>Every plan has everything. Start free, pay when the gym grows.</p>
            <a class="link" href="#book">Book a call</a>
          </div>
          <div class="tiers">
            <div><b>$0</b>up to 20 members</div>
            <div><b>$150</b>a month, up to 150 members</div>
            <div><b>$300</b>a month, unlimited members</div>
          </div>
        </div>
      </div>
    </section>

    <section class="book on-dark" id="book">
      <img class="book-bg" src="images/reel/f63.jpg" alt="" loading="lazy">
      <div class="wrap">
        <div class="book-intro">
          <h2 class="reveal">Twenty minutes. No pitch deck.</h2>
          <p class="reveal">Tell us about the gym or the show. We'll reply within one business day to set up a time.</p>
        </div>
        <form class="form" id="enquiry" action="https://api.web3forms.com/submit" method="POST" novalidate>
          <input type="hidden" name="access_key" value="5406bfa5-c77e-400b-b2ca-8432e988be85">
          <input type="hidden" name="subject" value="New enquiry from cornerhq.com.au">
          <input type="checkbox" name="botcheck" class="visually-hidden" tabindex="-1" autocomplete="off">

          <fieldset class="field">
            <legend class="label">What do you run?</legend>
            <div class="pills">
              <label><input type="radio" name="Business type" value="Gym" required><span>Gym</span></label>
              <label><input type="radio" name="Business type" value="Fight promotion"><span>Fight promotion</span></label>
              <label><input type="radio" name="Business type" value="Both"><span>Both</span></label>
            </div>
          </fieldset>

          <div class="field">
            <label for="f-name">Your name</label>
            <input id="f-name" name="Name" type="text" autocomplete="name" required>
          </div>
          <div class="field">
            <label for="f-business">Gym or promotion name</label>
            <input id="f-business" name="Business" type="text" autocomplete="organization" required>
          </div>
          <div class="field">
            <label for="f-email">Email</label>
            <input id="f-email" name="Email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="f-message">What do you need? (optional)</label>
            <textarea id="f-message" name="Message"></textarea>
          </div>

          <p class="form-error" id="form-error" role="alert"></p>
          <div>
            <button class="btn" type="submit" id="form-submit">Book a call</button>
          </div>
          <p class="form-fallback">Or email <a href="mailto:hello@cornerhq.com.au">hello@cornerhq.com.au</a>.</p>
        </form>
        <div class="form-success" id="form-success" role="status" tabindex="-1">
          Got it. We'll reply within one business day to set up a time.
        </div>
      </div>
    </section>

  </main>

  <footer>
    <div class="wrap">
      <img src="images/logo-light.png" alt="CornerHQ" width="176" height="64">
      <a href="mailto:hello@cornerhq.com.au">hello@cornerhq.com.au</a>
      <span>Sydney, Australia</span>
    </div>
  </footer>

  <dialog class="lightbox" id="lightbox">
    <div class="lightbox-inner">
      <video id="lightbox-video" controls playsinline preload="none" poster="images/reel/poster.jpg"></video>
      <button class="lightbox-close" type="button" id="lightbox-close">Close</button>
    </div>
  </dialog>

  <script src="js/site.js" defer></script>
</body>
</html>
```

- [ ] **Step 2: Confirm the email address**

The page uses `hello@cornerhq.com.au` in the form fallback and footer. Check with the owner that this address exists and is monitored. If it does not, replace both occurrences with the address they give you. Do not ship an address that bounces.

- [ ] **Step 3: Run the check script**

Run: `python scripts/check.py`
Expected: `FAIL` listing only `js/site.js` missing (or a FileNotFoundError for it). No dash failures, no missing image or video assets, no rule failures. If any asset is reported missing, fix the path before moving on.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Rebuild homepage as reel-first services site

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 5: Behaviour script

**Files:**
- Create: `js/site.js`

- [ ] **Step 1: Write the script**

```js
/* CornerHQ site behaviour. Four jobs, nothing else:
   1. Nav turns light once the hero has scrolled away (IntersectionObserver).
   2. Lightbox plays the full reel with sound.
   3. Enquiry form posts to Web3Forms and shows inline states.
   4. Reduced motion: no looping video, no smooth scroll. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Nav */
  var nav = document.getElementById('nav');
  var hero = document.getElementById('hero');
  if (nav && hero && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      nav.classList.toggle('is-light', !entries[0].isIntersecting);
    }, { rootMargin: '-72px 0px 0px 0px', threshold: 0 });
    io.observe(hero);
  }

  /* 2. Lightbox */
  var lightbox = document.getElementById('lightbox');
  var lightboxVideo = document.getElementById('lightbox-video');
  var lightboxClose = document.getElementById('lightbox-close');
  var FULL_REEL = 'video/reel-full.mp4';

  function openLightbox() {
    if (!lightbox || !lightboxVideo) return;
    if (!lightboxVideo.getAttribute('src')) lightboxVideo.setAttribute('src', FULL_REEL);
    if (typeof lightbox.showModal === 'function') lightbox.showModal();
    else lightbox.setAttribute('open', '');
    lightboxVideo.currentTime = 0;
    var p = lightboxVideo.play();
    if (p && typeof p.catch === 'function') p.catch(function () {});
  }

  function closeLightbox() {
    if (!lightbox || !lightboxVideo) return;
    lightboxVideo.pause();
    if (lightbox.open && typeof lightbox.close === 'function') lightbox.close();
    else lightbox.removeAttribute('open');
  }

  Array.prototype.forEach.call(document.querySelectorAll('.btn-watch'), function (btn) {
    btn.addEventListener('click', openLightbox);
  });
  if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
  if (lightbox) {
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox || e.target.classList.contains('lightbox-inner')) closeLightbox();
    });
    lightbox.addEventListener('close', function () { if (lightboxVideo) lightboxVideo.pause(); });
    lightbox.addEventListener('cancel', function () { if (lightboxVideo) lightboxVideo.pause(); });
  }

  /* 3. Enquiry form */
  var form = document.getElementById('enquiry');
  var formError = document.getElementById('form-error');
  var formSuccess = document.getElementById('form-success');
  var formSubmit = document.getElementById('form-submit');

  function showError(msg) {
    if (!formError) return;
    formError.textContent = msg;
    formError.classList.add('is-visible');
  }

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (formError) formError.classList.remove('is-visible');

      var type = form.querySelector('input[name="Business type"]:checked');
      var name = form.querySelector('#f-name').value.trim();
      var business = form.querySelector('#f-business').value.trim();
      var email = form.querySelector('#f-email').value.trim();
      var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

      if (!type) return showError('Tell us what you run.');
      if (!name) return showError('We need your name.');
      if (!business) return showError('We need the gym or promotion name.');
      if (!emailOk) return showError('That email does not look right.');

      formSubmit.disabled = true;
      formSubmit.textContent = 'Sending';

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        if (!res.ok) throw new Error('bad status ' + res.status);
        form.hidden = true;
        formSuccess.classList.add('is-visible');
        formSuccess.focus();
      }).catch(function () {
        showError('That did not send. Email hello@cornerhq.com.au instead.');
        formSubmit.disabled = false;
        formSubmit.textContent = 'Book a call';
      });
    });
  }

  /* 4. Reduced motion and media */
  var loops = document.querySelectorAll('.hero-video, .loop-video');
  if (reduceMotion) {
    Array.prototype.forEach.call(loops, function (v) {
      v.removeAttribute('autoplay');
      v.pause();
    });
  }

  /* Live site iframe: load after the page is idle, fade in when ready.
     If it never loads, the screenshot underneath stays visible. */
  var frame = document.querySelector('.site-frame');
  if (frame && frame.dataset.src) {
    var loadFrame = function () {
      frame.addEventListener('load', function () { frame.classList.add('is-loaded'); });
      frame.src = frame.dataset.src;
    };
    if ('requestIdleCallback' in window) requestIdleCallback(loadFrame, { timeout: 4000 });
    else setTimeout(loadFrame, 1500);
  }
})();
```

- [ ] **Step 2: Run the check script**

Run: `python scripts/check.py`
Expected: `OK: all checks passed`

- [ ] **Step 3: Commit**

```bash
git add js/site.js
git commit -m "Add nav switch, lightbox, enquiry form and reduced-motion behaviour

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 6: Local run and visual verification

**Files:**
- Create: `.claude/launch.json`

- [ ] **Step 1: Add a launch config for the Browser pane**

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "cornerhq-site",
      "runtimeExecutable": "python",
      "runtimeArgs": ["-m", "http.server", "8347", "--directory", "C:\\Users\\Thien\\Desktop\\CornerHQWeb"],
      "port": 8347
    }
  ]
}
```

- [ ] **Step 2: Start it and open the page**

Use the Browser pane `preview_start` with name `cornerhq-site`, or run `python -m http.server 8347` and open `http://localhost:8347`.

- [ ] **Step 3: Desktop pass (viewport 1280 wide or wider)**

Check each line and fix in `css/site.css` or `index.html` if it fails:

- Hero: video plays muted in the centre panel, stills either side, headline on two lines, both buttons visible without scrolling, no black flash on loop.
- Nav is dark over the hero and turns paper with the dark logo after scrolling past it. Logo has no tagline.
- "Watch with sound" and the phone both open the lightbox, the full reel plays with audio, Escape and Close both close it and the audio stops.
- Sing site browser frame shows the screenshot, then fades to the live iframe.
- App screenshot renders full width in its frame.
- Gyms and Fight promotions blocks are dark with the stills behind them.
- Services list: sticky heading holds while the four rows scroll.
- App pricing panel shows three numbers in a row.
- Form: submit with nothing filled shows "Tell us what you run." Fill it in and submit: the form hides and the success message shows. Confirm the email arrives in the owner's Gmail.
- No console errors (`read_console_messages`).

- [ ] **Step 4: Mobile pass (375 wide)**

- Hero shows only the video, headline wraps to three lines at most, buttons visible.
- Every section is single column. No horizontal scrollbar.
- Form pills wrap onto two lines cleanly.

- [ ] **Step 5: Reduced-motion pass**

In DevTools, emulate `prefers-reduced-motion: reduce` and reload. Expected: hero shows the poster, nothing loops, no reveal animations, anchors jump instead of smooth-scrolling.

- [ ] **Step 6: Commit**

```bash
git add .claude/launch.json
git commit -m "Add local preview launch config

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: Pre-flight, push, update memory

**Files:**
- Modify: `C:\Users\Thien\.claude\projects\C--Users-Thien-Desktop-CornerHQWeb\memory\project-cornerhq-landing.md`

- [ ] **Step 1: Run the full pre-flight**

Run:
```bash
python scripts/check.py && grep -c "Book a call" index.html && grep -nP "[\x{2014}\x{2013}]" index.html css/site.css js/site.js || echo "no dashes"
```
Expected: `OK: all checks passed`, a count of at least 5 for "Book a call", and `no dashes`.

Then walk the taste-skill pre-flight items that the script cannot check, by reading `index.html`:
- Hero has at most four text elements (headline, subtext, CTAs). Yes.
- No section repeats a layout family. Order is: triptych, single paragraph, split pieces, two dark tiles, sticky-list, tinted panel, dark band with form. Yes.
- No two consecutive split-image pieces beyond two. The third piece is full-width. Yes.
- Every number on the page is provable: 73s, 9:16, 1080p, 5 tiers, 4 trainers, 1 booking flow, $0, $150, $300, 20, 150 members. Yes.

- [ ] **Step 2: Push**

```bash
git push origin main
```

Expected: Vercel deploys within about a minute. Open `https://www.cornerhq.com.au` and confirm the new page is live and the video plays.

- [ ] **Step 3: Update the project memory file**

Replace the body of `project-cornerhq-landing.md` (keep its frontmatter, update `description`) with:

```markdown
CornerHQ is now a services company for the fight game: promo videos, marketing, websites and apps for combat sports gyms and fight promotions in Australia. The gym app is one of four services. SubForge (subforge.com.au) is the owner's separate studio for all other small businesses; the two must not look alike.

## What's built (2026-09-04 rebuild)

Static site at `C:\Users\Thien\Desktop\CornerHQWeb`: `index.html`, `css/site.css`, `js/site.js`. No build step.

- Reel-first homepage: dark hero triptych of the Sing Muay Thai promo reel, light paper body, single dark closing band with the enquiry form.
- Proof: Sing Muay Thai promo (73s reel), singmuaythai.com.au (live iframe with screenshot fallback), the CornerHQ app dashboard screenshot.
- Enquiry form posts to Web3Forms, key `5406bfa5-c77e-400b-b2ca-8432e988be85`, to thiendo9898@gmail.com. No calendar booking yet.
- App pricing unchanged: $0 to 20 members, $150 to 150, $300 unlimited, all features on every tier.
- Design rules locked in `docs/superpowers/specs/2026-09-04-cornerhq-services-site-design.md`. Run `python scripts/check.py` before every push.
- Assets rebuilt by `scripts/make-assets.sh` from the reel in Downloads and `images/logo.png`.

## Where it lives

- GitHub: https://github.com/ttd909/CornerHQWeb (branch: main)
- Vercel: auto-deploys on every push to main

## What's next

- Cal.com booking when the owner sets up an account.
- Proper two-version logo file without the tagline (current crop is a stopgap).
- Add case studies as real work ships, with client OK.
```

- [ ] **Step 4: Stop the brainstorm companion server**

```bash
bash "C:/Users/Thien/.claude/plugins/cache/superpowers-marketplace/superpowers/5.1.0/skills/brainstorming/scripts/stop-server.sh" "C:/Users/Thien/Desktop/CornerHQWeb/.superpowers/brainstorm/958-1788486281"
```

---

## Self-review against the spec

- **Section 4 page structure:** Tasks 3 and 4 implement all nine sections in order. Nav switch in Task 5.
- **Section 5 form:** Task 4 markup (fields, labels above inputs, Web3Forms key, honeypot), Task 5 validation and inline states, fallback email present.
- **Section 6 video:** Task 2 encodes both clips and the stills; Task 4 wires posters; Task 5 lightbox loads the full reel on demand only (`preload="none"`, src set on open).
- **Section 7 visual system:** tokens, fonts, radius rule, buttons, logo versions, motion dials and reduced motion all in Task 3; logos in Task 2.
- **Section 8 rules:** enforced mechanically by `scripts/check.py` (Task 1) plus the manual walk in Task 7.
- **Section 9 stack:** plain files, Vercel, self-hosted fonts, `.superpowers/` already ignored (committed with the spec).
- **Section 10 edge cases:** video poster fallback (Task 4), iframe screenshot fallback (Tasks 4 and 5), form error inline with email fallback (Task 5), lightbox Escape/backdrop/close (Task 5), reduced motion (Tasks 3 and 5).
- **Deviation from spec section 9:** the spec says "one index.html"; this plan splits CSS and JS into `css/site.css` and `js/site.js`. Still no build step, still plain files. The split keeps each file readable and lets the check script enforce "no inline styles or scripts". Recorded here so it is a known choice, not drift.
