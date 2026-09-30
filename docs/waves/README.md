# Atlas Implementation Waves Directory

This directory contains the authoritative, bounded implementation specifications for each wave in the **Atlas** engine roadmap.

Each wave document establishes:
- The exact subset of capability atoms activated and governed by that wave.
- The prerequisite integration gates that must be satisfied before opening the wave.
- The bounded technical deliverables and strict non-goals.
- The formal **Golden E2E Proof** specification and acceptance criteria.
- The Definition of Done (DoD).

---

## Waves Overview & Lifecycle Status

| Wave | Title | Governed Atoms | Status | Target Golden Proof |
|---|---|---|---|---|
| **Wave 0** | [Governance, Schemas & Contracts](WAVE_0_FOUNDATION_CONTRACTS.md) | `B01`, `B04`, `C01`, `C03` | **CLOSED** | Contract schema unit suite (6/6 passing) |
| **Wave 1** | [Ingestion & Deterministic Regex L1 Engine](WAVE_1_INGESTION_REGEX_ENGINE.md) | `A01`, `A02`, `A03`, `A04`, `A05`, `A06`, `A07`, `B01`, `B02`, `B03` | **READY TO OPEN** | `WAVE1_GOLDEN_E2E_DETERMINISTIC_INGESTION.md` |
| **Wave 2** | [Semantic Typing & Operator CLI v1](WAVE_2_SEMANTIC_TYPING_CLI_OPERATOR.md) | `C02`, `G01`, `G02`, `G03`, `G04` | **PLANNED** | `WAVE2_GOLDEN_E2E_JEV_AND_CLI_OPERATOR.md` |
| **Wave 3** | [Multi-Modal Fusion & Feature Store](WAVE_3_MULTIMODAL_FUSION_FEATURE_STORE.md) | `D01`, `D02`, `D03` | **PLANNED** | `WAVE3_GOLDEN_E2E_MULTIMODAL_FUSION.md` |
| **Wave 4** | [Latent Predictive Architecture (JEPA)](WAVE_4_JEPA_LATENT_REPRESENTATION.md) | `E01`, `E02`, `E03`, `E04`, `F01` | **PLANNED** | `WAVE4_GOLDEN_E2E_JEPA_REPRESENTATION.md` |
| **Wave 5** | [quant-platform Gateway & Divergence Signals](WAVE_5_QUANT_PLATFORM_GATEWAY.md) | `F02`, `F03` | **PLANNED** | `WAVE5_GOLDEN_E2E_QUANT_PLATFORM_GATEWAY.md` |

---

## Authority & Governance Chain

```text
PRODUCT.md -> CAPABILITY_MAP.md -> CAPABILITY_DAG.md -> ROADMAP.md -> docs/waves/WAVE_*.md -> SCOPE.md
```
