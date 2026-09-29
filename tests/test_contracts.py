"""Unit tests for core schemas, contracts, and invariants in Atlas."""

from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

from atlas.contracts.document import CanonicalDocument, EntityMention, SourcePlatform
from atlas.contracts.jev import PolarChoice, SemanticVector


def test_canonical_document_creation_and_hash():
    now_utc = datetime.now(timezone.utc)
    clean_text = "Bitcoin crosses $100k after massive institutional ETF inflows!"
    doc_id = CanonicalDocument.compute_document_id(
        SourcePlatform.TWITTER, "123456789", clean_text
    )

    doc = CanonicalDocument(
        document_id=doc_id,
        source=SourcePlatform.TWITTER,
        source_id="123456789",
        source_author="crypto_whale",
        source_url="https://x.com/crypto_whale/status/123456789",
        published_at=now_utc,
        observed_at=now_utc,
        raw_text="Bitcoin crosses $100k after massive institutional ETF inflows! https://t.co/xyz",
        clean_text=clean_text,
        language="en",
        entities=[
            EntityMention(symbol="BTC", raw_mention="$100k", span_start=16, span_end=21)
        ],
        has_btc_mention=True,
        regex_spam_score=0.05,
        raw_storage_uri="data/raw/twitter/2026-09-29/test.json.gz",
        raw_payload_sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )

    assert doc.document_id == doc_id
    assert doc.source == SourcePlatform.TWITTER
    assert doc.entities[0].symbol == "BTC"
    assert doc.published_at.tzinfo == timezone.utc
    assert doc.observed_at.tzinfo == timezone.utc


def test_canonical_document_immutability():
    now_utc = datetime.now(timezone.utc)
    clean = "Test Bitcoin news"
    doc_id = CanonicalDocument.compute_document_id(SourcePlatform.NEWS_CRYPTO, "99", clean)

    doc = CanonicalDocument(
        document_id=doc_id,
        source=SourcePlatform.NEWS_CRYPTO,
        source_id="99",
        published_at=now_utc,
        observed_at=now_utc,
        raw_text=clean,
        clean_text=clean,
        raw_storage_uri="data/raw/news/test.json",
        raw_payload_sha256="abc123",
    )

    with pytest.raises(ValidationError):
        # Should be frozen/immutable
        doc.clean_text = "Mutated text"  # type: ignore


def test_semantic_vector_factory():
    now_utc = datetime.now(timezone.utc)
    vec = SemanticVector.from_jev_raw(
        document_id="doc_test_1",
        observed_at=now_utc,
        is_btc_relevant=0.98,
        is_fud_or_rumor=0.05,
        sentiment_polarity="extreme_bullish",
        credibility_tier="tier1_media_or_official",
        market_urgency="high",
    )

    assert vec.document_id == "doc_test_1"
    assert vec.btc_relevance_prob == 0.98
    assert vec.polarity_score == 1.0
    assert vec.credibility_weight == 1.0
    assert vec.urgency_weight == 0.75
    # Impact should be strongly positive
    assert vec.effective_sentiment_impact > 0.8


def test_semantic_vector_bearish_fud():
    now_utc = datetime.now(timezone.utc)
    vec = SemanticVector.from_jev_raw(
        document_id="doc_test_2",
        observed_at=now_utc,
        is_btc_relevant=0.95,
        is_fud_or_rumor=0.90,
        sentiment_polarity="extreme_bearish",
        credibility_tier="reputable_analyst",
        market_urgency="critical",
    )

    assert vec.polarity_score == -1.0
    assert vec.fud_prob == 0.90
    assert vec.credibility_weight == 0.75
    assert vec.urgency_weight == 1.0
    # Impact should be strongly negative
    assert vec.effective_sentiment_impact < -0.7
