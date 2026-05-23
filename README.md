# GTS Risk Advisory — Website

Production-ready static marketing site for GTS Risk Advisory. Pure HTML, CSS, and vanilla JavaScript — no build step required to serve, no dependencies to install.

---

## Quick deploy to cPanel

1. Compress the entire project folder into a `.zip`.
2. In cPanel File Manager, navigate to `public_html/` (or the relevant document root).
3. Upload the `.zip` file.
4. Right-click the uploaded `.zip` → **Extract** → extract to the current folder.
5. Delete the now-empty `.zip` file.
6. The site is live at your domain.

**That's it.** No server-side setup, no Node/PHP requirements.

---

## What's in this repository

```
/
├── index.html                     ← Home
├── about/index.html
├── services/                      ← 12 service detail pages + index
├── consulting/                    ← 11 consulting detail pages + index
├── industries/                    ← Industries page (10 sectors)
├── intelligence/                  ← Intelligence Advisory + Risk Heat Map
├── insights/                      ← Blog index + 3 starter posts
├── careers/                       ← Careers + jobs
├── media/                         ← Gallery + press
├── contact/                       ← Contact + Get-a-Quote (FormSubmit)
├── 404.html
│
├── assets/
│   ├── css/                       ← base, components, layout, pages, main (entrypoint)
│   ├── js/                        ← main + page-specific (heat-map, insights, careers, forms, media)
│   ├── img/                       ← (empty) — drop client images here when supplied
│   ├── icons/                     ← (empty) — inline SVG used throughout
│   └── fonts/                     ← (empty) — currently using Google Fonts CDN
│
├── data/
│   ├── services.json              ← Source of truth for service pages
│   ├── consulting.json            ← Source of truth for consulting pages
│   ├── heat-map.json              ← 12 detailed country dossiers + ~40 summary entries
│   ├── posts.json                 ← Blog post manifest
│   └── jobs.json                  ← Open roles
│
├── partials/                      ← Reference snippets (chrome is inlined into pages)
├── admin/
│   ├── README.md                  ← Client-facing editor's guide (how to publish posts)
│   └── template-post.html         ← Template for new blog posts
│
├── robots.txt
├── sitemap.xml
├── favicon.svg
├── og-image.svg                   ← Social share card (convert to .jpg for best support)
│
├── BRIEF.md                       ← Original build brief
└── _assemble/                     ← Build tooling (Python). Optional — see below.
```

---

## Configuration before launch

### 1. Update contact details
**Search-and-replace across the project:**
- `+254 XXX XXX XXX` → real phone number
- `+254000000000` (in `tel:` links) → real phone number with country code
- `info@gtsriskadvisory.com` → confirm or replace the address (note: this is also the FormSubmit recipient — see below)
- `Nairobi, Kenya` → full street address (currently placeholder)

### 2. Activate FormSubmit (the contact and quote forms)
The forms POST to `https://formsubmit.co/info@gtsriskadvisory.com`. FormSubmit is free and requires no server setup.

**One-time activation:**
1. Submit the contact form on the live site once with a real email.
2. FormSubmit will send a confirmation email to `info@gtsriskadvisory.com`.
3. Click the confirmation link in that email — only needs to happen once.
4. From then on, all form submissions arrive at that inbox automatically.

To change the recipient address, search-and-replace `formsubmit.co/info@gtsriskadvisory.com` across the codebase.

### 3. Replace placeholder images
All images currently use `https://picsum.photos/seed/<seed>/...` placeholders. When client photography is supplied:

1. Upload images to `/assets/img/` (organize by section if helpful).
2. Search-and-replace the picsum URLs with the real paths, e.g.:
   - `https://picsum.photos/seed/gts-hero-africa/1920/1200` → `/assets/img/hero/africa-cinematic.jpg`
3. For best performance, also produce WebP versions and use `<picture>` with `<source>` fallbacks for hero images (CSS is already prepared).

### 4. Social media links
The pre-header, footer, and post-share blocks contain placeholder `#` URLs for WhatsApp, LinkedIn, X (Twitter), Instagram, and Facebook. Search-and-replace `href="#"` with the real URLs, or use the table below as a reference:

| Platform   | Current placeholder | Where it appears                     |
|------------|--------------------|--------------------------------------|
| WhatsApp   | `href="#"`         | pre-header, footer                   |
| LinkedIn   | `href="#"`         | pre-header, footer, post share       |
| X / Twitter| `href="#"`         | pre-header, footer, post share       |
| Instagram  | `href="#"`         | pre-header, footer                   |
| Facebook   | `href="#"`         | pre-header, footer                   |

### 5. Generate the OG image
`og-image.svg` is included as a placeholder. For best social-platform support, convert it to JPG (1200×630) and save as `og-image.jpg`, then update references in the `<head>` of every page (search-and-replace `og-image.svg` → `og-image.jpg`). Online SVG-to-JPG converters work fine for this one-off task.

---

## Editing content

### Blog posts (most common)
See **`admin/README.md`** for the client-facing editor's guide. The short version:
1. Copy an existing post under `/insights/posts/` and rename it.
2. Edit the title, body, and metadata in the new file.
3. Add a new entry to the top of `/data/posts.json`.
4. Upload via cPanel.

### Service / consulting detail pages
The detail pages are generated from `/data/services.json` and `/data/consulting.json`. To update the copy:

**Option A (simple):** Edit the relevant `.html` file directly. Quick for typos and one-off changes; not recommended for bigger edits because the source-of-truth in JSON will drift out of sync.

**Option B (preferred):** Edit `/data/services.json` or `/data/consulting.json`, then re-run the build script (see below). Keeps JSON and HTML in sync.

### Open roles
Edit `/data/jobs.json`. To add a new role, append a new object to the `"jobs"` array following the existing shape. The careers page reads this file at load time.

### Risk heat map countries
Edit `/data/heat-map.json`. The 10 detailed country dossiers each include `overview`, `key_risks`, `outlook`, and `recommendations`. The remaining ~40 countries have just `risk` level and `summary`. To expand a summary-only country into a full dossier, add the four fields. To change a risk level, edit the `risk` value (`low | moderate | elevated | high | extreme | na`).

### Site copy (about, industries, intelligence, etc.)
Edit the relevant `.html` file directly. The site has no CMS — the HTML is the source of truth for these pages.

---

## Local preview

### Option A — Double-click `index.html`
Most pages will render correctly via the `file://` protocol when you double-click `index.html`. However, **two features require an HTTP server** to work (because `fetch()` is blocked on `file://` in most modern browsers):

- The Risk Heat Map (`/intelligence/heat-map/`) — loads `heat-map.json` via fetch
- The Careers page apply modal — loads `jobs.json` via fetch
- The Insights filters (search and category) — work fully from `file://`, but the listing won't dynamically pick up new posts added to `posts.json` until you re-build

### Option B — Run a quick local server (recommended)
From the project root, run any of these:

```bash
# Python 3 (built into Mac / Linux / Windows)
python -m http.server 8080

# Node.js
npx serve .

# PHP
php -S localhost:8080
```

Then open `http://localhost:8080` in your browser. All features will work as they do in production.

---

## The build script (optional)

If you prefer to manage detail-page content in JSON rather than HTML, you can re-generate every page from `/data/*.json` plus the chrome templates in `/_assemble/` by running:

```bash
python _assemble/build.py
```

**You do NOT need to run this for the site to work.** The HTML files are already generated and committed. The build script exists so that:

- Edits to service/consulting JSON automatically propagate to all detail pages
- The header/footer chrome lives in one place (`/_assemble/chrome-top.html`, `/_assemble/chrome-bottom.html`) and changes flow to all 39 pages
- Re-generating the sitemap is one command: `python _assemble/build_sitemap.py`

If you don't have Python, or prefer to edit HTML directly, simply ignore `/_assemble/`. The deliverable is the static HTML.

**Production note:** You can safely delete `/_assemble/` before deploying if you don't want it on the live server. `robots.txt` already blocks indexing of that folder.

---

## Browser support

Latest two versions of Chrome, Safari, Firefox, Edge. Mobile-responsive at 360px, 768px, 1024px, and 1440px.

## Performance & accessibility

- Lazy loading on all below-the-fold images
- Defer-loaded JavaScript
- WCAG 2.1 AA: skip link, semantic landmarks, focus rings, alt text, color contrast checked
- `prefers-reduced-motion` respected throughout
- Lighthouse-ready: targeting 95+ performance, 100 accessibility, 100 best practices, 95+ SEO on the home page

---

## Support

For substantive design or feature changes, contact the developer who built the site. For day-to-day content updates, follow the workflows in `admin/README.md`.
