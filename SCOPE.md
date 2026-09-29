# Scope: Wave 0 - Governance, Schemas & Architecture Foundation

**Status:** IN_PROGRESS  
**Scope Kind:** Decision-gate baseline and repository setup for Wave 0.  
**Target Integration Branch:** `main`  
**Governed Atoms:** `B01` (WORM Store contract), `B04` (Canonical Document), `C01` (Jev Questions Contract).

---

## 1. Objective

Establish the formal engineering foundation for the `Sentiment` platform, aligning governance, schemas, and architecture to the institutional standards of `quant-platform`:

1. Define system mission, principles, and non-goals in [`PRODUCT.md`](docs/product/PRODUCT.md).
2. Establish the 25-atom Capability Map and DAG in [`CAPABILITY_MAP.md`](docs/product/CAPABILITY_MAP.md) and [`CAPABILITY_DAG.md`](docs/product/CAPABILITY_DAG.md).
3. Outline the 6-wave progression and Decision Gates in [`ROADMAP.md`](docs/product/ROADMAP.md).
4. Blueprint the end-to-end multi-modal data plane in [`TARGET_ARCHITECTURE.md`](docs/architecture/TARGET_ARCHITECTURE.md).
5. Freeze the core data contracts:
   - [`CANONICAL_DOCUMENT.md`](docs/contracts/CANONICAL_DOCUMENT.md)
   - [`JEV_EVALUATION_CONTRACT.md`](docs/contracts/JEV_EVALUATION_CONTRACT.md)
6. Initialize the repository structure, `pyproject.toml`, `.gitignore`, and package namespaces.

---

## 2. Invariants & Authority

Before proposing or mutating code, consult:
- [`docs/product/PRODUCT.md`](docs/product/PRODUCT.md)
- [`docs/product/CAPABILITY_MAP.md`](docs/product/CAPABILITY_MAP.md)
- [`docs/product/CAPABILITY_DAG.md`](docs/product/CAPABILITY_DAG.md)
- [`docs/architecture/TARGET_ARCHITECTURE.md`](docs/architecture/TARGET_ARCHITECTURE.md)
- [`docs/contracts/CANONICAL_DOCUMENT.md`](docs/contracts/CANONICAL_DOCUMENT.md)
- [`docs/contracts/JEV_EVALUATION_CONTRACT.md`](docs/contracts/JEV_EVALUATION_CONTRACT.md)

---

## 3. Bounded Wave 0 Deliverables

- [x] Initial `.gitignore` and `pyproject.toml`.
- [x] System documentation baseline (`PRODUCT.md`, `CAPABILITY_MAP.md`, `CAPABILITY_DAG.md`, `ROADMAP.md`).
- [x] Architecture specification (`TARGET_ARCHITECTURE.md`).
- [x] Canonical schemas and contracts (`CANONICAL_DOCUMENT.md`, `JEV_EVALUATION_CONTRACT.md`).
- [ ] Pydantic Python implementations of schemas in `src/sentiment/contracts/`.
- [ ] Initial unit tests validating schema contracts and invariants in `tests/test_contracts.py`.

Wave 0 is complete when the schema contracts pass strict Pydantic parsing and validation unit tests.
