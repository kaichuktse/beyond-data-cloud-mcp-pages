# Estimate Comparison - Beyond Data Cloud & MCP ARI 2026

**Pricing deferred - timeline, effort, and resourcing complete.** Add an indicative price by supplying bill rates (`commercials`).

> **Roster honesty note.** Both rosters and their FTE are a model-derived starting point that requires the Solution Lead's validation; the human owns the final team. The role-folding and allocation calls are judgment - least certain: whether MCP Next warrants a dedicated Technical Architect (R03/Q02b) rather than folding into the Solution Architect, and whether one agent-amplified build seat (Q04) is enough for six L-sized Data 360 workstream epics. Resourcing is a capability still being refined; treat this as decision-support, not a committed staffing plan.

> *This figure is benchmark-based, derived from the AI model's training data and general delivery patterns (not Salesforce-validated) - not a commitment. Final figures are confirmed through the applicable commercial agreement.*

## Headline

| | Traditional (anchor) | AI-native (conditional) |
|---|---|---|
| Critical-path duration | 24 weeks (user-committed) | 16-21 weeks |
| MCP Next parallel track | 20 weeks | 13-17 weeks |
| Program-average FTE | 8.62 | 7.27 |
| Person-hours (internal) | 8,280 | 6,980 |
| Roles / seats | 9 / 10 | 7 / 9 |

**Delta (script-derived):** AI-native vs traditional, decomposed: critical path 3-8 weeks shorter (24 vs 16-21, native_band ~13-34%); 1.35 FTE leaner (8.62 vs 7.27) and 1,300 fewer person-hours (8,280 vs 6,980), driven by the 2-seat volume pod collapsing to 1 agent-amplified seat under senior Agent Orchestrators, half-time second QA, and a narrower Functional Consultant window; architecture and independent QA leads held flat. Per decisions/0033 the shorter calendar is conditional on the customer committing to the AI-native way of working.

## Traditional lane (anchor)
User-committed 24-week critical path (timeline.user_commitment, matching the internal staffing draft's schedule), allocated across 5 sequenced phases via derive-hours.py --allocate; Phase 5 (MCP Next Remediation, 20wk) runs as a parallel track outside the critical-path sum. Benchmark-based, not a commitment - derived from the AI model's training data and general delivery patterns (not Salesforce-validated).

| ID | Role | Seniority | Location | Count | Phases | Allocation | Hours/person | Justification |
|---|---|---|---|---|---|---|---|---|
| R01 | Project / Program Manager | regular | onshore | 1 | 0-4 | full | 960 | Single PM spans both workstreams (Data 360 critical path + MCP Next parallel track) — customer relationship, gate decisions, scope governance across the whole 24wk program plus the 20wk MCP Next lane. Phase 5 (MCP Next) excluded: R03 is the dedicated Technical Architect leading that track full-time; PM oversight stays bound to the 24-week critical-path calendar, not a second concurrent full-time commitment. |
| R02 | Solution Architect | senior | onshore | 1 | 0-4 | full | 960 | Named lead for the Data 360 workstream (E02-E07) — Data Space/Data Share topology, identity-resolution grain, cross-entity activation design; the regulated-legacy shape (3 open compliance gates, no named owner) keeps this role senior and continuously engaged, not folded onto build. |
| R03 | Technical Architect | senior | onshore | 1 | 0,5 | full | 920 | Named lead for the MCP Next workstream (E01) — different platform/skillset than Data 360 (skills_needed: 'MCP Solution/Technical Architect'); owns the root-cause audit (G0101, no defect list yet) against a live production instance, a hard-problem domain that can't fold onto the Data 360 SA. |
| R04 | Developer | senior | offshore | 1 | 1-4 | full | 840 | Senior build lead for Data 360's critical-path integration load (4-table BigQuery sync, Acxiom enrichment, 5 ad-platform connectors, Braze) — enterprise/legacy integration work per estimates.json's complexity_drivers, not routine config. |
| R05a | Developer | regular | offshore | 1 | 1-4 | full | 840 | Volume build pod, seat 1 of 2 — scaled to the Data 360 workstream's weight (6 epics, E02-E07, all T-shirt L) spanning BigQuery sync, enrichment, personalization, 5 ad platforms, web, and email/Braze. Split from a single count:2 row into two count:1 rows per the resource-table convention (one row per named seat). |
| R05b | Developer | regular | offshore | 1 | 1-4 | full | 840 | Volume build pod, seat 2 of 2 — same basis as R05a; two regular seats keep the pod proportional to L×6 scope without over-staffing a single discipline per role. |
| R06 | Developer | senior | offshore | 1 | 0,5 | full | 920 | Senior MCP developer for the remediation build (skills_needed: 'Senior MCP Developer') — BBY US/Overstock defect fixes plus BuyBuyBaby's net-new Interactions SDK instrumentation, under the MCP Next TA. |
| R07 | Quality Assurance | senior | offshore | 1 | 1-4 | full | 840 | QA lead spanning both workstreams — the regulated-legacy shape (live-production remediation on E01, 3 open compliance gates on E03/E05/E06) sets a QA floor; a named senior owner, not a token pod, per resourcing-roles.md's anti-under-staffing rule. Phase 5 (MCP Next) allocation reduced to half: full-time on both the 21-week critical-path QA load and the 20-week parallel MCP Next track simultaneously is two full-time jobs for one person — half-time shared oversight on MCP Next is the realistic ceiling alongside full critical-path QA duty. Phase 5 (MCP Next) dropped entirely: R07 is already full-time on the critical-path QA load during the same calendar weeks Phase 5 runs concurrently in — any additional allocation there would put R07 over 1.0 FTE at once, which one person cannot do. |
| R08 | Quality Assurance | regular | offshore | 1 | 2-4 | full | 680 | QA engineer scaled to Data 360's build volume (E03-E07 activation/paid-media/web/email) under R07 — monotonic with the build pod, not a flat headcount. |
| R09 | Functional Consultant | regular | onshore | 1 | 0-4 | half | 480 | Config/story authoring and client-coordination support across Data 360 workstream epics — genuinely part-time while active, folds the BA function rather than carrying a full head. |

## AI-native lane - CONDITIONAL, for discussion only
Traditional 24-week critical path compressed by efficiency native_band ~13-34% (derive-hours.py --compress --band-from native); parallel MCP Next track compresses 20wk to 13-17wk. Conditional illustration only - Solution Lead override (2026-10-07) assumed M1-M5 at yellow for a customer discussion; not evidenced.

**Provisional:** CONDITIONAL, for customer-meeting discussion only. Qualification is a Solution Lead override: recommended verdict is not-yet (M2 red on the phase-gated staffing draft; M1/M3/M4/M5 unevidenced). The ~13-34% native band is provisional until AI-native actuals exist and reverts to no native band if the customer conversation does not move M1-M5 for real (decisions/0011, decisions/0033).

Roles map to the core-accountability floor: Q01 Program Lead; Q02a/Q02b Intent Architects (Data 360 / MCP Next); Q03a/Q03b Agent Orchestrators (senior Developers).

| ID | Role | Seniority | Location | Count | Phases | Allocation | Hours/person | Justification |
|---|---|---|---|---|---|---|---|---|
| Q01 | Program Lead | regular | onshore | 1 | 0-4 | full | 960 | Core-accountability floor: Program Lead — un-delegatable relationship/governance ownership across both workstreams, same scope as traditional's R01. Phase 5 (MCP Next) excluded for the same reason as R01: the MCP Next workstream has its own Intent Architect (Q02b) carrying technical oversight; program-lead scope stays bound to the 24-week critical-path calendar. |
| Q02a | Solution Architect | senior | onshore | 1 | 0-4 | full | 960 | Core-accountability floor: Intent Architect for the Data 360 workstream (E02-E07) — frames the agent fleet's build intents AND owns the hard-problem architecture calls (Data Space topology, identity resolution grain, cross-entity activation) an agent can't resolve. Same workstream scope as traditional's R02; stays senior and full-time — the regulated-legacy shape (3 open compliance gates, no named owner) keeps this un-delegatable regardless of delivery model. |
| Q02b | Technical Architect | senior | onshore | 1 | 0,5 | full | 920 | Core-accountability floor: Intent Architect for the MCP Next workstream (E01) — a different platform/skillset than Data 360, same split rationale as traditional's R02/R03. Owns the root-cause audit (G0101, no defect list yet) against a live production instance — hard-problem diagnosis an agent can assist but not own. |
| Q03a | Developer | senior | offshore | 1 | 1-4 | full | 840 | Agent Orchestrator for the Data 360 workstream (adjustment 3: sequencing multiplies senior coverage) — directs the agent fleet on the critical-path integration load (4-table BigQuery sync, Acxiom enrichment, 5 ad-platform connectors, Braze) that traditional spread across R04 + a 2-seat volume pod (R05a/R05b). One senior directing agents covers what traditional needed 3 build heads for. |
| Q03b | Developer | senior | offshore | 1 | 0,5 | full | 920 | Agent Orchestrator for the MCP Next workstream — same remediation-build accountability as traditional's R06 (BBY US/Overstock defect fixes, BuyBuyBaby Interactions SDK instrumentation), now directing agents against the root-cause audit's fix list under Q02b. |
| Q04 | Developer | regular | offshore | 1 | 1-4 | full | 840 | Adjustment 1 (volume → agents, not bodies): one agent-amplified build seat replaces traditional's 2-seat volume pod (R05a/R05b) — the agent fleet absorbs the routine config/integration volume across E02-E07's 6 L-sized epics, with one human seat retained because this project's regulated-legacy shape (live-production remediation + 3 open compliance gates) earns a critical-path human builder rather than a fully agent-run pod. |
| Q05 | Quality Assurance | senior | offshore | 1 | 1-4 | full | 840 | Adjustment 2 (un-delegatable accountabilities stay human; QA is agent-amplified, never agent-replaced): held flat at traditional's R07 scope and allocation — an agent can't be the independent check on its own output, and the regulated-legacy shape (live-production remediation, 3 open compliance gates with no named owner) is exactly the kind of hardening window QA should not shrink in. Phase 5 dropped for the same one-FTE-ceiling reason as R07. |
| Q06 | Quality Assurance | regular | offshore | 1 | 2-4 | half | 340 | Supporting QA scaled down from traditional's R08 full-time to half — agent-assisted test-case generation and regression coverage reduce the manual-execution load for Data 360's E03-E07 activation/paid-media/web/email volume, while a human seat stays in place because QA is amplified, not replaced (adjustment 2). |
| Q07 | Functional Consultant | regular | onshore | 1 | 1-3 | half | 360 | Adjustment 5 (buy depth fractionally, surge in risk windows): narrowed from traditional's R09 (half-time, Phases 0-4) to half-time, Phases 1-3 only — agent-drafted config/story authoring compresses the window this function is actively needed; client-coordination support stays human but doesn't need to span Phase 0 (no build yet) or Phase 4 (email/Braze handoff is Q03a/Q04's integration work, not config authoring). |

## Ownership split
All seven epics (E01-E07) are Salesforce-PS-delivered. Client-owned and excluded from both rosters: Acxiom contract/licensing and data rights, BigQuery schema/Data Mesh maintenance, Governance/CoE/change management/training (G0004), UAT execution and client-side test resourcing.

## Input provenance
Supplied by the Solution Lead: 24-week commitment, ownership split, AI-native override (2026-10-07), roster sign-off. Derived: all durations, hours, and FTE (`derive-hours.py`), efficiency bands (`efficiency.json`). Assumed: seven of eight size confidences are Unknown/Assumed, which widens ranges.
