# Wave 4: Latent Representation Learning (JEPA)

- **Status:** **PLANNED**
- **Governed Atoms:**
  - `E01` (JEPA Target State Formulation — Gated on DG-C)
  - `E02` (Multimodal Context Encoder)
  - `E03` (JEPA Target Encoder & Predictor)
  - `E04` (Self-Supervised JEPA Pre-training Loop)
  - `F01` (Intrinsic Representation & Non-Collapse Proof)
- **Decision Gates Resolved:** `DG-C` (Target state formulation $y_{t+\Delta t}$).
- **Prerequisite Gate:** Wave 3 Golden Proof verified on `main`.
- **Target Integration Branch:** `implement/wave-4`

---

## 1. Objective & Bounding Rules

Implement the self-supervised **Joint Embedding Predictive Architecture (JEPA)** that models the latent dynamics of the Bitcoin market without autoregressive token generation:

1. **Target State Formulation (`E01` / `DG-C`)**: Define the multidimensional target vector representing forward market reality (log return distribution across horizons, realized volatility, and liquidation volume).
2. **Context Encoder (`E02`)**: Train a temporal neural network (Transformer or MLP-Mixer) that maps a historical window of multimodal features $X_{t-k:t}$ into latent representation space $s_t \in \mathbb{R}^{64}$.
3. **Target Encoder & Predictor (`E03`)**: Implement an Exponential Moving Average (EMA) target encoder that generates future target embeddings $s_{t+\Delta t}$, while the predictor network learns transition dynamics.
4. **Self-Supervised Pre-Training & Non-Collapse (`E04`, `F01`)**: Formulate a training loop optimizing latent MSE regularized by VICReg variance/covariance terms to guarantee non-collapsing, highly informative embeddings.

### Explicit Wave 4 Non-Goals:
- Do **NOT** execute simulated trading or PnL backtests (trading validation belongs to `quant-platform`).
- Do **NOT** use generative text models (GPT/LLMs).

---

## 2. Technical Architecture & JEPA Model Formulation

```mermaid
flowchart TD
    subgraph InputStreams ["Historical Multi-Modal Features (From Wave 3)"]
        History["History Context Window: X_{t-k:t} (Sentiment + Flows + Derivs)"]
        Future["Future Market State: y_{t+Delta t} (Price returns, Vol, Liquidations)"]
    end

    subgraph JEPA_Arch ["JEPA Architecture (E02 - E03)"]
        ContextEncoder["Context Encoder: f_theta(X_{t-k:t})"]
        TargetEncoder["Target Encoder: g_xi(y_{t+Delta t})<br/>(Updated via EMA: xi <- m*xi + (1-m)*theta)"]
        Predictor["Latent Predictor: p_phi(s_t, Delta t)"]
    end

    subgraph LossOptimization ["Optimization & Non-Collapse (E04 - F01)"]
        LatentMSE["Latent Prediction Loss: || s_hat_{t+Delta t} - s_{t+Delta t} ||^2"]
        VICRegLoss["VICReg Regularization: Var(z) >= 1.0 & Cov(z) -> 0"]
        TotalLoss["Total Loss = MSE + lambda_var*Loss_var + lambda_cov*Loss_cov"]
    end

    History --> ContextEncoder
    ContextEncoder -->|s_t in R^64| Predictor
    Predictor -->|s_hat_{t+Delta t}| LatentMSE
    Future --> TargetEncoder
    TargetEncoder -->|s_{t+Delta t} in R^64| LatentMSE
    LatentMSE --> TotalLoss
    TargetEncoder --> VICRegLoss
    VICRegLoss --> TotalLoss
```

---

## 3. Bounded Implementation Tasks

### Task 4.1: Target State Definition (`E01` / `DG-C`)
* Module: `src/atlas/modeling/target_state.py`
* Mathematical vector formulation: forward 1h/4h/24h log returns, Parkinson realized volatility, and liquidation volume delta.

### Task 4.2: Context & Target Encoders (`E02`, `E03`)
* Module: `src/atlas/modeling/jepa.py`
* PyTorch implementation of `ContextEncoder` (Temporal MLP-Mixer), `TargetEncoder` (EMA weight updates), and `Predictor` (residual MLP).

### Task 4.3: VICReg Loss & Pre-Training Loop (`E04`, `F01`)
* Module: `src/atlas/modeling/train.py`
* Self-supervised training loop with AdamW, cosine annealing, and variance-invariance-covariance loss regularizers.

---

## 4. Golden E2E Proof Specification

- **Proof Document:** `docs/integration/WAVE4_GOLDEN_E2E_JEPA_REPRESENTATION.md`
- **Proof Runner:** `tools/wave4_golden_e2e.py`
- **Acceptance Criteria**:
  1. **Non-Collapse Proof (`F01`)**: Trained embeddings over out-of-sample test splits prove $\text{Var}(z_j) \ge 1.0$ across all 64 latent dimensions (rejects representation collapse).
  2. **Predictive Latent Correlation**: Predicted latent states $\hat{s}_{t+\Delta t}$ show positive cosine similarity ($> 0.35$) with actual future latent states $s_{t+\Delta t}$.
  3. **Execution Latency**: Online latent inference for a single window executes in $< 15$ ms on CPU.
