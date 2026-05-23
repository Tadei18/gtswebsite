# GTS Risk Advisory — Editor's Guide

This guide explains how to publish a new blog post and update other content on the site, using only the cPanel File Manager (no developer tools or build steps required).

---

## Publishing a new blog post

### Step 1.  Make a copy of an existing post

The fastest way to add a new post is to copy one that already exists:

1. In cPanel File Manager, navigate to `public_html/insights/posts/`.
2. Select any existing post (e.g. `east-africa-elections-outlook-2026.html`) and click **Copy**.
3. Paste it into the same `/insights/posts/` folder.
4. Rename the new file to a short, lowercase, hyphenated **slug** that describes the post.
   - Good: `east-africa-cyber-2026.html`, `cargo-theft-corridors-q3.html`
   - Avoid spaces, capital letters, or special characters.

### Step 2.  Edit the post's contents

1. Right-click the new file → **Edit** (or **Code Edit** for syntax highlighting).
2. Find these lines near the top and update them with your new post's details:
   ```html
   <title>YOUR POST TITLE — GTS Insights</title>
   <meta name="description" content="YOUR EXCERPT — under 155 chars">
   <link rel="canonical" href="https://gtsriskadvisory.com/insights/posts/YOUR-SLUG.html">
   ```
3. In the body of the page, find these sections and update them:
   - The breadcrumb category (`YOUR CATEGORY`)
   - The eyebrow label
   - The `<h1>` post title
   - The author name, role, date, and read time
   - The author avatar initials (two letters)
   - The article body — paragraphs, headings, blockquotes, lists
4. Save the file.

### Step 3.  Update `/data/posts.json`

This is the master list that tells the site about every post.

1. In cPanel File Manager, navigate to `public_html/data/`.
2. Right-click `posts.json` → **Edit**.
3. Add a new entry **at the top** of the `"posts": [` array. Copy this block exactly and edit the values:
   ```json
   {
     "slug": "your-slug-here",
     "title": "Your Post Title",
     "excerpt": "A one- or two-sentence summary that appears on the listing page.",
     "category": "Political Risk",
     "author": "Author Name",
     "author_role": "Author Role / GTS Intelligence Desk",
     "date": "2026-06-01",
     "read_time": "6 min",
     "cover": "/insights/assets/your-slug-here.jpg",
     "file": "/insights/posts/your-slug-here.html",
     "featured": false,
     "tags": ["tag-one", "tag-two"]
   },
   ```
4. **Important:** Don't forget the comma at the end of the new entry (unless it's the very last entry in the array — in which case, no comma). The file MUST be valid JSON or the insights page will not load.
5. Save the file.

### Step 4.  Add a cover image (optional but recommended)

1. Add your cover image to `public_html/insights/assets/`.
2. Use a sensible filename matching the slug (e.g. `east-africa-cyber-2026.jpg`).
3. Recommended size: 1600 × 1000 pixels, JPG format, under 500 KB.
4. If you don't add a cover image, the site will use a placeholder image automatically.

### Step 5.  Verify the post

Open the site in a browser:
- `https://gtsriskadvisory.com/insights/` should show your new post in the grid.
- `https://gtsriskadvisory.com/insights/posts/your-slug-here.html` should show the full post.

Clear your browser cache (Ctrl+F5 or Cmd+Shift+R) if you don't see updates immediately.

---

## Editing existing posts

To fix a typo or update content:
1. Open the post file in cPanel File Manager → Edit.
2. Make your changes.
3. Save.
4. Changes are live immediately.

---

## Categories and tags

Use one of these standard categories so the filter chips on the insights page work cleanly:

- **Political Risk**
- **Operational Risk**
- **Training**
- **Intelligence**
- **Industry**

You can add new categories by simply using them — they will appear automatically in the filter row.

---

## A note on writing in the GTS voice

The site voice is **authoritative, calm, precise, and discreet** — the voice of a senior advisor, never alarmist. A few things that help:

- Lead with the substantive point, not the warm-up
- Quantify and qualify rather than dramatize
- Avoid jargon where plain language works
- Land each piece with a clear recommendation, question, or next step
- Keep paragraphs tight; sub-headings every 3–5 paragraphs aid readability

---

## Troubleshooting

**The post doesn't appear in the insights list.**
Check `/data/posts.json` for a missing comma, an unclosed bracket, or a misnamed file path. The browser developer console (F12) will usually show a JSON parse error.

**The post page itself doesn't load.**
Check the file path under `/insights/posts/`. The `file` field in `posts.json` must exactly match the actual filename, including the `.html` extension.

**Images don't display.**
Check the file path of the image. Absolute paths starting with `/insights/assets/` work from any page; relative paths can break.

**Changes don't show up.**
Clear your browser cache and refresh hard (Ctrl+F5 / Cmd+Shift+R).

---

For anything beyond simple content edits — design changes, new sections, structural updates — contact your developer.
