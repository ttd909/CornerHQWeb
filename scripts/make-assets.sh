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
