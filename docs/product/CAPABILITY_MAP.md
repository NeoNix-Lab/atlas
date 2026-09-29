# Capability Map

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** CANONICAL BASELINE v1.0  
**Authority:** Atom-level dependencies, acceptance propositions, and decision gates are formally tracked in [`CAPABILITY_DAG.md`](CAPABILITY_DAG.md).

Decision state and implementation state are intentionally separated:
- **Decision State**: `FROZEN | RESOLVED | OPEN_BLOCKING | OPEN_DEFERABLE`
- **Implementation State**: `COMPLETE | PARTIAL | MISSING`

| Domain | Capability | Decision State | Implementation State | Target Owner | Atom(s) | Notes |
|---|---|---|---|---|---|---|
| **Ingestion** | Scraper Resilience & Rate-Limit Engine | RESOLVED | MISSING | Ingestion Plane | A01 | Backoff, session rotation, proxy abstraction. |
| **Ingestion** | Social Connector: Reddit | RESOLVED | MISSING | Ingestion Plane | A02 | Subreddit polling (r/Bitcoin, r/CryptoCurrency) via RSS/API. |
| **Ingestion** | Social Connector: Telegram | RESOLVED | MISSING | Ingestion Plane | A03 | MTProto ingestion for curated crypto channels. |
| **Ingestion** | Social Connector: X / Twitter | OPEN_BLOCKING | MISSING | Ingestion Plane | A04 | Subject to DG-A (Syndication vs Guest scrapers vs Proxy pool). |
| **Ingestion** | News & Regulatory Feed Harvester | RESOLVED | MISSING | Ingestion Plane | A05 | RSS ingest + Trafilatura full-text extraction (CoinDesk, Cointelegraph, SEC/Fed). |
| **Ingestion** | On-Chain Bitcoin Mempool & Capital Flow Monitor | RESOLVED | MISSING | Ingestion Plane | A06 | Dual-stream: continuous mempool metrics -> D02; discrete whale/flow events -> B04 for Jev semantic typing. |
| **Ingestion** | Derivatives Microstructure Monitor | RESOLVED | MISSING | Ingestion Plane | A07 | Real-time WebSocket streaming for Bybit/Binance Funding Rates & Open Interest. |
| **Processing** | WORM Raw Storage Tier | FROZEN | MISSING | Data Plane | B01 | Write-Once-Read-Many immutable storage with SHA-256 payload identity. |
| **Processing** | High-Throughput Regex Engine | RESOLVED | MISSING | Data Plane | B02 | Pre-filtering spam signatures, cashtags ($BTC), and entity mentions at line rate. |
| **Processing** | Anti-Sybil & Duplicate Filter | RESOLVED | MISSING | Data Plane | B03 | Fast hashing (MinHash/SimHash) to drop bot copy-pasta and airdrop farms. |
| **Processing** | Canonical Document Contract | FROZEN | COMPLETE | Data Plane | B04 | Pydantic schema enforcing strict dual timestamping (`published_at` vs `observed_at`). Verified in Wave 0. |
| **Semantic AI**| Jev Schema & Questions Contract | FROZEN | COMPLETE | Semantic Plane | C01 | TypeSafe AI typed primitives (`Noul`, `Choice`, `Score`) for sentiment and on-chain intent. Verified in Wave 0. |
| **Semantic AI**| Jev Async Gateway & Dispatcher | RESOLVED | MISSING | Semantic Plane | C02 | Concurrency management, batching, and circuit breakers against `api.typesafe.ai`. |
| **Semantic AI**| Semantic Feature Vectorization | RESOLVED | COMPLETE | Semantic Plane | C03 | Deterministic mapping of Jev responses into normalized numerical features. Verified in Wave 0. |
| **Feature Store**| Time-Window Resampler (Point-in-Time)| FROZEN | MISSING | Feature Store | D01 | Rolling window aggregation (1m, 5m, 15m, 1h) without lookahead leakage. |
| **Feature Store**| Cross-Modal Feature Matrix | RESOLVED | MISSING | Feature Store | D02 | Alignment of text sentiment vectors with on-chain flows and derivatives data. |
| **Feature Store**| Canonical Parquet Materialization | FROZEN | MISSING | Feature Store | D03 | Partitioned Parquet feature tables ready for DuckDB / Arrow consumption. |
| **Representation**| JEPA Target State Formulation | OPEN_BLOCKING | MISSING | Modeling | E01 | Subject to DG-C (Forward return, realized vol, or orderbook state). |
| **Representation**| Multimodal Context Encoder | RESOLVED | MISSING | Modeling | E02 | Temporal sequence encoder over Jev features, on-chain flows, and price changes. |
| **Representation**| JEPA Target Encoder & Predictor | RESOLVED | MISSING | Modeling | E03 | Non-collapsing architecture (EMA target or VICReg loss) predicting latent dynamics. |
| **Representation**| Self-Supervised JEPA Pre-training | RESOLVED | MISSING | Modeling | E04 | Offline training loop optimizing latent prediction error. |
| **Quality & Proof**| Intrinsic Representation & Non-Collapse Proof | FROZEN | MISSING | Quality / Proof | F01 | VICReg criteria proof: $\text{Var}(z_j) \ge 1.0$ and low covariance. Guarantees non-trivial latent representations. |
| **Quality & Proof**| Divergence Signal Engine | RESOLVED | MISSING | Quality / Proof | F02 | Rule-based detector flagging divergence between crowd sentiment and capital flows. |
| **Integration** | quant-platform Feature Gateway | FROZEN | MISSING | Integration | F03 | Export adapter delivering verified `FeatureArtifact` tables conforming to `ADR-0034`. |
| **Operations** | Configuration Engine (`atlas.toml`) | FROZEN | MISSING | Operations (CLI) | G01 | Declarative schema for active sources, polling rates, and token budget limits. |
| **Operations** | CLI Runtime Controller (`atlas`) | RESOLVED | MISSING | Operations (CLI) | G02 | Click/Rich CLI managing `daemon`, `status`, `backfill`, and `export` commands. |
| **Operations** | Pipeline Probe & Diagnostic Tool | RESOLVED | MISSING | Operations (CLI) | G03 | Interactive CLI command (`atlas probe`) executing live trace across L0-L3 for arbitrary text. |
| **Operations** | Budget Guardrail & Circuit Breaker | FROZEN | MISSING | Operations (CLI) | G04 | Automatic hard stop / fallback to Regex-only mode upon exceeding daily dollar caps. |
