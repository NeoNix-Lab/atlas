# [epic] Wave 1 — Ingestion Data Plane & Deterministic Regex L1 Engine

## Scope
Derived from `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md` and `SCOPE.md`.

## Macro Objective
Implement the high-throughput, fault-tolerant ingestion data plane and the zero-compute deterministic line-rate filtering engine:
1. Sourcing: Ingest Reddit, Telegram, Crypto/Macro News, Mempool, Whale events, and Derivatives feeds.
2. Storage Tier 0: Append-only WORM raw storage with SHA-256 content addressing.
3. Pre-filtering L1: Compiled Regex suite processing in <200us per doc and dropping >=75% of social spam.
4. Golden Proof: End-to-end deterministic proof over a frozen 1,000-message corpus.

## Governed Atoms
- `DG-A` (Twitter Sourcing Decision Gate)
- `B01` (WORM Raw Storage Tier)
- `B02` (High-Throughput Regex Engine)
- `B03` (Anti-Sybil MinHash Deduplication)
- `A01` (Resilience & Rate-Limiter Engine)
- `A05` (News & Regulatory Harvester)
- `A02` / `A03` (Reddit & Telegram Social Harvesters)
- `A06` (Dual-Stream Mempool & Whale Flow Monitor)
- `A07` (Derivatives Microstructure Monitor)
- `Wave 1 Golden Proof` (Deterministic Ingestion Proof)

## Acceptance Proposition
Wave 1 closes when all sub-issues are merged into `implement/wave-1`, `tools/wave1_golden_e2e.py` passes, and `docs/integration/WAVE1_GOLDEN_E2E_DETERMINISTIC_INGESTION.md` is recorded.
