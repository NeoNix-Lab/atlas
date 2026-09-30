## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **3 — Implement High-Throughput Line-Rate Regex Engine v1 (B02)**.

Blocked by: **B01**.

## Objective

Implement the compiled deterministic Regex pre-filtering engine (`src/atlas/processing/regex_filter.py`). It must parse raw text payloads at sub-millisecond line-rate ($<200 \mu s$ per payload, $>5,000$ payloads/sec), extract cryptocurrency ticker and entity mentions (`$BTC`, `Bitcoin`, `WBTC`, `Sats`, `Lightning`), compute a continuous `regex_spam_score` $[0.0, 1.0]$ based on known giveaway, airdrop phishing, and shilling signatures, and make the binary drop/pass decision.

## Authority

Start from:
- `docs/contracts/CANONICAL_DOCUMENT.md` (`EntityMention`, `has_btc_mention`, `regex_spam_score`)
- `docs/contracts/ATLAS_CONFIG_CONTRACT.md` (`blocked_patterns`, `target_symbols`, `min_spam_confidence_to_drop`)
- `docs/architecture/TARGET_ARCHITECTURE.md` (Stage 1 Filtering Funnel)

## Expected artifact

1. Code: `src/atlas/processing/regex_filter.py` (`RegexFilterEngine` class)
2. Interface:
   - `inspect_text(text: str) -> RegexMatchResult`
   - `RegexMatchResult`: contains `is_spam: bool`, `spam_score: float`, `has_btc: bool`, `entities: list[EntityMention]`, `clean_text: str`.
3. Tests: `tests/test_regex_filter.py` (including speed benchmark test verifying $>5,000$ docs/sec).

## Acceptance

- Benchmark test proves single-core execution time $< 200 \mu s$ per 280-char document.
- Accurately tags $BTC, #Bitcoin, WBTC, Satoshi, Lightning as `BTC` mentions with exact character spans.
- Scores known spam phrases (airdrop phishing, private key scams, fake giveaway templates) with `spam_score >= 0.70`.
- Zero false drops on legitimate financial news headlines (e.g. Fed rates, ETF net flows, exchange security updates).
- Unit tests pass.

## Stop conditions

Stop and report if implementation requires heavy NLP libraries (spaCy, NLTK, transformers); Regex L1 must run on pure compiled Python `re` / C-regex primitives.
