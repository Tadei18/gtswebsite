# GTS Risk Advisory — Claude Code Build Brief

You are building a complete, production-ready marketing website for **GTS Risk Advisory**, a premier security and risk consulting firm headquartered in Nairobi, serving clients across Kenya, East Africa, and the broader African continent.

This is a from-scratch build. Do not pull from any prior version of the site. Use only the specifications below.

---

## 1. NON-NEGOTIABLE CONSTRAINTS

- **Stack:** Plain HTML5, modern CSS3 (custom properties, grid, flexbox, clamp), and vanilla JavaScript (ES2020+). **No frameworks, no build step, no bundlers, no npm.** The site must run by simply uploading the folder to a cPanel `public_html` directory.
- **Asset strategy:** All assets local-first. Fonts via Google Fonts CDN link. Icons inline SVG (no icon libraries). Images: use placeholders from `https://picsum.photos/` keyed by seed for now (e.g. `https://picsum.photos/seed/gts-hero/1920/1080`) so the client can swap them later.
- **No external JS dependencies** except (optionally) a single CDN script for markdown rendering on the blog (`marked.min.js`) if you choose the markdown route.
- **Browser support:** Latest two versions of Chrome, Safari, Firefox, Edge. Mobile-first responsive (test at 360px, 768px, 1024px, 1440px).
- **Performance budget:** First page paint < 2s on 3G simulation. Lazy-load all below-the-fold images. No layout shift.
- **Accessibility:** WCAG 2.1 AA. Semantic landmarks, skip link, focus rings, alt text, aria-labels on icon buttons, color contrast checked.

---

## 2. BRAND POSITIONING

**Name:** GTS Risk Advisory
**Tagline (use prominently):** *Intelligence-Driven Security. Operational Resilience. Trusted Across Africa.*
**One-liner:** A premier security and risk consulting firm delivering tailored protection, risk intelligence, and operational resilience across Kenya, East Africa, and the African continent.
**Tone of voice:** Authoritative, calm, precise, discreet. Never alarmist. The voice of a senior advisor — confident, measured, evidence-based. Think *Control Risks* meets *Stratfor* meets a Nairobi-based partner who actually understands the ground.

---

## 3. DESIGN SYSTEM — "INTELLIGENCE DOSSIER"

The aesthetic is **dark, premium, intelligence-driven** — a classified-dossier feel, executed with restraint. No gimmicks (no fake redactions, no spinning radar gifs). The luxury is in the typography, spacing, and craft of the details.

### 3.1 Color Tokens (define as CSS custom properties on `:root`)

```css
:root {
  /* Surfaces */
  --color-bg:           #0A0E1A;   /* deep midnight, primary background */
  --color-surface-1:    #0F1524;   /* slightly raised */
  --color-surface-2:    #161E33;   /* cards, modals */
  --color-surface-3:    #1E2842;   /* hover states */

  /* Lines & borders */
  --color-border:       #232E4A;
  --color-border-strong:#3A4970;

  /* Ink */
  --color-ink-high:     #F4F1E8;   /* headlines, primary text — warm off-white */
  --color-ink-mid:      #B8C0D4;   /* body text */
  --color-ink-low:      #6B7593;   /* labels, captions, meta */
  --color-ink-faint:    #404B6B;   /* dividers in dark sections */

  /* Accent — Gold (used sparingly: CTAs, key numbers, active states only) */
  --color-gold:         #C9A961;
  --color-gold-bright:  #E0BE74;
  --color-gold-deep:    #8C7333;

  /* Status (for the Risk Heat Map) */
  --risk-low:           #4A7C59;   /* muted forest */
  --risk-moderate:      #C9A961;   /* gold */
  --risk-elevated:      #D17B3F;   /* burnt amber */
  --risk-high:          #B54533;   /* deep red */
  --risk-extreme:       #7A1F1F;   /* ox-blood */
  --risk-na:            #2A3554;   /* no data */

  /* Spacing scale (8pt grid) */
  --s-1: 4px;  --s-2: 8px;  --s-3: 12px; --s-4: 16px;
  --s-5: 24px; --s-6: 32px; --s-7: 48px; --s-8: 64px;
  --s-9: 96px; --s-10: 128px; --s-11: 160px;

  /* Type scale (fluid) */
  --t-display:  clamp(2.75rem, 5.5vw, 5rem);
  --t-h1:       clamp(2.25rem, 4vw, 3.5rem);
  --t-h2:       clamp(1.75rem, 3vw, 2.5rem);
  --t-h3:       clamp(1.35rem, 2vw, 1.75rem);
  --t-h4:       1.125rem;
  --t-body:     1rem;
  --t-small:    0.875rem;
  --t-xs:       0.75rem;
  --t-eyebrow:  0.6875rem;  /* uppercase labels */

  /* Radii */
  --r-sm: 2px; --r-md: 4px; --r-lg: 8px; --r-xl: 12px;

  /* Motion */
  --ease-out:  cubic-bezier(0.22, 1, 0.36, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --d-fast: 180ms; --d-med: 320ms; --d-slow: 560ms;

  /* Layout */
  --container-max: 1280px;
  --container-narrow: 880px;
  --container-wide: 1440px;
}
```

### 3.2 Typography

- **Display & headings:** `"Fraunces", "Playfair Display", Georgia, serif` — high contrast serif, gives the dossier/editorial weight. Use weights 400 and 600 only. Tight tracking (`letter-spacing: -0.02em`) on display sizes.
- **Body & UI:** `"Inter", "Helvetica Neue", system-ui, sans-serif` — weights 400, 500, 600. Body line-height 1.65.
- **Eyebrow labels (above headings):** Inter, 600 weight, `letter-spacing: 0.16em`, `text-transform: uppercase`, sized at `--t-eyebrow`, color `--color-gold`. These are the dossier-style section markers — use them generously above hero headlines and section titles.
- **Numeric / data:** `"JetBrains Mono", "SF Mono", monospace` for statistics, coordinates, classification stamps.

Load all three via a single Google Fonts link in `<head>`. Use `display=swap`.

### 3.3 Signature Visual Motifs

These are the things that make the site feel like an intelligence dossier rather than a generic dark-themed corporate site. Use them with restraint:

1. **Eyebrow labels everywhere.** Format: `— 001 / CORPORATE SECURITY` or `— REGION: EAST AFRICA`. Small gold uppercase, prefixed with an em-dash and a 3-digit zero-padded counter where appropriate (sections, services).
2. **Hairline gold accent rules.** 1px gold lines under section eyebrows, as section dividers, framing key callouts. Never thicker than 1px.
3. **Background grid texture.** A faint topographic-line SVG or 1px dotted grid on the body background at 3-5% opacity. Generate with CSS:
   ```css
   background-image:
     radial-gradient(circle, rgba(201,169,97,0.04) 1px, transparent 1px);
   background-size: 32px 32px;
   ```
4. **Coordinate-style metadata.** Footer and contact areas display Nairobi coordinates: `-1.2921° S, 36.8219° E` in JetBrains Mono.
5. **Stamp-style accents** for testimonials/credentials: thin gold border, monospace label inside, slightly off-axis (rotate -1.5deg). Use once per page maximum.
6. **Crosshair/corner brackets** on featured images and key cards: 12px L-shaped gold brackets at the four corners (pure CSS via `::before`/`::after`).
7. **Counter-up animations** on statistics when they scroll into view.
8. **Diagonal scroll-reveal:** Sections fade-in-and-rise on intersection (`translateY(24px) → 0`, opacity 0 → 1, 600ms staggered).

### 3.4 Component Patterns

- **Buttons:**
  - *Primary:* solid gold background, midnight text, 1px gold border. Hover: brightens to `--color-gold-bright`, subtle 2px Y-lift, gold glow shadow.
  - *Secondary:* transparent, 1px gold border, gold text. Hover: gold background, midnight text.
  - *Ghost:* no border, gold text with arrow `→` that translates right on hover.
  - All buttons: 14px vertical / 28px horizontal padding, `--t-small` weight 600, uppercase, 0.08em tracking, `--r-sm` radius.
- **Cards:** `--color-surface-2` background, 1px `--color-border` rule, hover lifts the border to `--color-border-strong` and reveals a 1px gold top accent. No drop shadows in dark mode — use borders and surface elevation instead.
- **Service tiles:** Square or 4:5 cards. Numbered eyebrow (`— 003 / FRAUD & SECURITY TRAINING`), serif h3 title, body summary, gold "Read more →" link at bottom. Hover: tile background lifts to `--color-surface-3`, gold corner bracket flashes in top-right.
- **Section headers:** Always include an eyebrow + serif headline + 60-character lede + optional gold hairline below. Center-aligned in hero sections, left-aligned for content sections.
- **Forms:** Dark inputs (`--color-surface-1` bg, 1px `--color-border` underline only — no full border). Floating labels in `--color-ink-low` that slide up and shrink to `--t-eyebrow` size on focus, turning gold. Focus state: gold underline expands left-to-right.

---

## 4. SITEMAP

```
/                              Home
/about/                        About Us
/services/                     Services index
/services/corporate-security/
/services/risk-management/
/services/fraud-security-training/
/services/forensic-investigations/
/services/supply-chain-security/
/services/executive-protection/
/services/events-security/
/services/manned-guarding/
/services/residential-security/
/services/command-centre/
/services/reception-security/
/services/security-systems/
/consulting/                   Consulting index
/consulting/security-risk-assessments/
/consulting/business-process-audits/
/consulting/travel-security/
/consulting/safety-evacuation/
/consulting/market-entry/
/consulting/mergers-acquisitions/
/consulting/embedded-consultancy/
/consulting/tailored-investigations/
/consulting/capacity-building/
/consulting/policy-sops/
/consulting/vetting-due-diligence/
/industries/                   Industries served
/intelligence/                 Intelligence Advisory Center (with embedded Risk Heat Map)
/intelligence/heat-map/        Standalone heat map page (full screen)
/insights/                     Blog / Insights index
/insights/[slug]/              Individual posts
/careers/                      Careers + job search
/media/                        Media / Gallery
/contact/                      Contact + Get a Quote
404.html
```

Each service / consulting detail page follows the same template (see §6.4).

---

## 5. PAGE-BY-PAGE SPECIFICATIONS

### 5.1 Global Chrome (Header & Footer)

**Header** (sticky, with backdrop-blur on scroll):
- Logo on the left (use a temporary SVG wordmark: `GTS` in Fraunces serif 600, followed by a thin gold vertical rule and `RISK ADVISORY` in Inter uppercase letter-spaced).
- Primary nav center/right: About, Services ▾, Consulting ▾, Industries, Intelligence, Insights, Careers, Media, Contact.
- Dropdowns are mega-menu style: dark surface, two columns listing all services / consulting offerings with one-line descriptions, plus a gold-accented "View all services →" CTA on the right.
- Far right: `GET A QUOTE` primary button.
- Mobile: hamburger opens a full-screen overlay nav (slide from right), with accordions for Services and Consulting.

**Pre-header strip** (16px tall, faint):
- Left: `— OPERATING ACROSS 12+ AFRICAN MARKETS` in eyebrow style.
- Right: `info@gtsriskadvisory.com  ·  +254 XXX XXX XXX` (use placeholder) + social icons (WhatsApp, LinkedIn, X, Instagram, Facebook).

**Footer** (4-column on desktop, stacked on mobile):
- Col 1: Logo + 80-char positioning statement + Nairobi coordinates + social icons.
- Col 2: Services (links to top 6 services + "View all").
- Col 3: Consulting (links to top 6 + "View all").
- Col 4: Company (About, Industries, Intelligence, Insights, Careers, Media, Contact) + Newsletter signup (email field, gold submit arrow).
- Bottom bar (after a 1px gold hairline): © 2026 GTS Risk Advisory. All rights reserved. · Privacy · Terms · Sitemap · Built with discretion.

### 5.2 Home Page

**Section 1 — Hero (full viewport min-height: 92vh):**
- Background: a dark, high-quality cinematic image (use `https://picsum.photos/seed/gts-hero-africa/1920/1200`) with a heavy navy-to-black gradient overlay (`linear-gradient(180deg, rgba(10,14,26,0.6) 0%, rgba(10,14,26,0.95) 100%)`).
- Eyebrow (centered, top): `— INTELLIGENCE  ·  RESILIENCE  ·  PROTECTION`
- Display headline (serif, Fraunces 600, --t-display): **"Smarter Security for a Changing Africa."**
- Lede (max-width 640px, --color-ink-mid): "We deliver intelligence-driven security solutions, risk consulting, and operational resilience services to corporations, governments, and individuals operating across the continent."
- CTA pair: `EXPLORE OUR SERVICES` (primary gold) + `REQUEST A BRIEFING →` (ghost).
- Bottom of hero: a 3-column metric strip — `12+ MARKETS COVERED` · `200+ ENGAGEMENTS` · `24/7 INTELLIGENCE DESK` (use animated count-ups on scroll into view).

**Section 2 — Capability Pillars (4 columns):**
- Eyebrow: `— 01 / CAPABILITIES`
- H2: "Four pillars of practice."
- Four cards with a small inline SVG icon (custom-drawn, 1.5px stroke, gold), title, 2-line description, and `→` link:
  1. **Corporate Security** — Tailored security strategies and integrated protection frameworks.
  2. **Risk Consulting** — Independent assessments, audits, and advisory.
  3. **Executive Services** — Discreet personal and travel protection.
  4. **Intelligence Advisory** — Country risk, daily briefs, and the GTS Risk Heat Map.

**Section 3 — Featured Service: Intelligence Advisory (split layout):**
- Left (40%): Mini interactive Africa preview — a teaser SVG of the continent with a few countries colored by risk level, hover to highlight, CTA `OPEN THE RISK HEAT MAP →` links to `/intelligence/heat-map/`.
- Right (60%): Eyebrow `— FEATURED PRACTICE`, h2 "Decisions are only as good as the intelligence behind them.", body copy from PDF (Customized Intelligence Reports paragraph), bullet list of intelligence products (Country Risk Analysis, Daily Monitoring Briefs, Situational Risk Analysis, Risk Heat Map).

**Section 4 — Industries We Serve (logo-grid style):**
- Eyebrow: `— 02 / INDUSTRIES`
- H2: "Trusted across sectors."
- Grid of 10 industry tiles (3 cols desktop, 2 mobile): Commercial Banks, Manufacturing, Insurance, NGOs, Agriculture, Hospitality & Retail, Investment Firms, Education, Parastatals, County Governments. Each tile: small line-icon, name, hover lifts surface and reveals a one-line use case in gold.

**Section 5 — How We Engage (process timeline):**
- Eyebrow: `— 03 / METHODOLOGY`
- H2: "A disciplined, evidence-based engagement model."
- Horizontal 4-step timeline (vertical on mobile): **01 Listen** → **02 Assess** → **03 Design** → **04 Deliver & Sustain**. Each step has a numbered monospace label, h4 title, and 2-line description. Connect with a 1px gold hairline that animates left-to-right on scroll.

**Section 6 — Insights teaser (3-card grid):**
- Eyebrow: `— 04 / INTELLIGENCE BRIEFS`
- H2: "From the desk."
- Three latest blog posts pulled from `posts.json`. Each card shows category eyebrow, date in mono, h3 title, 2-line excerpt, `READ →`.
- CTA below grid: `ALL INSIGHTS →`.

**Section 7 — CTA Band (full-bleed, gold-bordered):**
- Background: `--color-surface-1`, with thin gold rules top and bottom.
- Centered: eyebrow `— READY TO ENGAGE?`, h2 "Let's design your security posture.", supporting line, two buttons (`REQUEST A QUOTE` primary, `BOOK A CONSULTATION` secondary).

### 5.3 About Page

- Hero: eyebrow `— ABOUT GTS`, h1 **"A partner in safer tomorrows."**, lede pulled from the PDF About Us text.
- Section: **Who We Serve** — the "diverse clientele" paragraph from the PDF, rendered as flowing editorial copy in a narrow column (`--container-narrow`).
- Section: **Vision** & **Mission** — two-card split layout. Each card has eyebrow, big serif statement, 1px gold rule, supporting microcopy.
- Section: **Our Values** — 4 columns (Innovation, Client Focus, Integrity, Excellence) using the exact body copy from the PDF. Each in a card with a custom line-icon at top.
- Section: **Leadership** — placeholder grid of 4 portraits with name, title, short bio. Use `https://picsum.photos/seed/exec-1/600/800` etc. with grayscale + slight gold tint via CSS filter.
- Section: **Operating Footprint** — Africa SVG map with operating countries highlighted in gold dots, country list below in 3 columns.
- CTA band identical to home section 7.

### 5.4 Services Index & Detail Pages

**Services Index (`/services/`):**
- Hero: eyebrow `— SERVICES & PRODUCTS`, h1 "Integrated protection for an interconnected risk landscape.", lede.
- Grid: 12 service cards (numbered 01-12), 3 cols on desktop, each linking to the detail page. Card composition described in §3.4.

**Service Detail Template (used for all 12 service pages):**

Each service page has the same structure. Pull copy directly from the PDF for each.

1. **Hero** — full-bleed thematic image (use seeded picsum), eyebrow with service number (`— 03 / FRAUD & SECURITY TRAINING`), h1 service name, lede (first paragraph from PDF), two CTAs (`REQUEST A QUOTE`, `DOWNLOAD CAPABILITY BRIEF →` placeholder link).
2. **Overview** — narrow-column editorial copy, the full descriptive paragraphs from the PDF.
3. **Key Areas of Coverage** — 2-column bulleted grid with a gold check-bracket icon next to each item. Use the exact lists from the PDF.
4. **Why GTS** — 3-card row with bespoke value propositions for this service (Claude Code: synthesize 3 short props per service in the GTS voice, ≤14 words each, derived from the PDF content).
5. **Engagement Model** — short 3-step list specific to the service.
6. **Related Services** — 3 cards linking to other relevant services in the suite.
7. **CTA band.**

Apply this template to all 12 services and all 11 consulting offerings (23 detail pages total). Copy lives in a single `data/services.json` and `data/consulting.json` file, and each detail page reads from that — single template HTML file per category, or static HTML per page rendered from the data. Use **static HTML per page** (simpler for cPanel, better SEO) but generate them from the JSON via a small Node script that the user can run once locally, OR (preferred) just hand-write each HTML page using the JSON as your source of truth so the deliverable is purely static and zero-build.

**Recommendation:** Write each detail page as a standalone HTML file but extract repeated layout into included partials via a tiny inline JS include pattern (`<div data-include="/partials/header.html"></div>` with a fetch-and-inject script in `main.js`). This gives single-source headers/footers without a build step.

### 5.5 Consulting Index & Detail Pages

Mirror Services structure. Index page eyebrow `— CUSTOMIZED CONSULTING`, h1 "Independent counsel. Decisive insight.", lede.

### 5.6 Industries Page

- Hero: eyebrow `— INDUSTRIES`, h1 "Sector-specific security and risk expertise."
- 10 industry sections, each with: industry name (h2), 2-paragraph synthesized copy (Claude Code writes these in voice — security challenges + GTS approach for each sector, ~120 words each, drawing on the PDF), 3-bullet list of typical engagements, related services chips.
- Industries: Commercial Banks, Manufacturing, Insurance, NGOs, Agriculture, Malls/Residential/Hotels, Investment Firms, Universities & Schools, Parastatals, County Governments.

### 5.7 Intelligence Advisory Center

- Hero: eyebrow `— INTELLIGENCE ADVISORY`, h1 **"Foresight. Verified. Delivered."**, lede.
- 5 product sections (one per intelligence product from PDF: Customized Intelligence Reports, Political & Country Risk Analysis, Daily Monitoring Briefs, Situational Risk Analysis, Risk Heat Map). Each section: eyebrow with number, h2, full PDF copy, mock product preview on the right (PDF cover thumbnail, dashboard screenshot, etc. — use seeded picsum with overlay styling).
- **Embedded Risk Heat Map** preview (smaller version) at the bottom of the Risk Heat Map section, with CTA to open the full-screen experience.
- Pricing / subscription teaser: 3 tiers (`STANDARD` / `CORPORATE` / `EXECUTIVE`) with feature lists. Pricing shown as `ON REQUEST`. CTA to contact.

### 5.8 Risk Heat Map (`/intelligence/heat-map/`)  — INTERACTIVE FEATURE #1

A standalone full-screen experience.

- Header (slim, dark): logo, breadcrumb, share button.
- Sub-header bar: title `AFRICA RISK HEAT MAP — Q2 2026 EDITION`, last-updated timestamp in mono, 5 risk-level legend chips (Low / Moderate / Elevated / High / Extreme) using the `--risk-*` tokens.
- **Main canvas (60% width on desktop):** Inline SVG of the African continent, country borders as separate `<path>` elements with `data-iso` and `data-risk` attributes. Use the public-domain Natural Earth simplified Africa GeoJSON converted to inline SVG (Claude Code: generate or include this — if you cannot produce accurate country shapes, render a simplified geometric tile-grid map of African countries instead, with each tile labeled by ISO code).
  - Each country fills with the appropriate `--risk-*` color based on its `data-risk` attribute (`low|moderate|elevated|high|extreme|na`).
  - Hover: country gets a 1.5px gold stroke, cursor pointer, tooltip appears near cursor showing country name, ISO, risk level, and a 1-line summary.
  - Click: opens a slide-in panel from the right showing the country dossier (see right panel below).
- **Right panel (40%):** Country dossier panel — closed by default with a quiet prompt "Select a country to view dossier." When open:
  - Eyebrow with ISO code: `— KEN  ·  EAST AFRICA`
  - h2: Country name
  - Large risk chip with color + label
  - 4 score bars (out of 5): Security, Political, Economic, Operational — each animated to fill on open.
  - Tabs: `OVERVIEW` · `KEY RISKS` · `OUTLOOK` · `RECOMMENDATIONS` — short paragraphs in each tab (Claude Code: write plausible, neutral, non-defamatory placeholder content for ~10 representative African countries; remaining countries say "Detailed dossier available to subscribers — contact us").
  - Bottom: `REQUEST FULL COUNTRY REPORT →` CTA.
- **Top-right tools strip:** filter dropdown by risk level (multi-select), search input, region toggle (East / West / Southern / Central / North).
- **Mobile:** Map becomes a vertical scrolling list of country cards grouped by region, each color-coded. The right-panel becomes a bottom-sheet that slides up on tap.

Data lives in `data/heat-map.json` with this shape:
```json
{
  "edition": "Q2 2026",
  "updated": "2026-04-15",
  "countries": [
    {
      "iso": "KEN",
      "name": "Kenya",
      "region": "East Africa",
      "risk": "moderate",
      "scores": { "security": 3, "political": 3, "economic": 3, "operational": 3 },
      "summary": "Stable operating environment with localized concerns.",
      "overview": "…",
      "key_risks": ["…", "…"],
      "outlook": "…",
      "recommendations": ["…", "…"]
    }
  ]
}
```

Populate ~12 African countries with full content; remainder with `risk` level + 1-line `summary` only.

### 5.9 Insights / Blog (`/insights/`)  — CMS-READY FEATURE #2

**Architecture (cPanel-friendly, zero-build):**

```
/insights/
  index.html                  ← listing page, reads posts.json
  /posts/
    2026-05-east-africa-elections-outlook.html
    2026-04-supply-chain-risk-q1.html
    …
/data/
  posts.json                  ← manifest of all posts
/admin/
  README.md                   ← editing guide for the client
  template-post.html          ← copy-this-and-fill-in template
```

**`posts.json` schema:**
```json
{
  "posts": [
    {
      "slug": "east-africa-elections-outlook-2026",
      "title": "East Africa Elections Outlook 2026",
      "excerpt": "Three elections that will reshape the regional risk landscape.",
      "category": "Political Risk",
      "author": "GTS Intelligence Desk",
      "date": "2026-05-12",
      "read_time": "8 min",
      "cover": "/insights/assets/east-africa-elections.jpg",
      "file": "/insights/posts/east-africa-elections-outlook-2026.html",
      "featured": true,
      "tags": ["elections", "east-africa", "political-risk"]
    }
  ]
}
```

**Listing page (`/insights/index.html`):**
- Hero: eyebrow `— INSIGHTS`, h1 "From the GTS Intelligence Desk.", lede, search input + category filter chips.
- Featured post: large editorial card spanning two columns.
- Grid: remaining posts as cards (3 cols desktop), with category eyebrow, date in mono, h3 title, excerpt, read-time, `READ →`.
- Pagination or infinite-scroll (use Intersection Observer to lazy-load 9 at a time from `posts.json`).
- Sidebar (or below grid on mobile): Categories list, Tags cloud, Newsletter signup card.

**Individual post pages:**
- Use one standalone HTML file per post under `/insights/posts/<slug>.html` (full HTML, not markdown — easier for the client to copy/edit/upload).
- Template: full-width hero image with title overlay, narrow editorial column (`--container-narrow`), Fraunces serif for headings, drop-cap on first paragraph, pull-quote component, image-with-caption component, related-posts (3 cards) at the bottom, share buttons.
- Author byline with avatar circle, name, role, date in mono.

**Author UX (client-side editing):**
- Provide 3 starter posts already written and styled, with rich, on-brand placeholder content (~600 words each) demonstrating: a political risk briefing, a fraud awareness piece, a security technology trend piece.
- Provide `/admin/README.md` explaining how to:
  1. Copy `/admin/template-post.html` to `/insights/posts/<slug>.html`
  2. Edit the title, body, cover image
  3. Add a new entry to `/data/posts.json`
  4. Upload via cPanel File Manager

(Optional alternative the brief mentions but you should NOT implement unless asked: **Decap CMS** integration for git-based editing. The JSON approach is the primary deliverable.)

### 5.10 Careers Page

- Hero: eyebrow `— CAREERS`, h1 "Build a career in security and intelligence.", lede.
- Why GTS: 3-card row.
- Open positions: searchable/filterable list rendered from `/data/jobs.json` (department, location, type filters). 3 placeholder jobs (e.g. Security Operations Analyst, Senior Risk Consultant, Intelligence Researcher).
- Job detail modal/page with description, responsibilities, requirements, "Apply Now" form (name, email, phone, position, cover note, CV upload — form posts to FormSubmit, see §6.3).
- General application CTA at the bottom.

### 5.11 Media / Gallery Page

- Hero: eyebrow `— MEDIA`, h1 "In the field, on the record.", lede.
- Filter tabs: All · Events · Operations · Training · Press.
- Masonry grid of images with overlay captions on hover (use seeded picsum placeholders).
- Lightbox on click (vanilla JS).
- Press section: list of press mentions with publication logo, headline, date, external link.

### 5.12 Contact Page  — FORMS FEATURE #3

- Hero: eyebrow `— CONTACT`, h1 "Discreet by default. Responsive by design.", lede.
- Two-column layout:
  - **Left:** Contact information block (email, phone, WhatsApp, address in Nairobi, hours), Nairobi coordinates in mono, an embedded Google Maps iframe styled with a dark-mode overlay.
  - **Right:** Two stacked forms in a tabbed component:
    - **Tab 1 — General Enquiry:** Name, Company, Email, Phone, Message.
    - **Tab 2 — Request a Quote:** Name, Company, Email, Phone, Service Interest (dropdown — all 23 service/consulting items), Project Scope, Budget Range (optional), Timeline, Brief Description.
- Form handling: post to **FormSubmit.co** (no backend setup needed — works on plain cPanel hosting). Use `https://formsubmit.co/info@gtsriskadvisory.com` as the action. Include a honeypot field and the FormSubmit `_captcha`, `_template`, `_next` (redirect to `/contact/thank-you.html`), and `_subject` fields. Build a `thank-you.html` confirmation page with a quiet success state.
- Below forms: 3-card row of FAQs (How quickly do you respond? What information should I include? Do you sign NDAs? — yes, by default).

### 5.13 404 Page

- Dossier-themed: eyebrow `— STATUS: 404`, h1 "This file appears to be classified — or missing.", lede with a touch of dry wit, `RETURN TO BASE →` button.

---

## 6. TECHNICAL IMPLEMENTATION DETAILS

### 6.1 File Structure

```
/
├── index.html
├── about/index.html
├── services/
│   ├── index.html
│   ├── corporate-security/index.html
│   └── …(all 12)
├── consulting/
│   ├── index.html
│   └── …(all 11)
├── industries/index.html
├── intelligence/
│   ├── index.html
│   └── heat-map/index.html
├── insights/
│   ├── index.html
│   ├── posts/
│   │   ├── east-africa-elections-outlook-2026.html
│   │   ├── …
│   └── assets/
├── careers/index.html
├── media/index.html
├── contact/
│   ├── index.html
│   └── thank-you.html
├── 404.html
├── partials/
│   ├── header.html
│   ├── footer.html
│   ├── pre-header.html
│   └── cta-band.html
├── assets/
│   ├── css/
│   │   ├── base.css           (resets, variables, typography)
│   │   ├── components.css     (buttons, cards, forms, nav)
│   │   ├── layout.css         (grid, containers, spacing)
│   │   ├── pages.css          (page-specific overrides)
│   │   └── main.css           (single import-only file)
│   ├── js/
│   │   ├── main.js            (includes loader, nav, scroll, counters)
│   │   ├── heat-map.js        (map rendering + interactions)
│   │   ├── insights.js        (blog listing + filter + lazy-load)
│   │   ├── careers.js         (job filter + application form)
│   │   └── forms.js           (validation, submission)
│   ├── img/                   (replace placeholders here later)
│   ├── icons/                 (inline SVG source files)
│   └── fonts/                 (if self-hosting; otherwise Google Fonts link)
├── data/
│   ├── services.json
│   ├── consulting.json
│   ├── industries.json
│   ├── heat-map.json
│   ├── posts.json
│   └── jobs.json
├── admin/
│   ├── README.md
│   └── template-post.html
├── robots.txt
├── sitemap.xml
├── favicon.svg
└── README.md                  (handover doc)
```

### 6.2 Reusable Partials Loader

Tiny vanilla JS pattern in `main.js`:

```js
async function loadPartials() {
  const slots = document.querySelectorAll('[data-include]');
  for (const slot of slots) {
    const url = slot.getAttribute('data-include');
    const res = await fetch(url);
    slot.innerHTML = await res.text();
  }
  document.dispatchEvent(new CustomEvent('partials:loaded'));
}
document.addEventListener('DOMContentLoaded', loadPartials);
```

Wire the mobile nav, dropdowns, and any header-bound listeners inside the `partials:loaded` event so they bind after injection.

### 6.3 Form Handling

Use **FormSubmit.co** — no server needed, works on cPanel static hosting. Form markup:

```html
<form action="https://formsubmit.co/info@gtsriskadvisory.com" method="POST" class="form form--quote">
  <input type="hidden" name="_subject" value="New Quote Request — GTS Website">
  <input type="hidden" name="_next" value="https://gtsriskadvisory.com/contact/thank-you.html">
  <input type="hidden" name="_captcha" value="true">
  <input type="text" name="_honey" style="display:none">
  <!-- visible fields -->
</form>
```

Add client-side validation in `forms.js` (required fields, email regex, friendly inline errors styled with `--risk-elevated` color and a 1px underline accent).

### 6.4 Interactive Behaviors

- **Sticky header** with `position: sticky; top: 0;` and a class toggled by IntersectionObserver on a sentinel at top of page that adds `backdrop-filter: blur(12px)` and a `--color-bg/85` background.
- **Smooth scroll** for in-page anchors (`scroll-behavior: smooth` on `html`).
- **Reveal-on-scroll** with IntersectionObserver, threshold 0.15, adding `.is-in-view` class. CSS handles the fade + Y translation.
- **Number counter** for hero metrics: parse `data-target="200"` attribute, animate from 0 to target over 1600ms with `--ease-out`. Trigger when element enters view.
- **Mobile nav:** full-screen overlay, slides from right (`translateX(100%) → 0`), 320ms `--ease-out`. Lock body scroll while open. Trap focus.
- **Dropdown menus** (desktop): open on hover with 80ms delay, close on mouse-leave with 120ms delay. On focus, keyboard-navigable.
- **Heat map interactions:** all described in §5.8. Use plain SVG + event delegation on the SVG root for hover/click. Tooltip is an absolutely-positioned div, follows the mouse with `requestAnimationFrame`.
- **Lightbox** (media page): vanilla JS, ESC to close, arrow keys to navigate, focus trap.

### 6.5 SEO & Meta

For every page:
- Unique `<title>` (≤60 chars) and `<meta name="description">` (≤155 chars).
- Open Graph + Twitter card tags (use a default `og-image.jpg` placeholder, 1200x630, dark with gold logo).
- Canonical URL.
- JSON-LD structured data: `Organization` on home, `Service` on each service page, `Article` on each post, `JobPosting` on each careers role, `BreadcrumbList` site-wide.
- `robots.txt` allowing all, sitemap URL.
- `sitemap.xml` listing all pages.

### 6.6 Performance

- Defer non-critical JS (`<script src="..." defer>`).
- Inline critical CSS for above-the-fold in `<head>` of the home page only.
- `loading="lazy"` and `decoding="async"` on all `<img>` below the fold.
- Use `<picture>` with `<source>` for any large hero images, with WebP first and JPEG fallback (note this in the README for when the client adds real images).
- Preload the two display fonts.

### 6.7 Accessibility

- Skip link at top of every page (visually hidden until focused).
- Semantic landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`.
- All interactive elements keyboard-reachable; visible focus rings (gold, 2px offset).
- `aria-label` on all icon-only buttons.
- Color contrast: all body text against `--color-bg` and `--color-surface-*` passes WCAG AA. Test the gold-on-dark for at least AA (3:1 for large text, 4.5:1 for body — adjust to `--color-gold-bright` if needed for body text).
- `prefers-reduced-motion: reduce` → disable parallax, counters, and scroll reveals; instant transitions.

---

## 7. PLACEHOLDER CONTENT TO GENERATE

For each of the following, Claude Code must write the actual copy now (not "lorem ipsum"), in the GTS voice defined in §2:

1. **3 starter blog posts** (~600 words each), one each:
   - "East Africa Elections Outlook 2026" (Political Risk)
   - "Beyond the Perimeter: Rethinking Supply Chain Security in 2026" (Operational Risk)
   - "Behavioural Security Awareness: The Human Layer of Cyber Defence" (Awareness & Training)
2. **10 country dossiers** for the Heat Map (Kenya, Uganda, Tanzania, Rwanda, Ethiopia, Nigeria, Ghana, South Africa, Egypt, DRC) — each with overview, key risks, outlook, and recommendations. Neutral, factual, non-defamatory tone.
3. **3 leadership bios** (~80 words each) — fictional but credible: Managing Director, Head of Intelligence, Director of Operations.
4. **3 placeholder job postings** — Security Operations Analyst (Nairobi), Senior Risk Consultant (East Africa), Intelligence Researcher (Nairobi).
5. **All 23 service/consulting detail page bodies** — use the PDF copy verbatim where provided, then write the "Why GTS" 3-card props, the "Engagement Model" 3-step list, and the "Related Services" selections for each.
6. **10 industry sector descriptions** (~120 words each) for the Industries page.

---

## 8. SOURCE COPY — USE VERBATIM WHERE INDICATED

The following is the canonical copy from the client. Use it verbatim for all hero ledes, service descriptions, and value statements unless otherwise instructed.

### 8.1 About Us (verbatim)
> We are a premier security solutions provider specializing in delivering innovative, client-focused, and comprehensive risk management services. We offer unmatched expertise and tailored security strategies across Kenya, East Africa, and the broader African continent. Our approach is rooted in proactive risk assessment, advanced technology integration, and a deep understanding of the regional dynamics shaping security needs in Africa. We believe in making security smarter, more efficient, and more accessible. Whether you require comprehensive risk management for your business, tailored security solutions for special events, or proactive intelligence to mitigate threats, we are your partner in creating a safer tomorrow.
>
> We serve a diverse clientele, including corporations, government entities, non-governmental organizations, and private individuals. Our services cover various domains, from corporate security to personal protection, and from crisis management to advanced risk analytics. We are committed to enhancing safety and resilience in a rapidly evolving security landscape.

### 8.2 Vision (verbatim)
> To be the leading intelligence-driven security and risk consulting firm in Africa, recognized for delivering trusted advisory services, innovative risk solutions, highest standards of integrity and operational excellence.

### 8.3 Mission (verbatim)
> To deliver exceptional, innovative, and customized security and risk consulting services that empower our clients to operate confidently and securely in dynamic environments.

### 8.4 Values (verbatim — render each as a card)

**Innovation** — We continuously invest in advanced technologies, cutting-edge methodologies, and creative problem-solving approaches to stay ahead of emerging security challenges. By embracing innovation, we ensure that our solutions are not only effective but also adaptive to the ever-changing security landscape.

**Client Focus** — Our clients are at the heart of our operations. We take pride in delivering personalized, responsive, and reliable services that address each client's unique needs. Building long-term relationships based on trust and satisfaction is our top priority.

**Integrity** — We uphold the highest ethical standards in all our dealings. Transparency, honesty, and accountability are integral to our business, ensuring our clients can rely on us as a trusted partner in safeguarding their interests.

**Excellence** — We are committed to excellence in every aspect of our operations. From strategy development to service delivery, we strive for perfection and continuous improvement, ensuring we consistently exceed client expectations.

### 8.5 Service Descriptions

For each of the 12 services and 11 consulting offerings, copy the body paragraphs and "Key Areas of Coverage" lists from the provided PDF verbatim into `data/services.json` / `data/consulting.json` and render them on the respective detail pages. (PDF sections covered: Corporate Security Services, Risk Management Solutions, Fraud & Security Awareness Training, Corporate Forensic Investigations, Supply Chain Security Solutions, Executive Protection Services, Events Security Services, Manned Guarding Services, Residential Security Services, Command Centre Operations, Reception Security Services, Security Systems Design and Installations, Security Risk Assessments & Audits, Business Process Control Audits, Travel Security Risk Programs, Safety Evacuation Programs, Market Entry Assessments, Merger & Acquisition Risk Assessments, Embedded Consultancy Services, Tailored Investigations Services, Capacity Building Services, Policy & SOPs Designing & Formulation, Vetting & Due Diligence Services.)

### 8.6 Intelligence Products

For each of the 5 intelligence products (Customized Intelligence Reports, Political & Country Risk Analysis, Daily Monitoring Briefs, Situational Risk Analysis, Risk Heat Map), copy the descriptive paragraphs from the PDF verbatim.

### 8.7 Contact
- Email: `info@gtsriskadvisory.com`
- Phone: placeholder `+254 XXX XXX XXX` — leave as placeholder for client to fill in
- Address: placeholder `Nairobi, Kenya` — leave as placeholder for client to fill in
- Social: WhatsApp, Facebook, LinkedIn, X (Twitter), Instagram — use placeholder `#` hrefs

---

## 9. BUILD ORDER (execute in this sequence)

1. Scaffold the file structure in §6.1.
2. Build `assets/css/base.css` (tokens, reset, typography, body grid background).
3. Build `assets/css/components.css` (buttons, cards, forms, eyebrows, hairlines, corner brackets).
4. Build `assets/css/layout.css` (containers, grid utilities, section padding).
5. Build the `partials/` files (header, pre-header, footer, cta-band).
6. Build `assets/js/main.js` (partials loader, sticky header, mobile nav, reveals, counters).
7. Build the home page (`index.html`).
8. Build the `about/index.html` page.
9. Populate `data/services.json` and `data/consulting.json` from the PDF.
10. Build the services index + all 12 service detail pages.
11. Build the consulting index + all 11 consulting detail pages.
12. Build the industries page.
13. Populate `data/heat-map.json` with 10 detailed country dossiers + remaining countries with summary-only.
14. Build the intelligence index page + the standalone heat map page + `assets/js/heat-map.js`.
15. Populate `data/posts.json` and write the 3 starter blog posts.
16. Build the insights index + post template + 3 starter posts + `assets/js/insights.js`.
17. Populate `data/jobs.json` with 3 placeholder jobs.
18. Build the careers page + `assets/js/careers.js`.
19. Build the media/gallery page + lightbox.
20. Build the contact page + thank-you page + `assets/js/forms.js`.
21. Build the 404 page.
22. Add `robots.txt`, `sitemap.xml`, `favicon.svg`, `og-image.jpg` (placeholder).
23. Write `README.md` with deployment instructions for cPanel (FTP/File Manager upload, set FormSubmit recipient email, swap placeholder images, edit `posts.json` to publish new posts).
24. Write `admin/README.md` with the blog editing workflow.
25. Run a final QA pass: every link works, every page has unique meta tags, mobile layout tested at 360px and 768px, contrast passes AA, forms submit correctly to FormSubmit.

---

## 10. QUALITY BAR

The site must look like it cost USD 25,000+ from a senior boutique studio. Common AI-built-site giveaways to **actively avoid**:

- Generic stock-photo hero of "handshake / city skyline / man in suit pointing at hologram." Use moody, abstract, considered imagery (or solid surfaces with typographic hero treatments) until the client provides real photography.
- Vague rounded-everything cards floating on gradients. Our cards have hard edges, 1px borders, deliberate hierarchy.
- Centered-everything layouts. We use editorial asymmetry — narrow text columns offset against generous white (or in this case, dark) space.
- Three-icon "Why Choose Us" rows with smiley generic icons. Our value props are specific, sharp, and earn their place.
- "Lorem ipsum" or hand-wavy "engaging content here" placeholders. Every word on the live site is final copy.
- Bouncing, sliding, exploding hero text. Motion is restrained: fade + 24px rise, nothing more.

The right reference points (vibe, not direct copying):
- **Control Risks** — site structure and intelligence framing.
- **Stratfor / RANE** — country risk dashboard aesthetics.
- **Pinkerton** — heritage and gravitas.
- **Linear / Vercel** — dark UI craft and typographic discipline.

---

## 11. DELIVERABLES CHECKLIST

When you're done, the project root should contain a working static site that:

- [ ] Opens correctly when `index.html` is double-clicked OR served over any static file server.
- [ ] Has 50+ pages all linked and navigable, with no broken links.
- [ ] Has 23 service/consulting detail pages all populated with PDF copy.
- [ ] Has an interactive Africa Risk Heat Map with 10 fully-detailed country dossiers.
- [ ] Has 3 fully-written, on-brand blog posts and a working JSON-driven blog system.
- [ ] Has a working Contact form + Get a Quote form both posting to FormSubmit.
- [ ] Has a careers page with filterable jobs and an application form.
- [ ] Passes Lighthouse: 95+ Performance, 100 Accessibility, 100 Best Practices, 95+ SEO on the home page.
- [ ] Includes a clear `README.md` for the client covering deployment, content updates, and form configuration.

Begin.
