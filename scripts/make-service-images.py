"""Builds the four 4:5 images for the "What we do" row. Run from the repo root.

1. Promo videos: the "HEART" title card over the fighter, 66.2s into the Rodlek reel.
2. Marketing: the Sing Muay Thai timetable post made for Instagram.
3. Websites: singmuaythai.com.au on a phone, captured past its splash gate.
4. Apps: the Sing member app sign-in screen, set on a dark surround so the row
   reads as one band.
"""
import os
from PIL import Image, ImageDraw

W, H = 900, 1125
DARK = (14, 14, 16)
MARKETING_SRC = r"C:\Users\Thien\Desktop\SingMuayThai\instagram\Final.jpg"


REEL = "C:/Users/Thien/Downloads/Muay Thai Fighter Promo \u2014 IG Reel 1080p (1).mp4"


def fit_4x5(im, anchor=0.0):
    """Crop to 4:5. anchor is the vertical position of the crop window, 0 = top, 1 = bottom."""
    im = im.convert("RGB")
    target = W / H
    w, h = im.size
    if w / h > target:
        nw = int(h * target)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target)
        y = int((h - nh) * anchor)
        im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)


def save(im, name):
    im.save(name, quality=84, optimize=True)
    print(name, im.size, os.path.getsize(name))


# 1. Promo videos: the "HEART" title card over the fighter, 66.2s into the reel
import subprocess
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "66.2", "-i", REEL, "-frames:v", "1", "-q:v", "2", "images/_promo-frame.jpg"], check=True)
save(fit_4x5(Image.open("images/_promo-frame.jpg"), anchor=0.35), "images/svc-promo.jpg")
os.remove("images/_promo-frame.jpg")

# 2. Marketing
save(fit_4x5(Image.open(MARKETING_SRC)), "images/svc-marketing.jpg")

# 3. Websites: mobile capture past the splash gate
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True)
    page.goto("https://www.singmuaythai.com.au/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    loc = page.get_by_text("ENTER SITE", exact=False)
    if loc.count():
        loc.first.click()
    page.wait_for_timeout(2500)
    page.screenshot(path="images/_sing-mobile.png")
    b.close()
shot = Image.open("images/_sing-mobile.png")
save(fit_4x5(shot), "images/svc-website.jpg")
os.remove("images/_sing-mobile.png")

# 4. Apps: member app on a dark surround
app = Image.open("images/member-app.png").convert("RGB")
canvas = Image.new("RGB", (W, H), DARK)
aw = 720
ah = int(app.height * aw / app.width)
app = app.resize((aw, ah), Image.LANCZOS)
mask = Image.new("L", (aw, ah), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, aw - 1, ah - 1), radius=36, fill=255)
canvas.paste(app, ((W - aw) // 2, (H - ah) // 2), mask)
save(canvas, "images/svc-app.jpg")
