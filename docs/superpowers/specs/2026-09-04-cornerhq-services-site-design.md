# CornerHQ services site: rebuild design

**Date:** 2026-09-04
**Status:** Approved by owner (interactive brainstorm with browser mockups, this date)
**Replaces:** the app-only landing page currently live at cornerhq.com.au
**Mockup that was approved:** `.superpowers/brainstorm/958-1788486281/content/reel-first-v2.html` (dark hero, light body). Treat it as the visual reference, not as code to copy.

## 1. What this is

CornerHQ stops being "gym management software" and becomes the company that does
videos, marketing, websites and apps for the fight game. The app is one of four
services, not the headline.

The owner's other business, SubForge (subforge.com.au), serves all small
businesses. CornerHQ serves combat sports gyms and fight promotions only. Two
doors, no overlap, and the two sites must not look alike.

## 2. Positioning

- **Audience:** owners of combat sports gyms (Muay Thai, boxing, kickboxing, MMA,
  BJJ) and fight promoters, in Australia. Individual fighters can enquire but the
  site does not talk to them.
- **Headline:** "Videos, websites and apps for the fight game."
- **Subtext:** "CornerHQ works with combat sports gyms and fight promotions across
  Australia. One partner for the whole picture."
- **The idea:** the work leads. The homepage opens on real footage and the first
  scroll shows real projects. Services are explained only after the work has done
  the talking.
- **Voice:** blunt, short sentences, no agency fluff. Same rules as SubForge (see
  section 8).

## 3. Proof at launch

Three real pieces, all owned or made by CornerHQ:

1. **Fighter promo for Sing Muay Thai.** 73 seconds, 9:16, 1080p. Source file:
   `C:\Users\Thien\Downloads\Muay Thai Fighter Promo — IG Reel 1080p (1).mp4`.
2. **singmuaythai.com.au.** Live gym website. Shown as a live embed inside a
   browser frame, with a link out.
3. **The CornerHQ app.** Existing screenshot `images/dashboard-preview.png`.

No other proof ships. No placeholder projects, no anonymised case studies, no
invented numbers. Every figure on the page must be provable (runtime, aspect
ratio, tier counts, prices).

## 4. Page structure (one page, `index.html`)

Sections in order. Layout families must differ from section to section.

| # | Section | Layout | Content |
|---|---|---|---|
| 1 | Nav | fixed bar, 72px | Logo, Work, Services, The app, "Book a call" button. Dark over the hero, switches to light paper once the hero scrolls away (IntersectionObserver, no scroll listener). |
| 2 | Hero | full viewport, dark, triptych | Centre panel: muted looping 720p clip of the reel. Side panels: two stills from the reel at reduced opacity. Bottom-left: headline, subtext, "Book a call" + "See the work". Nothing else in the hero. |
| 3 | Opinion line | single paragraph on paper | "Most gym sites are a template with a logo dropped in. Most fight promos are phone footage with a beat under it. *We do the other thing.*" Gold italic on the last sentence. |
| 4 | The work | three pieces, hairline separated | Heading "The work" and one line: "Everything below is real, live and made by CornerHQ." Piece 1: text left, reel in a phone frame right, "Watch with sound" opens a lightbox with the full reel. Piece 2: live singmuaythai.com.au iframe in a browser frame left, text right, "Open the live site". Piece 3: full-width: text then the app screenshot in a browser frame. Under each: two or three real facts in mono. |
| 5 | Who it's for | two full-bleed dark image blocks | "Gyms" and "Fight promotions", each with one sentence and a "Book a call" link. Background stills from the reel. This is the only mid-page dark media block. |
| 6 | What we do | sticky heading left, list right | Heading "What we do", lead "Four things, done for one industry. Buy one or all of them." Four rows: Promo videos, Marketing, Websites, Apps. Each: title, one sentence, a 4:5 still from the reel. Hairlines between rows. |
| 7 | App pricing | tinted panel | "The gym app is priced by members, not features." One line of copy and the three tiers as a compact row of numbers: $0 up to 20 members, $150 up to 150, $300 unlimited. All tiers include every feature. Link to the enquiry form. |
| 8 | Book a call | dark band, image behind | Heading "Twenty minutes. No pitch deck." One line, then the enquiry form (section 5). |
| 9 | Footer | dark | Logo, email, "Sydney, Australia". |

Removed from the current site: the five feature cards, the app-only hero copy,
the three pricing cards, the two-step form.

## 5. Enquiry form

No calendar booking at launch. The form is the only contact path.

- Fields, in order: what do you run (radio pills: Gym, Fight promotion, Both),
  your name, business name, email, message (optional).
- Labels above inputs. No placeholder-as-label.
- Posts to Web3Forms with the existing access key
  `5406bfa5-c77e-400b-b2ca-8432e988be85`, delivering to the owner's Gmail.
- On success: inline confirmation, no navigation. Copy: "Got it. We'll reply
  within one business day to set up a time."
- On failure: inline error with the email address as fallback.
- Inputs, labels, placeholders and focus rings pass WCAG AA against the dark band.

## 6. Video handling

- **Hero and phone clip:** the reel from 1.5s to 31.5s, 720px wide, no audio,
  H.264, `faststart`, target about 1.2 MB. Autoplay, muted, loop, playsinline.
  Poster is a still from the reel so nothing flashes black.
- **Full reel:** the whole 73 seconds re-encoded to 1080p at roughly 8 MB, with
  audio, for the "Watch with sound" lightbox. Loaded only when opened.
- **Stills:** frames extracted from the reel with ffmpeg at 540px wide for the
  hero side panels, the "Who it's for" blocks, the service thumbnails and the
  closing band. Reuse the frames already in the mockup folder.
- All video and stills live in `images/` and `video/` in the repo. No external
  hosting.

## 7. Visual system

- **Theme:** light paper page. Dark surfaces appear only where media lives: the
  hero, the "Who it's for" blocks, and the single closing band (form + footer).
  No other section flips.
- **Palette:** paper `#F3F3F1`, raised paper `#E9E9E6`, ink `#1C1C1E`, muted ink
  `#6B6B70`, hairline `#D9D9D5`. Dark surfaces: `#0E0E10`, `#151517`, bone text
  `#EDE8DD`, muted bone `#9B968C`. Gold accent: `#B8891F` on paper, `#D4A83A`
  on dark. One accent, used identically everywhere.
- **Type:** Bricolage Grotesque for display and body (self-hosted, `font-display:
  swap`). JetBrains Mono for numbers and prices only. No Inter, no serif.
- **Radius:** 6px on buttons and thumbnails; 10px on browser frames; 28px on the
  phone frame. That is the documented rule.
- **Buttons:** "Book a call" is gold with dark text everywhere. Secondary
  "See the work" is a ghost button on the hero only.
- **Logo:** the current logo, with the "Gym Management Software" tagline
  cropped off, in two versions: white text for dark surfaces, charcoal text for
  the light nav. Gold ring unchanged.
- **Motion (dials: variance 8, motion 6, density 3):** hero copy rises on load;
  sections reveal with CSS scroll-driven animation (`animation-timeline: view()`,
  progressive enhancement); hover lifts on frames and buttons; nav colour switch.
  All gated behind `prefers-reduced-motion`. No animation libraries, no
  `window.addEventListener('scroll')`.
- **Responsive:** below 860px the triptych collapses to the video alone, all
  grids go single column, the sticky heading unsticks, the iframe shrinks to
  380px tall.

## 8. Rules carried from SubForge and the taste-skill

Locked. Do not re-litigate during implementation.

- Zero em or en dashes anywhere in visible copy. Hyphens only. A grep for
  `[—–]` over `index.html` must return nothing before every push.
- No eyebrow labels above headings. The small gold "Fighter promo / Gym website /
  Gym app" kind-labels on the work pieces are the single exception and there are
  no others on the page.
- No three-equal-card rows. No "Step 1/2/3". No scroll cues. No decorative dots.
  No middle-dot separator chains. No pills overlaid on images.
- No fake screenshots, no invented stats, no placeholder case studies.
- One CTA label per intent: "Book a call" is the contact CTA everywhere.
  "See the work" is the only secondary intent.
- Copy voice: blunt, short sentences, no neat triplets, no filler verbs.
- Design Read for the record: services and portfolio landing for combat sports
  gym owners and fight promoters, cinematic video-led language, native CSS with a
  strong sans display and restrained scroll motion, light paper with dark media.

## 9. Tech stack

- Plain HTML, CSS and vanilla JavaScript in one `index.html`, as today. No build
  step, no framework.
- Hosting stays on Vercel, auto-deploy on push to `main` of
  `github.com/ttd909/CornerHQWeb`. No DNS changes.
- Fonts self-hosted in `fonts/` (woff2), not linked from Google in production.
- Form backend stays Web3Forms.
- JavaScript budget: nav switch, lightbox open/close, form submit and
  confirmation, reduced-motion respect. Nothing else.
- Add `.superpowers/` to `.gitignore`.

## 10. Error handling and edge cases

- Video fails to load or autoplay is blocked: the poster still shows, the hero
  still reads. No spinner.
- singmuaythai.com.au iframe blocked or offline: the browser frame shows a static
  screenshot fallback (`images/sing-site.png`, captured during the build) with
  the link out still present.
- Form: client-side required-field check, server error surfaced inline, email
  address always visible as a fallback.
- Lightbox: closes on Escape, on backdrop click and on a close button; pauses the
  video when closed.
- Reduced motion: no autoplay looping in the hero (show the poster), no reveals,
  no hover transforms.

## 11. Out of scope

- Calendar booking (Cal.com). Revisit once the owner has an account.
- Separate pages for services, pricing or case studies. One page at launch.
- Blog, CMS, analytics changes.
- New logo design. The crop is a stopgap; a proper two-version logo file is a
  later task.
- Additional case studies. Add them as real work ships, with client OK.
