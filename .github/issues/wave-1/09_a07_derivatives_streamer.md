## Agent-ready mandate

Derived from `SCOPE.md` and `docs/waves/WAVE_1_INGESTION_REGEX_ENGINE.md`.

Active Path step: **9 — Implement Derivatives Microstructure Monitor v1 (A07)**.

Blocked by: **none**.

## Objective

Implement the real-time WebSocket client for derivatives microstructure (`src/atlas/ingestion/derivatives_streamer.py`). Connect to public WebSocket market data streams (Binance and Bybit USD-M Futures for `BTCUSDT`), streaming real-time Funding Rates, Open Interest delta, and Liquidation trade spikes. This continuous stream provides the quantitative anchor representing real capital positioning.

## Authority

Start from:
- `docs/architecture/TARGET_ARCHITECTURE.md` (Derivatives Microstructure Monitor)
- `docs/contracts/ATLAS_CONFIG_CONTRACT.md` (`sources.derivatives`)

## Expected artifact

1. Code: `src/atlas/ingestion/derivatives_streamer.py` (`DerivativesStreamer`)
2. Interface:
   - `start_stream() -> AsyncIterator[DerivativesTick]`
   - `DerivativesTick`: venue, symbol, timestamp_utc, funding_rate, open_interest, liquidation_vol_buy, liquidation_vol_sell.
3. Tests: `tests/test_derivatives_streamer.py` (with mock WebSocket message sequence).

## Acceptance

- Auto-reconnects on WebSocket disconnects or ping timeouts without crashing.
- Parses Binance markPrice / fundingRate and openInterest streams.
- Parses Bybit tickers / fundingRate stream.
- Unit tests pass using mocked async WebSocket frames.

## Stop conditions

Stop and report if implementation requires authenticated private exchange API keys or account signing; market data WebSocket feeds are 100% public.
