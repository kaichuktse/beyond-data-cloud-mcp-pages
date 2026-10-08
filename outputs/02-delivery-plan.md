# Delivery Plan — Beyond Data Cloud & MCP ARI 2026

Total program duration: **24 weeks** (per user commitment — matches the internal staffing draft's schedule, Oct 5, 2026 → Mar 15, 2027, carried forward from discovery as the operative target).

**Critical path: E02 → E03 → (E05, E06, E07)** — Data 360 Foundation and Acxiom Enrichment gate every downstream activation epic (paid media, web experience, email/Braze); slippage on either cascades through the rest of the build. MCP Next Remediation (E01) runs as an independent parallel track and does not sit on this path — it's grounded directly in the internal staffing draft's own schedule grid, which runs MCP Next as its own 20-week lane alongside the Data 360 track, not sequenced after it.

---

## Phase 0 — Discovery & Architecture Decisions (3 weeks)
**Objective:** Resolve the architecture forks that gate downstream build before any epic starts.
- Data Space/Data Share topology (AF3 / G0402)
- Identity-resolution grain for household-level Acxiom attributes (AF4 / G0303)
- Pinterest/TikTok connector-tier classification (G0501)
- Braze connection direction and open-time render mechanism (G0702/G0703)
- MCP Next root-cause audit scope (G0101)

**Success criteria:** AF3/AF4 ratified and documented; MCP Next audit scoped; connector-tier and Braze-pattern forks closed or deferred with a named owner.
**Dependencies:** None — gates everything downstream.
**Risk:** Any fork left open past this phase pushes rebuild risk onto E03/E04 (G0403).

## Phase 1 — Data 360 Foundation (4 weeks)
**Epics:** E02
**Objective:** Stand up Data 360; sync the 4 BigQuery Customer Data Mesh tables (bi_customer_account, bi_customer_storefront, bi_visit, bi_email_daily_summary); land identity resolution and Data Space topology per Phase 0.
**Success criteria:** 4 tables syncing via the confirmed per-table pattern (Zero Copy / ingestion / hybrid); identity resolution live; Data Space topology matches the AF3 decision.
**Depends on:** Phase 0 architecture decisions.
**Risk:** Zero Copy volume ceiling on high-volume tables (G0203); suppression-field delete semantics (G0204); lower-environment BigQuery connectivity for SIT/UAT unconfirmed (G0209).

## Phase 2 — Enrichment & Personalization Activation (7 weeks)
**Epics:** E03, E04
**Objective:** Layer Acxiom's ~39-attribute set onto Data 360 records across all 3 brands at the resolved identity grain, then activate enriched segments into MCP (scheduled audiences, value segmentation, lifecycle targeting). Near-real-time and cross-entity sub-types remain pending final AF3/AF4 confirmation.
**Success criteria:** Acxiom attributes land on Unified Individual records across BBY US, Overstock, BuyBuyBaby with suppression/compliance handling; MCP activation live for scheduled/value/lifecycle segments.
**Depends on:** E02 — both epics need Data 360's identity resolution and record structure in place first.
**Risk:** Household-vs-Individual grain mismatch (G0303); near-real-time requirement vs. Data 360's async-only activation path (G0401); no historical backfill creates a cold-start risk at cutover (G0406).

## Phase 3 — Paid Media & Web Experience (7 weeks)
**Epics:** E05, E06
**Objective:** Activate Data 360 segments to 5 ad platforms (Google Ads, Facebook, Criteo, Pinterest, TikTok); build the 10 web experience use cases (beacon/catalog-feed setup, person-record enrichment, 5 named campaigns).
**Success criteria:** 5 ad platforms receiving segments via the confirmed connector tier per platform; 10 web use cases live across 3 brand surfaces.
**Depends on:** E02, E03.
**Risk:** Pinterest/TikTok connector-tier classification unresolved (G0501); catalog-feed-to-MCP ingestion path undefined (G0602); income-based pricing campaign carries a flagged legal/compliance exposure (G0605) — route to Beyond's legal function before this phase locks.

## Phase 4 — Email Campaigns & Braze Integration (3 weeks)
**Epics:** E07
**Objective:** Build and launch the 7 brand-neutral email use cases, including the mortgage-follow-up open-time-content use case handing content/data to Braze.
**Success criteria:** 7 email use cases live; Braze connection built and operating per the Phase 0 decision.
**Depends on:** E02, E03.
**Risk:** 6 of 7 use cases were un-itemized at discovery time (G0701); Braze credential/contract access is an external dependency against this schedule (G0707) — flagged as the single highest-cost risk in the epic if open-time rendering requires new public-facing infrastructure (G0703).

## Phase 5 — MCP Next Remediation (20 weeks, parallel track)
**Epics:** E01
**Objective:** Audit and fix the live BBY US/Overstock MCP implementation; bring BuyBuyBaby onto the modern Interactions SDK → Data 360 Web Connector pattern. Runs concurrently with Phases 1-4, not sequenced after them — this mirrors the internal staffing draft's own two-track schedule.
**Success criteria:** Root-cause defects on BBY US/Overstock remediated; BuyBuyBaby net-new instrumentation live.
**Depends on:** Phase 0 (cross-track identity-mapping decision, G0102).
**Risk:** No root-cause defect list exists yet (G0101) — the whole track is estimated against an assumption; holiday change-freeze risk (Black Friday/Cyber Monday) sits inside this delivery window (G0104).

---

## Standard Processes
- **Testing:** SIT/UAT cadence per phase, consistent with the staffing draft's own SIT/UAT → UAT → Deploy → Scale cadence on both tracks.
- **Deployment:** Phased go-lives aligned to each phase's success criteria, not a single big-bang cutover.
- **Training/change management:** Flagged as an open discipline gap across multiple epics (G0106/G0107, G0207, G0305, G0405/G0407, G0503/G0507, G0606/G0607, G0705/G0706) — not yet confirmed in or out of scope. Recommend a deliberate client conversation before this plan locks.

## Consolidated Risk Table

| Risk | Gap(s) | Phase(s) Affected | Note |
|------|--------|--------------------|------|
| No root-cause defect list for MCP Next | G0101 | 5 | Whole track estimated against an assumption; could resize to XL |
| Holiday change-freeze (Black Friday/Cyber Monday) inside the delivery window | G0104 | 5 | Internal staffing-draft risk, not a client-committed external date |
| Lower-environment BigQuery connectivity unconfirmed | G0209 | 1 | Could block SIT/UAT timing |
| Household-grain Acxiom attributes vs. Data 360's Individual-grain resolution | G0303 | 0, 2 | 🔴 ungrounded architecture fork at design time |
| Cross-entity activation vs. Data Space isolation | G0402 | 0, 2 | 🟢 grounded fork; topology still undecided |
| Near-real-time requirement vs. async-only activation path | G0401 | 2 | Could force native-MCP build, larger than currently scoped |
| Pinterest/TikTok connector-tier classification | G0501 | 0, 3 | 🔴 ungrounded; 3 conflicting lists in client's own KB |
| Catalog-feed-to-MCP ingestion path undefined | G0602 | 3 | 🔴 ungrounded; two candidate patterns with very different cost |
| Income-based pricing legal/compliance exposure | G0605 | 3 | Needs Beyond's legal function, not a KB search |
| Braze connection pattern + open-time render mechanism | G0702, G0703 | 0, 4 | 🟡/🔴 — single most expensive use case risk in E07 |
| Braze credential/contract access | G0707 | 4 | External dependency outside this engagement's control |

## Team & Roster
The disciplines and named roster to deliver this plan — with defensible counts, per lane — come from `estimate`.

---

## Deliverables
- `/Users/ktse/Documents/Clients/Beyond Data Cloud & MCP ARI 2026/data/roadmap.json`
- `/Users/ktse/Documents/Clients/Beyond Data Cloud & MCP ARI 2026/data/csv/03-roadmap-phases.csv`
- `/Users/ktse/Documents/Clients/Beyond Data Cloud & MCP ARI 2026/outputs/02-delivery-plan.md`
- `/Users/ktse/Documents/Clients/Beyond Data Cloud & MCP ARI 2026/outputs/`
