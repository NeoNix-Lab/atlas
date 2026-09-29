# Contract: Feature Artifact Export Contract v1 (`FEATURE_ARTIFACT_EXPORT.md`)

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** FROZEN  
**Schema Identifier:** `atlas/feature-artifact@1`  
**Governed Atoms:** `D03`, `F03`  
**Target Specification:** Conforms to `quant-platform`'s `FeatureArtifact v1` ([`ADR-0034`](file:///D:/Documents/Active/quant-platform/docs/architecture/ADR-0034-feature-artifact-v1.md)).

---

## 1. Specification & Data Invariants

Atlas exports materialized multi-modal sentiment and latent state tables as partitioned Apache Parquet datasets.  
Each export partition strictly satisfies the following invariants:
1. **Zero Lookahead Leakage**: Every row represents a closed temporal window $[T_{\text{open}}, T_{\text{close}}]$. Only events where $\text{observed\_at} \le T_{\text{close}}$ are included in aggregations.
2. **Fixed Columnar Schema**: Parquet columns are strictly typed using PyArrow data types without schema drift.
3. **Deterministic Partitioning Scheme**:
   ```text
   data/features/resolution=<res>/year=<YYYY>/month=<MM>/atlas_features_<res>_<YYYY-MM-DD>.parquet
   ```
   Supported resolutions (`<res>`): `1m`, `5m`, `15m`, `1h`.

---

## 2. Parquet Schema Definition

| Column Name | Arrow Type | Nullable | Description |
|---|---|---|---|
| `timestamp_window_open` | `timestamp('us', 'UTC')` | No | Beginning of temporal aggregation bucket (inclusive) |
| `timestamp_window_close` | `timestamp('us', 'UTC')` | No | End of temporal aggregation bucket (exclusive) |
| `watermark_observed_at` | `timestamp('us', 'UTC')` | No | Max monotonic system ingestion timestamp included in row |
| **Social Sentiment** | | | |
| `social_volume_count` | `int32` | No | Total social messages surviving Regex L1 filter in window |
| `social_spam_dropped_count` | `int32` | No | Total spam/bot messages rejected by Regex L1 in window |
| `social_sentiment_mean` | `float64` | Yes | Mean polarity score from Jev ($-1.0$ to $+1.0$) |
| `social_sentiment_momentum` | `float64` | Yes | Rate of change of social sentiment vs 12-window moving average |
| `fud_intensity_prob` | `float64` | Yes | Max FUD probability detected from Jev in window ($0.0$ to $1.0$) |
| **News & Macro** | | | |
| `news_volume_count` | `int32` | No | Total articles ingested from crypto & financial wire feeds |
| `news_sentiment_mean` | `float64` | Yes | Mean sentiment polarity of published news |
| `news_credibility_weighted` | `float64` | Yes | Polarity scaled by source credibility tier ($-1.0$ to $+1.0$) |
| `max_market_urgency` | `float64` | Yes | Highest urgency score observed in window ($0.0$ to $1.0$) |
| **On-Chain Capital Flows** | | | |
| `whale_inflow_btc` | `float64` | No | Total BTC transferred to exchange deposit addresses |
| `whale_outflow_btc` | `float64` | No | Total BTC withdrawn to private/cold custody |
| `net_whale_intent_score` | `float64` | Yes | Volume-weighted Jev capital intent ($+1.0$ accumulation, $-1.0$ dump) |
| `mempool_median_fee_rate` | `float64` | Yes | Median transaction fee rate in sat/vB |
| `mempool_fee_velocity` | `float64` | Yes | First derivative of mempool congestion acceleration |
| **Derivatives Positioning** | | | |
| `derivatives_funding_rate` | `float64` | Yes | Binance/Bybit 8h perpetual funding rate at window close |
| `derivatives_oi_delta_usd` | `float64` | Yes | Absolute change in Open Interest over window |
| **JEPA Latent Representation** | | | |
| `jepa_latent_state` | `list<item: float32>[64]` | Yes | 64-dimensional latent state vector $s_t$ predicting market transition |
| **Composite Signal** | | | |
| `sentiment_divergence_score`| `float64` | Yes | Divergence metric: Crowd emotion vs On-chain/Derivatives reality |

---

## 3. Downstream Consumption in `quant-platform`

Inside `quant-platform`, this dataset is registered directly as a `FeatureSet` in the catalog:

```python
import duckdb

# Zero-copy query in quant-platform
query = """
SELECT 
    timestamp_window_close,
    social_sentiment_mean,
    news_credibility_weighted,
    net_whale_intent_score,
    sentiment_divergence_score,
    jepa_latent_state
FROM 'D:/Documents/Active/Sentiment/data/features/resolution=1h/**/*.parquet'
WHERE timestamp_window_close >= '2026-01-01'
ORDER BY timestamp_window_close ASC;
"""

df = duckdb.query(query).to_df()
```
