# Solution Architecture — Beyond Data Cloud & MCP ARI 2026

*Last updated: 2026-10-07*

This is the solution spine for the engagement: how Data 360 (Beyond's name for Salesforce Data Cloud) and Marketing Cloud Personalization (MCP) fit together across BBY US, Overstock, and BuyBuyBaby, and how each epic's work rides on that foundation. Architecture Foundations covers the horizontal decisions no single epic owns. Solution by Business Process walks the seven epics in build order — data foundation first, then the personalization engine, then each activation channel — with the supporting architecture woven into each one.

---

## Architecture Foundations

### AF1 — One Data 360 instance, existing org as home org

Beyond runs a single Data 360 instance rather than multiple independent instances or a Data Cloud One multi-org pattern. The three brands (BBY US, Overstock, BuyBuyBaby) don't need regulatory isolation, residency separation, or org-level autonomy from each other — the condition that would justify multiple instances — so one home org, tied to the existing Data 360 license, is the right default. `[KA-0016]`

### AF2 — One Business Unit + Data Space per brand

Each brand gets its own Business Unit in MC Next, and each Business Unit maps to exactly one Data Space — BBY US, Overstock, and BuyBuyBaby each get a dedicated Data Space. This is Marketing Cloud Next's documented partitioning model (not a Beyond-specific choice), and it's immutable once assigned, so it's a decision to get right before any Business Unit is provisioned. Content that's genuinely shared across brands (templates, reusable creative) goes through the Common Assets library rather than being duplicated per Data Space. `[KA-2766]`

### AF3 — Cross-brand activation is the one place AF2's isolation needs an explicit answer

Data Spaces have hard walls: no sharing data, content, campaigns, or access controls between them by default. E04's cross-entity requirement (a signal in one brand triggering a journey in another) runs directly into that wall. Two documented ways through it exist — a shared/default Data Space spanning the three brands instead of full per-brand isolation, or explicit Data Share (zero-copy, object-level cross-space sharing) scoped to just the DMOs backing this signal — but neither is picked yet. `[assumption: cross-entity activation scope — needs an explicit Data Space topology or Data Share configuration decision before build; validate with a Salesforce Data Cloud architect against KA-2766/KA-24122/KA-0016]`

### AF4 — Identity resolution defaults to Data 360's native Individual grain; household-grain Acxiom attributes are the open question

Data 360's documented, native identity-resolution grain is Individual → Unified Individual. That's the default this solution builds on. The Acxiom enrichment set doesn't fit that grain cleanly, though — most of its attributes (income, children-in-household, home value) are keyed at the household level, and one attribute is literally a household ID. No atom in the central knowledge base covers a household-grain resolution pattern, so reconciling household-grain Acxiom data onto person-grain Unified Individual profiles — likely a dedicated Household DMO or a flattening join — is a real design decision still open, not an established pattern to cite. `[assumption: household-to-individual resolution approach for Acxiom attributes — needs explicit architecture decision and validation; no central-KB atom covers household-grain resolution]`

### AF5 — Mostly configuration and connector setup; the custom work concentrates in web-event schema mapping

The bulk of this build is Data 360 connector configuration, Activation Target setup, and MC Next Business Unit/Data Space provisioning — declarative, not custom code. The one place real mapping work concentrates is web-event capture: the Salesforce Interactions SDK's unified event model (`sendEvent` API, identity/consent handling) needs explicit field-mapping work wherever a custom attribute lives under an event's `.attributes` collection, because those aren't auto-mapped to Data 360's Web Connector schema. That mapping effort is real, scoped, named work — not a config checkbox. `[KA-3063]` `[KA-3067]`

---

## Solution by Business Process

### Data 360 Foundation & BigQuery Sync

**Business context:** Beyond's customer data for all three brands lives today in four BigQuery tables (`bi_customer_account`, `bi_customer_storefront`, `bi_visit`, `bi_email_daily_summary`) — the system of record this entire engagement needs to read from.

**Solution approach:** Sync the four tables into Data 360 using a per-table decision between Zero Copy Data Federation and canonical Data Ingestion, rather than one pattern applied uniformly — the tables have genuinely different needs. `[KA-0015]` frames exactly this choice and recommends evaluating per-dataset; most real implementations land hybrid.

**Supporting architecture:** `bi_visit` (event-level, high-volume, latency-sensitive for personalization) is the strongest Zero Copy / Live Query candidate, but Zero Copy against BigQuery is capped at 10GB or 100 million rows before timeout — a real risk for a high-volume, multi-year, 3-brand table that needs validating against actual row counts before the pattern is locked (`gap: G0203`). `bi_customer_account` carries the one confirmed suppression field (Acxiom's DMA-suppression flag) and governance-sensitive attributes; Zero Copy doesn't support record deletion during incremental refresh, so this table needs an ingestion path regardless of what the rest of the schema uses (`gap: G0204`). Field- and type-level mapping between BigQuery's native types and Data 360's Data Model Objects is necessary, scoped work, not implied by picking a sync method (`gap: G0205`).

---

### Third-Party Enrichment (Acxiom)

**Business context:** Beyond's ~39-attribute Acxiom demographic/financial/lifestyle/property enrichment is live today for the current schema and needs to expand to cover all three brands.

**Solution approach:** Batch ingestion is the architecturally correct default for a periodic, non-time-sensitive third-party dataset like this — not real-time streaming. `[KA-0015]` establishes batch as the right default for this profile; `[KA-23607]` confirms Ingestion API, SDKs, MuleSoft Anypoint, and third-party connectors are the applicable connectivity paths for a non-Salesforce source like Acxiom.

**Supporting architecture:** The specific connector/delivery mechanism (SFTP flat file vs. programmatic API) and refresh cadence aren't confirmed with the client or Acxiom yet — that matters for freshness on decaying fields like move date and income (`gap: G0304`). The household-grain-vs-Individual-grain question (AF4) lands squarely here: this is the attribute set driving that fork. `[assumption: Acxiom delivery mechanism and refresh cadence — not yet confirmed with client/vendor; [KA-23607] grounds the connector category, not the specific choice]`

---

### MCP Next Remediation

**Business context:** MCP is already live at BBY US and Overstock and needs fixing — the engagement is framed as "Fix MCP Waterfall Work," a remediation of the existing install, not a greenfield build. Everything downstream (E04, E06, E07) runs on this engine, so getting it working correctly comes before layering new activation on top of it.

**Solution approach:** Remediate the two live instances and bring BuyBuyBaby's instrumentation up to the same standard, routed through the modern Salesforce Interactions SDK → Data 360 Web Connector path rather than legacy native MCP tagging — the standard web-event-capture pattern Salesforce now documents for Data 360 and Personalization. `[KA-3063]` `[KA-3067]`

**Supporting architecture:** The specific root-cause defects behind "fix the waterfall work" aren't itemized anywhere in the source material — this is the single highest-priority gap on the epic, since the whole track is staffed and estimated against an undiagnosed problem set (`gap: G0101`). The identity-field mapping at the MCP ↔ Data 360 connector seam has no named owner between the two tracks; Salesforce's documented default bundle maps Personalization Profile ID to the Data 360 Individual ID, but recommends aligning on a shared Customer ID as the party identifier — an architecture call, not a default to accept as-is. `[KA-23760]` BuyBuyBaby's catalog-feed/beacon setup is net-new work riding inside a "remediation" epic, and should use the SDK/Web Connector pattern consistently with BBY US/Overstock rather than inheriting the legacy approach by default (`gap: G0109`). `[assumption: specific root-cause defects in the current MCP install — not itemized in source docs]`

---

### MCP Personalization Activation

**Business context:** Beyond needs identity-resolved, unified-profile-driven activation inside MCP — near-real-time event messaging, scheduled segment audiences, cross-entity signal activation, value segmentation, and lifecycle targeting.

**Solution approach:** Scheduled segment audiences, value segmentation, and lifecycle targeting are a clean fit for Data 360's standard Segment Activation path into MCP via the Marketing Cloud Personalization connector. `[KA-23760]`

**Supporting architecture:** "Near-real-time event-based messaging" needs a direct flag before design locks: Data 360 reaches MCP only through Segment Activation, an asynchronous, scheduled-publish mechanism (12–24 hour cadence) — not through Data Action Targets, Data 360's actual synchronous mechanism, which explicitly does not list MCP as a supported target. `[KA-5871]` draws exactly this line (asynchronous Segment Activation vs. synchronous Data Action). If "near-real-time" is a literal requirement, that behavior has to come from MCP's own native event/decisioning layer, not a Data 360-side push (`gap: G0401`). Cross-entity signal activation (brand A activating brand B) is the AF3 fork — it needs the Data Space topology or Data Share decision made first (`gap: G0402`). Value and lifecycle segmentation both depend on Calculated Insights, which depend on identity resolution (AF4) and the Data Space decision (AF3) landing first — building segmentation logic ahead of those two decisions means rebuilding it later (`gap: G0403`). The MCP connector doesn't backfill historical engagement data from before its activation date, so lifecycle/cross-entity targeting that references "last purchase" or other historical milestones will cold-start at cutover rather than reflecting Beyond's existing MCP history (`gap: G0406`).

---

### Paid Media Activation

**Business context:** Beyond wants to activate Data 360 segments (lookalikes, non-marketing-email purchasers, seasonal/category purchasers, new movers, college-affiliated, expectant-family) out to five ad platforms: Google Ads, Facebook, Criteo, Pinterest, TikTok.

**Solution approach:** Segment activation to ad platforms is Data 360's standard asynchronous Data Integration pattern. `[KA-5871]` Google Ads and Facebook are native strategic-partner External Activation Targets; Criteo activates through a materially different connector tier — an AppExchange-published partner package, not Data 360's native strategic-partner setup flow — which is real, distinct build effort, not the same-shape work as the other two. `[KB: data_360_4-10-2026.md:124613-124619]`, cross-checked against `[KA-5871]`/`[KA-0031]`'s general pattern taxonomy, which doesn't break out the per-platform tier distinction.

**Supporting architecture:** Pinterest and TikTok's connector classification is unresolved — the client's own knowledge base names three different supported-platform lists across three sections, and no central-KB atom confirms either platform's Activation Target tier; a reporting feature listing them doesn't confirm they're buildable activation targets (`gap: G0501`). Every External Activation Target needs a CPRA privacy-type designation at setup, and no owner is named for that call across the five platforms, several of which will carry sensitive-adjacent Acxiom-sourced segment types (`gap: G0503`). The DMA-suppression field needs to be wired as a default-on Activation Membership filter, not a manual per-campaign step — paid media has no recall once an ad has served an impression (`gap: G0505`). `[assumption: Pinterest/TikTok connector tier — not confirmed by any central-KB atom; validate directly with Salesforce product docs or a live org check before staffing as same-effort builds alongside Google Ads/Facebook]`

---

### Web Experience Campaigns

**Business context:** Ten brand-neutral web use cases across the three brands, including beacon/catalog-feed setup, person-record enrichment with unified ID plus third-party attributes, and five named campaigns (mortgage targeting, income-based product recommendations, mover targeting, back-to-college seasonal, patio segmentation).

**Solution approach:** The five named campaigns build on the unified profile from E02/E03/E04 — personalization logic driven by Data 360 segments and attributes surfaced into MCP's decisioning.

**Supporting architecture:** No source or ingestion path is defined yet for the product catalog feed that powers MCP's recommendation engine across all ten use cases — this is a genuine coverage gap in both project knowledge and the central KB, not just an unanswered client question, and it needs an architect decision (direct commerce-platform-to-MCP feed vs. BigQuery → Data 360 → MCP) before this epic can be scoped (`gap: G0602`). Enriched attributes (income, move date, property type) aren't available to MCP's real-time decisioning until a visitor is identified and resolved to a Unified Individual, and even then Data 360's own refresh cadence can lag attribute availability by up to 15 minutes — any campaign assuming same-session attribute availability immediately after identification needs a fallback/default experience designed around that latency (`gap: G0603`). Whether campaign targeting logic lives natively in MCP's own decisioning framework or is built as Data 360 Audience/Segment Flows isn't decided, and it determines which track owns the bulk of the build for each campaign (`gap: G0604`). The income-based pricing campaign carries its own flagged risk, distinct from the general Acxiom compliance question: showing different price points based on inferred (not self-disclosed) income is a personalized-pricing practice several states have moved to regulate, and no atom in the central KB addresses retail personalized-pricing exposure — recommend Beyond's legal function review this specific use case before design locks (`gap: G0605`). `[assumption: catalog-feed ingestion path for MCP recommendations — genuine coverage gap, no atom in project knowledge or central KB names a direct product-catalog-to-legacy-MCP pattern]`

---

### Email Campaigns & Braze Integration

**Business context:** Seven brand-neutral email use cases, including one named use case — open-time mortgage-follow-up content — that hands content/data to Braze, a non-Salesforce ESP. The Salesforce delivery team owns building and maintaining that connection, not just a one-time export.

**Solution approach:** Only one of the seven email use cases is actually described in the source material; the other six are a bare count with no itemized scope and can't be sized until enumerated (`gap: G0701`). For the one named use case, the connection to Braze is a Salesforce-to-external integration — the only applicable grounding is the generic Type × Timing pattern-selection guide, since no Braze-specific atom exists in the central KB. `[KA-0138]` 🟡

**Supporting architecture:** Two forks are unresolved and should be flagged to the client before this epic's build starts, not inherited as settled: (1) whether Salesforce pushes to Braze or Braze pulls from a Salesforce/Data 360-exposed endpoint, and sync vs. async — each has a materially different build and ongoing-ops footprint (`gap: G0702`); and (2) "open-time" rendering implies content fetched at the moment of email open, not at send time — a different, likely larger mechanism (a public dynamic-content endpoint, or an AMP for Email component) than a standard triggered send, and nothing in the source material confirms which Braze expects or what Salesforce/Data 360 needs to expose. This could be the most expensive single use case in the epic if it requires new public-facing infrastructure, and no atom in two sessions of central-KB search covers open-time/AMP-style dynamic email content against an external ESP (`gap: G0703`). `[assumption: Braze open-time render mechanism — ungrounded; needs direct architect decision and Braze-side confirmation before build, flagged 🔴 per [KA-0138]'s generic-only coverage]`

---

## Grounding Summary

Grounding: 20 decisions tagged — 11 grounded, 2 inferred, 7 flagged assumptions: cross-entity activation scope (AF3), household-grain identity resolution (AF4), E01 remediation root cause, Acxiom ingestion mechanism (E03), Pinterest/TikTok/Criteo connector tier (G0501), income-based targeting legal exposure (G0605), Braze open-time render mechanism (G0703).

**Architecture-fork status:** G0303 🔴 (household-grain identity resolution — no atom covers this pattern) · G0401 🟢 `[KA-5871]` · G0402 🟢 `[KA-2766]`/`[KA-24122]`/`[KA-0016]` · G0501 🔴 (no atom confirms Pinterest/TikTok connector tier) · G0502 🟢 (project knowledge primary) · G0602 🟢 — resolved this session via `[KA-3063]`/`[KA-3067]` (upgraded from 🔴 in `requirements`) · G0605 — reclassified as a compliance/legal risk, not an architecture fork, carried forward · G0703 🟡 `[KA-0138]` generic only. Net: of the 5 forks that were 🔴 entering `design`, 2 remain 🔴 — both for reasons no architecture atom resolves (identity-model fit, partner-certification status), not for lack of searching.

**Phasing note:** This document doesn't assign any epic to a phase or wave. Where sequencing dependencies exist (e.g., E04's segmentation logic depending on AF3/AF4 landing first), they're called out as build-order constraints within the epic, not phase assignments — phasing itself is the client's call, to be made in `roadmap`.
