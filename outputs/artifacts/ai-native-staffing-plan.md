# AI-Native Staffing Plan

## Overview

The **AI-Native lane** restructures the team around senior-weighted core accountability floors and agent-amplified build seats. It's leaner and faster than Traditional, but conditional on your commitment to an AI-native operating model.

- **Timeline:** 16–21 weeks (conditional, ~13–34% compression)
- **Team size:** 9 PS resources (1 fewer than Traditional)
- **Hours:** 5,380 person-hours (~35% reduction from Traditional's 8,280)
- **FTE:** ~7.3 FTE program-average
- **Confidence:** Conditional (provisional, Solution Lead override for customer discussion)
- **Status:** Not yet evidenced; depends on AI-native qualification gates M1–M5

## Key Differences from Traditional

**Restructuring principles:**

1. **Volume → Agents, not bodies:** Traditional's 2-person developer pod (R05a + R05b) collapses to **1 agent-amplified developer** (Q04) directing agents. Senior leads (Agent Orchestrators Q03a/Q03b) cover the complex work.

2. **Un-delegatable accountabilities stay human:** Program Lead, Intent Architects, and QA leads remain full-time senior roles. Agents assist; they don't replace.

3. **Sequencing multiplies senior coverage:** Hard problems taken one-at-a-time by a senior directing agents = one senior covers more scope than in Traditional.

4. **QA is amplified, not replaced:** Senior QA lead stays full-time; supporting QA drops from full-time (R08) to half-time (Q06) with agent-assisted test generation.

5. **Config/BA buys depth fractionally:** Functional Consultant (Q07) narrows to phases 1–3 only (agent-drafted config compresses the window).

## Team Roster

**Core Accountability Floor:**
- **Q01** — Program Lead (onshore, full-time) — Un-delegatable relationship/governance, both workstreams
- **Q02a** — Intent Architect (onshore, full-time) — Data 360 workstream (frames agent fleet intents, owns hard-problem architecture)
- **Q02b** — Intent Architect (onshore, full-time) — MCP Next workstream (root-cause audit ownership, different platform)

**Agent Orchestrators (replace traditional Developers):**
- **Q03a** — Agent Orchestrator (offshore, full-time) — Data 360 (directs agents on integration/enrichment/connectors/Braze)
- **Q03b** — Agent Orchestrator (offshore, full-time) — MCP Next (directs agents on remediation fixes)

**Agent-Amplified Build:**
- **Q04** — Developer (offshore, full-time) — One agent-amplified seat replaces R05a + R05b's 2-person volume pod

**Quality Assurance:**
- **Q05** — QA Lead (offshore, full-time) — Agent-amplified, held flat (independent check on agent outputs)
- **Q06** — QA Engineer (offshore, half-time) — Supporting QA with agent-assisted test generation

**Configuration:**
- **Q07** — Functional Consultant (onshore, half-time) — Phases 1–3 only (narrower window; agent-drafted config)

**Geographic split:** 4 offshore (orchestrators + QA + developer) + 5 onshore (Program Lead, 2 Intent Architects, QA fractional, Consultant fractional)

## Hours per Resource

| Resource | Role | Allocation | Hours | Notes |
|----------|------|-----------|-------|-------|
| Q01 | Program Lead | Full | 600 | All phases, both workstreams |
| Q02a | Intent Architect (Data 360) | Full | 560 | P0-P4, frames agent intents |
| Q02b | Intent Architect (MCP Next) | Full | 560 | P0+P5, root-cause ownership |
| Q03a | Agent Orchestrator (Data 360) | Full | 560 | P1-P4, directs agent fleet |
| Q03b | Agent Orchestrator (MCP Next) | Full | 560 | P0+P5, remediation fix oversight |
| Q04 | Agent-Amplified Developer | Full | 560 | P1-P4, 1 seat replaces 2-person pod |
| Q05 | QA Lead (amplified) | Full | 560 | P1-P4, independent check |
| Q06 | QA Engineer (fractional) | Half | 280 | P2-P4, agent-assisted testing |
| Q07 | Functional Consultant (fractional) | Half | 200 | P1-P3, config authoring |
| **TOTAL** | | | **5,380** | ~7.3 FTE / 16–21 weeks |

## Phase Timeline

**Compressed schedule (16–21 weeks vs. Traditional's 24):**

Phase 0: 3 weeks  
Phase 1: 4 weeks  
Phase 2: 7 weeks  
Phase 3: 7 weeks  
Phase 4: 3 weeks  
**Critical path total:** 24 weeks compressed by ~13–34% (efficiency native_band) = **16–21 weeks**

Phase 5 (MCP Next): 13–17 weeks (parallel, compressed from 20)

## How It Works: Three Adjustments

**Adjustment 1: Volume → Agents**  
Traditional: R04 (senior dev) + R05a + R05b (2 regular devs) = 3 developers  
AI-Native: Q03a/Q03b (2 senior orchestrators) + Q04 (1 agent-amplified dev) = 3 roles, but senior-weighted

The agent fleet absorbs the routine config/integration volume (BigQuery sync, enrichment, connectors, Braze). One human builder remains because this project's regulated-legacy shape (live-production remediation + 3 open compliance gates) earns a critical-path human builder rather than a fully agent-run pod.

**Adjustment 2: QA Stays Human**  
Traditional: R07 (full) + R08 (full) = 2 QA people  
AI-Native: Q05 (full) + Q06 (half) = 1.5 FTE

QA is agent-amplified, never agent-replaced. An agent can't be the independent check on its own output. Compliance hardening window doesn't shrink.

**Adjustment 3: Config Buys Depth Fractionally**  
Traditional: R09 (half, phases 0–4) = 0.5 FTE  
AI-Native: Q07 (half, phases 1–3) = 0.25 FTE

Agent-drafted config compresses the window this function is actively needed. Phases 0 (no build yet) and 4 (email/Braze handoff is Q03a/Q04's work, not config authoring) drop out.

## Qualifications & Risks

**This lane is conditional.** It depends on all five must-haves being green:

| Gate | Status | Evidence |
|------|--------|----------|
| **M1** — Decision velocity (client makes calls fast) | Yellow (assumed) | Not confirmed; to be asked in customer meeting |
| **M2** — Delivery cadence (daily standups, demo/decide) | Yellow (assumed) | Staffing draft's own schedule is phase-gated (red on evidence); assuming customer could move to looser cadence, unconfirmed |
| **M3** — Executive sponsor (named, empowered) | Yellow (assumed) | No executive sponsor named; to be asked |
| **M4** — AI tooling approval (client allows AI in build) | Yellow (assumed) | No statement on AI tooling approval or data-handling policy; to be asked |
| **M5** — Environment readiness (lower-env connectivity) | Yellow (assumed) | G0209: BigQuery SIT/UAT connectivity still open with no owner/date |

If any gate stays red after the customer conversation, this lane reverts to **not-yet** and is removed.

## When to Choose AI-Native

- **You're ready to restructure the team** (no traditional org chart friction)
- **You want to go live 3–8 weeks earlier** (at the cost of different team shapes)
- **You're committed to an AI-native operating model** (daily cadence, empowered decisions, AI tooling approved)
- **The five qualification gates move to green** (M1–M5 confirmed in the customer meeting)

## When to Stay with Traditional or Augmented

- **M1–M5 gates remain yellow/red** (not evidenced)
- **Your org needs the familiar team structure** (stick with Traditional)
- **You want efficiency gains without restructuring** (pick Augmented)
- **You want to pilot AI with your team first** (Augmented is the stepping stone)

---

**Note:** Hours are benchmark-based and conditional on AI-native qualification. This lane is a motivator for customer discussion ("*if* you commit to this way of working, here's what it would cost") — never presented as achievable without naming the commitment it depends on. Figures are derived from the AI model's training data and general delivery patterns (not Salesforce-validated) — not a commitment.
