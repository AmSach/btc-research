---
name: btc-max-profit-engine
description: Multi-agent Bitcoin research system for daily signals, price prediction, and profit maximization. Uses parallel agent processing for technical, on-chain, and macro analysis. Generates daily trading signals with confidence scoring.
compatibility: Created for Zo Computer
metadata:
  author: man44.zo.computer
  version: "1.0"
  created: 2026-04-20
allowed-tools: Bash, Read, Write, WebSearch, WebResearch, ReadWebpage, Agent
---

# BTC Max Profit Engine

A multi-agent automated Bitcoin research and signal generation system.

## Usage

Run the full BTC analysis system:
```bash
cd /home/workspace/btc-research
python3 scripts/run_analysis.py
```

Run individual agents:
```bash
# Technical analysis
python3 agents/technical_agent.py

# On-chain analysis
python3 agents/onchain_agent.py

# Macro analysis
python3 agents/macro_agent.py
```

View latest signals:
```bash
cat signals/daily_signals.json
```

## Files

- `AUTOMATION.md` - Full system documentation
- `agents/` - Agent scripts
- `signals/` - Generated signals
- `reports/` - Daily reports

## Signal Output

The system outputs 5 signal types:
- **STRONG_BUY**: Score >= 0.75, take full position
- **BUY**: Score >= 0.60, partial position 25-50%
- **NEUTRAL**: Score >= 0.45, hold/no position
- **SELL**: Score >= 0.30, reduce position
- **STRONG_SELL**: Score < 0.30, exit all positions

## Configuration

Update `scripts/config.py` to set:
- Alert thresholds
- Weighting of each agent
- Delivery preferences