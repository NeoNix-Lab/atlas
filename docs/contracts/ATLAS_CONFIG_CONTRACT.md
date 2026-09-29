# Contract: Atlas Configuration Contract v1 (`ATLAS_CONFIG_CONTRACT.md`)

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** FROZEN  
**Schema Identifier:** `atlas/configuration@1`  
**Governed Atoms:** `G01`, `G04`

---

## 1. Specification & Philosophy

Atlas configuration follows the strict hierarchy established in `quant-platform`:
$$\text{CLI Flags} > \text{Environment Variables (.env)} > \text{atlas.toml} > \text{Hardcoded Safe Defaults}$$

1. **Secret Separation**: API keys (`TYPESAFE_API_KEY`, proxy credentials, Telegram secrets) must NEVER be written to `atlas.toml`. They are exclusively loaded from environment variables or a local `.env` file excluded by `.gitignore`.
2. **Deterministic Validation**: The configuration file is validated using a strict Pydantic model (`AtlasConfig`). Any typo, unrecognized field, or type error fails fast at startup (`Exit Code 1`).
3. **Hard Budget Guardrails**: Token limits are enforced by default to prevent accidental billing overruns.

---

## 2. Canonical `atlas.toml` Template

```toml
[system]
environment = "production"          # "development" | "staging" | "production"
data_dir = "data"                   # Root path for raw WORM, canonical, and features
log_level = "INFO"                  # "DEBUG" | "INFO" | "WARNING" | "ERROR"
max_concurrent_workers = 8

[budget]
max_daily_token_spend_usd = 1.50    # Hard limit on daily TypeSafe AI API spend
max_monthly_token_spend_usd = 30.00 # Hard limit on monthly TypeSafe AI API spend
circuit_breaker_on_limit = true     # When true, falls back to Regex-only mode if limit hit

[sources.reddit]
enabled = true
subreddits = ["Bitcoin", "CryptoCurrency"]
poll_interval_seconds = 30
max_items_per_poll = 50

[sources.telegram]
enabled = true
channels = [
    "@whale_alert_io",
    "@tier10_k",
    "@BitcoinMagazine"
]
poll_interval_seconds = 10

[sources.news]
enabled = true
feeds = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.theblock.co/rss.xml"
]
poll_interval_seconds = 60

[sources.onchain]
enabled = true
mempool_api_url = "https://mempool.space/api"
whale_threshold_btc = 100.0         # Transfers >= 100 BTC trigger discrete Jev evaluation
poll_interval_seconds = 15

[sources.derivatives]
enabled = true
venues = ["binance", "bybit"]
symbols = ["BTCUSDT"]
reconnect_interval_seconds = 5

[regex_rules]
min_spam_confidence_to_drop = 0.70
blocked_patterns = [
    "giveaway",
    "send 0.1 btc",
    "claim your airdrop",
    "t.me/claim",
    "guaranteed returns",
    "pump and dump"
]
target_symbols = ["BTC", "WBTC", "SATS", "LIGHTNING"]

[feature_store]
active_resolutions = ["1m", "5m", "15m", "1h"]
compression = "zstd"
retention_raw_days = 90
retention_canonical_days = 365
```

---

## 3. Environment Variables Specification (`.env`)

| Variable Name | Required | Default | Description |
|---|---|---|---|
| `TYPESAFE_API_KEY` | **Yes** | None | Authentication token for `api.typesafe.ai` |
| `ATLAS_CONFIG_PATH` | No | `atlas.toml` | Custom path to configuration file |
| `HTTP_PROXY_URL` | No | None | Optional residential/datacenter proxy pool URL |
| `TELEGRAM_API_ID` | No | None | Optional Telegram MTProto app ID |
| `TELEGRAM_API_HASH`| No | None | Optional Telegram MTProto app hash |
