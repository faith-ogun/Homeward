"""
Public landing page for the Homeward A2A agent.

This URL is the agent's A2A JSON-RPC endpoint. POST traffic from Prompt
Opinion hits this same path. A browser visiting it (GET) lands here, on
a static informational page that explains what Homeward is and where to
use it.
"""
from pathlib import Path

from starlette.requests import Request
from starlette.responses import HTMLResponse, Response

_STATIC_DIR = Path(__file__).parent / "static"
_LOGO_PATH = _STATIC_DIR / "logo.png"

GITHUB_URL = "https://github.com/faith-ogun/Homeward"
DEVPOST_URL = "https://agents-assemble.devpost.com/"
PROMPT_OPINION_URL = "https://app.promptopinion.ai"


_LANDING_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homeward — Post-Op Recovery Meets Pharmacogenomics</title>
<meta name="description" content="An A2A agent that monitors post-surgical recovery and flags pharmacogenomic medication risks, consultable from any clinician workspace in Prompt Opinion.">
<link rel="icon" type="image/png" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #F7F2E8;
    --bg-2: #FBF9F4;
    --ink: #1B2A20;
    --ink-2: #2A3B30;
    --muted: #6B7B70;
    --accent: #2F5C3E;
    --accent-soft: #DDEAD9;
    --line: #E5DECF;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  .container { max-width: 1080px; margin: 0 auto; padding: 0 28px; }

  /* ── Header ───────────────────────────────────────── */
  header {
    border-bottom: 1px solid var(--line);
    background: var(--bg);
    position: sticky;
    top: 0;
    z-index: 10;
    backdrop-filter: saturate(140%) blur(8px);
  }
  .nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0;
  }
  .brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 600;
    font-size: 22px;
    color: var(--ink);
    letter-spacing: -0.01em;
  }
  .brand img { width: 36px; height: 36px; border-radius: 8px; }
  .nav-links { display: flex; gap: 26px; align-items: center; }
  .nav-links a {
    color: var(--ink-2);
    font-size: 14px;
    font-weight: 500;
  }
  .nav-cta {
    padding: 9px 16px;
    border-radius: 999px;
    background: var(--ink);
    color: var(--bg) !important;
    font-size: 14px;
    font-weight: 500;
  }
  .nav-cta:hover { text-decoration: none; background: var(--accent); }

  /* ── Hero ─────────────────────────────────────────── */
  .hero { padding: 96px 0 72px; }
  .eyebrow {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 6px 12px;
    border-radius: 999px;
    margin-bottom: 24px;
  }
  h1.headline {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: clamp(40px, 6.4vw, 72px);
    line-height: 1.04;
    letter-spacing: -0.02em;
    margin: 0 0 24px;
    color: var(--ink);
    max-width: 880px;
  }
  h1.headline em {
    font-style: italic;
    color: var(--accent);
    font-weight: 400;
  }
  .lede {
    font-size: 19px;
    line-height: 1.6;
    color: var(--ink-2);
    max-width: 640px;
    margin: 0 0 36px;
  }
  .cta-row { display: flex; gap: 12px; flex-wrap: wrap; }
  .btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 14px 22px;
    border-radius: 999px;
    font-size: 15px;
    font-weight: 500;
    transition: transform .12s ease, background .12s ease;
  }
  .btn:hover { text-decoration: none; transform: translateY(-1px); }
  .btn-primary { background: var(--ink); color: var(--bg) !important; }
  .btn-primary:hover { background: var(--accent); }
  .btn-secondary {
    background: transparent;
    color: var(--ink) !important;
    border: 1px solid var(--ink);
  }
  .btn-secondary:hover { background: var(--ink); color: var(--bg) !important; }
  .btn .arrow { transition: transform .12s ease; }
  .btn:hover .arrow { transform: translateX(2px); }

  /* ── Stats strip ──────────────────────────────────── */
  .stats {
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
    background: var(--bg-2);
    padding: 40px 0;
  }
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 32px;
  }
  .stat .num {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 42px;
    font-weight: 500;
    color: var(--ink);
    line-height: 1;
    margin-bottom: 8px;
  }
  .stat .lbl { font-size: 14px; color: var(--muted); line-height: 1.45; }
  @media (max-width: 720px) {
    .stats-grid { grid-template-columns: 1fr; }
  }

  /* ── Skills section ───────────────────────────────── */
  .section { padding: 96px 0; }
  .section h2 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: clamp(30px, 4.4vw, 44px);
    line-height: 1.1;
    letter-spacing: -0.015em;
    margin: 0 0 16px;
    color: var(--ink);
    max-width: 720px;
  }
  .section .section-lede {
    font-size: 17px;
    color: var(--muted);
    max-width: 620px;
    margin: 0 0 56px;
  }
  .skills {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1px;
    background: var(--line);
    border: 1px solid var(--line);
    border-radius: 16px;
    overflow: hidden;
  }
  .skill {
    background: var(--bg-2);
    padding: 32px;
  }
  .skill .num {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 14px;
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.08em;
  }
  .skill h3 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: 22px;
    line-height: 1.2;
    margin: 8px 0 12px;
    color: var(--ink);
  }
  .skill p {
    font-size: 15px;
    color: var(--ink-2);
    margin: 0;
    line-height: 1.55;
  }
  @media (max-width: 720px) {
    .skills { grid-template-columns: 1fr; }
  }

  /* ── Endpoint callout ─────────────────────────────── */
  .callout {
    background: var(--ink);
    color: var(--bg);
    border-radius: 20px;
    padding: 56px;
    margin: 56px 0;
  }
  .callout .eyebrow {
    background: rgba(255,255,255,0.12);
    color: var(--accent-soft);
  }
  .callout h2 {
    font-family: 'Fraunces', Georgia, serif;
    font-weight: 500;
    font-size: 32px;
    line-height: 1.15;
    color: var(--bg);
    margin: 0 0 16px;
    max-width: 640px;
  }
  .callout p {
    font-size: 16px;
    color: rgba(247,242,232,0.78);
    max-width: 620px;
    margin: 0 0 28px;
  }
  .callout code {
    background: rgba(255,255,255,0.08);
    color: var(--accent-soft);
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.92em;
    font-family: 'SF Mono', 'Menlo', Consolas, monospace;
  }
  .callout .cta-row .btn-primary {
    background: var(--bg);
    color: var(--ink) !important;
  }
  .callout .cta-row .btn-primary:hover { background: var(--accent-soft); }
  .callout .cta-row .btn-secondary {
    color: var(--bg) !important;
    border-color: rgba(247,242,232,0.4);
  }
  .callout .cta-row .btn-secondary:hover {
    background: var(--bg);
    color: var(--ink) !important;
  }
  @media (max-width: 720px) {
    .callout { padding: 36px 28px; }
  }

  /* ── Footer ───────────────────────────────────────── */
  footer {
    border-top: 1px solid var(--line);
    padding: 48px 0;
    color: var(--muted);
    font-size: 14px;
  }
  .foot {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
  }
  .foot .brand { font-size: 18px; }
  .foot-links { display: flex; gap: 22px; }
  .foot-links a { color: var(--muted); }
</style>
</head>
<body>

<header>
  <div class="container nav">
    <a href="/" class="brand">
      <img src="/logo.png" alt="Homeward logo">
      Homeward
    </a>
    <nav class="nav-links">
      <a href="#what">What it does</a>
      <a href="{github}" target="_blank" rel="noopener">GitHub</a>
      <a href="#endpoint">Use in Prompt Opinion</a>
      <a href="{prompt_opinion}" target="_blank" rel="noopener" class="nav-cta">Open Prompt Opinion ↗</a>
    </nav>
  </div>
</header>

<main>

  <section class="hero">
    <div class="container">
      <span class="eyebrow">Agents Assemble · Healthcare AI</span>
      <h1 class="headline">Post-op recovery, <em>meets</em> pharmacogenomics.</h1>
      <p class="lede">
        Homeward is an A2A agent that monitors post-surgical recovery and flags
        pharmacogenomic medication risks. Consultable from any clinician
        workspace in Prompt Opinion. Live, deployed on Google Cloud Run, talking
        to a real FHIR server.
      </p>
      <div class="cta-row">
        <a href="{prompt_opinion}" target="_blank" rel="noopener" class="btn btn-primary">
          Consult Homeward in Prompt Opinion <span class="arrow">→</span>
        </a>
        <a href="{github}" target="_blank" rel="noopener" class="btn btn-secondary">
          View on GitHub
        </a>
      </div>
    </div>
  </section>

  <section class="stats">
    <div class="container stats-grid">
      <div class="stat">
        <div class="num">3rd</div>
        <div class="lbl">Leading cause of death worldwide is post-operative complication.<br>(Nepogodiev et al., Lancet 2019)</div>
      </div>
      <div class="stat">
        <div class="num">~99%</div>
        <div class="lbl">of people carry at least one actionable pharmacogenomic variant.<br>(Van Driest 2014; PREPARE 2023)</div>
      </div>
      <div class="stat">
        <div class="num">5</div>
        <div class="lbl">Skills in a single A2A agent: discharge, PGx review, recovery, escalation, FHIR action drafter.</div>
      </div>
    </div>
  </section>

  <section class="section" id="what">
    <div class="container">
      <h2>One agent. Five skills. The two blind spots, joined up.</h2>
      <p class="section-lede">
        Generic recovery agents miss the drug. Generic PGx tools miss the
        recovery. Homeward joins them at the patient level.
      </p>
      <div class="skills">
        <div class="skill">
          <div class="num">SKILL 01</div>
          <h3>Discharge Note Interpreter</h3>
          <p>Reads the discharge document and the patient's FHIR Procedure resource. Produces a structured recovery expectation: pain trajectory, mobility milestones, medication schedule, red-flag symptoms.</p>
        </div>
        <div class="skill">
          <div class="num">SKILL 02</div>
          <h3>Pharmacogenomic Medication Review</h3>
          <p>Pulls medications and the genomics report from FHIR. Parses CYP2D6, CYP2C19, CYP2C9, VKORC1, DPYD, UGT1A1 diplotypes. Cross-references CPIC. Enriches with ClinVar.</p>
        </div>
        <div class="skill">
          <div class="num">SKILL 03</div>
          <h3>Recovery Check-In Assessment</h3>
          <p>Compares reported symptoms against the procedure-specific timeline. Layers PGx context on top: uncontrolled pain may be drug-gene mismatch, not surgical complication.</p>
        </div>
        <div class="skill">
          <div class="num">SKILL 04</div>
          <h3>Escalation Summary Generator</h3>
          <p>Produces a single GREEN, AMBER, or RED clinical summary. Separate care-team and patient-facing language. Explicit reasoning. Recommended actions.</p>
        </div>
        <div class="skill" style="grid-column: 1 / -1;">
          <div class="num">SKILL 05</div>
          <h3>FHIR Action Drafter</h3>
          <p>The last mile. When a pharmacogenomic alternative is warranted, drafts FHIR R4 resources (MedicationRequest plus Communication) with <code style="background:var(--accent-soft);padding:2px 6px;border-radius:4px;font-family:'SF Mono',Menlo,monospace;font-size:0.92em;color:var(--accent);">status="draft"</code> and <code style="background:var(--accent-soft);padding:2px 6px;border-radius:4px;font-family:'SF Mono',Menlo,monospace;font-size:0.92em;color:var(--accent);">intent="proposal"</code>. Never auto-submits. Never auto-prescribes. The clinician reviews and approves.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="container" id="endpoint">
    <div class="callout">
      <span class="eyebrow">For the curious</span>
      <h2>This URL is an agent endpoint, not a website.</h2>
      <p>
        The page you are reading is a courtesy. The real Homeward lives at this same address as a JSON-RPC over HTTP A2A endpoint. Prompt Opinion sends authenticated <code>POST</code> traffic here; you are visiting with a <code>GET</code>, so you get this. To actually consult Homeward, open it inside a Prompt Opinion workspace.
      </p>
      <div class="cta-row">
        <a href="{prompt_opinion}" target="_blank" rel="noopener" class="btn btn-primary">
          Open Prompt Opinion <span class="arrow">→</span>
        </a>
        <a href="/.well-known/agent-card.json" class="btn btn-secondary">
          View agent card (JSON)
        </a>
      </div>
    </div>
  </section>

</main>

<footer>
  <div class="container foot">
    <a href="/" class="brand">
      <img src="/logo.png" alt="Homeward logo">
      Homeward
    </a>
    <div class="foot-links">
      <a href="{github}" target="_blank" rel="noopener">GitHub</a>
      <a href="{devpost}" target="_blank" rel="noopener">Devpost</a>
      <a href="/.well-known/agent-card.json">Agent card</a>
    </div>
    <div>Built for Agents Assemble · The Healthcare AI Endgame · 2026</div>
  </div>
</footer>

</body>
</html>
"""


async def landing_page(request: Request) -> HTMLResponse:
    html = (
        _LANDING_HTML
        .replace("{github}", GITHUB_URL)
        .replace("{devpost}", DEVPOST_URL)
        .replace("{prompt_opinion}", PROMPT_OPINION_URL)
    )
    return HTMLResponse(html)


async def logo_image(request: Request) -> Response:
    if not _LOGO_PATH.exists():
        return Response(status_code=404)
    return Response(
        content=_LOGO_PATH.read_bytes(),
        media_type="image/png",
        headers={"cache-control": "public, max-age=86400"},
    )


async def favicon(request: Request) -> Response:
    return await logo_image(request)
