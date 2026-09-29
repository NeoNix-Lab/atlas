"""Core data contracts, schemas, and typed invariants for Sentiment."""

from sentiment.contracts.document import CanonicalDocument, EntityMention, SourcePlatform
from sentiment.contracts.jev import JEV_BTC_QUESTIONS, PolarChoice, SemanticVector

__all__ = [
    "CanonicalDocument",
    "EntityMention",
    "SourcePlatform",
    "PolarChoice",
    "SemanticVector",
    "JEV_BTC_QUESTIONS",
]
