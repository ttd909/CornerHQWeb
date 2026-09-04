"""Screenshot singmuaythai.com.au past its splash gate, for the work panel."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
    page.goto("https://www.singmuaythai.com.au/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    for label in ["ENTER SITE", "Enter site", "Enter Site"]:
        loc = page.get_by_text(label, exact=False)
        if loc.count():
            loc.first.click()
            break
    page.wait_for_timeout(2500)
    page.screenshot(path="images/sing-site.jpg", type="jpeg", quality=82)
    b.close()
print("images/sing-site.jpg written")
