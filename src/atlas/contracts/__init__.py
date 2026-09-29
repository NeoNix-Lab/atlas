"""Core data contracts, schemas, and typed invariants for Atlas."""

from atlas.contracts.document import (
    CanonicalDocument,
    EntityMention,
    OnChainMetadata,
    SourcePlatform,
)
from atlas.contracts.jev import (
    JEV_BTC_QUESTIONS,
    JEV_NARRATIVE_QUESTIONS,
    JEV_ONCHAIN_QUESTIONS,
    OnChainFlowIntent,
    OnChainSemanticVector,
    PolarChoice,
    SemanticVector,
)

__all__ = [
    "CanonicalDocument",
    "EntityMention",
    "OnChainMetadata",
    "SourcePlatform",
    "PolarChoice",
    "OnChainFlowIntent",
    "SemanticVector",
    "OnChainSemanticVector",
    "JEV_BTC_QUESTIONS",
    "JEV_NARRATIVE_QUESTIONS",
    "JEV_ONCHAIN_QUESTIONS",
]
