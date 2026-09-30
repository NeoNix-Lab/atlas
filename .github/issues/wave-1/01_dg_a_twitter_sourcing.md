## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **1 — Design Gate DG-A: Twitter / X Sourcing & Proxy Resilience Policy v1**.

Blocked by: **none**.

## Objective

Resolve Decision Gate `DG-A` by formalizing an Architectural Decision Record (`ADR-0001-twitter-sourcing-and-proxy-resilience-v1.md`). Evaluate the trade-offs between official X API pricing ($100+/mo), guest token scrapers, syndication endpoints, and residential proxy rotation pools. Establish an immutable harvesting policy that bounds monthly proxy spend under €20/month while guaranteeing resilient ingestion of `$BTC` cashtag mentions.

## Authority

Start from:
- `docs/product/PRODUCT.md` (Cost success metrics: OPEX bounded under €25/mo)
- `docs/product/CAPABILITY_DAG.md` (`A04` acceptance proposition)
- `docs/product/ROADMAP.md` (`DG-A` entry)
- `docs/architecture/TARGET_ARCHITECTURE.md` (External sources topology)

## Expected artifact

`docs/architecture/ADR-0001-twitter-sourcing-and-proxy-resilience-v1.md` defining:
1. Exact harvesting strategy (syndication/guest tokens vs proxy pool).
2. Rate-limit backoff thresholds and circuit-breaker integration.
3. Fallback behavior when encountering Cloudflare/HTTP 429/403.
4. Concrete acceptance bounds for subsequent implementation of atom `A04`.

## Acceptance

- `ADR-0001` is written, reviewed, and checked into `docs/architecture/`.
- The decision does NOT rely on unbudgeted enterprise API tiers.
- Explicit non-complete/fallback disposition is documented if endpoints degrade.
- Decision state of `A04` in `CAPABILITY_MAP.md` is updated from `OPEN_BLOCKING` to `RESOLVED`.

## Stop conditions

Stop and report if resolution requires paying for official Twitter Enterprise API or violates the project's €25/month OPEX ceiling.
