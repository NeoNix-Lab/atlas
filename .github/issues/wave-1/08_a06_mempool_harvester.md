## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **8 — Implement Dual-Stream On-Chain Mempool & Capital Flow Monitor v1 (A06)**.

Blocked by: **B01, B02**.

## Objective

Implement the on-chain Bitcoin ingestion monitor (`src/atlas/ingestion/mempool_harvester.py`) operating over public mempool API endpoints (e.g., `mempool.space/api`):
1. **Continuous Stream**: Periodically poll median fee rates (sat/vB), unconfirmed transaction count, and fee velocity, emitting continuous telemetry for direct Feature Store aggregation.
2. **Discrete Capital Events**: Monitor and detect whale transactions ($\ge 100$ BTC), exchange cluster transfers, and large movements. Format each event into a `CanonicalDocument` with `onchain_data: OnChainMetadata` and route it to WORM storage (`B01`), making it ready for downstream Jev semantic typing.

## Authority

Start from:
- `docs/architecture/TARGET_ARCHITECTURE.md` (Dual-channel on-chain routing)
- `docs/contracts/CANONICAL_DOCUMENT.md` (`SourcePlatform.ONCHAIN_EVENT`, `OnChainMetadata`)
- `docs/contracts/ATLAS_CONFIG_CONTRACT.md` (`sources.onchain`)

## Expected artifact

1. Code: `src/atlas/ingestion/mempool_harvester.py` (`MempoolHarvester`)
2. Interface:
   - `poll_mempool_state() -> MempoolTelemetry`
   - `poll_whale_events(threshold_btc: float = 100.0) -> list[CanonicalDocument]`
3. Tests: `tests/test_mempool_harvester.py` (with static mempool response fixtures).

## Acceptance

- Accurately parses recommended fee rates (`fastestFee`, `halfHourFee`, `minimumFee`).
- Identifies transactions $\ge 100$ BTC and extracts txid, total BTC amount, and input/output cluster labels if present.
- Emits discrete transactions as valid `CanonicalDocument` objects with `SourcePlatform.ONCHAIN_EVENT` and `onchain_data` populated.
- Persists raw JSON responses to WORM storage (`B01`).
- Unit tests pass against checked-in JSON fixtures.

## Stop conditions

Stop and report if implementation requires running a 600GB local Bitcoin archival full node; v1 must utilize lightweight public RPC / mempool APIs.
