## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **7 — Implement Reddit & Telegram Social Harvesters v1 (A02, A03)**.

Blocked by: **A01, B01, B02**.

## Objective

Implement the social media connectors for Reddit (`src/atlas/ingestion/reddit_harvester.py`) and Telegram (`src/atlas/ingestion/telegram_harvester.py`):
1. **Reddit (`A02`)**: Poll submissions and top comments from target subreddits (`r/Bitcoin`, `r/CryptoCurrency`) using public JSON endpoints / RSS without paid API keys.
2. **Telegram (`A03`)**: Ingest messages from curated public crypto news & analyst channels using public channel preview endpoints or Telethon MTProto client.
3. Both connectors persist raw wire payloads to WORM storage (`B01`) and run text through Regex pre-filter (`B02`), producing `CanonicalDocument` records.

## Authority

Start from:
- `docs/contracts/CANONICAL_DOCUMENT.md` (`SourcePlatform.REDDIT`, `SourcePlatform.TELEGRAM`)
- `docs/contracts/ATLAS_CONFIG_CONTRACT.md` (`sources.reddit`, `sources.telegram`)
- Existing implementations: `ResilientHttpClient` (`A01`), `WormRawStore` (`B01`), `RegexFilterEngine` (`B02`).

## Expected artifact

1. Code:
   - `src/atlas/ingestion/reddit_harvester.py` (`RedditHarvester`)
   - `src/atlas/ingestion/telegram_harvester.py` (`TelegramHarvester`)
2. Tests: `tests/test_social_harvesters.py` (with static mocked payloads).

## Acceptance

- Reddit harvester handles pagination, extracts post title + selftext + comments, and captures author and created_utc.
- Telegram harvester handles channel text and media captions, capturing channel handle and timestamp.
- Strict dual timestamps recorded: UTC source `published_at` and system `observed_at`.
- Raw payloads persisted to WORM storage.
- Unit tests pass using offline mocked fixtures.

## Stop conditions

Stop and report if Reddit/Telegram integration requires unbudgeted commercial enterprise API tiers.
