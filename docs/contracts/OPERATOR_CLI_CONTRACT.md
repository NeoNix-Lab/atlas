# Contract: Operator CLI Contract v1 (`OPERATOR_CLI_CONTRACT.md`)

**Project:** Atlas (BTC Multi-Modal Sentiment & Latent Representation Engine)  
**Status:** FROZEN  
**Schema Identifier:** `atlas/operator-cli@1`  
**Governed Atoms:** `G01`, `G02`, `G03`, `G04`  
**CLI Tool Executable:** `atlas`

---

## 1. Specification & Design Principles

The `atlas` CLI is the authoritative, single-entrypoint operator control interface for Version 1.0.  
It adheres to the following invariants:
1. **Idempotence & Graceful Termination**: All daemon commands handle `SIGINT` (Ctrl+C) and `SIGTERM` by safely flushing in-flight WORM writes and unwritten Parquet buffers before exiting.
2. **Dual-Mode Rendering**:
   * *Human Mode (default)*: High-density, ANSI-colored Rich terminal tables with progress spinners and clear status highlights.
   * *Machine Mode (`--json`)*: Emits valid, unbuffered JSON strings to `stdout` for headless cron jobs, orchestration, and monitoring agents.
3. **Strict Exit Codes**: Commands exit with predictable POSIX-compliant status codes.

---

## 2. Command Inventory & Syntax

### 2.1 `atlas daemon` — Ingestion & Engine Lifecycle Controller
Controls the background harvesting, line-rate filtering, and Jev evaluation daemon.

```bash
# Start the ingestion workers
atlas daemon start [OPTIONS]
  --sources TEXT         Comma-separated source filter: 'reddit,telegram,news,onchain,derivatives' (default: all enabled in atlas.toml)
  --detached / --no-detached Run in background or foreground (default: foreground)
  --log-level [DEBUG|INFO|WARNING|ERROR] (default: from atlas.toml)

# Gracefully stop the running daemon
atlas daemon stop [OPTIONS]
  --timeout INTEGER      Maximum seconds to wait for buffer flush before SIGKILL (default: 30)

# Check daemon health and active worker status
atlas daemon status [OPTIONS]
  --json                 Emit machine-readable JSON health state
```

### 2.2 `atlas status` — Comprehensive System Telemetry
Renders a live operational dashboard in the terminal showing connector uptime, throughput, lag, and budget:

```bash
atlas status [OPTIONS]
  --json                 Emit complete status snapshot as JSON
```

**Human Terminal Rendering Example:**
```text
Atlas System Status (v0.1.0) — Environment: production
System Time: 2026-09-29 22:20:00 UTC | Daemon PID: 14820 (ACTIVE)

CONNECTOR STATUS:
┌──────────────┬─────────┬──────────────┬──────────────┬───────────────┐
│ Source       │ State   │ Ingested/min │ Spam Drop %  │ Lag (Obs-Pub) │
├──────────────┼─────────┼──────────────┼──────────────┼───────────────┤
│ Reddit       │ OK      │ 42 msgs/m    │ 81.2%        │ 12.4s         │
│ Telegram     │ OK      │ 18 msgs/m    │ 64.5%        │ 1.8s          │
│ Crypto News  │ OK      │ 4 articles/m │ 15.0%        │ 45.2s         │
│ On-Chain Mem │ OK      │ 60 ticks/m   │ 0.0%         │ 0.4s          │
│ Derivatives  │ OK      │ 120 ticks/m  │ 0.0%         │ 0.2s          │
└──────────────┴─────────┴──────────────┴──────────────┴───────────────┘

BUDGET & JEV AI INFERENCE:
  Today Spend:       $0.42 / $1.50 (28.0% of daily cap)
  Monthly Spend:     $8.65 / $30.00
  Circuit Breaker:   ARMED (Normal Operation)
  Jev Latency (p95): 280ms
```

### 2.3 `atlas probe` — Pipeline Diagnostic & Dry-Run Inspector
Runs an arbitrary text string or URL through the live multi-stage funnel without persisting the result to production storage:

```bash
atlas probe [OPTIONS]
  --text TEXT            Raw text to evaluate through L1 Regex -> L2 Jev
  --source TEXT          Simulated source platform (default: 'twitter')
  --json                 Output full evaluation trace as JSON
```

**Terminal Output:**
```text
PROBE TRACE:
1. Input Payload: "Breaking: SEC approves Bitcoin in-kind creations for BlackRock"
2. Regex L1 Filter:
   - Spam Drop Decision: PASS (Spam Score: 0.02)
   - Entities Extracted: [BTC ($BTC), SEC (Regulatory)]
3. TypeSafe AI Jev Evaluation (L2):
   - is_btc_relevant:      0.99 (Noul)
   - is_fud_or_rumor:      0.02 (Noul)
   - sentiment_polarity:   bullish (Choice)
   - credibility_tier:     tier1_media_or_official (Score: 1.0)
   - market_urgency:       high (Score: 0.75)
4. Resulting SemanticVector:
   - Polarity Score:       +0.50
   - Effective Impact:     +0.875
```

### 2.4 `atlas backfill` — Historical Harvesting
Fetches and processes historical feeds or archive dumps into WORM storage:

```bash
atlas backfill [OPTIONS]
  --source [reddit|news|onchain]
  --from-date YYYY-MM-DD
  --to-date YYYY-MM-DD
  --skip-ai              Run only Regex L1 and WORM ingestion (zero Jev token spend)
```

### 2.5 `atlas export` — quant-platform Feature Artifact Exporter
Compiles materialized time-windows into partitioned Parquet files formatted for `quant-platform`:

```bash
atlas export [OPTIONS]
  --resolution [1m|5m|15m|1h]
  --from-date YYYY-MM-DD
  --to-date YYYY-MM-DD
  --out-dir PATH         Destination path (default: data/features/)
```

### 2.6 `atlas check-config` — Configuration Validator
Validates `atlas.toml` and `.env` against the formal Pydantic schema without starting workers.

---

## 3. Exit Code Standard

| Exit Code | Identifier | Meaning |
|---|---|---|
| `0` | `SUCCESS` | Command completed successfully with no errors. |
| `1` | `ERR_CONFIG` | Invalid configuration in `atlas.toml`, missing `.env` key, or malformed CLI arguments. |
| `2` | `ERR_NETWORK_SOURCE` | External API unreachable or source returned persistent fatal HTTP errors. |
| `3` | `ERR_CIRCUIT_TRIPPED` | Daily/Monthly token budget cap exceeded; AI operations halted. |
| `4` | `ERR_FATAL_RUNTIME` | Unhandled internal exception, disk full, or corrupted WORM storage path. |
