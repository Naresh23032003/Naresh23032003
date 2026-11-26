#!/usr/bin/env python3
"""Builds every SVG in assets/ from the data at the top of this file.

Edit a number or a status line here, run `python3 scripts/build_assets.py`,
and commit the regenerated SVGs. No dependencies beyond the standard library.

Rules every scene follows, so the page reads correctly everywhere:
- Each element is fully visible in its resting state. Animations only add
  motion on top (fill-mode `both` means a renderer without CSS animation
  still shows the finished frame).
- `prefers-reduced-motion` turns all motion off.
- Scenes are self-contained dark cards (the receipt is paper), so they sit
  well on both GitHub's light and dark themes.
- System font stacks only: SVGs loaded through <img> cannot fetch web fonts.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

BG = "#0A0D14"
EDGE = "#1E2532"
INK = "#E6EDF3"
MUTED = "#8B949E"
DIM = "#4B5563"

UPDATED = "nov 2026"

# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

STATUS = [
    # (glyph, name, state, colour, note)
    ("●", "AEGIS", "active", "#34D399", "self-healing incident ops, signed approvals"),
    ("●", "Nikki AI Companion", "active", "#34D399", "offline companion on a 6 GB GPU"),
    ("◐", "mcp-approval-gateway", "building", "#F59E0B", "every agent write waits for your OK"),
    ("◐", "IDR crypto-premium paper", "writing", "#F59E0B", "stablecoin–FX basis, open replication"),
    ("✓", "product-factory-skills", "shipped", "#818CF8", "8 agent skills, Claude Code plugin"),
    ("✓", "Churn ML system", "shipped", "#818CF8", "promotion gate, rollback, drift checks"),
]

CARDS = [
    dict(
        slug="aegis", accent="#F59E0B", kicker="AGENTIC INCIDENT OPS", title="AEGIS",
        desc=["Agents diagnose and fix live faults, but act only",
              "through a typed catalog, an OPA gate and signatures."],
        metric="0", label="paths from model output to a shell",
        tags=["LangGraph", "OPA", "Ed25519", "Next.js"], motif="pipeline",
    ),
    dict(
        slug="nikki", accent="#F472B6", kicker="LOCAL-FIRST COMPANION", title="Nikki",
        desc=["Chat, long-term memory, voice calls and WhatsApp,",
              "fully offline. Guards live in code, not in prompts."],
        metric="6 GB", label="GPU budget for the whole voice stack",
        tags=["FastAPI", "Ollama", "ChromaDB", "91 evals"], motif="wave",
    ),
    dict(
        slug="churn", accent="#34D399", kicker="PRODUCTION ML", title="Churn ML system",
        desc=["Feature store, promotion gate, registry rollback,",
              "and drift checks that know when not to retrain."],
        metric="1.66 ms", label="p95 serving latency over real HTTP",
        tags=["FastAPI", "scikit-learn", "PSI", "124 tests"], motif="chart",
    ),
    dict(
        slug="pocket-professor", accent="#22D3EE", kicker="VOICE-FIRST LEARNING", title="Pocket Professor",
        desc=["Turns YouTube and PDFs into spoken quizzes, graded",
              "by an LLM and scheduled with FSRS."],
        metric="<2.5 s", label="budget for spoken feedback",
        tags=["Expo", "Supabase", "Groq", "RLS"], motif="spaced",
    ),
    dict(
        slug="insight-pulse", accent="#FB923C", kicker="CLOUD INFRASTRUCTURE", title="Insight Pulse",
        desc=["A Next.js SaaS taken all the way to EKS: Terraform",
              "VPC, real Stripe webhooks, SHA-pinned deploys."],
        metric="0", label="rebuilds needed to roll back",
        tags=["Terraform", "EKS", "Actions", "Stripe"], motif="deploy",
    ),
    dict(
        slug="product-factory", accent="#A78BFA", kicker="AGENT SKILLS", title="product-factory",
        desc=["Eight skills that take a product from idea to launch",
              "in Claude Code, Codex, Copilot and Antigravity."],
        metric="8", label="skills, each with a cited method",
        tags=["Claude Code", "SKILL.md", "plugin"], motif="steps",
    ),
]

RECEIPT = [
    ("Nikki evals, no model", "91 / 91"),
    ("Nikki VRAM budget", "6 GB"),
    ("RVC latency / chunk", "2000→300 ms"),
    ("AEGIS MTTR", "21–136 s"),
    ("AEGIS cost / incident", "≤ $0.003"),
    ("Prompt-leak ablation", "0.8 → 0.0"),
    ("Trace queries used", "0 / 29"),
    ("Churn p95 latency", "1.66 ms"),
    ("Churn test suite", "124"),
]

TIMELINE = [
    # (when, org, role, current)
    ("earlier", "Royal Enfield · Tecnod8", "Razorpay internships", False),
    ("may 2024", "TVS Electronics", "ML intern · RAG on Bedrock", False),
    ("jul 2024", "Razorpay", "Product development intern", False),
    ("jan 2025", "Accenture", "AI decision science analyst", False),
    ("jun 2026", "VaultStack AI", "Forward deployed engineer", True),
]

# --------------------------------------------------------------------------
# Shared pieces
# --------------------------------------------------------------------------

REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def svg(w: int, h: int, label: str, body: str, style: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'fill="none" role="img" aria-label="{escape(label)}">\n'
        f"<title>{escape(label)}</title>\n"
        f"<style>\n.s{{font-family:{SANS}}} .m{{font-family:{MONO}}}\n{style}\n{REDUCED}\n</style>\n"
        f"{body}\n</svg>\n"
    )


def t(x, y, text, size, fill=INK, cls="s", weight=400, anchor="start", extra=""):
    return (
        f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" {extra}>{escape(text)}</text>'
    )


def frame(w, h, glow=None, grid=True, rx=20):
    parts = [
        "<defs>",
        f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="{rx}"/></clipPath>',
        '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
        '<path d="M40 0H0v40" stroke="#fff" stroke-opacity="0.035"/></pattern>',
    ]
    if glow:
        parts.append(
            f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
            f'<stop offset="0" stop-color="{glow}" stop-opacity="0.32"/>'
            f'<stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>'
        )
    parts.append("</defs>")
    parts.append(f'<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="{BG}"/>')
    if grid:
        parts.append(f'<rect width="{w}" height="{h}" fill="url(#grid)"/>')
    return "\n".join(parts)


def frame_end(w, h, rx=20):
    return f'</g>\n<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{rx}" stroke="{EDGE}"/>'


# --------------------------------------------------------------------------
# Hero
# --------------------------------------------------------------------------


def hero() -> str:
    w, h = 1200, 380
    chips = ["input", "deterministic router", "local model", "guards + policy", "act · answer · abstain"]
    cx, top, step, cw, ch = 840, 64, 60, 300, 40
    body = [frame(w, h)]
    body.append(
        '<defs><radialGradient id="a" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#6366F1" stop-opacity=".45"/>'
        '<stop offset="1" stop-color="#6366F1" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="b" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#22D3EE" stop-opacity=".30"/>'
        '<stop offset="1" stop-color="#22D3EE" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="ink" x1="72" y1="0" x2="620" y2="0" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#22D3EE"/><stop offset="1" stop-color="#A78BFA"/></linearGradient></defs>'
    )
    body.append('<ellipse class="da" cx="260" cy="60" rx="420" ry="220" fill="url(#a)"/>')
    body.append('<ellipse class="db" cx="1000" cy="360" rx="420" ry="220" fill="url(#b)"/>')
    body.append(t(72, 96, "~/naresh  ·  applied AI engineer & researcher", 20, MUTED, "m"))
    body.append(t(72, 190, "Naresh R", 88, INK, "s", 700, extra='letter-spacing="-2"'))
    body.append(t(72, 252, "I build AI that runs where the data lives,", 32, "#C9D1D9"))
    body.append(t(72, 296, "and makes it prove what it did.", 32, "url(#ink)", "s", 600))
    body.append(t(72, 342, "agents · retrieval · local-first LLMs · full stack", 18, DIM, "m"))
    # request path
    line_x = cx + 22
    body.append(
        f'<line x1="{line_x}" y1="{top + ch/2}" x2="{line_x}" y2="{top + step*4 + ch/2}" stroke="{EDGE}" stroke-width="2"/>'
    )
    for i, label in enumerate(chips):
        y = top + i * step
        body.append(
            f'<g class="chip">'
            f'<rect x="{cx}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="#0F1420" stroke="{EDGE}"/>'
            f'<circle cx="{line_x}" cy="{y + ch/2}" r="5" fill="#6366F1"/>'
            f"{t(cx + 44, y + 26, label, 17, '#C9D1D9', 'm')}</g>"
        )
    body.append(
        f'<circle r="6" fill="#22D3EE"><animateMotion dur="5s" repeatCount="indefinite" '
        f'keyPoints="0;1;1" keyTimes="0;0.8;1" calcMode="linear" path="M{line_x} {top + ch/2} V{top + step*4 + ch/2}"/></circle>'
    )
    body.append(frame_end(w, h))
    style = """
.da{animation:drift 16s ease-in-out infinite alternate}
.db{animation:drift 20s ease-in-out infinite alternate-reverse}
@keyframes drift{to{transform:translate(60px,30px)}}
.chip rect{animation:lit 5s ease-in-out infinite both}
@keyframes lit{0%,100%{stroke:#1E2532}10%{stroke:#22D3EE}26%{stroke:#1E2532}}
"""
    # per-chip delay on the rect, synced with the travelling dot
    for i in range(len(chips)):
        style += f".chip:nth-of-type({i+1}) rect{{animation-delay:{i*1.0 - 0.5:.1f}s}}\n"
    return svg(w, h, "Naresh R. I build AI that runs where the data lives, and makes it prove what it did.", "\n".join(body), style)


# --------------------------------------------------------------------------
# Status terminal
# --------------------------------------------------------------------------


def status() -> str:
    w = 1200
    row0, rstep = 176, 46
    h = row0 + rstep * len(STATUS) + 70
    body = [frame(w, h, grid=False)]
    body.append(f'<rect width="{w}" height="52" fill="#0F1420"/><line x1="0" y1="52" x2="{w}" y2="52" stroke="{EDGE}"/>')
    for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        body.append(f'<circle cx="{32 + i*24}" cy="26" r="7" fill="{c}" fill-opacity=".85"/>')
    body.append(t(w / 2, 32, "zsh — naresh status --now", 17, MUTED, "m", anchor="middle"))
    body.append(
        f'<g class="ln" style="animation-delay:.2s">{t(48, 106, "$", 21, "#34D399", "m")}'
        f'{t(76, 106, "naresh status --now", 21, INK, "m")}'
        f'{t(w-48, 106, f"# updated {UPDATED}", 19, DIM, "m", anchor="end")}</g>'
    )
    body.append(f'<line x1="48" y1="132" x2="{w-48}" y2="132" stroke="{EDGE}" stroke-dasharray="4 6"/>')
    for i, (g, name, state, col, note) in enumerate(STATUS):
        y = row0 + i * rstep
        body.append(
            f'<g class="ln" style="animation-delay:{0.7 + i*0.35:.2f}s">'
            f"{t(52, y, g, 21, col, 'm')}{t(86, y, name, 21, INK, 'm', 600)}"
            f"{t(460, y, state, 21, col, 'm')}{t(590, y, note, 21, MUTED, 'm')}</g>"
        )
    py = row0 + rstep * len(STATUS) + 18
    body.append(
        f'<g class="ln" style="animation-delay:{0.9 + len(STATUS)*0.35:.2f}s">{t(48, py, "$", 21, "#34D399", "m")}'
        f'<rect class="cur" x="76" y="{py-19}" width="12" height="24" fill="{INK}"/></g>'
    )
    body.append(frame_end(w, h, 14))
    style = """
.ln{animation:in .5s ease-out both}
@keyframes in{from{opacity:0;transform:translateY(6px)}}
.cur{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
"""
    label = "What I am working on now: " + "; ".join(f"{n} ({s}): {d}" for _, n, s, _, d in STATUS)
    return svg(w, h, label, "\n".join(body), style)


# --------------------------------------------------------------------------
# Project cards
# --------------------------------------------------------------------------


def motif(kind: str, a: str) -> str:
    x0, y0, x1, y1 = 470, 236, 752, 340  # drawing box
    out = []
    if kind == "pipeline":
        labels = ["detect", "triage", "diagnose", "plan", "gate", "execute", "verify"]
        n = len(labels)
        gap = (x1 - x0) / (n - 1)
        cy = 280
        out.append(f'<line x1="{x0}" y1="{cy}" x2="{x1}" y2="{cy}" stroke="{EDGE}" stroke-width="2"/>')
        for i in range(n):
            x = x0 + i * gap
            if labels[i] == "gate":
                out.append(f'<rect class="nd" style="animation-delay:{i*0.45:.2f}s" x="{x-11}" y="{cy-11}" width="22" height="22" '
                           f'transform="rotate(45 {x} {cy})" fill="{BG}" stroke="{a}" stroke-width="2.5"/>')
            else:
                out.append(f'<circle class="nd" style="animation-delay:{i*0.45:.2f}s" cx="{x}" cy="{cy}" r="8" fill="{BG}" stroke="{a}" stroke-width="2.5"/>')
        out.append(f'<circle r="5" fill="{a}"><animateMotion dur="3.15s" repeatCount="indefinite" path="M{x0} {cy} H{x1}"/></circle>')
        out.append(t(x0 + 4 * gap, cy + 42, "policy gate", 17, a, "m", anchor="middle"))
    elif kind == "wave":
        n = 22
        bw = (x1 - x0) / n
        for i in range(n):
            hgt = 18 + (abs((i * 37) % 11 - 5)) * 9
            x = x0 + i * bw
            out.append(
                f'<rect class="bar" style="animation-delay:{(i*0.13)%1.3:.2f}s" x="{x:.1f}" y="{288 - hgt/2:.1f}" '
                f'width="{bw*0.55:.1f}" height="{hgt}" rx="3" fill="{a}" fill-opacity="{0.45 + (i%3)*0.2:.2f}"/>'
            )
    elif kind == "chart":
        pts = [(0, 86), (30, 82), (60, 88), (90, 80), (120, 85), (150, 79), (180, 86), (210, 81), (240, 84), (282, 80)]
        d = "M" + " L".join(f"{x0 + x} {y0 + y}" for x, y in pts)
        out.append(f'<line x1="{x0}" y1="{y0+20}" x2="{x1}" y2="{y0+20}" stroke="{MUTED}" stroke-dasharray="6 6" stroke-opacity=".6"/>')
        out.append(t(x1, y0 + 10, "150 ms objective", 16, MUTED, "m", anchor="end"))
        out.append(f'<path class="draw" d="{d}" stroke="{a}" stroke-width="3" stroke-linejoin="round" pathLength="1"/>')
        out.append(f'<line x1="{x0}" y1="{y0+100}" x2="{x1}" y2="{y0+100}" stroke="{EDGE}"/>')
    elif kind == "spaced":
        xs = [0, 24, 52, 88, 136, 196, 270]
        cy = 286
        out.append(f'<line x1="{x0}" y1="{cy}" x2="{x0+282}" y2="{cy}" stroke="{EDGE}" stroke-width="2"/>')
        for i, dx in enumerate(xs):
            out.append(f'<circle class="nd" style="animation-delay:{i*0.5:.1f}s" cx="{x0+dx+6}" cy="{cy}" r="9" fill="{BG}" stroke="{a}" stroke-width="2.5"/>')
        out.append(t(x0 + 282, cy + 42, "review intervals grow", 16, MUTED, "m", anchor="end"))
    elif kind == "deploy":
        stages = ["commit", "build", "ECR", "EKS"]
        gap = (x1 - x0 - 60) / 3
        cy = 270
        out.append(f'<line x1="{x0+30}" y1="{cy}" x2="{x1-30}" y2="{cy}" stroke="{EDGE}" stroke-width="2"/>')
        for i, s in enumerate(stages):
            x = x0 + 30 + i * gap
            out.append(f'<rect x="{x-28}" y="{cy-18}" width="56" height="36" rx="8" fill="{BG}" stroke="{a}" stroke-width="2"/>')
            out.append(t(x, cy + 52, s, 16, MUTED, "m", anchor="middle"))
        out.append(f'<rect width="12" height="12" rx="2" fill="{a}" y="-6" x="-6"><animateMotion dur="3s" repeatCount="indefinite" path="M{x0+30} {cy} H{x1-30}"/></rect>')
    elif kind == "steps":
        n = 8
        gap = (x1 - x0) / (n - 1)
        cy = 280
        for i in range(n):
            x = x0 + i * gap
            if i < n - 1:
                out.append(f'<line x1="{x+10}" y1="{cy}" x2="{x+gap-10}" y2="{cy}" stroke="{EDGE}" stroke-width="2"/>')
            out.append(f'<circle class="nd" style="animation-delay:{i*0.35:.2f}s" cx="{x}" cy="{cy}" r="9" fill="{BG}" stroke="{a}" stroke-width="2.5"/>')
        out.append(t(x0, cy + 42, "signals", 16, MUTED, "m"))
        out.append(t(x1, cy + 42, "launch", 16, MUTED, "m", anchor="end"))
    return "\n".join(out)


def card(c: dict) -> str:
    w, h, a = 800, 440, c["accent"]
    body = [frame(w, h, glow=a)]
    body.append(f'<ellipse class="gl" cx="700" cy="40" rx="320" ry="200" fill="url(#glow)"/>')
    body.append(f'<rect x="0" y="0" width="{w}" height="4" fill="{a}"/>')
    body.append(t(48, 72, c["kicker"], 19, a, "m", 600, extra='letter-spacing="2"'))
    body.append(t(48, 130, c["title"], 50, INK, "s", 700, extra='letter-spacing="-1"'))
    body.append(t(48, 176, c["desc"][0], 23, MUTED))
    body.append(t(48, 208, c["desc"][1], 23, MUTED))
    body.append(t(48, 310, c["metric"], 64, a, "s", 700, extra='letter-spacing="-1"'))
    body.append(t(48, 346, c["label"], 20, "#C9D1D9"))
    body.append(motif(c["motif"], a))
    x = 48
    for tag in c["tags"]:
        tw = len(tag) * 11.2 + 28
        body.append(f'<rect x="{x}" y="374" width="{tw:.0f}" height="36" rx="18" fill="#111827" stroke="{EDGE}"/>')
        body.append(t(x + tw / 2, 398, tag, 17, "#C9D1D9", "m", anchor="middle"))
        x += tw + 10
    body.append(t(w - 48, 398, "open repo →", 18, a, "m", anchor="end"))
    body.append(frame_end(w, h))
    style = """
.gl{animation:breathe 7s ease-in-out infinite}
@keyframes breathe{50%{opacity:.55}}
.nd{animation:pop 3.2s ease-in-out infinite both}
@keyframes pop{0%,100%{fill:#0A0D14}15%{fill:currentColor}35%{fill:#0A0D14}}
.bar{transform-box:fill-box;transform-origin:center;animation:eq 1.3s ease-in-out infinite both}
@keyframes eq{50%{transform:scaleY(.35)}}
.draw{stroke-dasharray:1;animation:draw 5s ease-in-out infinite both}
@keyframes draw{0%{stroke-dashoffset:1}40%,100%{stroke-dashoffset:0}}
"""
    style = style.replace("currentColor", a)
    label = f"{c['title']}: {' '.join(c['desc'])} {c['metric']} {c['label']}."
    return svg(w, h, label, "\n".join(body), style)


# --------------------------------------------------------------------------
# Receipt
# --------------------------------------------------------------------------


def receipt() -> str:
    w = 600
    top, step = 236, 44
    h = top + step * len(RECEIPT) + 210
    paper, ink, faint = "#F4F1EA", "#1F2328", "#6E7781"
    teeth = 14

    def zig(y, down):
        pts = []
        for i in range(0, w + teeth, teeth):
            pts.append(f"{i} {y + (0 if (i // teeth) % 2 else (teeth/2 if down else -teeth/2))}")
        return pts

    top_edge = zig(8, True)
    bot_edge = zig(h - 8, False)
    d = "M" + " L".join(top_edge) + f" L{w} {h-8} " + " L".join(reversed(bot_edge)) + " Z"
    body = [f'<path d="{d}" fill="{paper}"/>']
    body.append(t(w / 2, 82, "RECEIPTS", 34, ink, "m", 700, "middle", 'letter-spacing="6"'))
    body.append(t(w / 2, 116, "claims you can check in the repos", 18, faint, "m", anchor="middle"))
    body.append(t(w / 2, 144, f"github.com/Naresh23032003 · {UPDATED}", 16, faint, "m", anchor="middle"))
    body.append(f'<line x1="40" y1="176" x2="{w-40}" y2="176" stroke="{ink}" stroke-dasharray="3 6"/>')
    body.append(t(40, 210, "ITEM", 16, faint, "m", 700))
    body.append(t(w - 40, 210, "VALUE", 16, faint, "m", 700, "end"))
    for i, (k, v) in enumerate(RECEIPT):
        y = top + 12 + i * step
        body.append(
            f'<g class="ln" style="animation-delay:{0.3 + i*0.22:.2f}s">{t(40, y, k, 21, ink, "m")}'
            f'{t(w-40, y, v, 21, ink, "m", 700, "end")}</g>'
        )
    y = top + step * len(RECEIPT) + 4
    body.append(f'<line x1="40" y1="{y}" x2="{w-40}" y2="{y}" stroke="{ink}" stroke-dasharray="3 6"/>')
    body.append(
        f'<g class="ln" style="animation-delay:{0.5 + len(RECEIPT)*0.22:.2f}s">'
        f'{t(40, y + 42, "TOTAL", 22, ink, "m", 700)}{t(w-40, y + 42, "every number has a file", 20, ink, "m", 700, "end")}</g>'
    )
    # barcode
    bx, by = 120, y + 76
    import random

    rnd = random.Random(23032003)
    x = bx
    while x < w - 120:
        bw = rnd.choice([2, 2, 3, 4, 6])
        body.append(f'<rect x="{x}" y="{by}" width="{bw}" height="54" fill="{ink}"/>')
        x += bw + rnd.choice([2, 3, 4])
    body.append(t(w / 2, by + 84, "unflattering numbers stay on the receipt", 15, faint, "m", anchor="middle"))
    style = """
.ln{animation:print .35s steps(4) both}
@keyframes print{from{opacity:0;transform:translateY(-8px)}}
"""
    label = "Receipts, claims checkable in the repositories: " + "; ".join(f"{k}: {v}" for k, v in RECEIPT)
    return svg(w, h, label, "\n".join(body), style)


# --------------------------------------------------------------------------
# Timeline
# --------------------------------------------------------------------------


def timeline() -> str:
    w, h = 1200, 300
    cy = 150
    n = len(TIMELINE)
    xs = [170 + i * (860 / (n - 1)) for i in range(n)]
    body = [frame(w, h)]
    body.append(
        '<defs><linearGradient id="tl" x1="170" y1="0" x2="1030" y2="0" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#4B5563"/><stop offset=".6" stop-color="#6366F1"/>'
        '<stop offset="1" stop-color="#22D3EE"/></linearGradient></defs>'
    )
    body.append(f'<line class="draw" x1="{xs[0]}" y1="{cy}" x2="{xs[-1]}" y2="{cy}" stroke="url(#tl)" stroke-width="3" pathLength="1"/>')
    for i, ((when, org, role, now), x) in enumerate(zip(TIMELINE, xs)):
        up = i % 2 == 0
        col = "#22D3EE" if now else ("#818CF8" if i else DIM)
        delay = 0.4 + i * 0.45
        body.append(f'<g class="nd" style="animation-delay:{delay:.2f}s">')
        if now:
            body.append(f'<circle class="ring" cx="{x}" cy="{cy}" r="16" stroke="{col}" stroke-width="2"/>')
        body.append(f'<circle cx="{x}" cy="{cy}" r="9" fill="{BG}" stroke="{col}" stroke-width="3"/>')
        ty = cy - 82 if up else cy + 52
        body.append(t(x, ty, when, 16, col, "m", 600, "middle", 'letter-spacing="1"'))
        body.append(t(x, ty + 30, org, 21, INK, "s", 700, "middle"))
        body.append(t(x, ty + 56, role, 17, MUTED, "s", 400, "middle"))
        body.append("</g>")
    body.append(frame_end(w, h))
    style = """
.draw{stroke-dasharray:1;animation:draw 2.4s ease-out both}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.nd{animation:in .6s ease-out both}
@keyframes in{from{opacity:0;transform:translateY(6px)}}
.ring{transform-box:fill-box;transform-origin:center;animation:ping 2.4s ease-out infinite}
@keyframes ping{0%{transform:scale(.6);opacity:1}100%{transform:scale(1.8);opacity:0}}
"""
    label = "Career path: " + "; ".join(f"{w_}: {o}, {r}" for w_, o, r, _ in TIMELINE)
    return svg(w, h, label, "\n".join(body), style)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero(),
        "now.svg": status(),
        "receipt.svg": receipt(),
        "path.svg": timeline(),
    }
    for c in CARDS:
        files[f"card-{c['slug']}.svg"] = card(c)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"wrote assets/{name} ({len(content):,} bytes)")


if __name__ == "__main__":
    main()
