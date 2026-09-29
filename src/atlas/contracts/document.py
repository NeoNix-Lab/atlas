"""Canonical document contract and schema definitions."""

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
import hashlib

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SourcePlatform(StrEnum):
    TWITTER = "twitter"
    REDDIT = "reddit"
    TELEGRAM = "telegram"
    NEWS_CRYPTO = "news_crypto"
    NEWS_MAINSTREAM = "news_mainstream"
    REGULATORY = "regulatory"
    ONCHAIN_EVENT = "onchain_event"


class EntityMention(BaseModel):
    """Normalized entity mention extracted by the deterministic Regex tier."""
    model_config = ConfigDict(frozen=True)

    symbol: str = Field(description="Normalized symbol (e.g. BTC, WBTC, SATS, LIGHTNING)")
    raw_mention: str = Field(description="Exact substring in raw text (e.g. $BTC, #bitcoin)")
    span_start: int = Field(ge=0)
    span_end: int = Field(ge=0)


class OnChainMetadata(BaseModel):
    """Optional metadata attached to discrete on-chain capital events."""
    model_config = ConfigDict(frozen=True)

    tx_hash: str = Field(default="", description="Bitcoin transaction hash")
    amount_btc: float = Field(default=0.0, ge=0.0, description="Transferred volume in BTC")
    usd_value_approx: float = Field(default=0.0, ge=0.0)
    from_cluster: str = Field(default="", description="Origin entity/cluster (e.g. 'Coinbase Cold')")
    to_cluster: str = Field(default="", description="Destination entity/cluster (e.g. 'Binance Deposit')")


class CanonicalDocument(BaseModel):
    """Authoritative normalized document representation in Atlas.
    
    Guarantees strict point-in-time correctness via dual timestamping
    (published_at vs observed_at) and immutable content-addressed identity.
    """
    model_config = ConfigDict(frozen=True)

    document_id: str = Field(
        description="Unique SHA-256 hash derived from (source, source_id, clean_text)"
    )
    source: SourcePlatform
    source_id: str = Field(
        description="Native ID from upstream source platform (e.g., tweet_id, post_id, tx_hash)"
    )
    source_author: str = Field(
        default="", description="Username, channel handle, or news desk"
    )
    source_url: str = Field(
        default="", description="Direct permalink URL if available"
    )

    # Dual-Timestamp Mandate (Anti-Lookahead Invariant)
    published_at: datetime = Field(
        description="Publication timestamp declared at the source in UTC"
    )
    observed_at: datetime = Field(
        description="Monotonic ingestion timestamp when engine validated the payload in UTC"
    )

    # Content
    raw_text: str = Field(
        description="Raw, unedited message body as harvested"
    )
    clean_text: str = Field(
        description="Sanitized and normalized text for semantic analysis"
    )
    language: str = Field(
        default="en", description="ISO 639-1 language code"
    )

    # Deterministic Metadata Extracted by Regex L1
    entities: list[EntityMention] = Field(
        default_factory=list, description="Extracted cryptocurrency mentions"
    )
    has_btc_mention: bool = Field(
        default=True, description="True if text directly references BTC or derivatives"
    )
    regex_spam_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Heuristic spam probability from 0.0 to 1.0"
    )

    # On-Chain Metadata
    onchain_data: OnChainMetadata | None = Field(
        default=None, description="Structured metrics for discrete whale/flow events"
    )

    # Storage Lineage
    raw_storage_uri: str = Field(
        description="URI/Path to WORM raw payload blob"
    )
    raw_payload_sha256: str = Field(
        description="SHA-256 digest of original raw payload wire bytes"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Source-specific non-canonical metadata"
    )

    @field_validator("published_at", "observed_at")
    @classmethod
    def validate_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)

    @classmethod
    def compute_document_id(cls, source: SourcePlatform, source_id: str, clean_text: str) -> str:
        payload = f"{source}:{source_id}:{clean_text.strip()}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()
