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


class OnChainFlowIntent(StrEnum):
    EXCHANGE_INFLOW_DUMP = "exchange_inflow_dump"
    COLD_ACCUMULATION = "cold_accumulation"
    INTERNAL_CUSTODY_SWAP = "internal_custody_swap"
    MINER_DISTRIBUTION = "miner_distribution"
    DORMANT_REVIVAL = "dormant_revival"


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

FLOW_INTENT_NUMERICAL_MAP: dict[OnChainFlowIntent, float] = {
    OnChainFlowIntent.EXCHANGE_INFLOW_DUMP: -1.0,
    OnChainFlowIntent.MINER_DISTRIBUTION: -0.6,
    OnChainFlowIntent.DORMANT_REVIVAL: -0.5,
    OnChainFlowIntent.INTERNAL_CUSTODY_SWAP: 0.0,
    OnChainFlowIntent.COLD_ACCUMULATION: 1.0,
}

CAPITAL_MAGNITUDE_NUMERICAL_MAP: dict[str, float] = {
    "routine": 0.1,
    "notable": 0.4,
    "whale": 0.75,
    "market_moving_shock": 1.0,
}

# TypeSafe AI Jev Questions Definition for Narrative Streams
JEV_NARRATIVE_QUESTIONS: dict[str, dict[str, Any]] = {
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

# Alias for backward-compatibility with Wave 0
JEV_BTC_QUESTIONS = JEV_NARRATIVE_QUESTIONS

# TypeSafe AI Jev Questions Definition for Discrete On-Chain Capital Flows
JEV_ONCHAIN_QUESTIONS: dict[str, dict[str, Any]] = {
    "is_immediate_sell_pressure": {
        "type": "Noul",
        "instructions": (
            "Does this transfer represent an immediate exchange deposit, broker OTC liquidation, "
            "or active liquid sell pressure?"
        )
    },
    "flow_intent": {
        "type": "Choice",
        "instructions": "What is the primary economic intent of this on-chain transaction?",
        "criteria": {
            "exchange_inflow_dump": "Tokens transferred directly to known exchange deposit hot/spot wallets",
            "cold_accumulation": "Tokens withdrawn from exchanges into private cold storage or institutional custodians",
            "internal_custody_swap": "Rebalancing between known cold/hot wallets of the same exchange or custodian",
            "miner_distribution": "Transfers originating from mining pool coinbase rewards to liquid brokers/exchanges",
            "dormant_revival": "Coins unmoved for >3 years waking up and moving to active addresses"
        }
    },
    "capital_magnitude": {
        "type": "Score",
        "instructions": "How significant is this transfer relative to daily Bitcoin spot volume?",
        "criteria": [
            "routine",
            "notable",
            "whale",
            "market_moving_shock"
        ]
    }
}


class SemanticVector(BaseModel):
    """Normalized continuous feature vector synthesized from TypeSafe Jev narrative evaluation."""
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
        pol_choice = PolarChoice(sentiment_polarity.lower())
        pol_score = POLAR_NUMERICAL_MAP[pol_choice]
        cred_score = CREDIBILITY_NUMERICAL_MAP.get(credibility_tier.lower(), 0.1)
        urg_score = URGENCY_NUMERICAL_MAP.get(market_urgency.lower(), 0.0)

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


class OnChainSemanticVector(BaseModel):
    """Normalized continuous feature vector for discrete on-chain whale transactions."""
    model_config = ConfigDict(frozen=True)

    document_id: str = Field(description="Foreign key back to CanonicalDocument.document_id")
    observed_at: datetime = Field(description="Point-in-time observed timestamp in UTC")

    amount_btc: float = Field(ge=0.0)
    is_sell_pressure_prob: float = Field(ge=0.0, le=1.0)
    flow_intent: OnChainFlowIntent
    magnitude_weight: float = Field(ge=0.0, le=1.0)
    net_capital_intent_score: float = Field(ge=-1.0, le=1.0)

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
        amount_btc: float,
        is_immediate_sell_pressure: float,
        flow_intent: str,
        capital_magnitude: str,
    ) -> "OnChainSemanticVector":
        intent_enum = OnChainFlowIntent(flow_intent.lower())
        intent_dir = FLOW_INTENT_NUMERICAL_MAP[intent_enum]
        mag_score = CAPITAL_MAGNITUDE_NUMERICAL_MAP.get(capital_magnitude.lower(), 0.1)

        # Sell pressure overrides intent towards negative score
        net_score = intent_dir * (1.0 - 0.5 * is_immediate_sell_pressure) if intent_dir > 0 else intent_dir
        net_score = max(-1.0, min(1.0, net_score * mag_score))

        return cls(
            document_id=document_id,
            observed_at=observed_at,
            amount_btc=amount_btc,
            is_sell_pressure_prob=float(is_immediate_sell_pressure),
            flow_intent=intent_enum,
            magnitude_weight=mag_score,
            net_capital_intent_score=round(net_score, 4),
        )
