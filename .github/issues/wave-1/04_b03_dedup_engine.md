## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **4 — Implement Anti-Sybil MinHash Deduplication Filter v1 (B03)**.

Blocked by: **B02**.

## Objective

Implement the near-duplicate and copy-pasta suppression filter (`src/atlas/processing/dedup.py`). Social botnets frequently flood networks with slight permutations of identical shilling messages to artificially manipulate sentiment volume. The engine must maintain a sliding 60-minute in-memory MinHash / SimHash ring buffer that detects documents with Jaccard text similarity $\ge 0.85$ and suppresses duplicate amplification.

## Authority

Start from:
- `docs/architecture/TARGET_ARCHITECTURE.md` (Stage 1 Filtering & Sybil suppression)
- `docs/product/CAPABILITY_DAG.md` (`B03` acceptance proposition)

## Expected artifact

1. Code: `src/atlas/processing/dedup.py` (`MinHashDedupFilter` class)
2. Interface:
   - `is_duplicate(text: str, observed_at: datetime) -> tuple[bool, float]` (returns is_dup, max_similarity)
   - `reset_window(before_timestamp: datetime)` (cleans expired hashes)
3. Tests: `tests/test_dedup.py`

## Acceptance

- Identifies identical and near-identical messages ($>85\%$ overlap with minor typo or extra link) as duplicate.
- Does not falsely flag recurring short market phrases (e.g. "Bitcoin price update", "daily recap") if the remaining text body is unique.
- Memory consumption bounded under 50 MB for 100,000 hashed signatures.
- Window expiration automatically evicts records older than 60 minutes.
- Unit tests pass.

## Stop conditions

Stop and report if deduplication requires persistent external databases (Redis/Postgres); the v1 filter must run in-memory within the ingestion worker.
