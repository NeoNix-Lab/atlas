## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **2 — Implement WORM Raw Storage Tier v1 (B01)**.

Blocked by: **none**.

## Objective

Implement the Write-Once-Read-Many (WORM) raw storage engine (`src/atlas/storage/worm_store.py`). The module must persist raw, unparsed payload bytes (JSON, XML, HTML) received from any harvester into partitioned gzipped files named strictly by their SHA-256 digest: `data/raw/<source>/YYYY-MM-DD/<sha256>.json.gz`. It must enforce append-only immutability, preventing overwrites or in-place mutations.

## Authority

Start from:
- `docs/architecture/TARGET_ARCHITECTURE.md` (Storage Tiering: Tier 0 RAW WORM)
- `docs/product/CAPABILITY_DAG.md` (`B01` acceptance proposition)
- `docs/contracts/CANONICAL_DOCUMENT.md` (`raw_storage_uri` & `raw_payload_sha256` lineage)

## Expected artifact

1. Code: `src/atlas/storage/worm_store.py` (`WormRawStore` class)
2. Interface:
   - `write_raw(source: str, payload_bytes: bytes, observed_at: datetime) -> tuple[str, str]` (returns uri, sha256)
   - `read_raw(uri: str) -> bytes`
   - `verify_integrity(uri: str, expected_sha256: str) -> bool`
3. Tests: `tests/test_worm_store.py`

## Acceptance

- Payloads are written to `data/raw/<source>/<YYYY-MM-DD>/<sha256>.json.gz`.
- Files are compressed with gzip.
- Overwriting an existing file with different bytes raises a strict `ImmutabilityViolationError`.
- SHA-256 digest recalculation matches 100% of persisted files.
- Unit tests pass with $>95\%$ branch coverage.

## Stop conditions

Stop and report if storage requires external cloud drivers or distributed file systems; Tier 0 must execute on the local POSIX/Windows filesystem.
