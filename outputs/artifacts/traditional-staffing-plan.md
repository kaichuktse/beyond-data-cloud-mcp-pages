# Traditional Staffing Plan

## Overview

The **Traditional lane** is the committed anchor — your baseline for delivery scope, timeline, and team.

- **Timeline:** 24 weeks (committed)
- **Team size:** 10 PS resources
- **Hours:** 8,280 person-hours
- **FTE:** ~8.6 FTE program-average
- **Confidence:** Confirmed (benchmark-based)

## Team Roster

**Leadership & Architecture:**
- **R01** — Project Manager (onshore, full-time) — Both workstreams (Data 360 critical path + MCP Next parallel)
- **R02** — Solution Architect (onshore, full-time) — Data 360 workstream lead (topology, identity, activation)
- **R03** — Technical Architect (onshore, full-time) — MCP Next workstream lead (remediation + audit)

**Build Team:**
- **R04** — Senior Developer (offshore, full-time) — Data 360 critical-path integration load
- **R05a** — Developer (offshore, full-time) — Volume pod seat 1 (BigQuery sync, enrichment, connectors, Braze)
- **R05b** — Developer (offshore, full-time) — Volume pod seat 2 (BigQuery sync, enrichment, connectors, Braze)
- **R06** — Senior MCP Developer (offshore, full-time) — BBY US/Overstock fixes + BuyBuyBaby instrumentation

**Quality & Config:**
- **R07** — QA Lead (offshore, full-time) — Both workstreams (remediation + compliance hardening)
- **R08** — QA Engineer (offshore, full-time) — Data 360 activation/paid-media/web/email volume
- **R09** — Functional Consultant (onshore, half-time) — Config/story authoring, client coordination

**Geographic split:** 6 offshore (build + QA) + 4 onshore (PM, Architects, Consultant)

## Hours per Resource

| Resource | Role | Phases | Allocation | Hours | Notes |
|----------|------|--------|-----------|-------|-------|
| R01 | Project Manager | 0-4 | Full | 960 | (3+4+7+7+3)×40 = 24×40 |
| R02 | Solution Architect | 0-4 | Full | 960 | (3+4+7+7+3)×40 = 24×40 |
| R03 | Technical Architect | 0,5 | Full | 920 | (3+20)×40 = 23×40 |
| R04 | Senior Developer | 1-4 | Full | 840 | (4+7+7+3)×40 = 21×40 |
| R05a | Developer | 1-4 | Full | 840 | (4+7+7+3)×40 = 21×40 |
| R05b | Developer | 1-4 | Full | 840 | (4+7+7+3)×40 = 21×40 |
| R06 | Senior MCP Developer | 0,5 | Full | 920 | (3+20)×40 = 23×40 |
| R07 | QA Lead | 1-4 | Full | 840 | (4+7+7+3)×40 = 21×40 |
| R08 | QA Engineer | 2-4 | Full | 680 | (7+7+3)×40 = 17×40 |
| R09 | Functional Consultant | 0-4 | Half | 480 | (3+4+7+7+3)×40×0.5 = 24×20 |
| **TOTAL** | | | | **8,280** | ~8.6 FTE / 24 weeks |

## Phase Timeline

**Phase 0:** Discovery & Architecture (3 weeks)  
**Phase 1:** Data 360 Foundation (4 weeks)  
**Phase 2:** Enrichment & Personalization (7 weeks)  
**Phase 3:** Paid Media & Web (7 weeks)  
**Phase 4:** Email & Braze (3 weeks)  
**Phase 5:** MCP Next Remediation (parallel, 20 weeks)

Critical path: E02 → E03 → (E05, E06, E07) = 24 weeks  
Phase 5 runs alongside and is not included in the 24-week sum.

## What's Included

- Root-cause audit of MCP Interactions SDK (live-production issues)
- BBY US & Overstock defect remediation + BuyBuyBaby instrumentation
- Data 360 foundation with BigQuery sync (4-table Customer Data Mesh)
- Acxiom enrichment (~39 attributes) + identity resolution
- MCP personalization activation
- 5 ad-platform connectors (Google, Facebook, Criteo, Pinterest, TikTok)
- Web experience (10 brand-neutral use cases)
- Email campaigns (7 use cases) + Braze integration
- Full QA, testing, and compliance hardening

---

**Note:** Hours are benchmark-based, derived from the AI model's training data and general delivery patterns (not Salesforce-validated) — not a commitment. Final figures are confirmed through the applicable commercial agreement.
