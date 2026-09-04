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
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        fail(f"missing file: {path}")
        return None
    with open(full, encoding="utf-8") as f:
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
    if css:
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
        "images/og.jpg": 300_000,
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
    labels = re.findall(r'class="(?:btn|link)[^"]*"[^>]*>([^<]+)<', html)
    contact_like = {label.strip() for label in labels if re.search(r"contact|touch|talk|enquir|start", label, re.I)}
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
        (r"\b(?:Seamless|Elevate|Unleash|Next-Gen)\b", "filler verb"),
    ]:
        if re.search(pat, html):
            fail(f"banned copy pattern: {why} ({pat})")
    # Middle-dot chains.
    if re.search(r"·[^·\n]*·", html):
        fail("middle-dot separator chain found")
    # No inline styles or scripts.
    if re.search(r'\sstyle="', html):
        fail("inline style attribute found; put it in css/site.css")
    if re.search(r"<script(?![^>]*\bsrc=)(?:\s[^>]*)?>[^<]", html):
        fail("inline script found; put it in js/site.js")
    # Google Fonts must not be linked.
    if "fonts.googleapis.com" in html:
        fail("Google Fonts linked; fonts must be self-hosted")


def check_js():
    js = read("js/site.js")
    if js and ("addEventListener('scroll'" in js or 'addEventListener("scroll"' in js):
        fail("scroll listener found in site.js; use IntersectionObserver")


def main():
    html = read("index.html")
    css = read("css/site.css")
    js = read("js/site.js")
    if html:
        check_dashes("index.html", html)
        check_assets(html)
        check_rules(html)
    if css:
        check_dashes("css/site.css", css)
    if js:
        check_dashes("js/site.js", js)
    check_sizes()
    check_js()
    if failures:
        print("FAIL")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("OK: all checks passed")


if __name__ == "__main__":
    main()
