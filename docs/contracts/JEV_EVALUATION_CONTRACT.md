# Contract: Jev Evaluation Contract v1 (`JEV_EVALUATION_CONTRACT.md`)

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** FROZEN  
**Schema Identifier:** `atlas/jev-evaluation@1`  
**Governed Atoms:** `C01`, `C02`, `C03`  
**Provider:** TypeSafe AI (`typesafe-sdk`, model: `jev-latest`)

---

## 1. Dual Topology Specification

Atlas leverages TypeSafe AI's non-generative System-One engine to evaluate two distinct payload domains:
1. **Narrative Stream (Social, News, Regulatory)**: Evaluates sentiment direction, FUD probability, credibility standing, and market urgency.
2. **Capital Flow Stream (Whale Alerts, Exchange Inflows/Outflows, Dormant Coins)**: Evaluates economic intent, liquid selling pressure, and market magnitude.

---

## 2. Narrative Stream Topology (`JEV_NARRATIVE_QUESTIONS`)

| Question Key | Primitive | Criteria / Description | Output Range |
|---|---|---|---|
| `is_btc_relevant` | `Noul` | Specifically discusses Bitcoin, its network, price action, or regulation. | $[0.0, 1.0]$ |
| `is_fud_or_rumor` | `Noul` | Reports unverified panic, regulatory crackdowns, hacks, or catastrophic rumors. | $[0.0, 1.0]$ |
| `sentiment_polarity` | `Choice` | `extreme_bearish`, `bearish`, `neutral`, `bullish`, `extreme_bullish` | Discretized: $\{-1.0, -0.5, 0.0, +0.5, +1.0\}$ |
| `credibility_tier` | `Score` | `anonymous_noise` ($0.1$), `community` ($0.4$), `reputable_analyst` ($0.75$), `tier1_media_or_official` ($1.0$) | Normalized: $[0.0, 1.0]$ |
| `market_urgency` | `Score` | `negligible` ($0.0$), `low` ($0.25$), `medium` ($0.5$), `high` ($0.75$), `critical` ($1.0$) | Normalized: $[0.0, 1.0]$ |

### Python SDK Schema:
```python
from typesafe_sdk import Choice, Noul, Score

JEV_NARRATIVE_QUESTIONS = {
    "is_btc_relevant": Noul(
        instructions="Does this text specifically discuss Bitcoin (BTC), its network, price action, macro adoption, or regulatory impact?"
    ),
    "is_fud_or_rumor": Noul(
        instructions="Does this text report unverified panic, sudden regulatory enforcement, exchange insolvency, network attacks, or catastrophic rumors?"
    ),
    "sentiment_polarity": Choice(
        instructions="What is the direct market sentiment or directional price implication conveyed?",
        criteria={
            "extreme_bearish": "Panic selling, systemic collapse, liquidation cascades, insolvency claims",
            "bearish": "Negative price action, profit taking, macroeconomic headwinds, regulatory concern",
            "neutral": "Factual reporting of stats, technical updates, neutral market commentary",
            "bullish": "Positive price expectation, accumulation, spot ETF inflows, bullish breakout",
            "extreme_bullish": "Parabolic euphoria, hyperbitcoinization claims, massive institutional buy"
        }
    ),
    "credibility_tier": Score(
        instructions="How credible and authoritative is the author or information source?",
        criteria=["anonymous_noise", "community", "reputable_analyst", "tier1_media_or_official"]
    ),
    "market_urgency": Score(
        instructions="How urgent and market-moving is this event?",
        criteria=["negligible", "low", "medium", "high", "critical"]
    )
}
```

---

## 3. On-Chain Capital Flow Topology (`JEV_ONCHAIN_QUESTIONS`)

| Question Key | Primitive | Criteria / Description | Output Range |
|---|---|---|---|
| `is_immediate_sell_pressure` | `Noul` | Does the transfer represent direct exchange deposit or liquid sell pressure? | $[0.0, 1.0]$ |
| `flow_intent` | `Choice` | Primary economic intent behind the movement (see criteria below). | Categorical string |
| `capital_magnitude` | `Score` | `routine` ($0.1$), `notable` ($0.4$), `whale` ($0.75$), `market_moving_shock` ($1.0$) | Normalized: $[0.0, 1.0]$ |

### Python SDK Schema:
```python
JEV_ONCHAIN_QUESTIONS = {
    "is_immediate_sell_pressure": Noul(
        instructions="Does this transfer represent an immediate exchange deposit, broker OTC liquidation, or active liquid sell pressure?"
    ),
    "flow_intent": Choice(
        instructions="What is the primary economic intent of this on-chain transaction?",
        criteria={
            "exchange_inflow_dump": "Tokens transferred directly to known exchange deposit hot/spot wallets",
            "cold_accumulation": "Tokens withdrawn from exchanges into private cold storage or institutional custodians",
            "internal_custody_swap": "Rebalancing between known cold/hot wallets of the same exchange or custodian",
            "miner_distribution": "Transfers originating from mining pool coinbase rewards to liquid brokers/exchanges",
            "dormant_revival": "Coins unmoved for >3 years waking up and moving to active addresses"
        }
    ),
    "capital_magnitude": Score(
        instructions="How significant is this transfer relative to daily Bitcoin spot volume?",
        criteria=["routine", "notable", "whale", "market_moving_shock"]
    )
}
```

---

## 4. Vectorized Feature Records (`SemanticVector` & `OnChainSemanticVector`)

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class SemanticVector(BaseModel):
    """Normalized continuous feature vector for narrative social/news text."""
    model_config = ConfigDict(frozen=True)

    document_id: str
    observed_at: datetime
    
    btc_relevance_prob: float = Field(ge=0.0, le=1.0)
    fud_prob: float = Field(ge=0.0, le=1.0)
    polarity_score: float = Field(ge=-1.0, le=1.0)
    credibility_weight: float = Field(ge=0.0, le=1.0)
    urgency_weight: float = Field(ge=0.0, le=1.0)
    effective_sentiment_impact: float = Field(ge=-1.0, le=1.0)


class OnChainSemanticVector(BaseModel):
    """Normalized continuous feature vector for discrete on-chain whale transactions."""
    model_config = ConfigDict(frozen=True)

    document_id: str
    observed_at: datetime
    
    amount_btc: float = Field(ge=0.0)
    is_sell_pressure_prob: float = Field(ge=0.0, le=1.0)
    flow_intent_category: str
    magnitude_weight: float = Field(ge=0.0, le=1.0)
    
    # Net directional flow impact: (+1.0 accumulation, -1.0 dump, 0.0 internal swap)
    net_capital_intent_score: float = Field(ge=-1.0, le=1.0)
```
