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

| Resource | Role | Allocation | Hours | Notes |
|----------|------|-----------|-------|-------|
| R01 | Project Manager | Full | 1,040 | All phases, both workstreams |
| R02 | Solution Architect | Full | 940 | P0-P4, Data 360 lead |
| R03 | Technical Architect | Full | 940 | P0+P5, MCP Next lead |
| R04 | Senior Developer | Full | 1,040 | P1-P4, integration lead |
| R05a | Developer | Full | 940 | P1-P4, volume pod |
| R05b | Developer | Full | 940 | P1-P4, volume pod |
| R06 | Senior MCP Developer | Full | 1,040 | P0+P5, remediation |
| R07 | QA Lead | Full | 1,040 | P1-P4, both workstreams |
| R08 | QA Engineer | Full | 800 | P2-P4, Data 360 volume |
| R09 | Functional Consultant | Half | 500 | P0-P4, config/BA |
| **TOTAL** | | | **8,280** | ~8.6 FTE / 24 weeks |

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
