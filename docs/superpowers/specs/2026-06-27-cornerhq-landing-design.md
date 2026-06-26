# CornerHQ Landing Page — Design Spec

**Date:** 2026-06-27
**Status:** Approved

---

## Overview

A single-page marketing website for CornerHQ — a gym management and member engagement platform built for combat sports gyms (Muay Thai, boxing, kickboxing, martial arts). The page communicates what the product does, highlights key features, and converts visitors via a contact form.

**Stack:** Plain HTML + CSS (no framework). Static file, deployable anywhere.
**Form delivery:** Formspree (free tier) — no backend required.

---

## Brand

- **Primary:** Navy Blue (`#0A1628`)
- **Accent:** Safety Orange (`#FF6B00`)
- **Background (features):** White (`#FFFFFF`)
- **Background (contact):** Light Gray (`#F5F7FA`)
- **Text (body):** Dark gray (`#333333`)
- **Text (on dark):** White / light gray

**Tone:** Clean, modern SaaS. Professional and trustworthy, with energy from the orange accent.

---

## Page Structure

### 1. Nav Bar

- Logo/wordmark "CornerHQ" — top left, white text
- Single link "Get in Touch" — top right, anchors to `#contact`
- Fixed or static; transparent overlay on hero background

### 2. Hero Section

- **Background:** Navy (`#0A1628`), full viewport height
- **Headline:** "The All-in-One Platform Built for Combat Sports Gyms"
- **Subheadline:** "Manage classes, members, trainers, payments and progress — all in one place. Built for Muay Thai, boxing, kickboxing and martial arts."
- **CTA button (orange):** "Talk to Us & Save" — scrolls to `#contact`
- **Below button (small text):** "Book a free demo today"
- Content centered vertically and horizontally

### 3. Features Strip

- **Background:** White
- **Layout:** 2-row grid — 3 items top row, 2 items centered bottom row
- **Each feature:** Icon (orange), bold label (navy), one-line description (gray)

| Label | Description |
|-------|-------------|
| Class Management | Schedule classes, manage trainers and track attendance |
| Member Profiles | Track levels, progress notes and training pathways |
| Payments | Memberships, billing and payment history in one place |
| Communication | Keep members engaged and connected with your gym |
| Built Around You | Every feature can be tailored to fit the way your gym operates |

### 4. Contact Form

- **Background:** Light gray (`#F5F7FA`)
- **Anchor:** `id="contact"`
- **Heading:** "Get in Touch" (navy)
- **Subtext:** "Tell us about your gym and we'll be in touch shortly."
- **Fields:** Name, Gym Name, Email, Message (textarea)
- **Submit button (orange):** "Send Message"
- **On submit:** Success message replaces form — "Thanks! We'll be in touch soon."
- **Delivery:** Formspree endpoint (user to provide or create a free account at formspree.io)

### 5. Footer

- Simple one-line footer: "© 2026 CornerHQ. All rights reserved."
- Navy background, white text

---

## Implementation Notes

- Single `index.html` file with embedded `<style>` block — no external CSS framework
- No JavaScript framework — vanilla JS only (for smooth scroll and form success state)
- Mobile responsive via CSS flexbox/grid
- SVG icons inline or from a CDN (e.g. heroicons or similar)
- Formspree integration: `action="https://formspree.io/f/<ID>"` on the `<form>` tag
