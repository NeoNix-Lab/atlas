## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **10 — Wave 1 Golden E2E: Prove Deterministic Ingestion & Regex Line-Rate Performance**.

Blocked by: **all Wave 1 implementation slices (#1, #2, #3, #4, #5, #6, #7, #8, #9)**.

## Objective

Build and execute the authoritative Golden End-to-End integration proof for Wave 1 (`tools/wave1_golden_e2e.py`).  
Run an end-to-end deterministic verification over a checked-in, frozen 1,000-message test corpus (`fixtures/wave1_corpus_1000_frozen.json`), demonstrating that:
1. Ingestion loads raw payloads and writes to WORM raw storage with exact SHA-256 content addressing.
2. High-throughput Regex L1 processes the full 1,000 items in $< 200$ ms ($> 5,000$ docs/sec line rate).
3. The engine successfully rejects $\ge 75\%$ of the known spam population while dropping 0% of legitimate Bitcoin financial news.
4. Record closeout evidence in `docs/integration/WAVE1_GOLDEN_E2E_DETERMINISTIC_INGESTION.md`.

## Authority

Start from:
- `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md` (Section 4 Golden Proof specification)
- `fixtures/wave1_corpus_1000_frozen.json`
- All Wave 1 modules: `worm_store.py`, `regex_filter.py`, `dedup.py`, `resilience.py`, harvesters.

## Expected artifact

1. Runner tool: `tools/wave1_golden_e2e.py`
2. Test: `tests/test_wave1_golden_e2e.py`
3. Fixture: `fixtures/wave1_corpus_1000_frozen.json`
4. Proof document: `docs/integration/WAVE1_GOLDEN_E2E_DETERMINISTIC_INGESTION.md`

## Acceptance

- `python tools/wave1_golden_e2e.py --json` exits with code 0 and emits structured pass evidence.
- Measured execution throughput exceeds $5,000$ documents/sec.
- Measured spam rejection rate on the spam subset is $\ge 75\%$.
- False rejection rate on the legitimate news subset is exactly $0\%$.
- All 1,000 raw payloads have verified WORM SHA-256 entries in `data/raw/`.
- Repository verification passes (`python -m pytest tests`, `ruff check .`).

## Stop conditions

Stop and report if the Regex L1 engine fails to achieve $>5,000$ docs/sec throughput or if legitimate financial news headlines are rejected by the spam filter.
