## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **6 — Implement News & Regulatory Harvester v1 (A05)**.

Blocked by: **A01, B01, B02**.

## Objective

Implement the RSS and full-text article harvester (`src/atlas/ingestion/news_harvester.py`). It must asynchronously poll configured crypto-native RSS feeds (CoinDesk, Cointelegraph, Decrypt, The Block) and official regulatory feeds (SEC, CFTC, Fed), extract new items, fetch the full article HTML when needed, clean boilerplates using `trafilatura`, persist the raw wire content into WORM storage (`B01`), and emit valid `CanonicalDocument` objects with strict dual timestamps.

## Authority

Start from:
- `docs/contracts/CANONICAL_DOCUMENT.md` (`SourcePlatform.NEWS_CRYPTO`, `SourcePlatform.REGULATORY`)
- `docs/contracts/ATLAS_CONFIG_CONTRACT.md` (`sources.news.feeds`)
- Existing implementations: `ResilientHttpClient` (`A01`), `WormRawStore` (`B01`), `RegexFilterEngine` (`B02`).

## Expected artifact

1. Code: `src/atlas/ingestion/news_harvester.py` (`NewsHarvester` class)
2. Interface:
   - `poll_all_feeds() -> list[CanonicalDocument]`
   - `parse_feed_entry(entry: dict, raw_xml: str) -> CanonicalDocument`
3. Tests: `tests/test_news_harvester.py` (with static RSS fixture files).

## Acceptance

- Accurately parses standard RSS and Atom feed XML formats.
- Extracts clean article body text using `trafilatura` without navigation menus or cookie disclaimers.
- Enforces UTC timezone on `published_at` (from RSS pubDate) and records exact UTC `observed_at`.
- Persists raw XML/HTML bytes to WORM store before producing `CanonicalDocument`.
- Unit tests pass against checked-in RSS fixtures without live internet access.

## Stop conditions

Stop and report if news sites require paying for subscription paywalls or enterprise Bloomberg wire terminals.
