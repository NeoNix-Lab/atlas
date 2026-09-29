# Contract: Canonical Document v1 (`CANONICAL_DOCUMENT.md`)

**Status:** FROZEN  
**Schema Identifier:** `sentiment/canonical-document@1`  
**Governed Atoms:** `B04`, `C01`, `D01`

---

## 1. Specification

A `CanonicalDocument` represents a single parsed, normalized, and pre-filtered unit of text harvested from any source (social, news, official statement).

Every record must satisfy the following invariant rules:
1. **Immutable Identity**: Content-derived SHA-256 hash or deterministic UUID.
2. **Dual-Timestamp Mandate**: Both `published_at` (source timestamp) and `observed_at` (system receipt timestamp) must be explicit, UTC-zoned ISO-8601 strings.
3. **Clean Text**: Text payload stripped of HTML tags, tracking parameters, and normalized to UTF-8.
4. **Lineage Reference**: Direct reference to the raw WORM storage locator and raw payload hash.

---

## 2. Pydantic Reference Schema

```python
from datetime import datetime
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field, HttpUrl

class SourcePlatform(StrEnum):
    TWITTER = "twitter"
    REDDIT = "reddit"
    TELEGRAM = "telegram"
    NEWS_CRYPTO = "news_crypto"
    NEWS_MAINSTREAM = "news_mainstream"
    REGULATORY = "regulatory"
    ONCHAIN_ALERT = "onchain_alert"

class EntityMention(BaseModel):
    symbol: str = Field(description="Normalized symbol (e.g. BTC, WBTC, SATS, LIGHTNING)")
    raw_mention: str = Field(description="Exact substring in raw text (e.g. $BTC, #bitcoin)")
    span_start: int
    span_end: int

class CanonicalDocument(BaseModel):
    document_id: str = Field(description="Unique SHA-256 hash of (source, source_id, clean_text)")
    source: SourcePlatform
    source_id: str = Field(description="Original ID in the upstream platform (e.g. Tweet ID, Reddit comment ID)")
    source_author: str = Field(default="", description="Username or author handle")
    source_url: str = Field(default="", description="Direct permalink if available")
    
    # Dual-timestamping (Anti-Lookahead Invariant)
    published_at: datetime = Field(description="Declared publication time at the source (UTC)")
    observed_at: datetime = Field(description="Exact time ingested and recorded by our system (UTC)")
    
    # Content
    raw_text: str = Field(description="Original unedited text body")
    clean_text: str = Field(description="Sanitized text with URLs/emojis normalized")
    language: str = Field(default="en", description="ISO 639-1 language code")
    
    # Deterministic metadata extracted by Regex L1
    entities: list[EntityMention] = Field(default_factory=list)
    has_btc_mention: bool = Field(default=True)
    regex_spam_score: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # Lineage
    raw_storage_uri: str = Field(description="Path to gzipped raw payload in Tier 0 storage")
    raw_payload_sha256: str = Field(description="SHA-256 digest of original raw wire bytes")
    metadata: dict[str, Any] = Field(default_factory=dict)
```
