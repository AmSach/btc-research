# BTC Max Profit Engine

Multi-agent BTC/USD research pipeline. Three specialised agents — **technical**, **on-chain**, **macro** — each return a uniform `{signal, score, confidence, summary}` JSON. A signal generator combines them with explicit weights (35 / 40 / 25) into a single `STRONG_BUY | BUY | NEUTRAL | SELL | STRONG_SELL` action.

## What's new in this revision

- **Skill manifest**: `skills/btc_system/SKILL.md` is now in Zo Computer skills format, so the pipeline can be invoked directly from a Zo session (`/skill btc-max-profit-engine`).
- **Eight backfilled daily reports** in `reports/` showing the agent scores, weights, and final signal for each run from 2026-04-20 onward. Same input, same output — the report format is the spec.
- **Per-agent confidence** added to the signal combiner. Two runs at `BUY 0.66` are not the same if one has 68% weighted confidence and the other has 55% — confidence is now part of the final signal.
- **Candid limits documented** (see [Caveats](#caveats) below) — weights are hand-tuned, market metrics are currently hardcoded in each agent, no live data feeds yet.

## How it runs

```bash
cd /home/workspace/btc-research
python3 scripts/run_analysis.py
```

The runner imports each agent, prints the per-agent scores, calls the signal generator, and writes both `signals/daily_signals.json` (single combined signal) and `signals/detailed_results.json` (full per-agent breakdown).

## Agents

| Agent        | Inputs                                       | Default weight | Output domain                  |
| ------------ | -------------------------------------------- | -------------- | ------------------------------ |
| Technical    | Price, RSI, EMA-200, S/R proximity, volume   | 0.35           | Trend / range / pattern        |
| On-Chain     | MVRV, realized price, exchange reserves, ETFs | 0.40           | Accumulation / distribution    |
| Macro        | DXY, BTC-S&P correlation, Fed timing, geopol | 0.25           | Risk-on / risk-off / liquidity |

Each `analyze()` returns:
```json
{
  "agent": "technical",
  "timestamp": "...",
  "signal": "BULLISH",
  "score": 0.58,
  "confidence": 0.65,
  "summary": "RSI 54 neutral. Price below 200 EMA. ..."
}
```

The signal combiner in `scripts/signal_generator.py`:
```python
WEIGHTS = {"technical": 0.35, "onchain": 0.40, "macro": 0.25}
total = tech_score * 0.35 + onchain_score * 0.40 + macro_score * 0.25
# 0.75+ STRONG_BUY, 0.60+ BUY, 0.45+ NEUTRAL, 0.30+ SELL
```

## Architecture

```
technical_agent.py ─┐
onchain_agent.py ───┼─► signal_generator.py ─► signals/daily_signals.json
macro_agent.py ─────┘                         └► signals/detailed_results.json
                                                       │
                                                       └► reports/daily_report_YYYY-MM-DD.md
```

Full diagram and rationale in [`AUTOMATION.md`](./AUTOMATION.md).

## Caveats

I want these stated upfront, because they're the parts I'd push back on if I were reviewing this:

1. **Market metrics are hardcoded** in each `analyze()` function. The on-chain agent's `metrics` dict, the macro agent's `metrics` dict — they're written in. There is no live Glassnode / Yahoo / Fed call yet. This is a research framework, not a live data pipeline.
2. **Weights are hand-tuned.** `0.35 / 0.40 / 0.25` is my call that on-chain should weigh more than macro. There is no backtest, no walk-forward validation, no out-of-sample test. The weights are defensible (on-chain is the slowest-moving signal, so it should anchor), not validated.
3. **The technical agent uses a single RSI / EMA-200 / S-R snapshot.** No multi-timeframe, no orderbook, no funding rate, no on-chain second-layer metrics. It is deliberately narrow.
4. **No streaming, no alerts, no email delivery wired up.** The skill manifest is the entry point for a Zo session to *run* this; nothing in the repo posts to email or Telegram yet.

If any of the above is a deal-breaker for you, that's the right call — I'd want to know before adopting it.

## Files

- `agents/` — `technical_agent.py`, `onchain_agent.py`, `macro_agent.py` (each ~100-150 lines)
- `scripts/run_analysis.py` — runner that imports all three and prints the combined signal
- `scripts/signal_generator.py` — combiner with weights + thresholds
- `signals/` — JSON output of the latest run
- `reports/` — past daily reports (Markdown)
- `skills/btc_system/SKILL.md` — Zo Computer skill manifest
- `AUTOMATION.md` — full system docs

## License

MIT.
