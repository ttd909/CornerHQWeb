# Pricing Section — Design

**Date:** 2026-07-08
**Status:** Approved pending user review

## Goal

Add a pricing section to the CornerHQ landing page (`index.html`) so visitors can see plans and prices without contacting us first.

## Pricing model

Member-count-based pricing. Every tier includes every feature; tiers differ only by active-member cap. This is stated explicitly on the page as a selling point.

| Tier | Price | Member cap | Badge | CTA label |
|------|-------|-----------|-------|-----------|
| Starter | $0/month | Up to 20 active members | — | Get Started Free |
| Advanced | $150/month | Up to 150 active members | "Most Popular" (highlighted card) | Talk to Us |
| Professional | $300/month | Unlimited members | — | Talk to Us |

Prices shown as plain dollar amounts (no currency code).

## Placement & navigation

- New `<section class="pricing" id="pricing">` inserted between the Features section and the Contact section in `index.html`.
- Add a "Pricing" nav link (`href="#pricing"`) next to the existing "Get in Touch" link.

## Section contents

1. **Header:** heading "Simple, Honest Pricing" plus subline: "Every plan includes every feature. You only pay for the size of your gym."
2. **Three pricing cards** side by side (stack vertically on mobile), styled to match the existing navy (#0A1628) + gold colour scheme. Middle card (Advanced) is visually highlighted with a "Most Popular" badge.
   - Each card shows: tier name, price + "/month", member cap sub-label, a ✓ checklist of features, CTA button.
   - The checklist is identical in all three cards: Branded gym app (PWA), Class management, Member profiles, Payments & billing, Automated emails, Reports, Social media links.
   - All CTA buttons link to `#contact` (no self-serve signup exists; all leads go through the existing form).
3. **PWA callout box** at the bottom of the section:
   > **Your Own Gym App — Included in Every Plan**
   > Every plan comes with a Progressive Web App (PWA) carrying your gym's logo. When members save it to their home screen, it looks and behaves exactly like a regular app — no browser bar, works offline, and supports push notifications. No app store approval, no extra cost.

## Implementation notes

- Plain HTML/CSS in `index.html`, consistent with the rest of the site (no framework, styles in the `<style>` block).
- Responsive: 3 columns on desktop, stacked cards on mobile, matching existing breakpoints (960px, 640px).
- No JavaScript required beyond existing smooth-scroll behaviour of anchor links.

## Out of scope

- Self-serve signup or checkout.
- Annual billing toggle.
- Currency code display (AUD/USD) — revisit later if needed.
