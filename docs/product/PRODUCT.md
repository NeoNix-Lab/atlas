# PRODUCT.md

**Project:** BTC Multi-Modal Sentiment Engine (`Sentiment`)  
**Status:** DRAFT v0.1 — Product baseline and governance foundation  
**Target:** High-throughput, multi-modal Bitcoin market sentiment engine with point-in-time correctness, deterministic regex pre-filtering, TypeSafe Jev semantic typing, and JEPA latent state representation.  
**Canonical codebase:** `Sentiment`  
**Downstream integration:** `quant-platform` (Feature Store & Strategy Engine)

---

## 1. Product Mission

`Sentiment` is the authoritative engine for harvesting, parsing, semantically classifying, and fusing market-wide sentiment signals for Bitcoin (BTC).

The platform transforms unstructured and noisy external streams (social media, mainstream news, regulatory releases, on-chain flows, and derivatives microstructure) into temporally rigorous, quantitative features capable of predicting market state dynamics:

1. **Harvest multi-channel raw data** from social platforms (X, Reddit, Telegram), media (crypto-native, financial wire, regulatory agencies), and market feeds (mempool, funding rates, open interest) with fault-tolerant scraping and polling engines.
2. **Filter noise and spam deterministically at line-rate** via high-throughput Regex matching and heuristic rule sets before invoking AI compute.
3. **Classify semantic intent, credibility, and impact** with high speed and zero hallucination using TypeSafe AI's **Jev** non-generative System-One model (`Noul`, `Choice`, `Score`).
4. **Enforce strict point-in-time correctness** with dual timestamping (`published_at` vs `observed_at`) to guarantee zero lookahead bias in historical research and backtests.
5. **Learn joint cross-modal market representations** using **JEPA** (Joint Embedding Predictive Architecture) to predict future latent market states without autoregressive token generation.
6. **Expose verified sentiment features and divergence signals** through a clean Feature Store gateway designed for direct consumption by `quant-platform`.

The system is not an ad-hoc sentiment aggregator or a vanity Fear & Greed gauge. The central deliverable is an **attributable, reproducible, predictive feature stream with proven Information Coefficient (IC)**.

---

## 2. Product Principles

### 2.1 Absolute Point-in-Time Correctness (Dual-Timestamp Invariant)
Every ingested piece of text or data record carries two distinct temporal attributes:
* `published_at`: The self-declared timestamp of publication at the source.
* `observed_at`: The monotonic system timestamp recording when the engine first validated and stored the item.

Any feature calculation or backtest query for timestamp $T$ strictly forbids data where $\text{observed\_at} > T$, regardless of $\text{published\_at}$.

### 2.2 Cascading Elimination of Noise (The Funnel Architecture)
Compute cost and noise must be minimized as early as possible in the processing pipeline:

```text
[Raw Web / Social Stream: 100%]
            │
            ▼ (Regex & Heuristics: Drops 75-80% spam/bot noise at ~0 compute cost)
[Clean Signal Candidates: 20-25%]
            │
            ▼ (TypeSafe Jev: Strong semantic typing at $0.042/1M tokens)
[Typed Semantic Records: 20-25%]
            │
            ▼ (Temporal Window Aggregation & Cross-Modal Fusion with On-Chain/Derivatives)
[Unified Market State Vector]
            │
            ▼ (JEPA Latent Predictor)
[Predictive Latent Features & Alpha Signals]
```

### 2.3 Non-Generative, Strongly-Typed AI Inference
The system explicitly rejects free-form generative LLMs (e.g., standard ChatGPT prompt wrappers) for sentiment scoring. Generative LLMs suffer from high latency, parsing errors, hallucination, non-deterministic formatting, and unsustainable token costs.  
Instead, the semantic layer relies on **TypeSafe AI Jev**, utilizing constrained decoding to return typed primitives:
* `Noul`: Calibrated binary probabilities $[0.0, 1.0]$.
* `Choice`: Constrained categorical classification.
* `Score`: Calibrated ordinal ratings.

### 2.4 Representation Learning via JEPA over Autoregression
Market sentiment and price dynamics interact non-linearly. Rather than attempting to predict the next word or token, the analytical modeling track utilizes **JEPA** (Joint Embedding Predictive Architecture):
* The **Context Encoder** embeds the multi-modal history (sentiment scores + on-chain flow + orderbook dynamics).
* The **Target Encoder** embeds future market states.
* The **Predictor** learns state transitions in latent embedding space without generative reconstruction overhead.

### 2.5 WORM Raw Data Protection & Lineage
Raw payloads (raw HTML, RSS XML, API responses) are stored in a Write-Once-Read-Many (WORM) raw tier with content-addressed SHA-256 hashes. Derived sentiment scores and embeddings must maintain attributable lineage back to their source raw payloads.

---

## 3. Target Personas and Downstream Consumers

1. **Quantitative Trading Strategies (`quant-platform`)**:
   Consumes high-frequency and low-frequency sentiment features (sentiment momentum, sentiment-price divergence, sudden social volume spikes, extreme negative funding + high fear) to trigger or condition execution.
2. **Market Regime Classifier**:
   Uses latent JEPA embeddings to identify regime shifts (e.g., transition from liquidity-driven regime to narrative-driven retail frenzy or regulatory panic).
3. **Risk & Capital Preservation Engine**:
   Triggers emergency position de-risking when systemic shock scores exceed defined confidence thresholds.

---

## 4. Non-Goals

1. **No Manual Discretionary News Terminal**: The platform does not aim to build a Bloomberg-style GUI for human journalists or discretionary traders to read news feeds.
2. **No Direct Order Execution**: `Sentiment` does not connect to exchange execution endpoints or manage account balances. Execution is the sole responsibility of `quant-platform`.
3. **No Unbounded Generative Chat**: The engine will not host conversational chatbots or generate creative summaries. All outputs are structured numerical features, classifications, and embeddings.
4. **No Unfiltered Social Firehose**: The platform will not store petabytes of unfiltered internet chatter. Unfiltered data is dropped at the Regex tier.

---

## 5. Success Metrics

1. **Predictive Utility**:
   * Out-of-sample Information Coefficient ($\text{IC} > 0.03$) on forward BTC returns and realized volatility across 1h, 4h, and 24h horizons.
   * Statistical significance under Deflated Sharpe Ratio (DSR) and low Probability of Backtest Overfitting (PBO).
2. **Throughput & Latency**:
   * L1 Regex throughput: $> 5,000$ messages/sec per core.
   * L2 Jev round-trip latency: $< 500$ ms for batched queries.
   * End-to-end ingestion-to-feature latency: $< 2$ seconds for high-priority news and alerts.
3. **Operational Cost**:
   * Monthly inference cost bounded under **€25/month** for a throughput of 40,000+ daily classified events.
