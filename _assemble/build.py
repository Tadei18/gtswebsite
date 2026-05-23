"""
GTS Risk Advisory — Page Assembler
Renders every page by wrapping body HTML in the shared chrome.

Run from project root:  python _assemble/build.py
"""
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parent.parent
CHROME_TOP = (ROOT / '_assemble/chrome-top.html').read_text(encoding='utf-8')
CHROME_BOT = (ROOT / '_assemble/chrome-bottom.html').read_text(encoding='utf-8')

CTA_BAND_SNIPPET = '''    <!-- CTA BAND -->
    <section class="cta-band">
      <div class="container">
        <div class="cta-band__inner reveal">
          <span class="eyebrow">Ready to engage?</span>
          <h2>Let's design your security posture.</h2>
          <p class="lede">Whether you need a single risk assessment or an embedded long-term advisory relationship, we're ready to listen first and propose second.</p>
          <div class="btn-group">
            <a href="/contact/" class="btn btn--primary">Request a quote</a>
            <a href="/contact/" class="btn btn--secondary">Book a consultation</a>
          </div>
        </div>
      </div>
    </section>
  </main>'''


def render(out_path, title, desc, canonical, body, extra_head='', extra_scripts='', include_cta_band=True):
    top = CHROME_TOP
    top = top.replace('__CANONICAL_PATH__', canonical)
    top = top.replace('__OG_TITLE__', _escape_attr(title))
    top = top.replace('__OG_DESC__', _escape_attr(desc))
    top = top.replace('__EXTRA_HEAD__', extra_head)

    bot = CHROME_BOT
    bot = bot.replace('__EXTRA_SCRIPTS__', extra_scripts)
    if not include_cta_band:
        bot = bot.replace(CTA_BAND_SNIPPET, '  </main>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{_escape_attr(desc)}">
{top}
{body}
{bot}"""

    out = ROOT / out_path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding='utf-8')
    print(f"  wrote {out_path} ({len(html):,} bytes)")


def _escape_attr(s):
    return s.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def load_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


# =========================================================================
# SHARED FRAGMENTS
# =========================================================================
def service_detail_body(item, kind='services', counter=1, total=12):
    label = f"{counter:02d} / {item['name'].upper()}"
    crumbs_label = 'Services' if kind == 'services' else 'Consulting'
    image_seed = item.get('image_seed', item['slug'])

    coverage_section = ''
    if item.get('coverage'):
        coverage_html = '<ul class="coverage">' + ''.join(
            f'<li>{c}</li>' for c in item['coverage']
        ) + '</ul>'
        coverage_section = f"""
    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Coverage</span>
          <h2>Key areas of coverage.</h2>
        </div>
        <div class="reveal" data-delay="1">{coverage_html}</div>
      </div>
    </section>"""

    why_html = ''.join(
        f'''<div class="why-gts__card reveal" data-delay="{i+1}">
          <div class="why-gts__num">0{i+1}</div>
          <h3 class="why-gts__title">{w['title']}</h3>
          <p>{w['body']}</p>
        </div>''' for i, w in enumerate(item['why_gts'])
    )

    engagement_html = ''.join(
        f'''<div class="engagement__step">
          <div class="engagement__num">PHASE {i+1:02d}</div>
          <h4 class="engagement__title">{s['title']}</h4>
          <p>{s['body']}</p>
        </div>''' for i, s in enumerate(item['engagement'])
    )

    related_html = ''
    if item.get('related'):
        related_cards = []
        for r in item['related']:
            related_cards.append(f'''<a href="{r['href']}" class="card">
              <div class="card__eyebrow"><span class="eyebrow">{r['kind']}</span></div>
              <h3 class="card__title">{r['name']}</h3>
              <p class="card__body">{r['body']}</p>
              <span class="card__link">Explore <span class="arrow">→</span></span>
            </a>''')
        related_html = f"""
    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Related</span>
          <h2>Often deployed alongside.</h2>
        </div>
        <div class="related reveal" data-delay="1">
          {''.join(related_cards)}
        </div>
      </div>
    </section>"""

    overview_paragraphs = ''.join(f'<p>{p}</p>' for p in item['overview'])

    return f"""
    <section class="service-hero">
      <div class="service-hero__media" aria-hidden="true">
        <img src="https://picsum.photos/seed/{image_seed}/1920/1080" alt="" loading="eager">
      </div>
      <div class="container service-hero__inner reveal">
        <div class="service-hero__crumbs">
          <a href="/">Home</a> <span class="sep">/</span>
          <a href="/{kind}/">{crumbs_label}</a> <span class="sep">/</span>
          <span>{item['name']}</span>
        </div>
        <span class="eyebrow">{label}</span>
        <h1 style="margin:var(--s-4) 0 var(--s-5);">{item['name']}</h1>
        <p class="lede">{item['lede']}</p>
        <div class="btn-group">
          <a href="/contact/" class="btn btn--primary">Request a quote</a>
          <a href="/contact/" class="btn btn--ghost">Download capability brief <span class="arrow">→</span></a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="editorial drop-cap reveal">
          {overview_paragraphs}
        </div>
      </div>
    </section>
{coverage_section}

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Why GTS</span>
          <h2>Built for operational reality.</h2>
        </div>
        <div class="why-gts">{why_html}</div>
      </div>
    </section>

    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Engagement Model</span>
          <h2>How we deliver this work.</h2>
        </div>
        <div class="engagement reveal" data-delay="1">{engagement_html}</div>
      </div>
    </section>
{related_html}
"""


def _service_jsonld(item, schema_type):
    name = item['name'].replace('"', '\\"')
    desc = item.get('meta_desc', '').replace('"', '\\"')
    return f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "{schema_type}",
    "name": "{name}",
    "description": "{desc}",
    "provider": {{
      "@type": "Organization",
      "name": "GTS Risk Advisory",
      "url": "https://gtsriskadvisory.com"
    }},
    "areaServed": ["KE", "UG", "TZ", "RW", "ET", "NG", "GH", "ZA"]
  }}
  </script>"""


def _services_index_body(services):
    tiles = []
    for idx, s in enumerate(services, 1):
        tiles.append(f'''<a href="/services/{s['slug']}/" class="tile has-brackets">
          <div class="tile__num">{idx:02d} / {s['name'].upper()}</div>
          <h3 class="tile__title">{s['name']}</h3>
          <p class="tile__body">{s['summary']}</p>
          <span class="tile__link">Read more <span class="arrow">→</span></span>
        </a>''')
    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Services & Products</span>
        <h1>Integrated protection for an interconnected risk landscape.</h1>
        <p class="lede">Twelve operational and specialist service lines, designed to be deployed individually or stitched into a unified security posture. Every engagement is shaped by intelligence, calibrated to your operating environment, and delivered with discretion.</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="grid grid--3 reveal">
          {''.join(tiles)}
        </div>
      </div>
    </section>
"""


def _consulting_index_body(consulting):
    tiles = []
    for idx, c in enumerate(consulting, 1):
        tiles.append(f'''<a href="/consulting/{c['slug']}/" class="tile has-brackets">
          <div class="tile__num">{idx:02d} / {c['name'].upper()}</div>
          <h3 class="tile__title">{c['name']}</h3>
          <p class="tile__body">{c['summary']}</p>
          <span class="tile__link">Read more <span class="arrow">→</span></span>
        </a>''')
    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Customized Consulting</span>
        <h1>Independent counsel. Decisive insight.</h1>
        <p class="lede">Eleven consulting offerings designed for the moments where the cost of misjudgment is high — pre-deal diligence, market entry, governance reform, complex investigations, and the disciplined work of building resilience.</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="grid grid--3 reveal">
          {''.join(tiles)}
        </div>
      </div>
    </section>
"""


# =========================================================================
# HOME PAGE
# =========================================================================
def _home_body():
    return """
    <!-- HERO -->
    <section class="hero">
      <div class="hero__media" aria-hidden="true">
        <picture>
          <source srcset="/assets/img/hero/nairobi-cityscape.webp" type="image/webp">
          <img src="/assets/img/hero/nairobi-cityscape.jpg"
               alt=""
               loading="eager"
               decoding="async"
               fetchpriority="high"
               width="1920" height="1080">
        </picture>
      </div>
      <div class="container hero__inner reveal">
        <span class="eyebrow">Intelligence · Resilience · Protection</span>
        <h1 class="display">Smarter Security for a Changing Africa.</h1>
        <p class="lede">We deliver intelligence-driven security solutions, risk consulting, and operational resilience services to corporations, governments, and individuals operating across the continent.</p>
        <div class="btn-group">
          <a href="/services/" class="btn btn--primary">Explore our services</a>
          <a href="/contact/" class="btn btn--ghost">Request a briefing <span class="arrow">→</span></a>
        </div>
        <div class="hero__metrics">
          <div class="metric">
            <div class="metric__num"><span data-counter data-target="12">0</span><span class="suffix">+</span></div>
            <div class="metric__label">Markets covered</div>
          </div>
          <div class="metric">
            <div class="metric__num"><span data-counter data-target="200">0</span><span class="suffix">+</span></div>
            <div class="metric__label">Engagements delivered</div>
          </div>
          <div class="metric">
            <div class="metric__num"><span data-counter data-target="24">0</span><span class="suffix">/7</span></div>
            <div class="metric__label">Intelligence desk</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CAPABILITY PILLARS -->
    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">01 / Capabilities</span>
          <h2>Four pillars of practice.</h2>
          <p class="lede">A disciplined, layered model — from boots-on-the-ground operations to country-level intelligence — calibrated to your risk profile and operating tempo.</p>
        </div>

        <div class="pillars">
          <a href="/services/" class="pillar reveal" data-delay="1">
            <svg class="pillar__icon" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M16 4l11 4v8c0 7-5 12-11 12S5 23 5 16V8l11-4z"/>
              <path d="M11 16l4 4 7-7"/>
            </svg>
            <h3>Corporate Security</h3>
            <p>Tailored security strategies and integrated protection frameworks for organizations operating in complex environments.</p>
            <span class="pillar__link">Explore →</span>
          </a>
          <a href="/consulting/" class="pillar reveal" data-delay="2">
            <svg class="pillar__icon" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5">
              <rect x="4" y="6" width="24" height="20" rx="1"/>
              <path d="M9 14h14M9 19h10M9 24h6"/>
              <path d="M22 4v4M14 4v4"/>
            </svg>
            <h3>Risk Consulting</h3>
            <p>Independent assessments, audits, and advisory grounded in evidence, regional context, and operational realism.</p>
            <span class="pillar__link">Explore →</span>
          </a>
          <a href="/services/executive-protection/" class="pillar reveal" data-delay="3">
            <svg class="pillar__icon" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="16" cy="11" r="5"/>
              <path d="M5 28c0-6 5-10 11-10s11 4 11 10"/>
            </svg>
            <h3>Executive Services</h3>
            <p>Discreet personal and travel protection for principals, dignitaries, and high-profile individuals across the continent.</p>
            <span class="pillar__link">Explore →</span>
          </a>
          <a href="/intelligence/" class="pillar reveal" data-delay="4">
            <svg class="pillar__icon" viewBox="0 0 32 32" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="16" cy="16" r="12"/>
              <path d="M4 16h24M16 4c4 3 6 7 6 12s-2 9-6 12c-4-3-6-7-6-12s2-9 6-12z"/>
            </svg>
            <h3>Intelligence Advisory</h3>
            <p>Country risk, daily monitoring briefs, and the GTS Risk Heat Map — actionable foresight, not headlines.</p>
            <span class="pillar__link">Explore →</span>
          </a>
        </div>
      </div>
    </section>

    <!-- FEATURED: INTELLIGENCE -->
    <section class="section">
      <div class="container">
        <div class="split">
          <div class="intel-teaser__media reveal">
            <span class="label">— Risk Heat Map · Q2 2026</span>
            <svg viewBox="0 0 400 480" aria-hidden="true">
              <path d="M180 50 q40 -10 80 5 q25 15 30 50 q5 40 -10 80 q-5 40 10 70 q20 40 5 90 q-15 50 -60 90 q-30 25 -55 30 q-30 5 -50 -20 q-25 -30 -35 -75 q-15 -65 -10 -110 q5 -50 25 -100 q15 -40 30 -75 q15 -25 40 -35 z"
                    fill="#1E2842" stroke="#3A4970" stroke-width="1"/>
              <circle cx="195" cy="195" r="6" fill="#C9A961"/>
              <circle cx="215" cy="180" r="5" fill="#D17B3F"/>
              <circle cx="180" cy="220" r="5" fill="#C9A961"/>
              <circle cx="155" cy="200" r="5" fill="#B54533"/>
              <circle cx="170" cy="280" r="6" fill="#C9A961"/>
              <circle cx="200" cy="330" r="5" fill="#4A7C59"/>
              <circle cx="180" cy="380" r="6" fill="#4A7C59"/>
              <circle cx="100" cy="160" r="4" fill="#D17B3F"/>
              <circle cx="130" cy="180" r="4" fill="#C9A961"/>
              <circle cx="220" cy="120" r="5" fill="#D17B3F"/>
              <circle cx="195" cy="195" r="11" fill="none" stroke="#C9A961" stroke-width="1.5"/>
              <text x="210" y="195" font-family="JetBrains Mono" font-size="10" fill="#C9A961" letter-spacing="0.1em">KEN</text>
            </svg>
            <div style="position:absolute;bottom:var(--s-4);left:var(--s-4);right:var(--s-4);">
              <a href="/intelligence/heat-map/" class="btn btn--ghost" style="padding:0;">Open the Risk Heat Map <span class="arrow">→</span></a>
            </div>
          </div>

          <div class="reveal" data-delay="1">
            <span class="eyebrow">Featured Practice</span>
            <h2 style="margin-top:var(--s-3);margin-bottom:var(--s-4);">Decisions are only as good as the intelligence behind them.</h2>
            <p>Our intelligence products are tailored analytical outputs developed through a structured methodology that integrates verified open-source intelligence, field insights, and contextual analysis. Each is designed to support executive leadership and operational teams with intelligence that directly informs strategy, planning, and execution.</p>
            <ul class="bullet-list mt-5">
              <li><strong style="color:var(--color-ink-high)">Customized Intelligence Reports</strong> — sector- and geography-specific products tailored to your operational picture.</li>
              <li><strong style="color:var(--color-ink-high)">Political & Country Risk Analysis</strong> — geopolitical, regulatory, and security conditions across African markets.</li>
              <li><strong style="color:var(--color-ink-high)">Daily Monitoring Briefs</strong> — concise, intelligence-driven updates from verified sources.</li>
              <li><strong style="color:var(--color-ink-high)">Situational Risk Analysis</strong> — real-time, incident-driven assessments with mitigation guidance.</li>
              <li><strong style="color:var(--color-ink-high)">Risk Heat Map</strong> — visual intelligence tool for prioritization and resource allocation.</li>
            </ul>
            <div class="btn-group mt-6">
              <a href="/intelligence/" class="btn btn--secondary">Intelligence Advisory Centre</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- INDUSTRIES -->
    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">02 / Industries</span>
          <h2>Trusted across sectors.</h2>
          <p class="lede">We work with leadership teams in regulated, capital-intensive, and operationally complex sectors — wherever security is both a duty of care and a competitive edge.</p>
        </div>

        <div class="industries-grid reveal" data-delay="1">
          <a href="/industries/#commercial-banks" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="4" y="12" width="24" height="14"/><path d="M16 4l12 8H4z"/><path d="M9 16v6M16 16v6M23 16v6"/></svg>
            <span class="industry-tile__name">Commercial Banks</span>
            <span class="industry-tile__hover">Fraud, branch security, cash logistics →</span>
          </a>
          <a href="/industries/#manufacturing" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 28V14l8 5V14l8 5V14l8 5v9z"/><path d="M4 28h24"/></svg>
            <span class="industry-tile__name">Manufacturing</span>
            <span class="industry-tile__hover">Plant security, supply chain integrity →</span>
          </a>
          <a href="/industries/#insurance" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M16 4l11 4v9c0 7-5 12-11 14-6-2-11-7-11-14V8z"/></svg>
            <span class="industry-tile__name">Insurance</span>
            <span class="industry-tile__hover">Claims investigations, fraud detection →</span>
          </a>
          <a href="/industries/#ngos" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="16" cy="16" r="12"/><path d="M4 16h24M16 4c3 4 5 8 5 12s-2 8-5 12c-3-4-5-8-5-12s2-8 5-12z"/></svg>
            <span class="industry-tile__name">NGOs</span>
            <span class="industry-tile__hover">Field safety, travel security, evacuations →</span>
          </a>
          <a href="/industries/#agriculture" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M16 28V12M16 12c0-4 4-7 8-7 0 5-4 7-8 7zM16 18c0-4-4-7-8-7 0 5 4 7 8 7z"/></svg>
            <span class="industry-tile__name">Agriculture</span>
            <span class="industry-tile__hover">Estate protection, harvest logistics →</span>
          </a>
          <a href="/industries/#hospitality" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="4" y="10" width="24" height="18"/><path d="M4 10l12-6 12 6M11 28v-8h10v8"/></svg>
            <span class="industry-tile__name">Hospitality & Retail</span>
            <span class="industry-tile__hover">Guest screening, perimeter, events →</span>
          </a>
          <a href="/industries/#investment-firms" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 24l8-8 6 6L28 8M22 8h6v6"/></svg>
            <span class="industry-tile__name">Investment Firms</span>
            <span class="industry-tile__hover">Due diligence, deal-stage risk →</span>
          </a>
          <a href="/industries/#education" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M16 6L4 12l12 6 12-6zM8 15v6c0 2 4 4 8 4s8-2 8-4v-6"/></svg>
            <span class="industry-tile__name">Education</span>
            <span class="industry-tile__hover">Campus safety, child protection →</span>
          </a>
          <a href="/industries/#parastatals" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 28h24M6 28V14M14 28V14M18 28V14M26 28V14M4 14h24L16 4z"/></svg>
            <span class="industry-tile__name">Parastatals</span>
            <span class="industry-tile__hover">Critical infrastructure, governance →</span>
          </a>
          <a href="/industries/#county-governments" class="industry-tile">
            <svg class="industry-tile__icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M16 4L4 14h24z"/><path d="M6 14v14h20V14"/><path d="M14 28v-8h4v8"/></svg>
            <span class="industry-tile__name">County Governments</span>
            <span class="industry-tile__hover">Public safety, capacity programs →</span>
          </a>
        </div>

        <div class="text-center mt-7 reveal">
          <a href="/industries/" class="btn btn--ghost">All industries we serve <span class="arrow">→</span></a>
        </div>
      </div>
    </section>

    <!-- METHODOLOGY -->
    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">03 / Methodology</span>
          <h2>A disciplined, evidence-based engagement model.</h2>
          <p class="lede">Each engagement moves through the same four-stage rhythm. We invest the time upfront so the deliverable is grounded in your reality, not a templated playbook.</p>
        </div>

        <div class="timeline reveal" data-delay="1">
          <div class="timeline__step">
            <div class="timeline__num">01</div>
            <h3 class="timeline__title">Listen</h3>
            <p class="timeline__body">Discovery sessions with leadership, security teams, and operators to map the real picture — risks, controls, gaps, dependencies.</p>
          </div>
          <div class="timeline__step">
            <div class="timeline__num">02</div>
            <h3 class="timeline__title">Assess</h3>
            <p class="timeline__body">On-site evaluation, threat modeling, and intelligence overlay. We pressure-test current controls against the threats that actually matter.</p>
          </div>
          <div class="timeline__step">
            <div class="timeline__num">03</div>
            <h3 class="timeline__title">Design</h3>
            <p class="timeline__body">Pragmatic, prioritized recommendations — phased to your budget cycle, tied to clear outcomes, costed honestly.</p>
          </div>
          <div class="timeline__step">
            <div class="timeline__num">04</div>
            <h3 class="timeline__title">Deliver & Sustain</h3>
            <p class="timeline__body">Implementation support, training, and ongoing intelligence so resilience compounds rather than decays after the report is filed.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- INSIGHTS TEASER -->
    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">04 / Intelligence Briefs</span>
          <h2>From the desk.</h2>
          <p class="lede">Short-form intelligence and analysis from the GTS desk — written for the people who have to act on it.</p>
        </div>

        <div class="grid grid--3 reveal" data-delay="1" id="home-insights-grid">
          <a class="post-card" href="/insights/posts/east-africa-elections-outlook-2026.html">
            <div class="post-card__cover"><img src="https://picsum.photos/seed/insight-elections/800/500" alt="" loading="lazy"></div>
            <div class="post-card__body">
              <div class="post-card__meta"><span class="post-card__cat">Political Risk</span><span>·</span><span>12 May 2026</span><span>·</span><span>8 min</span></div>
              <h3 class="post-card__title">East Africa Elections Outlook 2026</h3>
              <p class="post-card__excerpt">Three elections that will reshape the regional risk landscape — and what operators should be doing about it now.</p>
              <span class="post-card__readlink">Read →</span>
            </div>
          </a>
          <a class="post-card" href="/insights/posts/supply-chain-security-2026.html">
            <div class="post-card__cover"><img src="https://picsum.photos/seed/insight-supply/800/500" alt="" loading="lazy"></div>
            <div class="post-card__body">
              <div class="post-card__meta"><span class="post-card__cat">Operational Risk</span><span>·</span><span>28 Apr 2026</span><span>·</span><span>7 min</span></div>
              <h3 class="post-card__title">Beyond the Perimeter: Rethinking Supply Chain Security in 2026</h3>
              <p class="post-card__excerpt">Why your supply chain is your second front line, and the four control upgrades that pay back inside a year.</p>
              <span class="post-card__readlink">Read →</span>
            </div>
          </a>
          <a class="post-card" href="/insights/posts/behavioural-security-awareness.html">
            <div class="post-card__cover"><img src="https://picsum.photos/seed/insight-training/800/500" alt="" loading="lazy"></div>
            <div class="post-card__body">
              <div class="post-card__meta"><span class="post-card__cat">Training</span><span>·</span><span>14 Apr 2026</span><span>·</span><span>6 min</span></div>
              <h3 class="post-card__title">Behavioural Security Awareness: The Human Layer of Cyber Defence</h3>
              <p class="post-card__excerpt">The most expensive perimeter is the one between your employees' ears. How to actually move the needle on behaviour.</p>
              <span class="post-card__readlink">Read →</span>
            </div>
          </a>
        </div>

        <div class="text-center mt-7 reveal">
          <a href="/insights/" class="btn btn--secondary">All insights →</a>
        </div>
      </div>
    </section>
"""


HOME_PRELOAD = '  <link rel="preload" as="image" href="/assets/img/hero/nairobi-cityscape.webp" type="image/webp" fetchpriority="high">\n'

HOME_JSONLD = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "GTS Risk Advisory",
    "url": "https://gtsriskadvisory.com",
    "logo": "https://gtsriskadvisory.com/favicon.svg",
    "description": "Intelligence-driven security and risk consulting firm operating across Kenya, East Africa, and the African continent.",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Nairobi",
      "addressCountry": "KE"
    },
    "contactPoint": {
      "@type": "ContactPoint",
      "telephone": "+254-XXX-XXX-XXX",
      "contactType": "customer service",
      "email": "info@gtsriskadvisory.com",
      "areaServed": ["KE", "UG", "TZ", "RW", "ET", "NG", "GH", "ZA"]
    },
    "sameAs": []
  }
  </script>"""


# =========================================================================
# ABOUT PAGE
# =========================================================================
def _about_body():
    return """
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">About GTS</span>
        <h1>A partner in safer tomorrows.</h1>
        <p class="lede">We are a premier security solutions provider specializing in delivering innovative, client-focused, and comprehensive risk management services. We offer unmatched expertise and tailored security strategies across Kenya, East Africa, and the broader African continent.</p>
      </div>
    </section>

    <section class="section">
      <div class="container container--narrow editorial drop-cap reveal">
        <p>Our approach is rooted in proactive risk assessment, advanced technology integration, and a deep understanding of the regional dynamics shaping security needs in Africa. We believe in making security smarter, more efficient, and more accessible. Whether you require comprehensive risk management for your business, tailored security solutions for special events, or proactive intelligence to mitigate threats, we are your partner in creating a safer tomorrow.</p>
        <p>We serve a diverse clientele, including corporations, government entities, non-governmental organizations, and private individuals. Our services cover various domains, from corporate security to personal protection, and from crisis management to advanced risk analytics. We are committed to enhancing safety and resilience in a rapidly evolving security landscape.</p>
      </div>
    </section>

    <section class="section section--surface-1">
      <div class="container">
        <div class="grid grid--2 grid--lg">
          <div class="vm-card reveal">
            <span class="eyebrow">Vision</span>
            <h2>To be the leading intelligence-driven security and risk consulting firm in Africa.</h2>
            <div class="hairline"></div>
            <p>Recognized for delivering trusted advisory services, innovative risk solutions, and the highest standards of integrity and operational excellence.</p>
          </div>
          <div class="vm-card reveal" data-delay="1">
            <span class="eyebrow">Mission</span>
            <h2>To deliver exceptional, innovative, and customized security and risk consulting services.</h2>
            <div class="hairline"></div>
            <p>Empowering our clients to operate confidently and securely in dynamic environments — through expertise that meets them where they are.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Our Values</span>
          <h2>What we stand for.</h2>
        </div>
        <div class="grid grid--4 grid--lg">
          <div class="card reveal" data-delay="1">
            <svg class="icon icon--lg" viewBox="0 0 32 32" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true" style="margin-bottom:16px">
              <circle cx="16" cy="16" r="6"/>
              <path d="M16 4v4M16 24v4M4 16h4M24 16h4M7 7l3 3M22 22l3 3M25 7l-3 3M10 22l-3 3"/>
            </svg>
            <h3 class="card__title">Innovation</h3>
            <p class="card__body">We continuously invest in advanced technologies, cutting-edge methodologies, and creative problem-solving approaches to stay ahead of emerging security challenges. By embracing innovation, we ensure that our solutions are not only effective but also adaptive to the ever-changing security landscape.</p>
          </div>
          <div class="card reveal" data-delay="2">
            <svg class="icon icon--lg" viewBox="0 0 32 32" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true" style="margin-bottom:16px">
              <circle cx="16" cy="12" r="5"/>
              <path d="M6 28c0-5 4-9 10-9s10 4 10 9"/>
            </svg>
            <h3 class="card__title">Client Focus</h3>
            <p class="card__body">Our clients are at the heart of our operations. We take pride in delivering personalized, responsive, and reliable services that address each client's unique needs. Building long-term relationships based on trust and satisfaction is our top priority.</p>
          </div>
          <div class="card reveal" data-delay="3">
            <svg class="icon icon--lg" viewBox="0 0 32 32" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true" style="margin-bottom:16px">
              <path d="M16 4l11 4v8c0 7-5 12-11 12S5 23 5 16V8l11-4z"/>
              <path d="M11 16l4 4 7-7"/>
            </svg>
            <h3 class="card__title">Integrity</h3>
            <p class="card__body">We uphold the highest ethical standards in all our dealings. Transparency, honesty, and accountability are integral to our business, ensuring our clients can rely on us as a trusted partner in safeguarding their interests.</p>
          </div>
          <div class="card reveal" data-delay="4">
            <svg class="icon icon--lg" viewBox="0 0 32 32" fill="none" stroke="#C9A961" stroke-width="1.5" aria-hidden="true" style="margin-bottom:16px">
              <polygon points="16,4 20,12 28,13 22,19 24,28 16,24 8,28 10,19 4,13 12,12"/>
            </svg>
            <h3 class="card__title">Excellence</h3>
            <p class="card__body">We are committed to excellence in every aspect of our operations. From strategy development to service delivery, we strive for perfection and continuous improvement, ensuring we consistently exceed client expectations.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Leadership</span>
          <h2>Senior practitioners with regional depth.</h2>
          <p class="lede">A leadership team drawn from intelligence, corporate security, and consulting backgrounds — with operational experience across the African continent.</p>
        </div>
        <div class="grid grid--3 grid--lg">
          <div class="leader reveal" data-delay="1">
            <div class="leader__portrait"><img src="https://picsum.photos/seed/gts-leader-1/600/800" alt="Portrait of managing director" loading="lazy"></div>
            <span class="leader__role">Managing Director</span>
            <h3 class="leader__name">James Otieno</h3>
            <p class="leader__bio">Two decades leading corporate security and risk programmes across East and Southern Africa, including senior in-house roles with multinational banks and energy operators. Known for translating complex risk into executive-ready decisions and for the quiet discipline of his engagement style.</p>
          </div>
          <div class="leader reveal" data-delay="2">
            <div class="leader__portrait"><img src="https://picsum.photos/seed/gts-leader-2/600/800" alt="Portrait of head of intelligence" loading="lazy"></div>
            <span class="leader__role">Head of Intelligence</span>
            <h3 class="leader__name">Amina Kassim</h3>
            <p class="leader__bio">Background in political risk analysis with both government and private-sector intelligence units. Leads the GTS Intelligence Desk, including the Risk Heat Map, country reporting practice, and daily monitoring service. Published widely on African elections and governance risk.</p>
          </div>
          <div class="leader reveal" data-delay="3">
            <div class="leader__portrait"><img src="https://picsum.photos/seed/gts-leader-3/600/800" alt="Portrait of director of operations" loading="lazy"></div>
            <span class="leader__role">Director of Operations</span>
            <h3 class="leader__name">Peter Mwangi</h3>
            <p class="leader__bio">Former special operations and corporate security leadership across multiple sectors. Oversees GTS field operations — manned guarding, command centres, executive protection, and event security — with relentless focus on selection, training, and operational discipline.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">Operating Footprint</span>
            <h2 style="margin-top:var(--s-3);margin-bottom:var(--s-4);">Operations across 12+ African markets.</h2>
            <p>From our headquarters in Nairobi, we deliver engagements directly or through trusted in-country partners across East, Southern, West, and North Africa — backed by an intelligence picture that spans the continent.</p>
            <ul class="bullet-list mt-5" style="columns:2;column-gap:var(--s-6)">
              <li>Kenya</li><li>Uganda</li><li>Tanzania</li><li>Rwanda</li>
              <li>Ethiopia</li><li>South Africa</li><li>Nigeria</li><li>Ghana</li>
              <li>Egypt</li><li>DRC</li><li>Zambia</li><li>Mozambique</li>
            </ul>
          </div>
          <div class="intel-teaser__media reveal" data-delay="1">
            <span class="label">— Operational Footprint</span>
            <svg viewBox="0 0 400 480" aria-hidden="true">
              <path d="M180 50 q40 -10 80 5 q25 15 30 50 q5 40 -10 80 q-5 40 10 70 q20 40 5 90 q-15 50 -60 90 q-30 25 -55 30 q-30 5 -50 -20 q-25 -30 -35 -75 q-15 -65 -10 -110 q5 -50 25 -100 q15 -40 30 -75 q15 -25 40 -35 z"
                    fill="#1E2842" stroke="#3A4970" stroke-width="1"/>
              <g fill="#C9A961">
                <circle cx="195" cy="195" r="5"/>
                <circle cx="215" cy="180" r="4"/>
                <circle cx="180" cy="220" r="4"/>
                <circle cx="170" cy="280" r="5"/>
                <circle cx="200" cy="330" r="4"/>
                <circle cx="180" cy="380" r="5"/>
                <circle cx="100" cy="160" r="4"/>
                <circle cx="130" cy="180" r="4"/>
                <circle cx="220" cy="120" r="4"/>
                <circle cx="220" cy="260" r="4"/>
              </g>
            </svg>
          </div>
        </div>
      </div>
    </section>
"""


# =========================================================================
# INDUSTRIES PAGE
# =========================================================================
INDUSTRIES = [
    {
        "id": "commercial-banks",
        "name": "Commercial Banks",
        "challenges": "Commercial banks across Africa face a layered threat picture — branch security, ATM and cash-in-transit risk, internal and external fraud, social engineering, and increasingly sophisticated cyber-enabled financial crime. Each layer interacts with regulatory exposure and reputational sensitivity that makes incidents more consequential than the immediate loss.",
        "approach": "GTS supports banks with integrated risk management — combining branch security frameworks, fraud investigation capability, behavioural security training, vetting of staff and vendors, and policy and SOP design. We work with security operations, internal audit, and compliance leadership to put security inside business decisions, not alongside them.",
        "engagements": [
            "Branch security frameworks and ATM risk programmes",
            "Internal fraud and misconduct investigations",
            "Vendor and staff vetting at scale"
        ],
        "related": [
            {"name": "Corporate Forensic Investigations", "href": "/services/forensic-investigations/"},
            {"name": "Business Process Control Audits", "href": "/consulting/business-process-audits/"},
            {"name": "Vetting & Due Diligence", "href": "/consulting/vetting-due-diligence/"}
        ]
    },
    {
        "id": "manufacturing",
        "name": "Manufacturing",
        "challenges": "Plant security, supply chain integrity, and labour-relations risk dominate the manufacturing security agenda. Sites combine high-value assets, complex perimeters, large workforces, and time-sensitive logistics — and the cost of any disruption cascades quickly across production schedules and customer commitments.",
        "approach": "We build plant security programmes that work as one system — perimeter, access, surveillance, manned response, and command-centre oversight — integrated with supply chain controls upstream and downstream. We also run targeted investigations into shrinkage, sabotage, and procurement irregularity, and design behavioural safety and security training for the operating workforce.",
        "engagements": [
            "Plant security framework and integration",
            "Supply chain risk and route security",
            "Shrinkage and procurement-fraud investigations"
        ],
        "related": [
            {"name": "Corporate Security Services", "href": "/services/corporate-security/"},
            {"name": "Supply Chain Security Solutions", "href": "/services/supply-chain-security/"},
            {"name": "Security Systems Design & Installation", "href": "/services/security-systems/"}
        ]
    },
    {
        "id": "insurance",
        "name": "Insurance",
        "challenges": "Insurance carriers face concentrated fraud exposure across claims, distribution, and motor lines — alongside the security and conduct risks that affect every financial institution. Investigation capability, intelligence on emerging fraud patterns, and partner due diligence are core operating requirements rather than optional capabilities.",
        "approach": "GTS provides specialist investigation support for complex and high-value claims, behavioural analytics and training for fraud teams, vetting of brokers and assessors, and intelligence support to underwriting in higher-risk segments and geographies. We also help carriers stand up structured investigation governance — case management, evidence handling, and reporting standards.",
        "engagements": [
            "Complex claim and broker-fraud investigations",
            "Vetting of brokers, assessors, and partner networks",
            "Fraud-team training and investigation governance"
        ],
        "related": [
            {"name": "Tailored Investigations", "href": "/consulting/tailored-investigations/"},
            {"name": "Vetting & Due Diligence", "href": "/consulting/vetting-due-diligence/"},
            {"name": "Fraud & Security Awareness Training", "href": "/services/fraud-security-training/"}
        ]
    },
    {
        "id": "ngos",
        "name": "Non-Governmental Organizations",
        "challenges": "NGOs and development agencies operate in some of the most demanding security environments on the continent — areas where political instability, communal conflict, and rapidly evolving safety conditions are routine. Duty of care to staff, partners, and beneficiaries sits alongside donor compliance and operational continuity pressures.",
        "approach": "We support NGOs with travel security programmes, journey management, evacuation planning, security risk assessments at field office level, capacity-building for country teams, and intelligence support that helps leadership decide when to scale, pause, or withdraw. Engagements are calibrated to organizational scale and the realities of donor budgets.",
        "engagements": [
            "Travel security and journey management programmes",
            "Field office risk assessments and evacuation planning",
            "Country-team training and security focal-point development"
        ],
        "related": [
            {"name": "Travel Security Programs", "href": "/consulting/travel-security/"},
            {"name": "Safety Evacuation Programs", "href": "/consulting/safety-evacuation/"},
            {"name": "Capacity Building Services", "href": "/consulting/capacity-building/"}
        ]
    },
    {
        "id": "agriculture",
        "name": "Agricultural Sector",
        "challenges": "Large agricultural operations are inherently exposed — long perimeters, valuable mobile assets, seasonal labour peaks, harvest-time logistics windows, and remote locations far from rapid response. Theft, encroachment, and labour-related incidents can move quickly from operational annoyance to material loss.",
        "approach": "We design integrated estate security — combining trained manned guarding, perimeter and surveillance technology, command-centre oversight, and harvest-period reinforcement. Investigations support resolves shrinkage and produce traceability problems, and our intelligence work tracks the localized risks that affect specific estates and corridors.",
        "engagements": [
            "Integrated estate and perimeter security",
            "Harvest and logistics-window security reinforcement",
            "Shrinkage investigation and prevention programmes"
        ],
        "related": [
            {"name": "Manned Guarding Services", "href": "/services/manned-guarding/"},
            {"name": "Security Systems Design & Installation", "href": "/services/security-systems/"},
            {"name": "Tailored Investigations", "href": "/consulting/tailored-investigations/"}
        ]
    },
    {
        "id": "hospitality",
        "name": "Malls, Residential & Hotels",
        "challenges": "Mixed-use developments, hotels, and residential communities share a difficult security brief — protecting people and assets while preserving the experience of visiting, living, or staying. Visible security must coexist with hospitality standards, and protocols must work for residents, guests, contractors, and the steady flow of unknown visitors.",
        "approach": "We design layered programmes that combine trained manned guarding, reception security, access control, CCTV and command-centre integration, and event-specific reinforcement. Programmes are calibrated to property type — luxury hospitality, gated communities, regional malls, mixed-use towers — and the specific community of users each one serves.",
        "engagements": [
            "Property-wide security programme design",
            "Reception, access control, and visitor management",
            "Event reinforcement and peak-period operations"
        ],
        "related": [
            {"name": "Residential Security Services", "href": "/services/residential-security/"},
            {"name": "Reception Security Services", "href": "/services/reception-security/"},
            {"name": "Events Security Services", "href": "/services/events-security/"}
        ]
    },
    {
        "id": "investment-firms",
        "name": "Investment Firms",
        "challenges": "Investors and private equity firms operating across Africa face decision-stage risk: how reliable is the target, how clean are the counterparties, how exposed is the operating environment, and what surprises lurk in the next reporting cycle. The cost of imperfect information is high — and slow-built reputations can be eroded by a single bad deal.",
        "approach": "We deliver pre-deal vetting and due diligence, market entry analysis, M&A risk assessments, embedded advisory through transactions, and ongoing intelligence support for portfolio companies. Outputs are designed for investment committees and boards — concise, risk-rated, and defensible.",
        "engagements": [
            "Pre-deal vetting and due diligence",
            "Market entry and M&A risk assessments",
            "Embedded advisory and portfolio company support"
        ],
        "related": [
            {"name": "Vetting & Due Diligence", "href": "/consulting/vetting-due-diligence/"},
            {"name": "Market Entry Assessments", "href": "/consulting/market-entry/"},
            {"name": "M&A Risk Assessments", "href": "/consulting/mergers-acquisitions/"}
        ]
    },
    {
        "id": "education",
        "name": "Universities, Colleges & Schools",
        "challenges": "Educational institutions balance an open culture with non-negotiable safety obligations — campus access, student safety, residential security, large-event management, and increasingly, online and behavioural risks. Incidents become public quickly and the institutional response shapes reputation for years.",
        "approach": "We support institutions with campus risk assessments, integrated security programmes that respect academic openness, manned and technical security for residential blocks, event security, behavioural awareness training for staff and students, and incident-response governance — including the difficult conversations around child protection.",
        "engagements": [
            "Campus risk assessment and security framework design",
            "Residential and event security operations",
            "Behavioural awareness and incident-response training"
        ],
        "related": [
            {"name": "Security Risk Assessments", "href": "/consulting/security-risk-assessments/"},
            {"name": "Manned Guarding Services", "href": "/services/manned-guarding/"},
            {"name": "Fraud & Security Awareness Training", "href": "/services/fraud-security-training/"}
        ]
    },
    {
        "id": "parastatals",
        "name": "Parastatals",
        "challenges": "State-owned enterprises sit at the intersection of commercial operations, public expectation, and political scrutiny. Security and risk programmes must be operationally effective, demonstrably ethical, and resilient to changes in leadership — across critical infrastructure, public-service estates, and high-value asset bases.",
        "approach": "GTS supports parastatals with security risk assessments, governance and policy design, capacity building for in-house security teams, embedded advisory through reform programmes, and investigations capability that meets the higher evidentiary bar of public-sector accountability.",
        "engagements": [
            "Security risk assessments and framework design",
            "Policy, SOP, and governance reform support",
            "Investigation capability and capacity building"
        ],
        "related": [
            {"name": "Security Risk Assessments", "href": "/consulting/security-risk-assessments/"},
            {"name": "Policy & SOPs Design", "href": "/consulting/policy-sops/"},
            {"name": "Embedded Consultancy", "href": "/consulting/embedded-consultancy/"}
        ]
    },
    {
        "id": "county-governments",
        "name": "County Governments",
        "challenges": "County governments carry frontline responsibility for public safety, infrastructure protection, and emergency preparedness — often with limited specialist capacity and a heavy political accountability burden. Building durable security and risk capability inside the county system is as important as any single programme delivered.",
        "approach": "We work with county governments on capacity-building for security and emergency response teams, evacuation and disaster-preparedness programmes, security risk assessments for county facilities, and structured policy and SOP development to embed sustainable practice across departments.",
        "engagements": [
            "Capacity building for county security and response teams",
            "Evacuation and disaster preparedness programmes",
            "County facility risk assessments and policy support"
        ],
        "related": [
            {"name": "Capacity Building Services", "href": "/consulting/capacity-building/"},
            {"name": "Safety Evacuation Programs", "href": "/consulting/safety-evacuation/"},
            {"name": "Policy & SOPs Design", "href": "/consulting/policy-sops/"}
        ]
    }
]


def _industries_body():
    sections = []
    for idx, ind in enumerate(INDUSTRIES, 1):
        related_chips = ''.join(
            f'<a class="chip" href="{r["href"]}">{r["name"]}</a>'
            for r in ind['related']
        )
        engagements = ''.join(f'<li>{e}</li>' for e in ind['engagements'])
        sections.append(f'''
    <section id="{ind['id']}" class="section{' section--surface-1' if idx % 2 == 0 else ''}">
      <div class="container">
        <div class="split">
          <div class="reveal">
            <span class="eyebrow">{idx:02d} / Sector</span>
            <h2 style="margin-top:var(--s-3);margin-bottom:var(--s-5);">{ind['name']}</h2>
            <p>{ind['challenges']}</p>
            <p style="margin-top:var(--s-4)">{ind['approach']}</p>
          </div>
          <div class="reveal" data-delay="1">
            <span class="eyebrow">Typical Engagements</span>
            <ul class="bullet-list mt-4 mb-6">
              {engagements}
            </ul>
            <span class="eyebrow">Related Practices</span>
            <div style="display:flex;flex-wrap:wrap;gap:var(--s-2);margin-top:var(--s-3)">
              {related_chips}
            </div>
          </div>
        </div>
      </div>
    </section>''')

    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Industries</span>
        <h1>Sector-specific security and risk expertise.</h1>
        <p class="lede">Across ten sectors, we tailor security programmes, intelligence products, and advisory engagements to the specific risk profile, regulatory context, and operational tempo each industry actually faces.</p>
      </div>
    </section>
    {''.join(sections)}
"""


# =========================================================================
# INTELLIGENCE PAGE
# =========================================================================
INTEL_PRODUCTS = [
    {
        "name": "Customized Intelligence Reports",
        "lede": "Tailored analytical products designed to meet your specific operational, sectoral, and geographic intelligence needs.",
        "body": [
            "The reports are tailored analytical products designed to meet the specific operational, sectoral, and geographic intelligence needs of each client. These reports are developed using a structured intelligence methodology that integrates verified open-source intelligence, field insights, and contextual analysis to ensure accuracy, relevance, and reliability.",
            "Each report is carefully designed to support executive leadership, security teams, and decision-makers with actionable intelligence that directly informs strategy, planning, and operational execution. The reports also include trend analysis, forecasting, and scenario-based evaluations to support forward-looking risk management."
        ],
        "image_seed": "intel-custom"
    },
    {
        "name": "Political & Country Risk Analysis",
        "lede": "In-depth evaluation of geopolitical, governance, regulatory, and security conditions that may impact your operations, investments, and strategic decisions.",
        "body": [
            "Political & Country Risk Analysis provides in-depth evaluation of geopolitical, governance, regulatory, and security conditions that may impact business operations, investments, and strategic decision-making. This service examines both current developments and emerging trends within a country or region to provide a comprehensive understanding of the operating environment.",
            "Key focus areas include political stability, electoral processes, government transitions, civil unrest, policy shifts, and regulatory frameworks. The analysis also assesses macro-level risks such as economic volatility, corruption exposure, and institutional strength, alongside localized risks including protests, conflict dynamics, and social instability. Scenario modeling and forecasting techniques are applied to anticipate potential developments and their implications for organizations.",
            "This service supports investors, corporations, NGOs, and government entities in making informed decisions regarding market entry, expansion, or continuity of operations. It helps clients understand not only the current risk landscape but also how evolving political conditions may influence long-term strategic objectives."
        ],
        "image_seed": "intel-country"
    },
    {
        "name": "Daily Monitoring Briefs",
        "lede": "Concise, timely, intelligence-driven updates on the critical developments affecting your operational and risk environment.",
        "body": [
            "The briefs provide concise, timely, and intelligence-driven updates on critical developments affecting clients' operational and risk environments. Each briefing consolidates relevant updates from multiple verified sources and presents them in a structured, easy-to-read format.",
            "Coverage typically includes breaking security incidents, political developments, regulatory updates, sector-specific alerts, and regional or global risk highlights. The briefs function as an early warning mechanism, enhancing organizational readiness and responsiveness in dynamic environments."
        ],
        "image_seed": "intel-daily"
    },
    {
        "name": "Situational Risk Analysis",
        "lede": "Real-time, incident-driven assessments of evolving threats and operational conditions — with mitigation guidance, not just analysis.",
        "body": [
            "Delivers real-time, incident-driven assessments of evolving threats and operational conditions that may affect organizations, assets, or personnel. This service focuses on analyzing specific events or emerging situations to determine their immediate and potential future impact on business continuity and security posture. Each analysis evaluates the nature of the incident, its severity, escalation potential, and geographic or sectoral implications.",
            "A key component of this service is the provision of mitigation guidance, offering clear recommendations to reduce exposure, manage risk, and ensure operational continuity. This may include advisory on movement restrictions, asset protection measures, communication protocols, or contingency planning."
        ],
        "image_seed": "intel-situational"
    },
    {
        "name": "Risk Heat Map",
        "lede": "A visual intelligence tool to identify, prioritize, and manage risks based on likelihood and potential impact — across geographies, business units, or sectors.",
        "body": [
            "The Risk Heat Map is a visual intelligence tool designed to help organizations identify, prioritize, and manage risks based on their likelihood and potential impact. It is customized to reflect geographic regions, business units, or industry-specific risk profiles, offering flexibility for diverse organizational needs.",
            "By providing a clear, at-a-glance overview of risk exposure, the Risk Heat Map enhances strategic planning, resource allocation, and executive decision-making. It enables leadership teams to focus attention and resources where they are needed most, improving overall resilience and risk governance."
        ],
        "image_seed": "intel-heatmap",
        "cta": {"href": "/intelligence/heat-map/", "label": "Open the Africa Risk Heat Map →"}
    }
]


def _intelligence_body():
    blocks = []
    for idx, p in enumerate(INTEL_PRODUCTS, 1):
        body_html = ''.join(f'<p>{para}</p>' for para in p['body'])
        cta_html = ''
        if 'cta' in p:
            cta_html = f'<div class="mt-5"><a href="{p["cta"]["href"]}" class="btn btn--primary">{p["cta"]["label"]}</a></div>'
        reverse_class = ' split--reverse' if idx % 2 == 0 else ''
        blocks.append(f'''
        <article class="product-block">
          <div class="container">
            <div class="split{reverse_class}">
              <div class="reveal">
                <span class="eyebrow">Product {idx:02d}</span>
                <h2 style="margin-top:var(--s-3);margin-bottom:var(--s-4);">{p['name']}</h2>
                <p class="lede mb-5">{p['lede']}</p>
                {body_html}
                {cta_html}
              </div>
              <div class="product-preview reveal" data-delay="1">
                <img src="https://picsum.photos/seed/{p['image_seed']}/800/1000" alt="" loading="lazy">
                <span class="stamp">CLASSIFIED · GTS · {idx:03d}</span>
              </div>
            </div>
          </div>
        </article>''')

    tiers = '''
        <div class="tiers">
          <div class="tier reveal" data-delay="1">
            <div class="tier__name">Standard</div>
            <div class="tier__price">On request</div>
            <ul class="tier__features">
              <li>Weekly country risk briefs</li>
              <li>Sector alerts (one sector)</li>
              <li>Quarterly Risk Heat Map</li>
              <li>Email delivery</li>
            </ul>
            <a href="/contact/" class="btn btn--secondary btn--block">Discuss</a>
          </div>
          <div class="tier tier--featured reveal" data-delay="2">
            <div class="tier__name">Corporate</div>
            <div class="tier__price">On request</div>
            <ul class="tier__features">
              <li>Daily monitoring briefs</li>
              <li>Customized country reports (4 / year)</li>
              <li>Situational risk analysis on call</li>
              <li>Risk Heat Map subscriber access</li>
              <li>Quarterly executive briefing</li>
            </ul>
            <a href="/contact/" class="btn btn--primary btn--block">Discuss</a>
          </div>
          <div class="tier reveal" data-delay="3">
            <div class="tier__name">Executive</div>
            <div class="tier__price">On request</div>
            <ul class="tier__features">
              <li>Everything in Corporate</li>
              <li>Embedded intelligence analyst</li>
              <li>Bespoke deep-dive reports</li>
              <li>Crisis response advisory</li>
              <li>Direct line to Head of Intelligence</li>
            </ul>
            <a href="/contact/" class="btn btn--secondary btn--block">Discuss</a>
          </div>
        </div>
'''

    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Intelligence Advisory</span>
        <h1>Foresight. Verified. Delivered.</h1>
        <p class="lede">Five intelligence products — built around a structured methodology that fuses verified open-source intelligence, field insights, and contextual analysis. Designed for the decisions you actually have to make.</p>
      </div>
    </section>
    {''.join(blocks)}

    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head centered reveal">
          <span class="eyebrow">Subscriptions</span>
          <h2>Three tiers. Built around how you'll use the intelligence.</h2>
          <p class="lede">Each tier scales delivery cadence, depth, and analyst access. Pricing is calibrated to scope — request a tailored proposal.</p>
        </div>
        {tiers}
      </div>
    </section>
"""


# =========================================================================
# HEAT MAP PAGE — separate template (no CTA band)
# =========================================================================
def _heatmap_body():
    return """
    <section class="heatmap-page">
      <div class="heatmap-bar">
        <div class="heatmap-bar__title">
          AFRICA RISK HEAT MAP
          <small class="mono">Q2 2026 EDITION · UPDATED 15 APR 2026</small>
        </div>
        <div class="heatmap-bar__legend" role="legend" aria-label="Risk level legend">
          <span class="chip chip--risk chip--risk-low">Low</span>
          <span class="chip chip--risk chip--risk-moderate">Moderate</span>
          <span class="chip chip--risk chip--risk-elevated">Elevated</span>
          <span class="chip chip--risk chip--risk-high">High</span>
          <span class="chip chip--risk chip--risk-extreme">Extreme</span>
          <span class="chip chip--risk chip--risk-na">No Data</span>
        </div>
      </div>

      <div class="container" style="padding-top:var(--s-4);padding-bottom:var(--s-4)">
        <div class="heatmap-tools">
          <input type="search" id="heatmap-search" placeholder="Search country or ISO…" aria-label="Search country">
          <select id="heatmap-region" aria-label="Filter by region">
            <option value="">All regions</option>
            <option value="East Africa">East Africa</option>
            <option value="West Africa">West Africa</option>
            <option value="Southern Africa">Southern Africa</option>
            <option value="Central Africa">Central Africa</option>
            <option value="North Africa">North Africa</option>
          </select>
          <select id="heatmap-risk" aria-label="Filter by risk level">
            <option value="">All risk levels</option>
            <option value="low">Low</option>
            <option value="moderate">Moderate</option>
            <option value="elevated">Elevated</option>
            <option value="high">High</option>
            <option value="extreme">Extreme</option>
          </select>
          <a href="/contact/" class="btn btn--secondary btn--small" style="margin-left:auto">Subscribe →</a>
        </div>
      </div>

      <div class="heatmap-body">
        <div class="heatmap-canvas" id="heatmap-canvas">
          <!-- Africa simplified tile grid rendered by JS -->
        </div>

        <aside class="heatmap-dossier" id="heatmap-dossier" aria-live="polite">
          <div class="empty">
            <span class="eyebrow eyebrow--bare">Dossier panel</span>
            <p>Select a country on the map to view its risk dossier — overview, key risks, outlook, and recommendations.</p>
          </div>
        </aside>
      </div>

      <div class="heatmap-tooltip" id="heatmap-tooltip" role="tooltip" aria-hidden="true"></div>
    </section>
"""


# =========================================================================
# INSIGHTS INDEX + POST PAGES
# =========================================================================
def _insights_index_body(posts):
    featured = next((p for p in posts if p.get('featured')), posts[0])
    others = [p for p in posts if p['slug'] != featured['slug']]

    other_cards = ''
    for p in others:
        other_cards += f'''<a class="post-card" href="{p['file']}">
            <div class="post-card__cover"><img src="https://picsum.photos/seed/{p['slug']}/800/500" alt="" loading="lazy"></div>
            <div class="post-card__body">
              <div class="post-card__meta">
                <span class="post-card__cat">{p['category']}</span><span>·</span>
                <span>{_format_date(p['date'])}</span><span>·</span><span>{p['read_time']}</span>
              </div>
              <h3 class="post-card__title">{p['title']}</h3>
              <p class="post-card__excerpt">{p['excerpt']}</p>
              <span class="post-card__readlink">Read →</span>
            </div>
          </a>'''

    cats = sorted(set(p['category'] for p in posts))
    chips_html = '<a class="chip is-active" data-cat="">All</a>' + ''.join(
        f'<a class="chip" data-cat="{c}">{c}</a>' for c in cats
    )

    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Insights</span>
        <h1>From the GTS Intelligence Desk.</h1>
        <p class="lede">Short-form intelligence, sector analysis, and methodology pieces from our analysts and practitioners — written for the people who have to act on it.</p>
        <div style="display:flex;gap:var(--s-3);flex-wrap:wrap;margin-top:var(--s-6)">
          <input type="search" class="field__input" id="insights-search" placeholder="Search insights..." aria-label="Search insights" style="min-width:280px;padding:14px 16px;border:1px solid var(--color-border);border-radius:var(--r-sm);background:var(--color-surface-2)">
        </div>
        <div style="display:flex;gap:var(--s-2);flex-wrap:wrap;margin-top:var(--s-5)" id="insights-filters">
          {chips_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <article class="featured-post reveal">
          <div class="featured-post__cover">
            <img src="https://picsum.photos/seed/{featured['slug']}/1000/750" alt="" loading="lazy">
          </div>
          <div>
            <div class="featured-post__meta">
              <span style="color:var(--color-gold)">{featured['category']}</span><span>·</span>
              <span>{_format_date(featured['date'])}</span><span>·</span>
              <span>{featured['read_time']}</span>
            </div>
            <h2>{featured['title']}</h2>
            <p>{featured['excerpt']}</p>
            <a href="{featured['file']}" class="btn btn--secondary">Read the full brief →</a>
          </div>
        </article>

        <div class="grid grid--3 reveal" id="insights-grid">
          {other_cards}
        </div>
      </div>
    </section>
"""


def _format_date(iso):
    # iso = "2026-05-12" → "12 May 2026"
    import datetime
    d = datetime.date.fromisoformat(iso)
    return d.strftime('%-d %b %Y') if os.name != 'nt' else d.strftime('%#d %b %Y')


def _post_page_body(post, all_posts):
    body_html = post['body_html']
    related = [p for p in all_posts if p['slug'] != post['slug']][:3]
    related_cards = ''.join(
        f'''<a class="post-card" href="{r['file']}">
          <div class="post-card__cover"><img src="https://picsum.photos/seed/{r['slug']}/800/500" alt="" loading="lazy"></div>
          <div class="post-card__body">
            <div class="post-card__meta"><span class="post-card__cat">{r['category']}</span></div>
            <h3 class="post-card__title">{r['title']}</h3>
            <p class="post-card__excerpt">{r['excerpt']}</p>
          </div>
        </a>''' for r in related
    )

    initials = ''.join(w[0] for w in post['author'].split()[:2]).upper()

    return f"""
    <article>
      <section class="post-hero">
        <div class="post-hero__media" aria-hidden="true">
          <img src="https://picsum.photos/seed/{post['slug']}/1920/900" alt="" loading="eager">
        </div>
        <div class="container post-hero__inner reveal">
          <div class="service-hero__crumbs">
            <a href="/">Home</a> <span class="sep">/</span>
            <a href="/insights/">Insights</a> <span class="sep">/</span>
            <span>{post['category']}</span>
          </div>
          <span class="eyebrow">{post['category']}</span>
          <h1 style="margin:var(--s-4) 0">{post['title']}</h1>
          <div class="post-hero__meta">
            <span class="cat">{post['author']}</span>
            <span>·</span>
            <span>{_format_date(post['date'])}</span>
            <span>·</span>
            <span>{post['read_time']}</span>
          </div>
        </div>
      </section>

      <div class="post-body drop-cap">
        <div class="author">
          <div class="author__avatar">{initials}</div>
          <div>
            <div class="author__name">{post['author']}</div>
            <div class="author__role">{post.get('author_role', 'GTS Intelligence Desk')}</div>
          </div>
        </div>

        {body_html}

        <div class="share" aria-label="Share this post">
          <span style="font-family:var(--font-mono);font-size:var(--t-xs);letter-spacing:.12em;color:var(--color-ink-low)">SHARE:</span>
          <a href="#" aria-label="Share to LinkedIn"><svg class="icon icon--sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="1"/><line x1="8" y1="10" x2="8" y2="17"/><circle cx="8" cy="7" r="0.5"/><path d="M12 17v-4a2 2 0 1 1 4 0v4"/><line x1="12" y1="10" x2="12" y2="17"/></svg></a>
          <a href="#" aria-label="Share to X"><svg class="icon icon--sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 4l7 9-7 7h3l5.5-5.5L17 20h3l-7.5-9.5L19.5 4H17l-5 5L8 4H4Z"/></svg></a>
          <a href="mailto:?subject={post['title']}" aria-label="Email"><svg class="icon icon--sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="5" width="18" height="14"/><path d="M3 5l9 8 9-8"/></svg></a>
        </div>
      </div>

      <section class="section section--surface-1">
        <div class="container">
          <div class="section-head">
            <span class="eyebrow">Related Briefs</span>
            <h2>Continue reading.</h2>
          </div>
          <div class="grid grid--3">{related_cards}</div>
        </div>
      </section>
    </article>
"""


# =========================================================================
# CAREERS
# =========================================================================
def _careers_body(jobs):
    rows = ''
    for j in jobs:
        rows += f'''<a class="job-row" href="#job-{j['id']}" data-job="{j['id']}">
          <div class="job-row__title">{j['title']}</div>
          <div class="job-row__dept">{j['department']}</div>
          <div class="job-row__loc">{j['location']}</div>
          <div class="job-row__cta">View role →</div>
        </a>'''

    jobs_jsonld = []
    for j in jobs:
        jobs_jsonld.append(f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "JobPosting",
  "title": "{j['title']}",
  "description": "{j.get('description_short', j['title'])}",
  "hiringOrganization": {{
    "@type": "Organization",
    "name": "GTS Risk Advisory",
    "sameAs": "https://gtsriskadvisory.com"
  }},
  "jobLocation": {{
    "@type": "Place",
    "address": {{ "@type": "PostalAddress", "addressLocality": "{j['location']}", "addressCountry": "KE" }}
  }},
  "employmentType": "{j['type'].upper()}",
  "datePosted": "{j['posted']}"
}}
</script>''')

    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Careers</span>
        <h1>Build a career in security and intelligence.</h1>
        <p class="lede">We hire experienced practitioners and high-calibre early-career talent who want to do work that matters — across operations, intelligence, and advisory practice. If you're considering your next move, we'd like to hear from you.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Why GTS</span>
          <h2>What you can expect.</h2>
        </div>
        <div class="grid grid--3 grid--lg">
          <div class="card reveal" data-delay="1">
            <span class="eyebrow">Practice</span>
            <h3 class="card__title">Senior practitioner culture.</h3>
            <p class="card__body">Working alongside people who've operated in the environments we advise on. Expect substantive mentorship, not slide reviews.</p>
          </div>
          <div class="card reveal" data-delay="2">
            <span class="eyebrow">Scope</span>
            <h3 class="card__title">Continental reach.</h3>
            <p class="card__body">Engagements across East, Southern, West, and North Africa. Travel where it adds value — never as a performance metric.</p>
          </div>
          <div class="card reveal" data-delay="3">
            <span class="eyebrow">Standards</span>
            <h3 class="card__title">Discretion and rigour.</h3>
            <p class="card__body">Both are non-negotiable here. The work we do for clients depends on both, and so does the professional reputation you build with us.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Open Roles</span>
          <h2>Currently hiring.</h2>
        </div>

        <div style="display:flex;gap:var(--s-3);flex-wrap:wrap;margin-bottom:var(--s-5)" id="job-filters">
          <select id="job-filter-dept" class="field__select" style="max-width:240px;padding:10px 16px;background:var(--color-surface-2);border:1px solid var(--color-border)" aria-label="Filter by department">
            <option value="">All departments</option>
            <option>Intelligence</option>
            <option>Consulting</option>
            <option>Operations</option>
          </select>
          <select id="job-filter-loc" class="field__select" style="max-width:240px;padding:10px 16px;background:var(--color-surface-2);border:1px solid var(--color-border)" aria-label="Filter by location">
            <option value="">All locations</option>
            <option>Nairobi</option>
            <option>East Africa</option>
          </select>
          <input type="search" id="job-filter-search" placeholder="Search roles..." style="flex:1;min-width:200px;padding:10px 16px;background:var(--color-surface-2);border:1px solid var(--color-border);color:var(--color-ink-high)" aria-label="Search roles">
        </div>

        <div class="job-list reveal" id="job-list">
          {rows}
        </div>

        <div class="text-center mt-7 reveal">
          <span class="eyebrow eyebrow--bare" style="margin-bottom:12px;display:block">— Don't see a fit?</span>
          <p style="margin-bottom:var(--s-4);color:var(--color-ink-mid)">We always want to hear from strong practitioners. Send your CV with a short note explaining where you'd add value.</p>
          <a href="mailto:careers@gtsriskadvisory.com?subject=General%20Application" class="btn btn--secondary">Submit a general application</a>
        </div>
      </div>
    </section>

    <!-- Application modal -->
    <div class="modal" id="job-modal" role="dialog" aria-modal="true" aria-labelledby="job-modal-title">
      <div class="modal__panel">
        <button class="modal__close" type="button" aria-label="Close">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>
        </button>
        <div id="job-modal-content"></div>
      </div>
    </div>

    {''.join(jobs_jsonld)}
"""


# =========================================================================
# MEDIA / GALLERY
# =========================================================================
GALLERY_ITEMS = [
    ("operations",  "gts-media-1",  "Field Operations · Nairobi"),
    ("training",    "gts-media-2",  "Crisis Response Drill · Mombasa"),
    ("events",      "gts-media-3",  "Corporate Event Security · Westlands"),
    ("operations",  "gts-media-4",  "Command Centre · Nairobi"),
    ("training",    "gts-media-5",  "Investigator Training · Naivasha"),
    ("events",      "gts-media-6",  "Conference Security · KICC"),
    ("operations",  "gts-media-7",  "Estate Patrol · Karen"),
    ("press",       "gts-media-8",  "Press Interview · Daily Nation"),
    ("training",    "gts-media-9",  "Manned Guarding Selection"),
    ("operations",  "gts-media-10", "Cash-in-transit Operations"),
    ("events",      "gts-media-11", "Government Summit Coverage"),
    ("press",       "gts-media-12", "Sector Report Launch"),
]

PRESS_MENTIONS = [
    ("Business Daily", "GTS Risk Advisory leads African private-sector security growth.", "12 Mar 2026"),
    ("The Standard",   "Boutique consultancies reshape East Africa's risk landscape.",   "22 Feb 2026"),
    ("Capital FM",     "Q&A: Inside Africa's intelligence-driven security shift.",       "08 Feb 2026"),
    ("The East African","M&A risk in East Africa — the GTS view.",                       "29 Jan 2026"),
]


def _media_body():
    items = ''
    for cat, seed, caption in GALLERY_ITEMS:
        items += f'''<div class="gallery__item is-visible" data-cat="{cat}" data-caption="{caption}">
          <img src="https://picsum.photos/seed/{seed}/800/600" alt="{caption}" loading="lazy">
          <div class="gallery__caption">{caption}</div>
        </div>'''

    press = ''
    for pub, headline, date in PRESS_MENTIONS:
        press += f'''<a class="job-row" href="#" style="grid-template-columns:200px 1fr 140px auto">
          <div class="job-row__title" style="font-family:var(--font-mono);font-size:var(--t-eyebrow);letter-spacing:.16em;color:var(--color-gold);text-transform:uppercase">{pub}</div>
          <div class="job-row__title" style="font-weight:400">{headline}</div>
          <div class="job-row__loc">{date}</div>
          <div class="job-row__cta">Read →</div>
        </a>'''

    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Media</span>
        <h1>In the field, on the record.</h1>
        <p class="lede">A selection of operational, training, and event imagery — alongside selected press mentions and analyst commentary.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div style="display:flex;gap:var(--s-2);flex-wrap:wrap;margin-bottom:var(--s-6)" id="media-filters">
          <a class="chip is-active" data-filter="all">All</a>
          <a class="chip" data-filter="events">Events</a>
          <a class="chip" data-filter="operations">Operations</a>
          <a class="chip" data-filter="training">Training</a>
          <a class="chip" data-filter="press">Press</a>
        </div>

        <div class="gallery" id="media-gallery">
          {items}
        </div>
      </div>
    </section>

    <section class="section section--surface-1">
      <div class="container">
        <div class="section-head reveal">
          <span class="eyebrow">Press</span>
          <h2>Selected coverage and commentary.</h2>
        </div>
        <div class="job-list reveal">
          {press}
        </div>
      </div>
    </section>

    <!-- Lightbox -->
    <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image lightbox">
      <button class="lightbox__close" type="button" aria-label="Close lightbox">✕</button>
      <button class="lightbox__prev" type="button" aria-label="Previous image">‹</button>
      <button class="lightbox__next" type="button" aria-label="Next image">›</button>
      <img class="lightbox__img" id="lightbox-img" alt="">
      <div class="lightbox__caption" id="lightbox-caption"></div>
    </div>
"""


# =========================================================================
# CONTACT + THANK YOU + 404
# =========================================================================
def _contact_body(services, consulting):
    # Build the service dropdown
    options = ['<option value="" disabled selected>Select a service or consulting area</option>']
    options.append('<optgroup label="Services">')
    for s in services:
        options.append(f'<option value="{s["name"]}">{s["name"]}</option>')
    options.append('</optgroup>')
    options.append('<optgroup label="Consulting">')
    for c in consulting:
        options.append(f'<option value="{c["name"]}">{c["name"]}</option>')
    options.append('</optgroup>')
    options.append('<option value="General enquiry / not sure">General enquiry / not sure</option>')
    service_options = ''.join(options)

    return f"""
    <section class="page-hero">
      <div class="container page-hero__inner reveal">
        <span class="eyebrow">Contact</span>
        <h1>Discreet by default. Responsive by design.</h1>
        <p class="lede">For general enquiries, quote requests, or a confidential conversation about a specific situation — reach us through any of the channels below, or use the secure forms.</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="contact-grid">

          <div class="contact-info reveal">
            <div class="contact-info__block">
              <span class="label">Email</span>
              <a href="mailto:info@gtsriskadvisory.com" class="value" style="font-size:1.0625rem;text-decoration:none">info@gtsriskadvisory.com</a>
            </div>
            <div class="contact-info__block">
              <span class="label">Phone & WhatsApp</span>
              <a href="tel:+254000000000" class="value" style="font-size:1.0625rem;text-decoration:none">+254 XXX XXX XXX</a>
              <p style="font-size:var(--t-small);color:var(--color-ink-low)">Mon–Fri · 08:00–18:00 EAT · 24/7 desk for retained clients</p>
            </div>
            <div class="contact-info__block">
              <span class="label">Headquarters</span>
              <span class="value" style="font-size:1.0625rem">Nairobi, Kenya</span>
              <span class="mono">-1.2921° S, 36.8219° E</span>
            </div>
            <div class="contact-info__block">
              <span class="label">Operating Hours</span>
              <span class="value" style="font-size:1rem">Mon – Fri · 08:00 – 18:00 EAT</span>
              <span style="font-size:var(--t-small);color:var(--color-ink-mid)">Out-of-hours intelligence desk available to subscribers.</span>
            </div>
            <div class="contact-info__map" aria-label="Map of Nairobi headquarters location">
              <iframe src="https://www.openstreetmap.org/export/embed.html?bbox=36.78%2C-1.31%2C36.86%2C-1.27&amp;layer=mapnik&amp;marker=-1.2921%2C36.8219" title="Nairobi headquarters"></iframe>
            </div>
          </div>

          <div class="reveal" data-delay="1">
            <div class="tabs">
              <div class="tabs__list" role="tablist">
                <button class="tabs__tab is-active" type="button" role="tab" aria-selected="true" data-tab="general">General Enquiry</button>
                <button class="tabs__tab" type="button" role="tab" aria-selected="false" data-tab="quote">Request a Quote</button>
              </div>

              <div class="tabs__panel is-active" id="tab-general" role="tabpanel">
                <form action="https://formsubmit.co/info@gtsriskadvisory.com" method="POST" class="form" novalidate>
                  <input type="hidden" name="_subject" value="New General Enquiry — GTS Website">
                  <input type="hidden" name="_template" value="table">
                  <input type="hidden" name="_captcha" value="true">
                  <input type="hidden" name="_next" value="/contact/thank-you.html">
                  <input type="text" name="_honey" class="honeypot" autocomplete="off" tabindex="-1">

                  <div class="form-row">
                    <div class="field">
                      <input type="text" name="name" id="g-name" required placeholder=" " class="field__input">
                      <label for="g-name" class="field__label">Full name *</label>
                      <span class="field__error">Please enter your full name.</span>
                    </div>
                    <div class="field">
                      <input type="text" name="company" id="g-company" placeholder=" " class="field__input">
                      <label for="g-company" class="field__label">Company / Organization</label>
                    </div>
                  </div>

                  <div class="form-row">
                    <div class="field">
                      <input type="email" name="email" id="g-email" required placeholder=" " class="field__input">
                      <label for="g-email" class="field__label">Email *</label>
                      <span class="field__error">Please enter a valid email.</span>
                    </div>
                    <div class="field">
                      <input type="tel" name="phone" id="g-phone" placeholder=" " class="field__input">
                      <label for="g-phone" class="field__label">Phone</label>
                    </div>
                  </div>

                  <div class="field">
                    <textarea name="message" id="g-message" required placeholder=" " class="field__textarea"></textarea>
                    <label for="g-message" class="field__label">Message *</label>
                    <span class="field__error">Please add a brief message.</span>
                  </div>

                  <div class="form__actions">
                    <button type="submit" class="btn btn--primary">Send enquiry</button>
                    <p style="font-size:var(--t-xs);color:var(--color-ink-low);margin:0;flex:1;min-width:200px">Confidential. We typically respond within one business day.</p>
                  </div>
                </form>
              </div>

              <div class="tabs__panel" id="tab-quote" role="tabpanel">
                <form action="https://formsubmit.co/info@gtsriskadvisory.com" method="POST" class="form" novalidate>
                  <input type="hidden" name="_subject" value="New Quote Request — GTS Website">
                  <input type="hidden" name="_template" value="table">
                  <input type="hidden" name="_captcha" value="true">
                  <input type="hidden" name="_next" value="/contact/thank-you.html">
                  <input type="text" name="_honey" class="honeypot" autocomplete="off" tabindex="-1">

                  <div class="form-row">
                    <div class="field">
                      <input type="text" name="name" id="q-name" required placeholder=" " class="field__input">
                      <label for="q-name" class="field__label">Full name *</label>
                      <span class="field__error">Please enter your full name.</span>
                    </div>
                    <div class="field">
                      <input type="text" name="company" id="q-company" required placeholder=" " class="field__input">
                      <label for="q-company" class="field__label">Company / Organization *</label>
                      <span class="field__error">Please enter your organization.</span>
                    </div>
                  </div>
                  <div class="form-row">
                    <div class="field">
                      <input type="email" name="email" id="q-email" required placeholder=" " class="field__input">
                      <label for="q-email" class="field__label">Email *</label>
                      <span class="field__error">Please enter a valid email.</span>
                    </div>
                    <div class="field">
                      <input type="tel" name="phone" id="q-phone" required placeholder=" " class="field__input">
                      <label for="q-phone" class="field__label">Phone *</label>
                      <span class="field__error">Please enter a phone number.</span>
                    </div>
                  </div>
                  <div class="field field--select">
                    <select name="service" id="q-service" required class="field__select">
                      {service_options}
                    </select>
                    <label for="q-service" class="field__label">Service interest *</label>
                  </div>
                  <div class="form-row">
                    <div class="field">
                      <input type="text" name="scope" id="q-scope" required placeholder=" " class="field__input">
                      <label for="q-scope" class="field__label">Project scope (1 line) *</label>
                      <span class="field__error">Please add a brief scope.</span>
                    </div>
                    <div class="field field--select">
                      <select name="budget" id="q-budget" class="field__select">
                        <option value="" disabled selected>Optional</option>
                        <option>Not yet defined</option>
                        <option>&lt; USD 10,000</option>
                        <option>USD 10,000 – 50,000</option>
                        <option>USD 50,000 – 250,000</option>
                        <option>USD 250,000 +</option>
                      </select>
                      <label for="q-budget" class="field__label">Budget range</label>
                    </div>
                  </div>
                  <div class="form-row">
                    <div class="field field--select">
                      <select name="timeline" id="q-timeline" required class="field__select">
                        <option value="" disabled selected>Select timeline</option>
                        <option>Immediate (within 30 days)</option>
                        <option>1–3 months</option>
                        <option>3–6 months</option>
                        <option>6+ months / planning</option>
                      </select>
                      <label for="q-timeline" class="field__label">Timeline *</label>
                    </div>
                  </div>
                  <div class="field">
                    <textarea name="description" id="q-desc" required placeholder=" " class="field__textarea"></textarea>
                    <label for="q-desc" class="field__label">Brief description *</label>
                    <span class="field__error">Please add a brief description.</span>
                  </div>
                  <div class="form__actions">
                    <button type="submit" class="btn btn--primary">Request quote</button>
                    <p style="font-size:var(--t-xs);color:var(--color-ink-low);margin:0;flex:1;min-width:200px">Confidential. NDA available on request — we sign by default.</p>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>

        <div class="faq-row">
          <div class="faq reveal">
            <h4>How quickly do you respond?</h4>
            <p>Within one business day for new enquiries; same-day for retained clients during operating hours. Out-of-hours desk available to subscribers.</p>
          </div>
          <div class="faq reveal" data-delay="1">
            <h4>What information should I include?</h4>
            <p>The shorter version is better than the longer one. Tell us what you're trying to achieve, when, and where — we'll come back with questions.</p>
          </div>
          <div class="faq reveal" data-delay="2">
            <h4>Do you sign NDAs?</h4>
            <p>Yes — by default, for any conversation that involves substantive operational or commercial detail. Send us yours or use ours.</p>
          </div>
        </div>
      </div>
    </section>
"""


def _thankyou_body():
    return """
    <section class="fourohfour">
      <span class="eyebrow">Message received</span>
      <h1>Thank you. We'll be in touch.</h1>
      <p class="lede">Your message has reached the GTS intake desk. A team member will follow up — usually within one business day. For urgent matters, please call or WhatsApp the number on the contact page.</p>
      <div class="btn-group">
        <a href="/" class="btn btn--primary">Return to home</a>
        <a href="/insights/" class="btn btn--secondary">Read the latest brief →</a>
      </div>
    </section>
"""


def _404_body():
    return """
    <section class="fourohfour">
      <span class="eyebrow">Status: 404</span>
      <h1>This file appears to be classified — or missing.</h1>
      <p class="lede">The page you were looking for isn't where we expected to find it. Either it's been moved, retired, or — less likely — the link was redacted before it reached you. Either way, this is on us.</p>
      <div class="btn-group">
        <a href="/" class="btn btn--primary">Return to base <span class="arrow">→</span></a>
        <a href="/contact/" class="btn btn--secondary">Report a broken link</a>
      </div>
      <p class="mono" style="margin-top:var(--s-7);color:var(--color-ink-low);font-size:var(--t-xs);letter-spacing:.12em">REF: 404 · ROUTE NOT FOUND · -1.2921° S, 36.8219° E</p>
    </section>
"""


# =========================================================================
# RENDER ALL
# =========================================================================
def main():
    print("Building GTS site...")

    services = load_json('data/services.json')['services']
    consulting = load_json('data/consulting.json')['consulting']

    # ---- Service detail pages
    for idx, s in enumerate(services, 1):
        body = service_detail_body(s, kind='services', counter=idx, total=len(services))
        render(
            out_path=f"services/{s['slug']}/index.html",
            title=f"{s['name']} — GTS Risk Advisory",
            desc=s['meta_desc'],
            canonical=f"/services/{s['slug']}/",
            body=body,
            extra_head=_service_jsonld(s, 'Service'),
        )

    # ---- Consulting detail pages
    for idx, c in enumerate(consulting, 1):
        body = service_detail_body(c, kind='consulting', counter=idx, total=len(consulting))
        render(
            out_path=f"consulting/{c['slug']}/index.html",
            title=f"{c['name']} — GTS Risk Advisory",
            desc=c['meta_desc'],
            canonical=f"/consulting/{c['slug']}/",
            body=body,
            extra_head=_service_jsonld(c, 'ConsultingService'),
        )

    # ---- Services & Consulting index
    render('services/index.html',
           'Services & Products — GTS Risk Advisory',
           'Integrated security solutions across twelve operational and specialist service lines — calibrated to your operating environment.',
           '/services/', _services_index_body(services))
    render('consulting/index.html',
           'Customized Consulting — GTS Risk Advisory',
           'Independent counsel for boards, executives, and operators navigating complex risk environments across Africa.',
           '/consulting/', _consulting_index_body(consulting))

    # ---- Home
    render('index.html',
           'GTS Risk Advisory — Intelligence-Driven Security Across Africa',
           'A premier security and risk consulting firm delivering tailored protection, risk intelligence, and operational resilience across Kenya, East Africa, and the continent.',
           '/', _home_body(), extra_head=HOME_PRELOAD + HOME_JSONLD)

    # ---- About
    render('about/index.html',
           'About GTS Risk Advisory',
           'A premier security solutions provider delivering innovative, client-focused risk management across Kenya, East Africa, and the broader African continent.',
           '/about/', _about_body())

    # ---- Industries
    render('industries/index.html',
           'Industries We Serve — GTS Risk Advisory',
           'Sector-specific security and risk expertise across banking, manufacturing, insurance, NGOs, agriculture, hospitality, investment, education, parastatals, and county governments.',
           '/industries/', _industries_body())

    # ---- Intelligence
    render('intelligence/index.html',
           'Intelligence Advisory Center — GTS Risk Advisory',
           'Five intelligence products — customized reports, country risk analysis, daily monitoring, situational analysis, and the GTS Risk Heat Map for African markets.',
           '/intelligence/', _intelligence_body())

    # ---- Heat Map (no CTA band, custom JS)
    render('intelligence/heat-map/index.html',
           'Africa Risk Heat Map · Q2 2026 — GTS Risk Advisory',
           'Interactive Africa risk heat map — country-level risk dossiers, scores, key risks, outlook, and recommendations from the GTS Intelligence Desk.',
           '/intelligence/heat-map/', _heatmap_body(),
           extra_scripts='  <script src="/assets/js/heat-map.js" defer></script>',
           include_cta_band=False)

    # ---- Insights
    posts = load_json('data/posts.json')['posts']
    render('insights/index.html',
           'Insights — GTS Risk Advisory',
           'Intelligence briefs, sector analysis, and methodology pieces from the GTS Intelligence Desk — for the people who have to act on them.',
           '/insights/', _insights_index_body(posts),
           extra_scripts='  <script src="/assets/js/insights.js" defer></script>')

    # ---- Posts
    for p in posts:
        render(out_path=p['file'].lstrip('/'),
               title=f"{p['title']} — GTS Insights",
               desc=p['excerpt'],
               canonical=p['file'],
               body=_post_page_body(p, posts),
               extra_head=_article_jsonld(p))

    # ---- Careers
    jobs = load_json('data/jobs.json')['jobs']
    render('careers/index.html',
           'Careers — GTS Risk Advisory',
           'Build a career in security, intelligence, or risk consulting at GTS Risk Advisory. Current openings across Nairobi and East Africa.',
           '/careers/', _careers_body(jobs),
           extra_scripts='  <script src="/assets/js/careers.js" defer></script>')

    # ---- Media
    render('media/index.html',
           'Media & Gallery — GTS Risk Advisory',
           'Operational, training, and event imagery from GTS Risk Advisory, plus selected press coverage and analyst commentary.',
           '/media/', _media_body(),
           extra_scripts='  <script src="/assets/js/media.js" defer></script>')

    # ---- Contact
    render('contact/index.html',
           'Contact GTS Risk Advisory',
           'Reach the GTS team for general enquiries, quote requests, or a confidential conversation about a specific security or risk situation.',
           '/contact/', _contact_body(services, consulting),
           extra_scripts='  <script src="/assets/js/forms.js" defer></script>')

    # ---- Thank you
    render('contact/thank-you.html',
           'Thank you — GTS Risk Advisory',
           'Your message has reached the GTS intake desk. We will be in touch shortly.',
           '/contact/thank-you.html', _thankyou_body(),
           include_cta_band=False)

    # ---- 404
    render('404.html',
           '404 — GTS Risk Advisory',
           'The page you were looking for could not be found.',
           '/404.html', _404_body(),
           include_cta_band=False)

    print("Done.")


def _article_jsonld(post):
    return f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{post['title']}",
    "description": "{post['excerpt']}",
    "author": {{ "@type": "Organization", "name": "{post['author']}" }},
    "publisher": {{ "@type": "Organization", "name": "GTS Risk Advisory", "url": "https://gtsriskadvisory.com" }},
    "datePublished": "{post['date']}",
    "articleSection": "{post['category']}",
    "url": "https://gtsriskadvisory.com{post['file']}"
  }}
  </script>'''


if __name__ == '__main__':
    main()
