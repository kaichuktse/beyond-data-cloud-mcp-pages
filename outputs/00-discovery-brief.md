# Discovery Brief — Beyond Data Cloud & MCP ARI 2026

*Last updated: 2026-10-07*

## Executive Summary

Beyond (the multi-brand retailer behind BBY US, Overstock, and BuyBuyBaby) needs its Marketing Cloud Personalization (MCP) implementation fixed — not built from scratch — alongside a parallel Data 360 (Data Cloud) build-out that feeds it. The two tracks run on a shared 24-week waterfall schedule (Oct 5, 2026 → Mar 15, 2027) with an internal staffing draft of $800,000 across 6,825 hours. This is a remediation engagement with a build-out riding alongside it, which changes the risk profile versus a greenfield project: root-cause unknowns on the existing MCP install carry real schedule risk that a clean build wouldn't have.

## Company and Industry Context

Beyond is a multi-brand e-commerce retailer. Brands referenced across the discovery material: BBY US, Overstock, BuyBuyBaby (in scope for this engagement — confirmed), plus Kirkland Homes, Container Store, and Zulily (named in prior scope versions, now out of scope — Kirkland Homes and Container Store are explicitly struck through as requiring new MCP implementations the client isn't pursuing; Zulily was in the 2024 Implementation footprint but dropped from Current Scope).

## Current vs. Target Salesforce Landscape

- **Current state:** MCP (Marketing Cloud Personalization, née Interaction Studio/Evergage) is already installed and live at BBY US and Overstock.
- **Target state:** Two parallel delivery tracks:
  - **MCP Next** — fixes/modernizes the existing MCP implementation (per the engagement's "Fix MCP Waterfall Work" framing, confirmed as remediation, not a naming coincidence).
  - **Data 360** (the client's name for Data Cloud) — new foundation to feed enriched, unified customer data into MCP and paid-media activation.
- **Explicitly out of scope:** Salesforce CRM ↔ Data Cloud connectors — the scope table lists **0** across every scope column (June Scoping Questions, 2024 Implementation, and Current Scope alike). This isn't a gap; it's a stated non-goal.

## Project Scope and Objectives

**In-scope domains (confirmed):** BBY US, Overstock, BuyBuyBaby — 3 domains, 1 language (English), 1 mobile app.

**Data pipeline:**
- Google BigQuery → Data 360 sync (Zero Copy or Acceleration) across 4 Customer Data Mesh tables: `bi_customer_account`, `bi_customer_storefront`, `bi_visit`, `bi_email_daily_summary`. An updated schema has already been provided; the client asked whether other tables should be added — unresolved.
- 3rd-party enrichment via Acxiom, layered onto records outside the core data-mesh schema (demographic, financial, lifestyle, and property attributes — ~39 fields including income ranges, children-in-household, education, and home value). This is **complete for the current schema today**, and **expanding it to all brands is confirmed in scope for this estimate** — not a deferred future phase.

**Activation:**
- MCP Personalization — near-real-time event-based messaging, scheduled segment audiences, cross-entity purchase/browse signal activation, value segmentation, lifecycle targeting.
- Paid media — Google Ads, Facebook, Criteo, Pinterest, TikTok. Segment types include lookalikes, non-marketing-email purchasers, seasonal/category purchasers, new movers, college-affiliated, and expectant-family audiences.
- Web campaigns (10 brand-neutral use cases) and email campaigns (7 brand-neutral use cases), including beacon/catalog-feed setup, person-record enrichment with unified ID + 3rd-party attributes, and five named web campaigns (mortgage targeting, income-based product recs via Einstein, mover targeting, back-to-college seasonal, patio category segmentation).
- **Braze integration is confirmed in scope** — one email use case (open-time email content for mortgage follow-up) hands content/data to Braze, a non-Salesforce ESP, and the Salesforce delivery team is responsible for building that connection, not just producing a one-time export.

**Delivery shape:** 24-week waterfall schedule, Oct 5, 2026 → Mar 15, 2027, phased Discover → Define → Design → Deliver → SIT/UAT → UAT → Deploy → Scale, run across two tracks (MCP Next, Data 360) plus a Program Oversight (PM) role spanning both.

**Staffing (internal draft, not yet shared with the client):** $800,000 / 6,825 hours total.
- MCP Next: MC Sr Solution Architect (Onshore), MC Sr Technical Architect, Sr Developer, Developer, QA Consultant (GDC India)
- Data 360: MC Solution Architect (Onshore), MC Technical Architect, Sr Developer, QA Consultant (GDC India), Sr. Experience Architect (Onshore)
- Program Oversight: Project Manager (Onshore), spanning the full 24 weeks

This figure is an internal staffing-plan draft the client has not seen — carried here as planning context only, not as validated or quotable pricing. Per the engagement's pricing gate, no indicative price can be issued to the client until a rate is supplied and validated through the `commercials` skill.

## Data and Compliance Considerations

The Acxiom enrichment set includes sensitive-adjacent attributes — estimated income, presence/age of children, marital status, home value, move date — layered onto customer records for targeting (including a mortgage-interest use case and family/parent-stage segmentation). One field is explicitly a SHA-256-hashed email list for matching. No compliance or regulatory framework (CCPA, state privacy law, DMA/postal suppression obligations beyond the one listed field) is discussed in the source material — this is an **open question**, not a confirmed gap, given the sensitivity of the data in play.

## Open Questions

The following were deliberately deferred to a client question list rather than resolved internally — they don't block this brief, but should go back to Beyond before design work locks in:

1. **End users and personas.** No user counts, named roles beyond two individuals ("Dave," who owns the scoping/LOE spreadsheets referenced in the source docs; "Henrik Braemus," cited as an example candidate for the "1 onshore SA/TA" role noted in Scope v2). Who are the actual stakeholders, approvers, and day-to-day operators of MCP and Data 360 on Beyond's side?
2. **Compliance and privacy posture.** Given the Acxiom attribute set (income, children, home value, move date, etc.), what privacy framework governs this data (CCPA or other state law), and are there retention, consent, or suppression requirements beyond the single DMA-suppression field already listed?
3. **Data migration.** Not mentioned anywhere in the source material — is there legacy MCP configuration, segment, or audience data that needs to carry forward, or is this a clean cutover on the existing live install?
4. **Governance and change management.** No mention of a Center of Excellence, training plan, or adoption/change plan for the teams operating MCP and Data 360 post-launch. Who owns ongoing campaign management and data-attribute governance after go-live?
5. **BigQuery schema completeness.** The client's own question remains unresolved in the source docs: should additional tables beyond the 4 listed (`bi_customer_account`, `bi_customer_storefront`, `bi_visit`, `bi_email_daily_summary`) be included in the Data 360 ↔ BigQuery sync?
6. **Paid media segment volume.** The client's own question remains unresolved: exactly how many target segments are required per paid channel (Google, Facebook, Criteo, Pinterest, TikTok)?

## Research Findings and Market Context

Not run this session — the user opted to skip web research for now. Available on request via the `discover` skill.

---

## Terminology (client-specific)

| Beyond's term | Meaning |
|---|---|
| MCP | Marketing Cloud Personalization — the product formerly known as Interaction Studio / Evergage |
| MCP Next | The remediation/modernization track for the existing MCP implementation |
| Data 360 | Beyond's name for Salesforce Data Cloud |
| Data Mesh | Beyond's internal BigQuery schema/table naming convention for customer data |
| "Dave's SPW" / "Dave's LOE" | Internal scope and level-of-effort spreadsheets referenced but not included in the discovery package (Google Sheets links only) |
