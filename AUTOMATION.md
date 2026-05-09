# BTC Max Profit Research System
# Version 1.0 - April 20, 2026

## Overview
Automated multi-agent Bitcoin research, analysis, and signal generation system.
Runs daily and generates trading signals with 100% focus on profit maximization.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MASTER CONTROLLER (zo.ask)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ TECHNICAL    │     │ ON-CHAIN    │     │ MACRO        │
│ ANALYSIS     │     │ ANALYST     │     │ STRATEGIST   │
│ AGENT        │     │ AGENT       │     │ AGENT        │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Price Action │     │ Glassnode   │     │ DXY, Fed     │
│ Patterns    │     │ ETF Flows   │     │ S&P500 Corr  │
│ Support/Res  │     │ MVRV, NVT   │     │ Risk Assets  │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
              ┌─────────────────────────┐
              │   SIGNAL GENERATOR       │
              │   & CONFIDENCE SCORER    │
              └────────────┬────────────┘
                           ▼
              ┌─────────────────────────┐
              │   DAILY REPORT          │
              │   (email/Telegram)      │
              └─────────────────────────┘
```

## Agents

### 1. Technical Analysis Agent
- Candlestick patterns (daily/weekly/monthly)
- Support/resistance identification
- Moving average crossovers (50, 100, 200 MA)
- RSI, MACD, Bollinger Bands
- Volume analysis
- Price prediction confidence: 65-75%

### 2. On-Chain Analyst Agent
- Glassnode metrics (MVRV, Realized Price, ETF flows)
- Exchange reserves, whale activity
- Accumulation Trend Score
- Long-term holder dominance
- Prediction confidence: 70-80%

### 3. Macro Strategist Agent
- DXY correlation analysis
- S&P500/Nasdaq correlation
- Fed rate expectations
- Geopolitical risk (Iran, wars)
- Risk-on/risk-off positioning
- Prediction confidence: 60-70%

## Signal Types

| Signal | Description | Action |
|--------|-------------|--------|
| STRONG_BUY | Confluence of 3+ agents bullish | Full position (50-100%) |
| BUY | 2 agents bullish | Partial position (25-50%) |
| NEUTRAL | Mixed signals | No position / hedge |
| SELL | 2 agents bearish | Reduce/close position |
| STRONG_SELL | Confluence of 3+ bearish | Full short if available |

## Current Market Context (April 20, 2026)

### Price: $76,086 (BTC/USD Bitstamp)
- Down 40.8% from ATH ($125,835) on Oct 6, 2025
- RSI: 54 (neutral zone)
- 200-day EMA: $82,919 (overhead resistance)
- Key Support: $68,900
- Key Resistance: $75,000 (100-day MA / gamma node)

### Key Metrics
- BTC/SPX 30-day Correlation: 0.74 (high - trades like equity)
- DXY: ~98.7 (elevated, pressuring risk assets)
- ETF Flows Q1 2026: $2.5B inflows (institutions buying correction)
- Exchange Reserves: 7-year lows (~11.9% of supply)
- MVRV: ~1.5 (historically "buy" territory)
- Realized Price Floor: $50k-$62k

### Recent Developments
- Fed rate cuts pushed to 2027 (Goolsbee)
- Iran war risk elevated (Strait of Hormuz)
- Strategy (MSTR) bought 34,164 BTC @ $74,395 ($2.54B)
- Tether holds 97,000+ BTC
- SpaceX holds $600M+ BTC (unchanged since 2024)
- Trump Strategic Bitcoin Reserve: 328,372 BTC (~$24.5B)

## Confidence Scoring Formula

```
Total Score = (Technical × 0.35) + (On-Chain × 0.40) + (Macro × 0.25)

STRONG_BUY: Score >= 0.75
BUY: Score >= 0.60
NEUTRAL: Score >= 0.45
SELL: Score >= 0.30
STRONG_SELL: Score < 0.30
```

## Files Structure

```
btc-research/
├── agents/
│   ├── technical_agent.py      # Technical analysis
│   ├── onchain_agent.py        # On-chain analysis  
│   └── macro_agent.py          # Macro analysis
├── signals/
│   ├── daily_signals.json      # Generated signals
│   └── signal_history.json     # Historical signals
├── data/
│   ├── btc_price_cache.json    # Price data
│   └── metrics_cache.json      # On-chain cache
├── reports/
│   └── daily_report_*.md       # Daily reports
├── scripts/
│   ├── collect_data.py         # Data collection
│   ├── run_analysis.py        # Run all agents
│   └── send_signals.py        # Send signals
├── skills/
│   └── btc_system/SKILL.md    # Zo skill definition
└── AUTOMATION.md             # This file
```

## Daily Automation Schedule (UTC)

| Time | Task | Agent |
|------|------|-------|
| 06:00 | Collect overnight price action | System |
| 06:30 | Fetch on-chain metrics | On-Chain Agent |
| 07:00 | Analyze macro conditions | Macro Agent |
| 07:30 | Technical analysis | Technical Agent |
| 08:00 | Generate signals | Signal Generator |
| 08:30 | Compile daily report | Master |
| 09:00 | Send to user (email/telegram) | Delivery |

## Disclaimer

This system provides research signals only.
Not financial advice. Always do your own due diligence.
Cryptocurrency investments carry high risk.