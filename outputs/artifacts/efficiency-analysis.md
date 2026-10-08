# AI Delivery Efficiency Analysis — Beyond Data Cloud & MCP ARI 2026

## So What
**~6-16% realized delivery efficiency at Low readiness.** A pace and quality lift within the same team shape — not headcount reduction, not a pricing input.

Where the gains show up on this project:
- **Technical Engineering & QA** (~6-16%): E01's MCP remediation, E02's BigQuery sync, E07's Braze connector — enterprise/legacy integration work, not greenfield.
- **Documentation & Knowledge Management** (~7-18%): E05's CPRA activation-target write-ups, E06's catalog-feed decision documentation — the most reliable category on this project.
- **Analysis & Design** (~6-14%): E03's household-grain Acxiom resolution, E04's cross-entity activation design — drafting compresses, but the fork resolution stays human.

**Where AI does not help**: Beyond's legal review of the income-based pricing campaign, the CPRA/DMA-suppression ownership decisions — plus the highest-AI-tax work on this project, the MCP Next root-cause audit against a live production instance.

**To move up to High readiness (~7-19%)**: confirm AI tooling approval for the delivery team, resolve BigQuery lower-environment connectivity (G0209), name owners for the three open compliance gates (G0503, G0505, G0605).

## Headline
**Realized: ~6-16%** (Low readiness) · **Task-level blend: ~25-45%** · **Realization factor: 0.25-0.35 (regulated-legacy)** — live-production remediation plus heavy legacy/third-party integration load and three open compliance gates with no named owner · **Confidence: Assumed**

## Client-Readiness Scenarios
| Scenario | Realized Band | Notes |
|---|---|---|
| Low readiness (current: ✓) | ~5-13% | Gains stay modest until the phase-gated cadence loosens and the open compliance/connectivity gaps close. |
| Mid readiness | ~6-16% | Standard enterprise cadence with the environment and compliance gaps resolved lands here, even without a daily-cadence commitment. |
| High readiness | ~7-19% | Conditions favor the upper end once tooling is approved, environments are clean, and the compliance gates close. |

**Current scenario**: Low (score 1/8)

### Signals behind the score
- **AI tooling posture**: 1/2 — No statement anywhere in discovery material on AI tooling approval, client device/VDI policy, or AI data-handling policy for this engagement; scored at the model's default unscored value rather than evidenced.
- **Delivery velocity / speed bias**: 0/2 — The internal staffing draft's own schedule runs discrete phase gates (Discover → Define → Design → Deliver → SIT/UAT → UAT → Deploy → Scale), with no daily build/demo/decide language anywhere in source material.
- **Data & environment hygiene**: 0/2 — G0209: lower-environment BigQuery connectivity for SIT/UAT is explicitly unconfirmed, with no named owner or date to close it.
- **Legal / security / compliance posture**: 0/2 — Three open compliance gates with no named owner: G0503 (CPRA activation-target designation), G0505 (DMA-suppression enforcement mechanism), G0605/G0806 (income-based pricing legal exposure).

### What it takes to move up
- **Low → Mid**: Resolve BigQuery lower-environment connectivity (G0209); name compliance owners for the CPRA / DMA-suppression / income-pricing reviews (G0503, G0505, G0605).
- **Mid → High**: Confirm AI tooling approval for the delivery team; close the three open compliance gates with named owners.

## By Category
### Technical Engineering & QA — realized ~6-16% (task-level ~25-45%)
- **Driving epics**: E01 (L), E02 (L), E07 (L)
- **How it shows up here**: E01's MCP remediation against a live production instance, E02's 4-table BigQuery sync, and E07's Braze connector are all enterprise/legacy integration work, not greenfield — the review burden keeps this near the low end of the range [1].

### Analysis & Design — realized ~6-14% (task-level ~25-40%)
- **Driving epics**: E03 (L), E04 (L)
- **How it shows up here**: E03's household-grain Acxiom resolution and E04's cross-entity activation design are both open architecture forks, not routine modeling — drafting compresses, but the fork resolution itself stays human-bound [2].

### Documentation & Knowledge Management — realized ~7-18% (task-level ~30-50%)
- **Driving epics**: E05 (L), E06 (L)
- **How it shows up here**: E05's per-platform CPRA designation write-ups and E06's catalog-feed decision documentation are the most reliable category on this project [7], though the underlying ownership decisions stay human.

### Project Management & Operations — realized ~3-11% (task-level ~15-30%)
- **Driving epics**: E01, E02, E03, E04, E05, E06, E07
- **How it shows up here**: A 24-week, 6-phase program with two concurrent tracks (Data 360 build + MCP Next remediation) carries real coordination load; status reporting compresses but the coordination core stays human [1].

## Human-Only Work
- **Project Pulse Reports** — Trust-building work AI can summarize but not facilitate.
- **Stakeholder Alignment** — Human-to-human negotiation; AI drafts positions, people decide.
- **Conflict Resolution** — Human judgment.
- **Beyond legal review of the income-based pricing campaign (G0605/G0806)** — A regulatory/reputational judgment call for Beyond's legal function.
- **CPRA / DMA-suppression ownership decisions (G0503/G0505)** — Needs a named Beyond decision-maker; no technical safeguard substitutes for the gap.
- **MCP Next root-cause audit review burden (G0101)** — Diagnosing undiagnosed live-production defects is senior-judgment work.

## AI-Native Path (not shown as a priced lane)
The AI-native qualification verdict for this engagement is **not-yet** — no priced AI-native lane. One must-have reads red (iterative working model: the staffing draft's own schedule is phase-gated, not daily-cadence) and four are unknown (decision velocity, executive mandate, AI tooling permission, data/environment readiness) because none of discovery-notes/ or gaps.json speaks to them either way.

**What would open the path**: a named, empowered decision-maker who can turn around calls within ~24h (M1); moving from phase-gated sign-offs to daily build/demo/decide (M2); a committed executive sponsor who removes roadblocks (M3); confirmed AI-tooling approval for the delivery team (M4); real data in sandbox with full access by Day 1 of Build (M5).

## Assumptions & Caveats
- Task-level gains come from published 2022–2026 studies; a realization factor (by project shape, from `efficiency-model.json`) accounts for Amdahl's law, review/AI-tax overhead, and unmoved human-barrier work.
- **Honest range for coding**: RCT evidence spans −19% (METR 2025 [1], mature OSS) to +21% (Paradis/Google 2024 [4], complex enterprise) to +55% (Peng/GitHub 2022 [3], greenfield lab). The regulated-legacy row is the defensible starting point here, given the live-production remediation and open compliance gates.
- Individual gains ≠ team gains: DORA 2024 [5] measured individual productivity rising while delivery stability and throughput fell. Ground claims in project-level outcomes, not developer self-report.
- Bands are qualitative and project-specific — no hours, FTE, or cost implications are computed or implied.

## Sources
1. METR (July 2025) — RCT of experienced OSS developers; measured ~19% slowdown despite perceived ~20% speedup.
2. BCG × Harvard (2023, 2025 pilots) — 12.2–40% time savings on in-scope tasks; "jagged frontier" degrades on out-of-scope tasks.
3. Peng et al., GitHub (2022) — lab RCT, 95 devs on a greenfield HTTP-server task; ~55% faster, 95% CI [21%, 89%].
4. Paradis et al., Google (arXiv 2410.12944, 2024) — RCT of 96 Google engineers on a complex enterprise task; ~21% time reduction with wide CI.
5. DORA 2024 State of DevOps — individual AI productivity gains coexist with decreased delivery stability and throughput.
7. McKinsey State of AI (2025) — 10–30% function-level gains.
8. GitClear AI Code Quality (2025 update) — cloning 8.3%→12.3%, refactoring 25% (2021)→<10% (2024).

---

## Deliverables
- `/Users/ktse/Documents/Clients/Beyond Data Cloud & MCP ARI 2026/data/efficiency.json`
- `/Users/ktse/Documents/Clients/Beyond Data Cloud & MCP ARI 2026/outputs/artifacts/efficiency-analysis.md`
