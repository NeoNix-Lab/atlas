# Contract: Jev Evaluation Contract v1 (`JEV_EVALUATION_CONTRACT.md`)

**Status:** FROZEN  
**Schema Identifier:** `sentiment/jev-evaluation@1`  
**Governed Atoms:** `C01`, `C02`, `C03`  
**Provider:** TypeSafe AI (`typesafe-sdk`, model: `jev-latest`)

---

## 1. Specification & Questions Topology

The Semantic Plane converts a `CanonicalDocument.clean_text` into a deterministic, typed evaluation record using the TypeSafe AI System-One engine.

The contract defines five core questions across the three native primitives:

| Field Name | Primitive | Description & Criteria | Numerical Range |
|---|---|---|---|
| `is_btc_relevant` | `Noul` | Is this text directly about Bitcoin, its network, price action, adoption, or regulations? | $[0.0, 1.0]$ |
| `is_fud_or_rumor` | `Noul` | Does the text spread unconfirmed panic, FUD, hacks, regulatory bans, or negative rumors? | $[0.0, 1.0]$ |
| `sentiment_polarity` | `Choice` | Directional price expectation: `EXTREME_BEARISH`, `BEARISH`, `NEUTRAL`, `BULLISH`, `EXTREME_BULLISH` | Discretized: $\{-2, -1, 0, +1, +2\}$ |
| `credibility_tier` | `Score` | Authoritative source standing: `ANONYMOUS_NOISE`, `COMMUNITY`, `REPUTABLE_ANALYST`, `TIER1_MEDIA_OR_OFFICIAL` | Normalized: $[0.0, 1.0]$ |
| `market_urgency` | `Score` | Breaking news impact urgency: `NEGLIGIBLE`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` | Normalized: $[0.0, 1.0]$ |

---

## 2. Python SDK Implementation Mapping

```python
from typesafe_sdk import Choice, Noul, Score

JEV_BTC_QUESTIONS = {
    "is_btc_relevant": Noul(
        instructions="Does this text specifically discuss Bitcoin (BTC), its price, macro adoption, or network fundamentals?"
    ),
    "is_fud_or_rumor": Noul(
        instructions="Does this text report unverified panic, regulatory enforcement, network vulnerabilities, or catastrophic rumors?"
    ),
    "sentiment_polarity": Choice(
        instructions="What is the direct market sentiment or price implication conveyed in this text?",
        criteria={
            "extreme_bearish": "Panic selling, systemic collapse, liquidation cascades, insolvency claims",
            "bearish": "Negative price action, profit taking, macroeconomic headwinds, regulatory concern",
            "neutral": "Factual reporting of stats, technical updates, neutral market commentary",
            "bullish": "Positive price expectation, accumulation, spot ETF inflows, bullish breakout",
            "extreme_bullish": "Parabolic euphoria, hyperbitcoinization claims, massive institutional buy announcements"
        }
    ),
    "credibility_tier": Score(
        instructions="How credible and authoritative is the author or information source?",
        criteria=[
            "anonymous_noise",      # Random unverified social account
            "community",            # Known community participant / enthusiast
            "reputable_analyst",    # Established crypto researcher or analytics desk
            "tier1_media_or_official" # Official SEC/Fed/Exchange release or Tier-1 financial media
        ]
    ),
    "market_urgency": Score(
        instructions="How urgent and market-moving is this event?",
        criteria=[
            "negligible",  # Routine chatter / stale commentary
            "low",         # Minor opinion / routine market recap
            "medium",      # Notable whale transfer, moderate macro news
            "high",        # Major rate decision, ETF approval/rejection, large exchange disruption
            "critical"     # Systemic event, exchange insolvency, government emergency ban
        ]
    )
}
```

---

## 3. Vectorized Semantic Record (`SemanticVector`)

The output from Jev is deterministically mapped into a continuous feature vector:

```python
from pydantic import BaseModel, Field

class SemanticVector(BaseModel):
    document_id: str
    observed_at: datetime
    
    # Normalized numerical features
    btc_relevance_prob: float = Field(ge=0.0, le=1.0)
    fud_prob: float = Field(ge=0.0, le=1.0)
    polarity_score: float = Field(ge=-1.0, le=1.0, description="Normalized: extreme_bearish=-1.0 to extreme_bullish=1.0")
    credibility_weight: float = Field(ge=0.0, le=1.0, description="0.0=noise, 1.0=tier1")
    urgency_weight: float = Field(ge=0.0, le=1.0, description="0.0=negligible, 1.0=critical")
    
    # Composite instant signal
    # Signal = polarity * credibility_weight * urgency_weight * btc_relevance_prob
    effective_sentiment_impact: float = Field(ge=-1.0, le=1.0)
```
