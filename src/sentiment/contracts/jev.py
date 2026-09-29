"""TypeSafe AI Jev semantic evaluation contract and vectorized representation."""

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator


class PolarChoice(StrEnum):
    EXTREME_BEARISH = "extreme_bearish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    BULLISH = "bullish"
    EXTREME_BULLISH = "extreme_bullish"


POLAR_NUMERICAL_MAP: dict[PolarChoice, float] = {
    PolarChoice.EXTREME_BEARISH: -1.0,
    PolarChoice.BEARISH: -0.5,
    PolarChoice.NEUTRAL: 0.0,
    PolarChoice.BULLISH: 0.5,
    PolarChoice.EXTREME_BULLISH: 1.0,
}

CREDIBILITY_NUMERICAL_MAP: dict[str, float] = {
    "anonymous_noise": 0.1,
    "community": 0.4,
    "reputable_analyst": 0.75,
    "tier1_media_or_official": 1.0,
}

URGENCY_NUMERICAL_MAP: dict[str, float] = {
    "negligible": 0.0,
    "low": 0.25,
    "medium": 0.5,
    "high": 0.75,
    "critical": 1.0,
}

# TypeSafe AI Jev Questions Definition dictionary template
JEV_BTC_QUESTIONS: dict[str, dict[str, Any]] = {
    "is_btc_relevant": {
        "type": "Noul",
        "instructions": (
            "Does this text specifically discuss Bitcoin (BTC), its network, price action, "
            "macro adoption, or regulatory impact?"
        )
    },
    "is_fud_or_rumor": {
        "type": "Noul",
        "instructions": (
            "Does this text report unverified panic, sudden regulatory enforcement, "
            "exchange insolvency, network attacks, or catastrophic rumors?"
        )
    },
    "sentiment_polarity": {
        "type": "Choice",
        "instructions": "What is the direct market sentiment or directional price implication conveyed?",
        "criteria": {
            "extreme_bearish": "Panic selling, systemic collapse, liquidation cascades, insolvency claims",
            "bearish": "Negative price action, profit taking, macroeconomic headwinds, regulatory concern",
            "neutral": "Factual reporting of stats, technical updates, neutral market commentary",
            "bullish": "Positive price expectation, accumulation, spot ETF inflows, bullish breakout",
            "extreme_bullish": "Parabolic euphoria, hyperbitcoinization claims, massive institutional buy"
        }
    },
    "credibility_tier": {
        "type": "Score",
        "instructions": "How credible and authoritative is the author or information source?",
        "criteria": [
            "anonymous_noise",
            "community",
            "reputable_analyst",
            "tier1_media_or_official"
        ]
    },
    "market_urgency": {
        "type": "Score",
        "instructions": "How urgent and market-moving is this event?",
        "criteria": [
            "negligible",
            "low",
            "medium",
            "high",
            "critical"
        ]
    }
}


class SemanticVector(BaseModel):
    """Normalized continuous feature vector synthesized from TypeSafe Jev evaluation."""
    model_config = ConfigDict(frozen=True)

    document_id: str = Field(description="Foreign key back to CanonicalDocument.document_id")
    observed_at: datetime = Field(description="Point-in-time observed timestamp in UTC")

    # Normalized dimension scores
    btc_relevance_prob: float = Field(ge=0.0, le=1.0)
    fud_prob: float = Field(ge=0.0, le=1.0)
    polarity_score: float = Field(ge=-1.0, le=1.0)
    credibility_weight: float = Field(ge=0.0, le=1.0)
    urgency_weight: float = Field(ge=0.0, le=1.0)

    # Composite signal: Polarity scaled by credibility, urgency, and relevance
    effective_sentiment_impact: float = Field(ge=-1.0, le=1.0)

    @field_validator("observed_at")
    @classmethod
    def validate_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)

    @classmethod
    def from_jev_raw(
        cls,
        document_id: str,
        observed_at: datetime,
        is_btc_relevant: float,
        is_fud_or_rumor: float,
        sentiment_polarity: str,
        credibility_tier: str,
        market_urgency: str,
    ) -> "SemanticVector":
        """Deterministic factory transforming raw Jev response types into a SemanticVector."""
        pol_choice = PolarChoice(sentiment_polarity.lower())
        pol_score = POLAR_NUMERICAL_MAP[pol_choice]
        cred_score = CREDIBILITY_NUMERICAL_MAP.get(credibility_tier.lower(), 0.1)
        urg_score = URGENCY_NUMERICAL_MAP.get(market_urgency.lower(), 0.0)

        # Composite formulation:
        # Effective sentiment scales with relevance, credibility, and urgency
        weight = is_btc_relevant * cred_score * (0.5 + 0.5 * urg_score)
        impact = max(-1.0, min(1.0, pol_score * weight))

        return cls(
            document_id=document_id,
            observed_at=observed_at,
            btc_relevance_prob=float(is_btc_relevant),
            fud_prob=float(is_fud_or_rumor),
            polarity_score=pol_score,
            credibility_weight=cred_score,
            urgency_weight=urg_score,
            effective_sentiment_impact=round(impact, 4),
        )
