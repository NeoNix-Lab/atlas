## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **5 — Implement Ingestion Resilience & Rate-Limiter Engine v1 (A01)**.

Blocked by: **B01**.

## Objective

Implement the reusable asynchronous network client and resilience layer (`src/atlas/ingestion/resilience.py`). All downstream harvesters (News, Reddit, Telegram, Mempool) must execute through this engine. It provides token-bucket rate limiting per host, exponential backoff with full jitter on HTTP 429/503 status codes, user-agent/fingerprint rotation, and proxy interface routing.

## Authority

Start from:
- `docs/architecture/TARGET_ARCHITECTURE.md` (Ingestion Plane A01)
- `docs/contracts/ATLAS_CONFIG_CONTRACT.md` (Proxy configuration, poll intervals)

## Expected artifact

1. Code: `src/atlas/ingestion/resilience.py` (`ResilientHttpClient` class wrapping `httpx.AsyncClient`)
2. Interface:
   - `get(url: str, params: dict | None, headers: dict | None) -> httpx.Response`
   - Configurable retry count, backoff multiplier, and per-domain rate limits.
3. Tests: `tests/test_resilience.py` (using `pytest-mock` to test 429 backoff, retry exhaustion, and proxy injection).

## Acceptance

- Successfully recovers from simulated HTTP 429 responses with exponential backoff.
- Distinguishes non-retryable 4xx client errors from transient 5xx server errors.
- Never crashes the parent ingestion daemon on network timeouts or connection drops.
- Unit tests pass.

## Stop conditions

Stop and report if implementation requires heavy browser automation frameworks (Playwright/Selenium); A01 must remain an ultra-fast async HTTP client.
