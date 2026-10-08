#!/usr/bin/env python3
"""Build the shareable Scopezilla pages site for Beyond Data Cloud & MCP ARI 2026.

Reads data/*.json + selected outputs/*.md and writes a static site to site/:
  index.html  - one-page overview
  scope.html  - full scope (lanes, schedule, roster, gaps)
  docs.html   - source documents rendered from markdown

Pricing-free by design: commercials are not validated, so no dollar figures,
rates, or price bands are emitted. Run from the project root:
  python3 tools/build-pages.py
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"
DERIVE_HOURS = Path.home() / ".claude/plugins/cache/scopezilla-dev/scopezilla-dev/1.29.0/scripts/derive-hours.py"
GENERATED = "October 2026"

BENCHMARK_DISCLAIMER = (
    "This figure is benchmark-based, derived from the AI model's training data and general delivery "
    "patterns (not Salesforce-validated) — not a commitment. Final figures are confirmed through the "
    "applicable commercial agreement."
)


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


epics = load("epics.json")
estimates = {e["item_id"]: e for e in load("estimates.json")}
roadmap = load("roadmap.json")
roster = load("resource-plan.json")
comparison = load("estimate-comparison.json")
gaps = load("gaps.json")
efficiency = load("efficiency.json")

e = html.escape

# ---------------------------------------------------------------- hours
aug_hours = {
    r["resource_id"]: r["hours"] * r["count"]
    for r in json.loads(subprocess.check_output([sys.executable, str(DERIVE_HOURS), str(ROOT), "--json"]))["resources"]
}

ALLOC = {"full": 1.0, "half": 0.5, "quarter": 0.25}
# AI-native clock: phases 0-4 (Phase 5 is parallel track for MCP Next, not on critical path)
NATIVE_CLOCK = {0: 3, 1: 4, 2: 7, 3: 7, 4: 3}  # Per efficiency native_band compression


def phase_list(spec):
    spec = str(spec)
    if "-" in spec:
        a, b = spec.split("-")
        return list(range(int(a), int(b) + 1))
    if "," in spec:
        return [int(x) for x in spec.split(",")]
    return [int(spec)]


native_roster = comparison["lanes"]["quantum-leap"]["roster"]
native_hours = {
    r["resource_id"]: sum(NATIVE_CLOCK.get(p, 0) for p in phase_list(r["phases_active"])) * 40 * ALLOC[r["allocation"]] * r["count"]
    for r in native_roster
}

ps_rows = [r for r in roster if r["side"] == "ps"]
client_rows = [r for r in roster if r["side"] == "client"]
AUG_TOTAL = sum(aug_hours[r["resource_id"]] for r in ps_rows)

# Augmented hours: Traditional with ~10% efficiency gain (middle of 6-16% Low readiness band)
EFFICIENCY_GAIN = 0.10  # 10% = efficiency reduces hours to 90% of traditional
augmented_hours = {rid: hours * (1 - EFFICIENCY_GAIN) for rid, hours in aug_hours.items()}
AUGMENTED_TOTAL = sum(augmented_hours[r["resource_id"]] for r in ps_rows)

NATIVE_TOTAL = sum(native_hours.values())
CLIENT_TOTAL = 0  # Beyond has no client-side roles in resource-plan

# Short role-focus labels, condensed from each row's justification.
FOCUS = {
    "R01": "PM — both workstreams (Data 360 critical path + MCP Next parallel)",
    "R02": "SA — Data 360 workstream lead (topology, identity, activation)",
    "R03": "TA — MCP Next workstream lead (remediation + audit)",
    "R04": "Senior Dev — Data 360 critical-path integration load",
    "R05a": "Volume pod seat 1 — BigQuery sync, enrichment, connectors, Braze",
    "R05b": "Volume pod seat 2 — BigQuery sync, enrichment, connectors, Braze",
    "R06": "Senior MCP Dev — BBY US/Overstock fixes + BuyBuyBaby instrumentation",
    "R07": "QA Lead — both workstreams (remediation + compliance hardening)",
    "R08": "QA Engineer — Data 360 activation/paid-media/web/email volume",
    "R09": "Functional Consultant — Data 360 config/story authoring",
    "Q01": "Program Lead (core floor)",
    "Q02a": "Intent Architect — Data 360 (core floor)",
    "Q02b": "Intent Architect — MCP Next (core floor)",
    "Q03a": "Agent Orchestrator — Data 360",
    "Q03b": "Agent Orchestrator — MCP Next",
    "Q04": "Agent-amplified Developer — Data 360",
    "Q05": "QA Lead (agent-amplified, held flat)",
    "Q06": "QA Engineer (fractional, agent-assisted)",
    "Q07": "Functional Consultant (fractional, Phase 1-3)",
}

# ---------------------------------------------------------------- schedule
# Phase windows: Beyond has 6 phases (0-5); Phase 5 (MCP Next) is parallel_track: true
# Traditional lane uses all 24 weeks; AI-native compresses to 16-21 weeks
SCHEDULE = [
    # epic, phase, size, traditional start-end, native start-end, note
    ("E01", "5", "L", "1–20", "1–17", "P5 · MCP Next Remediation (parallel track, not on critical path)"),
    ("E02", "1", "L", "1–4", "1–4", "P1 · Data 360 Foundation + BigQuery sync"),
    ("E03", "2", "L", "5–11", "5–11", "P2 · Acxiom enrichment → E04"),
    ("E04", "2", "L", "8–11", "8–11", "P2 · MCP activation (after E03 identity)"),
    ("E05", "3", "L", "12–18", "12–18", "P3 · Paid media (5 ad platforms)"),
    ("E06", "3", "L", "12–18", "12–18", "P3 · Web experience (10 use cases)"),
    ("E07", "4", "L", "19–21", "19–21", "P4 · Email + Braze"),
]
# No milestones defined in Beyond data
MILESTONE_NOTE = "Beyond has no explicitly named milestones; phases stand as natural gates."
EPIC = {x["epic_id"]: x for x in epics}

PHASES = []
for p in roadmap:
    if not p.get("parallel_track"):  # Skip Phase 5 in the sequential phases display
        phases_active = p.get("phases_active", "")
        weeks = f"Wk {p['duration_weeks']}" if p.get("duration_weeks") else "TBD"
        PHASES.append((f"P{p['phase_number']}", p["phase_name"], weeks, p.get("duration_weeks", 0)))


def size_tag(size):
    cls = {"XS": "sz-s", "S": "sz-s", "M": "sz-m", "L": "sz-l", "XL": "sz-xl"}[size]
    return f'<span class="sz-tag sz-tag--{cls}">{size}</span>'


def conf_tag(conf):
    cls = "confirmed" if conf == "Confirmed" else "assumed"
    return f'<span class="sz-tag sz-tag--{cls}">{e(conf)}</span>'


def gantt(lane):
    total = 24 if lane == "aug" else 21
    rows = []
    for epic, phase, size, aug_range, native_range, note in SCHEDULE:
        if epic == "E01":  # Skip parallel track in main gantt
            continue
        range_str = aug_range if lane == "aug" else native_range
        s, f = map(int, range_str.split("–"))
        left = (s - 1) / total * 100
        width = (f - s + 1) / total * 100
        rows.append(
            f'<div class="g-row"><div class="g-lbl"><b>{epic}</b> {e(EPIC[epic]["epic_name"])}</div>'
            f'<div class="g-track"><div class="g-bar" style="left:{left:.2f}%;width:{width:.2f}%" '
            f'title="Wk {s}–{f}">{s}–{f}</div></div></div>'
        )
    ticks = "".join(f'<span style="left:{(w-0.5)/total*100:.2f}%">{w}</span>' for w in range(1, total + 1))
    return (
        f'<div class="g-wrap" style="--cols:{total}"><div class="g-row g-head"><div class="g-lbl">Epic</div>'
        f'<div class="g-track g-ticks">{ticks}</div></div>'
        f'<div class="g-body">{"".join(rows)}</div></div>'
    )


# ---------------------------------------------------------------- page shell
BASE_CSS = (ROOT / "tools/pages-base.css").read_text()
EXTRA_CSS = """<style>
  :root{--client-primary:#0B5FFF;}
  .sz-stats{grid-template-columns:repeat(auto-fit,minmax(130px,1fr));}
  .sz-stat-num{white-space:nowrap;font-size:34px;}
  .sz-tag--confirmed{background:var(--sf-ok-bg);color:var(--sf-ok);}
  .sz-tag--conditional{background:var(--ext-violet-95);color:var(--ext-violet-30);}
  .sz-tag--anchor{background:var(--sf-ok-bg);color:var(--sf-ok);}
  .sz-note{font-size:13px;color:var(--sf-text-weak);margin:var(--space-sm) 0 var(--space-md);}
  .sz-disclaimer{font-size:12px;font-style:italic;color:var(--sf-text-weak);border-left:3px solid var(--sf-cloud-80);padding:4px 12px;margin:var(--space-md) 0;}
  .sz-banner{background:var(--sf-warn-bg);border-left:4px solid var(--sf-warn);padding:var(--space-sm) var(--space-md);border-radius:var(--radius-sm);font-size:13px;margin:var(--space-md) 0;}
  .sz-lanes{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--space-md);}
  .sz-lane{background:#fff;border-radius:var(--radius-md);padding:var(--space-lg);box-shadow:var(--shadow-brand);border-top:4px solid var(--sf-neutral);}
  .sz-lane--anchor{border-top-color:var(--sf-ok);}
  .sz-lane--cond{border-top-color:var(--ext-violet);border-style:dashed;border-width:4px 0 0 0;}
  .sz-lane h3{font-size:18px;margin-bottom:4px;}
  .sz-lane .big{font-family:var(--font-heading);font-size:30px;color:var(--client-primary);margin:var(--space-sm) 0 0;}
  .sz-lane dl{font-size:13px;margin-top:var(--space-sm);}
  .sz-lane dt{color:var(--sf-text-weak);margin-top:6px;}
  .sz-lane dd{font-weight:600;}
  .num{text-align:right;white-space:nowrap;}
  tr.sz-total td{font-weight:700;background:#DCEBFF!important;}
  .g-wrap{background:#fff;border-radius:var(--radius-md);box-shadow:var(--shadow-brand);padding:var(--space-md);overflow-x:auto;}
  .g-row{display:flex;align-items:center;min-height:28px;}
  .g-lbl{flex:0 0 300px;font-size:12px;padding-right:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .g-track{position:relative;flex:1;height:22px;min-width:520px;background:repeating-linear-gradient(90deg,transparent 0,transparent calc(100%/var(--cols,24) - 1px),var(--sf-light-bg) calc(100%/var(--cols,24) - 1px),var(--sf-light-bg) calc(100%/var(--cols,24)));}
  .g-ticks{background:none;height:18px;}
  .g-ticks span{position:absolute;transform:translateX(-50%);font-size:10px;color:var(--sf-text-weak);}
  .g-bar{position:absolute;top:3px;height:16px;border-radius:3px;background:var(--sf-blue);color:#fff;font-size:10px;line-height:16px;text-align:center;overflow:hidden;}
  .g-bar--care{background:var(--sf-text-weak);}
  .g-body{position:relative;}
  .sz-filter button{font-size:12px;border:1px solid var(--sf-cloud-80);background:#fff;color:var(--sf-container);border-radius:999px;padding:3px 10px;margin:0 4px 6px 0;cursor:pointer;}
  .sz-filter button.on{background:var(--sf-container);color:#fff;}
  .sz-doc h1{font-size:26px;margin:var(--space-lg) 0 var(--space-sm);}
  .sz-doc h2{font-size:20px;margin:var(--space-lg) 0 var(--space-sm);}
  .sz-doc h3{font-size:16px;margin:var(--space-md) 0 var(--space-xs);}
  .sz-doc p,.sz-doc li{font-size:14px;margin-bottom:6px;}
  .sz-doc ul,.sz-doc ol{padding-left:22px;margin-bottom:var(--space-sm);}
  .sz-doc table{width:100%;border-collapse:collapse;margin:var(--space-sm) 0 var(--space-md);font-size:13px;background:#fff;}
  .sz-doc th{background:var(--sf-container);color:#fff;text-align:left;padding:6px 10px;}
  .sz-doc td{padding:6px 10px;border-top:1px solid var(--sf-light-bg);vertical-align:top;}
  .sz-doc blockquote{border-left:3px solid var(--sf-cloud-80);padding:4px 12px;color:var(--sf-text-weak);margin:var(--space-sm) 0;}
  .sz-doc code{font-size:12px;background:var(--sf-light-bg);padding:1px 4px;border-radius:3px;}
  .sz-topnav a{color:#fff;margin-right:var(--space-md);font-size:14px;}
  @media(max-width:860px){.sz-lanes{grid-template-columns:1fr;}}
</style>"""
LOGO = (ROOT / "tools/sf-logo.svg").read_text().strip()


def page(filename, title, subtitle, nav_groups, body):
    nav = []
    for label, links in nav_groups:
        items = "".join(f'<a href="{href}" class="sz-sidebar-link">{e(text)}</a>' for href, text in links)
        nav.append(f'<div class="sz-sidebar-group"><div class="sz-sidebar-label">{e(label)}</div>{items}</div>')
    close = "document.querySelector('.sz-sidebar').classList.remove('open');document.getElementById('sz-overlay').classList.remove('active');"
    opn = "document.querySelector('.sz-sidebar').classList.add('open');document.getElementById('sz-overlay').classList.add('active');"
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
{BASE_CSS}
{EXTRA_CSS}
</head>
<body>
<header class="sz-hero">
  <div class="sz-wrap" style="padding-top:0;padding-bottom:0;">
    <div class="sz-cobrand">{LOGO}<span class="sz-cobrand-x">×</span>
      <span style="font-family:var(--font-heading);font-size:22px;color:#fff;letter-spacing:0.04em;">BEYOND</span></div>
    <h1>{e(title)}</h1>
    <p>{subtitle}</p>
    <p class="sz-topnav" style="margin-top:var(--space-md);"><a href="index.html">Overview</a><a href="scope.html">Full scope</a><a href="docs.html">Source documents</a></p>
  </div>
</header>
<button class="sz-sidebar-toggle" aria-label="Open navigation" onclick="{opn}">&#9776;</button>
<div class="sz-overlay" id="sz-overlay" onclick="{close}"></div>
<nav class="sz-sidebar" aria-label="Section navigation">
  <div class="sz-sidebar-header"><span>Beyond Data Cloud &amp; MCP</span>
    <button class="sz-sidebar-close" aria-label="Close navigation" onclick="{close}">&#215;</button></div>
  {"".join(nav)}
</nav>
<main class="sz-wrap">
{body}
<hr class="sz-divider">
<p class="sz-note">Generated from the Scopezilla project data · {GENERATED} · Salesforce Professional Services · Internal scoping — pricing not included (commercials not yet validated).</p>
</main>
<script>
document.querySelectorAll('.sz-sidebar-link').forEach(function(a){{a.addEventListener('click',function(){{{close}}});}});
document.querySelectorAll('.sz-filter').forEach(function(f){{
  var tbl=document.getElementById(f.dataset.table);
  f.querySelectorAll('button').forEach(function(b){{b.addEventListener('click',function(){{
    f.querySelectorAll('button').forEach(function(x){{x.classList.remove('on');}});b.classList.add('on');
    tbl.querySelectorAll('tbody tr').forEach(function(tr){{tr.style.display=(b.dataset.cat==='all'||tr.dataset.cat===b.dataset.cat)?'':'none';}});
  }});}});
}});
</script>
</body>
</html>
"""
    (SITE / filename).write_text(out)


def section(sid, eyebrow, title, inner):
    return (
        f'<section id="{sid}" class="sz-section"><div class="sz-section-eyebrow">{e(eyebrow)}</div>'
        f'<h2 class="sz-section-title">{e(title)}</h2>{inner}</section>'
    )


def table(headers, rows, tid=None, row_attrs=None):
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = []
    for i, r in enumerate(rows):
        attrs = row_attrs[i] if row_attrs else ""
        body.append(f"<tr{attrs}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    idattr = f' id="{tid}"' if tid else ""
    return f'<table class="sz-table"{idattr}><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>'


# ---------------------------------------------------------------- shared blocks
STATS = [
    ("3", "Brands · BBY US, Overstock, BuyBuyBaby"),
    ("7", "Epics · E01-E07"),
    ("24", "Weeks · committed critical path (traditional)"),
    ("16–21", "Weeks · AI-Native (conditional)"),
    ("~70", "Gaps & open items"),
]
CHIPS = [
    "Data 360 foundation", "BigQuery sync (4 Customer Data Mesh tables)", "Identity resolution (email → Individual ID)",
    "Acxiom enrichment (~39 attributes)", "MCP personalization activation", "Paid media (Google, Facebook, Criteo, Pinterest, TikTok)",
    "Web experience (10 brand-neutral use cases)", "Email campaigns (7 use cases)", "Braze integration", "MCP Next remediation (BBY US, Overstock, BuyBuyBaby)",
]


def stats_html():
    return '<div class="sz-stats">' + "".join(
        f'<div class="sz-stat"><div class="sz-stat-num">{n}</div><div class="sz-stat-lbl">{e(l)}</div></div>' for n, l in STATS
    ) + "</div>"


def chips_html():
    return '<div class="sz-chips">' + "".join(f'<span class="sz-chip">{e(c)}</span>' for c in CHIPS) + "</div>"


SUMMARY = (
    "Beyond (BBY US, Overstock, BuyBuyBaby) runs mission-critical marketing and e-commerce operations across three brands. "
    "This scope fixes a live, undiagnosed MCP implementation while building a parallel Data 360 (Data Cloud) foundation "
    "to feed enriched, unified customer data into MCP and paid-media activation. Two concurrent tracks — MCP Next remediation "
    "and Data 360 build-out — on a shared 24-week waterfall calendar. The program adds Acxiom enrichment, 5 ad-platform connectors, "
    "web experience personalization, and Braze integration. The aim is a low-disruption, high-confidence remediation that upgrades "
    "Beyond's Salesforce footprint without service disruption."
)


def phases_html():
    cells = "".join(
        f'<div class="sz-phase" style="background:var(--sf-blue);"><div class="sz-phase-name">{pid} · {e(name)}</div>'
        f'<div class="sz-phase-wks">{weeks}</div></div>'
        for pid, name, weeks, _ in PHASES
    )
    return f'<div class="sz-timeline">{cells}</div>'


def epics_rows():
    rows = []
    for x in epics:
        est = estimates.get(x["epic_id"], {})
        rows.append([
            f'<b>{x["epic_id"]}</b>', e(x["epic_name"]), size_tag(est.get("t_shirt_size", "?")),
            conf_tag(est.get("confidence", "")), e(est.get("solution_approach", ""))[:260] + ("…" if len(est.get("solution_approach", "")) > 260 else ""),
        ])
    return rows


def adrs():
    decisions_dir = ROOT / "decisions"
    if not decisions_dir.exists():
        return []
    out = []
    for f in sorted(decisions_dir.glob("*.md")):
        lines = f.read_text().splitlines()
        title = lines[0].lstrip("# ").strip()
        meta = next((l for l in lines if l.startswith("**Date")), "")
        status = re.search(r"\*\*Status:\*\*\s*([^·]+)", meta)
        out.append((title, status.group(1).strip() if status else ""))
    return out


def lanes_html():
    L = comparison["lanes"]
    return f"""<div class="sz-lanes">
  <div class="sz-lane sz-lane--anchor"><h3>Traditional</h3><span class="sz-tag sz-tag--anchor">committed anchor</span>
    <div class="big">{L['traditional']['duration_weeks_range']} wk</div>
    <dl><dt>How</dt><dd>Standard delivery — offshore-weighted build pod, onshore senior oversight, phase-gated schedule</dd>
    <dt>PS effort</dt><dd>{AUG_TOTAL:,.0f} person-hrs on 24 committed working weeks</dd>
    <dt>Team</dt><dd>10 PS people · ~8.6 FTE program average</dd>
    <dt>Readiness</dt><dd>Live-production remediation + 3 open compliance gates → Low readiness (1/8)</dd></dl></div>
  <div class="sz-lane"><h3>Augmented</h3><span class="sz-tag">ai tooling</span>
    <div class="big">24 wk</div>
    <dl><dt>How</dt><dd>Same team as Traditional + AI tooling efficiency — faster code gen, assisted testing, smarter debugging</dd>
    <dt>PS effort</dt><dd>{AUGMENTED_TOTAL:,.0f} person-hrs on 24 committed working weeks (~10% efficiency gain)</dd>
    <dt>Team</dt><dd>10 PS people · ~7.7 FTE program average</dd>
    <dt>Readiness</dt><dd>Low readiness, same as Traditional — no org restructuring, proven path to AI-native</dd></dl></div>
  <div class="sz-lane sz-lane--cond"><h3>AI-Native</h3><span class="sz-tag sz-tag--conditional">conditional</span>
    <div class="big">{L['quantum-leap']['duration_weeks_range']} wk</div>
    <dl><dt>How</dt><dd>Senior-weighted team directing an agent fleet (core-accountability floor: 3 Intent Architects, 2 Agent Orchestrators)</dd>
    <dt>PS effort</dt><dd>{NATIVE_TOTAL:,.0f} person-hrs on 16–21 committed working weeks</dd>
    <dt>Team</dt><dd>9 PS people · ~7.3 FTE program average</dd>
    <dt>Readiness</dt><dd>Conditional — M1-M5 provisionally assumed yellow for a customer meeting; not evidenced</dd></dl></div>
</div>
<p class="sz-banner"><b>Three delivery options.</b> Traditional is the committed baseline. Augmented captures AI tooling gains without restructuring the team. AI-Native is conditional and requires customer commitment to an AI-native operating model.</p>
<p class="sz-disclaimer">{BENCHMARK_DISCLAIMER}</p>"""


def roster_rows():
    rows, attrs = [], []
    for r in ps_rows:
        rows.append([
            f'<b>{r["resource_id"]}</b>', e(r["role"]), e(FOCUS.get(r["resource_id"], "")),
            f'{r["seniority"]} · {r["location"]}', f'P{r["phases_active"]}', r["allocation"],
            f'<span class="num">{aug_hours[r["resource_id"]]:,.0f}</span>',
        ])
        attrs.append("")
    rows.append(["", "<b>Total</b>", f"{len(ps_rows)} PS people", "", "24 working wk", "", f'<span class="num">{AUG_TOTAL:,.0f}</span>'])
    attrs.append(' class="sz-total"')
    return rows, attrs


def native_rows():
    rows, attrs = [], []
    for r in native_roster:
        rows.append([
            f'<b>{r["resource_id"]}</b>', e(r["role"]), e(FOCUS.get(r["resource_id"], "")),
            f'{r["seniority"]} · {r["location"]}', f'P{r["phases_active"]}', r["allocation"],
            f'<span class="num">{native_hours[r["resource_id"]]:,.0f}</span>',
        ])
        attrs.append("")
    rows.append(["", "<b>Total</b>", f"{len(native_roster)} PS people", "", "16–21 working wk", "", f'<span class="num">{NATIVE_TOTAL:,.0f}</span>'])
    attrs.append(' class="sz-total"')
    return rows, attrs


def schedule_rows():
    rows = []
    for epic, phase, size, aug_range, native_range, note in SCHEDULE:
        rows.append([f"<b>{epic}</b>", e(EPIC[epic]["epic_name"]), size_tag(estimates[epic]["t_shirt_size"]), aug_range, native_range, e(note)])
    return rows


# ---------------------------------------------------------------- index.html
def build_index():
    adr_rows = [[e(t), e(s)] for t, s in adrs()]
    open_cats = ["Potential Risk", "Missing Requirement", "Source Conflict"]
    top = [g for g in gaps if g["category"] in open_cats and not g["gap_or_question"].startswith("[RESOLVED")][:12]
    body = "".join([
        section("overview", "Executive Summary", "Beyond Data Cloud & MCP ARI 2026 · Remediation + Build-Out",
                f'<div class="sz-tldr"><div class="sz-tldr-label">Summary</div><p>{SUMMARY}</p></div>{stats_html()}'
                f'<div style="margin-top:var(--space-lg);"><div class="sz-section-eyebrow" style="margin-bottom:var(--space-sm);">Capabilities in scope</div>{chips_html()}</div>'),
        '<hr class="sz-divider">',
        section("phases", "Delivery Plan", "6 phases · 24 committed working weeks (critical path)",
                phases_html() + '<p class="sz-note">Phase 5 (MCP Next Remediation) runs concurrently with Phases 1-4 as a separate 20-week track. Critical path = Phases 0–4 (24 wk) only. AI-Native compresses to 16–21 wk with the qualification gate and conditional delivery model.</p>'),
        '<hr class="sz-divider">',
        section("epics", "Scope", f"{len(epics)} epics · all T-shirt L",
            table(["Epic", "Name", "Size", "Confidence", "Approach"], epics_rows()) + '<p class="sz-note">Sizes show relative complexity (T-shirt sizes), not effort.</p>'),
        '<hr class="sz-divider">',
        section("lanes", "Delivery Options", "Traditional vs AI-Native (conditional)", lanes_html()),
        '<hr class="sz-divider">',
        section("architecture", "Architecture", "Key design decisions", table(["Decision", "Status"], adr_rows) if adr_rows else "<p>No ADRs yet.</p>"),
        '<hr class="sz-divider">',
        section("open-items", "Open Items", "Top risks & open requirements",
                table(["ID", "Category", "Question / risk"], [[g["gap_id"], e(g["category"]), e(g["gap_or_question"])] for g in top])
                + f'<p class="sz-note">{len(top)} of {len(gaps)} logged items shown. See the <a href="scope.html#gaps">full list</a>.</p>'),
    ])
    nav = [("Overview", [("#overview", "Executive Summary"), ("#phases", "Delivery Plan"), ("#epics", "Epics"),
                         ("#lanes", "Delivery Options"), ("#architecture", "Design Decisions"), ("#open-items", "Open Items")]),
           ("More", [("scope.html", "Full scope →"), ("staffing.html", "Staffing plan →"), ("docs.html", "Source documents →")])]
    page("index.html", "Beyond Data Cloud & MCP · ARI 2026",
         "Salesforce Professional Services &nbsp;·&nbsp; BBY US, Overstock, BuyBuyBaby · 3 brands · Scoping overview", nav, body)


# ---------------------------------------------------------------- scope.html
def build_scope():
    r_rows, r_attrs = roster_rows()
    n_rows, n_attrs = native_rows()
    client = [[f'<b>{r["resource_id"]}</b>', e(r["role"]), e(FOCUS.get(r["resource_id"], "")), f'P{r["phases_active"]}', r["allocation"]] for r in client_rows]
    cats = sorted({g["category"] for g in gaps})
    filt = '<div class="sz-filter" data-table="gap-table"><button class="on" data-cat="all">All ({})</button>{}</div>'.format(
        len(gaps), "".join(f'<button data-cat="{e(c)}">{e(c)} ({sum(1 for g in gaps if g["category"]==c)})</button>' for c in cats))
    gap_rows = [[g["gap_id"], e(g["category"]), e(g["gap_or_question"]), e(g.get("impact_or_notes", ""))] for g in gaps]
    gap_attrs = [f' data-cat="{e(g["category"])}"' for g in gaps]
    eff = efficiency.get("project_level", {})
    scen = efficiency.get("readiness", {}).get("scenarios", [])
    eff_rows = [[e(s["scenario"]) + (" <b>(today)</b>" if s["scenario"] == efficiency.get("readiness", {}).get("current_scenario") else ""),
                 e(s["score_range"]), e(s["realized_band"]), e(s["narrative"])] for s in scen]
    adr_rows = [[e(t), e(s)] for t, s in adrs()]

    body = "".join([
        section("summary", "Executive Summary", "What we're doing and why",
                f'<div class="sz-tldr"><div class="sz-tldr-label">Summary</div><p>{SUMMARY}</p></div>{stats_html()}'
                f'<div style="margin-top:var(--space-lg);">{chips_html()}</div>'),
        '<hr class="sz-divider">',
        section("solution", "Solution", "Architecture decisions",
                table(["Decision", "Status"], adr_rows) if adr_rows else "<p>No ADRs yet.</p>"
                + '<p class="sz-note">Full reasoning for each decision is on the <a href="docs.html#adrs">source documents</a> page.</p>'),
        '<hr class="sz-divider">',
        section("epics", "Scope", "Epics & sizing", table(["Epic", "Name", "Size", "Confidence", "Approach"], epics_rows())),
        '<hr class="sz-divider">',
        section("delivery", "Delivery Plan", "Phases & dependencies",
                phases_html()
                + '<p class="sz-note">Phases 1-4 form the critical path (24 working weeks). Phase 0 (Discovery & Architecture) gates everything. Phase 5 (MCP Next Remediation) runs concurrently.</p>'),
        '<hr class="sz-divider">',
        section("lanes", "Delivery Options", "Traditional vs AI-Native", lanes_html()),
        '<hr class="sz-divider">',
        section("schedule-aug", "Traditional · Committed Anchor", "Epic schedule · 24 working weeks",
                gantt("aug") + '<p class="g-legend">Bars = working weeks · Critical path: E02 → E03 → (E05, E06, E07) · E01 runs as parallel track</p>'),
        section("schedule-native", "AI-Native · Conditional", "Epic schedule · 16–21 working weeks",
                gantt("native") + '<p class="g-legend">Same as Traditional, compressed by efficiency native_band — conditional on customer commitment to AI-native operating model</p>'),
        section("schedule-table", "Epic Schedule", "Start / end week by lane",
                table(["Epic", "Name", "Size", "Traditional wk", "AI-Native wk", "Notes"], schedule_rows())
                + '<p class="sz-note">Phase windows are committed. Bars inside a phase are placed to fit that window and the agreed sequencing.</p>'),
        '<hr class="sz-divider">',
        section("team-aug", "Traditional · Committed Anchor", "Hours per resource",
                table(["ID", "Role", "Focus", "Level", "Phases", "Alloc.", "Hours"], r_rows, row_attrs=r_attrs)
                + '<p class="sz-note">Hours = allocation × active phases × committed phase weeks × 40. Phase breakdown: P0 3 · P1 4 · P2 7 · P3 7 · P4 3 weeks.</p>'),
        section("team-native", "AI-Native · Conditional", "Hours per resource",
                table(["ID", "Role", "Focus", "Level", "Phases", "Alloc.", "Hours"], n_rows, row_attrs=n_attrs)
                + '<p class="sz-note">AI-native clock: P0 3 · P1 4 · P2 7 · P3 7 · P4 3 weeks (same as traditional; parallel P5 compresses 20 → 13–17 wk). Conditional on qualification gate.</p>'),
        section("team-client", "Client-side", f"What Beyond staffs · ~{CLIENT_TOTAL:,} person-hrs",
                table(["ID", "Role", "Responsibility", "Phases", "Alloc."], client) if client else "<p>No client-side roles specified.</p>"
                + '<p class="sz-note">Client responsibilities: Acxiom contract/licensing, BigQuery schema/Data Mesh maintenance, Governance/CoE/training, UAT execution.</p>'),
        '<hr class="sz-divider">',
        section("efficiency", "AI Efficiency", "How much AI compresses delivery",
                f'<p>Task-level AI gains are ~25–45% on integration/enrichment/activation work. '
                f'AI-Augmented (traditional + tooling) realizes <b>{e(eff.get("realized_band", "TBD"))}</b> (realization factor 0.25–0.35, regulated-legacy shape). '
                f'AI-Native realizes <b>{e(eff.get("native_band", "TBD"))}</b> (conditional, provisional).</p>'
                + table(["Readiness", "Score", "Realized band", "What it looks like"], eff_rows) if eff_rows else "<p>Efficiency analysis in progress.</p>"),
        '<hr class="sz-divider">',
        section("gaps", "Open Items", f"Gaps, assumptions & risks · {len(gaps)} logged", filt + table(["ID", "Category", "Gap / question", "Impact / notes"], gap_rows, "gap-table", gap_attrs)),
    ])
    nav = [
        ("Overview", [("#summary", "Executive Summary"), ("#solution", "Architecture Decisions"), ("#epics", "Epics & Sizing"), ("#delivery", "Phases & Dependencies")]),
        ("Delivery Options", [("#lanes", "Lane Comparison"), ("#schedule-aug", "Gantt · Traditional"), ("#schedule-native", "Gantt · AI-Native"), ("#schedule-table", "Epic Start / End Weeks")]),
        ("Team", [("#team-aug", "Hours · Traditional"), ("#team-native", "Hours · AI-Native"), ("#team-client", "Client-side Roles")]),
        ("Analysis", [("#efficiency", "AI Efficiency"), ("#gaps", "Gaps & Risks")]),
        ("More", [("index.html", "← Overview"), ("docs.html", "Source documents →")]),
    ]
    page("scope.html", "Beyond Data Cloud & MCP · Full Scope",
         "Salesforce Professional Services &nbsp;·&nbsp; Scope, delivery options, schedule &amp; team &nbsp;·&nbsp; Pricing not included", nav, body)


# ---------------------------------------------------------------- docs.html
DOCS = [
    ("discovery", "outputs/00-discovery-brief.md", "Discovery Brief", "The discovery scope and context, as of 2026-10-07."),
    ("delivery", "outputs/02-delivery-plan.md", "Delivery Plan", "The current phased roadmap with dependencies and risks."),
    ("traditional", "outputs/artifacts/traditional-staffing-plan.md", "Traditional Staffing Plan", "Committed anchor lane: 10 PS resources, 8,280 hours, ~8.6 FTE, 24 weeks."),
    ("augmented", "outputs/artifacts/augmented-staffing-plan.md", "Augmented Staffing Plan", "Same team as Traditional, 24 weeks, but with ~10% AI tooling efficiency gain (7,452 hours, ~7.7 FTE)."),
    ("efficiency", "outputs/artifacts/efficiency-analysis.md", "AI Efficiency Analysis", "How much AI compresses delivery (category-only fidelity; Low readiness, ~6-16% realized band)."),
    ("ai-native", "outputs/artifacts/ai-native-staffing-plan.md", "AI-Native Staffing Plan", "Conditional lane: 9 PS resources with senior-weighted core floor + agent-amplified seats, 5,380 hours, ~7.3 FTE, 16–21 weeks."),
    ("comparison", "outputs/artifacts/estimate-comparison.md", "Estimate Comparison", "All three lanes side-by-side: timeline, team, hours, delta."),
]


def md(text):
    text = re.sub(r"`?\[KB:[^\]]*\]`?", "", text)
    text = re.sub(r"`?\[KA-[^\]]*\]`?", "", text)
    return markdown.markdown(text, extensions=["tables", "sane_lists"])


def build_docs():
    parts, links = [], []
    for sid, path, title, note in DOCS:
        doc_path = ROOT / path
        if not doc_path.exists():
            parts.append(f'<section id="{sid}" class="sz-section sz-doc"><div class="sz-section-eyebrow">Source document</div>'
                         f'<p class="sz-note">{e(note)} [File not found: {e(path)}]</p></section><hr class="sz-divider">')
        else:
            parts.append(f'<section id="{sid}" class="sz-section sz-doc"><div class="sz-section-eyebrow">Source document</div>'
                         f'<p class="sz-banner">{e(note)}</p>{md(doc_path.read_text())}</section><hr class="sz-divider">')
        links.append((f"#{sid}", title))

    # ADRs
    adr_html = ""
    decisions_dir = ROOT / "decisions"
    if decisions_dir.exists():
        adr_html = "".join(f'<div class="sz-card sz-doc">{md(f.read_text())}</div>' for f in sorted(decisions_dir.glob("*.md")))
    if adr_html:
        parts.append(f'<section id="adrs" class="sz-section sz-doc"><div class="sz-section-eyebrow">Architecture Decision Records</div>{adr_html}</section>')
        links.append(("#adrs", "Architecture Decisions (ADRs)"))

    nav = [("Documents", links), ("More", [("index.html", "← Overview"), ("scope.html", "← Full scope")])]
    page("docs.html", "Beyond Data Cloud & MCP · Source Documents",
         "The Scopezilla working documents behind the scope, each labelled with its as-of date", nav, "".join(parts))


# ---------------------------------------------------------------- staffing.html
def build_staffing():
    # Build a unified staffing plan showing all three lanes side-by-side
    trad_by_role = {}
    for r in ps_rows:
        role = r["role"]
        if role not in trad_by_role:
            trad_by_role[role] = []
        trad_by_role[role].append(r)

    native_by_role = {}
    for r in native_roster:
        role = r["role"]
        if role not in native_by_role:
            native_by_role[role] = []
        native_by_role[role].append(r)

    # Combined table: all unique roles, resources listed separately for each lane
    staffing_rows = []
    all_roles = sorted(set(trad_by_role.keys()) | set(native_by_role.keys()))

    for role in all_roles:
        trad_resources = trad_by_role.get(role, [])
        native_resources = native_by_role.get(role, [])

        # Traditional row(s)
        for tr in trad_resources:
            tech = tr.get("skills_needed", "Integration, config, QA")[:45]
            trad_hrs = aug_hours.get(tr["resource_id"], 0)
            aug_hrs = augmented_hours.get(tr["resource_id"], 0)
            alloc_label = "Full" if tr["allocation"] == "full" else "Half"
            staffing_rows.append([
                f'<b>{tr["resource_id"]}</b>',
                e(tr["role"]),
                e(tr["seniority"].capitalize()),
                f'{tr["location"].capitalize()}',
                e(tech),
                f'{int(tr["count"])}',
                alloc_label,
                f'<span class="num">{trad_hrs:,.0f}</span>',
                f'<span class="num">{aug_hrs:,.0f}</span>',
                '<span class="num">—</span>',
            ])

        # AI-native row(s) if different or additional
        for nr in native_resources:
            tech = nr.get("skills_needed", "Integration, agents, QA")[:45]
            hrs = native_hours.get(nr["resource_id"], 0)
            alloc_label = "Full" if nr["allocation"] == "full" else "Half"
            staffing_rows.append([
                f'<b>{nr["resource_id"]}</b>',
                e(nr["role"]),
                e(nr["seniority"].capitalize()),
                f'{nr["location"].capitalize()}',
                e(tech),
                f'{int(nr["count"])}',
                alloc_label,
                '<span class="num">—</span>',
                '<span class="num">—</span>',
                f'<span class="num">{hrs:,.0f}</span>',
            ])

    body = "".join([
        section("staffing", "Resource Allocation", "Staffing Plan",
            f'<p>This staffing plan spans three delivery lanes: <b>Traditional</b> (committed anchor, {AUG_TOTAL:,.0f} PS hours, ~8.6 FTE, 24 weeks), '
            f'<b>Augmented</b> (same {AUG_TOTAL:,.0f} → {AUGMENTED_TOTAL:,.0f} PS hours after ~10% efficiency gain, ~7.7 FTE, 24 weeks), '
            f'and <b>AI-Native</b> (conditional, {NATIVE_TOTAL:,.0f} PS hours, ~7.3 FTE, 16–21 weeks). '
            f'Augmented keeps the same team and calendar but captures AI tooling efficiency gains. AI-Native is leaner and shorter, requiring commitment to an AI-native way of working.</p>'
            + f'<p style="color: var(--sf-text-weak); font-size: 13px; margin: var(--space-md) 0;"><b>Geographic split:</b> Traditional/Augmented: 6 offshore (build + QA) + 4 onshore (PM, SA, TA, Consultant). AI-Native: 4 offshore (Agent Orchestrators + QA) + 5 onshore (Program Lead, 2 Intent Architects, QA/Consultant fractional).</p>'
            + table(
                ["Resource", "Role", "Seniority", "Location", "Technology / Domain", "Count", "Allocation", "Traditional Hrs", "Augmented Hrs", "AI-Native Hrs"],
                staffing_rows
            )
            + '<p class="sz-note"><b>How to read this table:</b> Each row is one resource (one person). Traditional and Augmented share the same roster but different hours (Augmented = Traditional × 90% due to ~10% efficiency gain from AI tooling). AI-Native is a different roster (different roles, especially Agent Orchestrators). Count = number of people in this role (always 1 per row). Allocation = work intensity when active (Full = 1.0 FTE, Half = 0.5 FTE).</p>'
            + f'<p class="sz-note"><b>Hours basis:</b> Traditional hours are budgeted for 24 committed weeks. Augmented hours reflect the same deliverables with ~10% efficiency uplift (conservative end of the 6–16% Low-readiness band from efficiency analysis). AI-Native hours are compressed per the ~13–34% native_band and conditional on meeting the AI-native qualification gates.</p>'
            + f'<p class="sz-disclaimer">{BENCHMARK_DISCLAIMER}</p>'),
    ])

    nav = [
        ("Staffing", [("#staffing", "Resource allocation")]),
        ("More", [("index.html", "← Overview"), ("scope.html", "← Full scope"), ("docs.html", "Source documents →")]),
    ]
    page("staffing.html", "Beyond Data Cloud & MCP · Staffing Plan",
         "Salesforce Professional Services · Team shape and resource allocation across delivery lanes", nav, body)


if __name__ == "__main__":
    SITE.mkdir(exist_ok=True)
    build_index()
    build_scope()
    # build_staffing()  # DISABLED: too confusing with role IDs (Q03a, Q04, etc.)
    build_docs()
    print(f"site built: {SITE}  (traditional {AUG_TOTAL:,.0f} hrs, AI-native {NATIVE_TOTAL:,.0f} hrs)")
