# CornerHQ Dashboard Preview — Design Spec

**Date:** 2026-06-30
**Status:** Approved

---

## Overview

A static HTML page (`preview.html`) that shows prospective customers a realistic sample of what the CornerHQ admin dashboard looks like. It lives at `cornerhq.com.au/preview` — URL-only access, no link from the main site, no password protection.

**Stack:** Plain HTML + CSS + Chart.js from CDN. No build step. Same pattern as `index.html`.

---

## Brand

Matches the existing site:

- **Primary / sidebar background:** Navy (`#0A1628`)
- **Accent / active nav / section labels / charts:** Orange (`#FF6B00`)
- **Page background:** Light gray (`#eef0f4`)
- **Cards:** White (`#ffffff`), border `#e4e9f0`
- **Body text:** Dark gray (`#333333`)
- **Muted text:** `#aaa` / `#999`

---

## Layout

Two-column fixed layout — sidebar on the left, scrollable main content on the right.

### Sidebar (190px, navy)

- **CornerHQ** logo text in orange (small, uppercase)
- **ADMIN** in white below it
- Nav items: TODAY, SCHEDULE, MEMBERS, MEMBERSHIPS, CLASS SETUP, PT, **ANALYTICS** (active — orange highlight pill), SETTINGS
- Nav items are non-functional (static display only)

### Main Content Area

**Compact page header** — single line, no large title block:
- Left: "ANALYTICS" in small bold uppercase
- Right: "LAST 30 DAYS" muted label
- Thin divider line below

Then three scrollable sections, each with:
- An orange section label (e.g. "MEMBERS") + horizontal rule spanning the remaining width
- Stat cards immediately below the label
- Charts below the stat cards

---

## Sections & Content

### 1. Members

**Stat cards (4-column grid):**

| Label | Value | Description |
|-------|-------|-------------|
| Attendance | 247 | Total check-ins |
| First-Timers | 18 | First seen in the period |
| Retention | 78% | 66 of 89 members seen |
| No-Shows | 3 | Booked, not checked in |

**Charts (2-column):**

- **Attendance Over Time** — Bar chart (Chart.js). Daily check-ins over the last 30 days. Orange bars. X-axis: dates. Y-axis: check-in count. Tooltip on hover.
- **Retention Rate Trend** — Line chart (Chart.js). Monthly retention % over 6 months. Orange line with fill. X-axis: month labels. Y-axis: percentage. Tooltip on hover.

---

### 2. Finance

**Stat cards (4-column grid):**

| Label | Value | Description |
|-------|-------|-------------|
| Cash This Month | $1,240 | Recorded cash passes |
| One-Off Received | $3,890 | Cash and Stripe passes |
| Weekly Run-Rate | $1,120 | Active Stripe weekly passes |
| Active Subscriptions | 34 | Stripe recurring memberships |

**Charts (2/3 + 1/3 split):**

- **Revenue Over Time** — Line chart (Chart.js). Monthly revenue over 6 months. Navy line with light fill. X-axis: month labels. Y-axis: dollar amounts. Tooltip on hover.
- **Membership Breakdown** — Doughnut chart (Chart.js). Three segments: Monthly 60% (orange), Casual 30% (navy), Annual 10% (light gray). Legend beside the chart.

**Cash Payments List** (below charts, full width card):
- Heading: "Cash Payments This Month"
- Tabular list of recent payments: name, membership/pass type, amount, date
- Sample data: Sarah Mitchell ($180, 10-Class Pass, Mon 29/6), James Tran ($120, Monthly Membership, Fri 26/6), Priya Sharma ($25, Casual Drop-In, Wed 24/6), Connor Walsh ($95, 5-Class Pass, Mon 22/6)

---

### 3. Classes

**Stat cards (3-column grid):**

| Label | Value | Description |
|-------|-------|-------------|
| Total Classes Run | 62 | This period |
| Avg. Class Size | 12 | Members per session |
| Busiest Day | Tue | Highest avg. attendance |

**Top Classes** (full width card):
- Heading: "Top Classes" with "BY CHECK-INS" label right-aligned
- Horizontal bar chart (CSS-rendered, no Chart.js needed — simpler and sufficient):
  - Muay Thai All Levels — 89
  - Boxing Fundamentals — 64
  - Sparring — 49
  - Strength & Conditioning — 34
  - Kids Muay Thai — 11

---

## Chart.js Integration

- Load from CDN: `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`
- All Chart.js instances initialised in a single `<script>` block at the bottom of the file
- Charts use made-up but realistic data
- Shared config defaults: no legend title, clean tooltips, responsive, maintain aspect ratio

**Chart data (made-up):**

*Attendance Over Time (last 30 days, weekly buckets for readability):*
Labels: Week 1, Week 2, Week 3, Week 4
Data: 48, 61, 72, 66

*Retention Rate Trend (last 6 months):*
Labels: Jan, Feb, Mar, Apr, May, Jun
Data: 62, 65, 68, 71, 75, 78

*Revenue Over Time (last 6 months):*
Labels: Jan, Feb, Mar, Apr, May, Jun
Data: 3200, 3800, 3500, 4100, 4600, 5130

*Membership Breakdown:*
Labels: Monthly, Casual, Annual
Data: 60, 30, 10

---

## Implementation Notes

- Single `preview.html` file in the repo root, alongside `index.html`
- No navigation link from `index.html` to `preview.html`
- All styles in an embedded `<style>` block — no external CSS
- Chart.js loaded via CDN `<script>` tag in `<head>`
- No JavaScript beyond Chart.js initialisation
- Mobile responsive via CSS grid (stat grids collapse to 2-col on narrow screens, 1-col on mobile)
- All data is hardcoded — this is a static demo, not a live dashboard
