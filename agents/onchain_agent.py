#!/usr/bin/env python3
"""
On-Chain Analyst Agent - BTC Max Profit Engine
Analyzes Glassnode metrics, ETF flows, MVRV, exchange reserves
"""

import json
import sys
from datetime import datetime

def analyze():
    """Run on-chain analysis on BTC"""
    
    # From research data
    metrics = {
        'mvrv': 1.5,
        'realized_price_floor': 50000,
        'realized_price_ceiling': 62000,
        'exchange_reserves_pct': 11.9,  # 7-year low
        'etf_flows_q1_2026_billions': 2.5,
        'supply_in_profit_pct': 60,  # ~60% per Glassnode
        'accumulation_trend_score': 0.45,  # below 0.5 = weak accumulation
        'btc_price_now': 76099
    }
    
    signals = []
    confidence_factors = []
    
    # 1. MVRV Analysis
    mvrv = metrics['mvrv']
    if mvrv < 1.5:
        signals.append({'indicator': 'MVRV', 'signal': 'UNDERVALUED', 'weight': 0.20})
        confidence_factors.append(0.80)
    elif mvrv < 2.5:
        signals.append({'indicator': 'MVRV', 'signal': 'FAIR_VALUE', 'weight': 0.10})
        confidence_factors.append(0.70)
    elif mvrv < 3.5:
        signals.append({'indicator': 'MVRV', 'signal': 'OVERVALUED', 'weight': -0.15})
        confidence_factors.append(0.70)
    else:
        signals.append({'indicator': 'MVRV', 'signal': 'EXTREME_OVERVALUED', 'weight': -0.25})
        confidence_factors.append(0.80)
    
    # 2. Realized Price Analysis
    realized_floor = metrics['realized_price_floor']
    realized_ceiling = metrics['realized_price_ceiling']
    price = metrics['btc_price_now']
    
    if price < realized_floor:
        signals.append({'indicator': 'REALIZED_PRICE', 'signal': 'BELOW_REALIZED_BUY_ZONE', 'weight': 0.25})
        confidence_factors.append(0.85)
    elif price < realized_ceiling:
        signals.append({'indicator': 'REALIZED_PRICE', 'signal': 'NEAR_REALIZED_SUPPORT', 'weight': 0.15})
        confidence_factors.append(0.75)
    else:
        signals.append({'indicator': 'REALIZED_PRICE', 'signal': 'ABOVE_REALIZED', 'weight': 0.05})
        confidence_factors.append(0.60)
    
    # 3. Exchange Reserves (inverse = bullish when low)
    reserves = metrics['exchange_reserves_pct']
    if reserves < 12:
        signals.append({'indicator': 'EXCHANGE_RESERVES', 'signal': 'LOW_RESERVES_BULLISH', 'weight': 0.15})
        confidence_factors.append(0.75)
    elif reserves < 15:
        signals.append({'indicator': 'EXCHANGE_RESERVES', 'signal': 'NORMAL_RESERVES', 'weight': 0.05})
        confidence_factors.append(0.60)
    else:
        signals.append({'indicator': 'EXCHANGE_RESERVES', 'signal': 'HIGH_RESERVES_BEARISH', 'weight': -0.10})
        confidence_factors.append(0.70)
    
    # 4. ETF Flows
    etf_flows = metrics['etf_flows_q1_2026_billions']
    if etf_flows > 1.5:
        signals.append({'indicator': 'ETF_FLOWS', 'signal': 'STRONG_INSTITUTIONAL_INFLOW', 'weight': 0.20})
        confidence_factors.append(0.80)
    elif etf_flows > 0:
        signals.append({'indicator': 'ETF_FLOWS', 'signal': 'POSITIVE_INSTITUTIONAL_FLOW', 'weight': 0.10})
        confidence_factors.append(0.70)
    else:
        signals.append({'indicator': 'ETF_FLOWS', 'signal': 'ETF_OUTFLOWS', 'weight': -0.15})
        confidence_factors.append(0.75)
    
    # 5. Supply in Profit
    supply_profit = metrics['supply_in_profit_pct']
    if supply_profit < 40:
        signals.append({'indicator': 'SUPPLY_IN_PROFIT', 'signal': 'EARLY_CYCLE_BULLISH', 'weight': 0.20})
        confidence_factors.append(0.75)
    elif supply_profit < 60:
        signals.append({'indicator': 'SUPPLY_IN_PROFIT', 'signal': 'MID_CYCLE', 'weight': 0.10})
        confidence_factors.append(0.70)
    elif supply_profit < 75:
        signals.append({'indicator': 'SUPPLY_IN_PROFIT', 'signal': 'LATE_CYCLE', 'weight': -0.10})
        confidence_factors.append(0.70)
    else:
        signals.append({'indicator': 'SUPPLY_IN_PROFIT', 'signal': 'EXTREME_LATE_CYCLE', 'weight': -0.25})
        confidence_factors.append(0.80)
    
    # 6. Accumulation Trend Score
    ats = metrics['accumulation_trend_score']
    if ats < 0.4:
        signals.append({'indicator': 'ACCUMULATION_TREND', 'signal': 'WEAK_ACCUMULATION', 'weight': -0.10})
        confidence_factors.append(0.65)
    elif ats < 0.6:
        signals.append({'indicator': 'ACCUMULATION_TREND', 'signal': 'MODERATE_ACCUMULATION', 'weight': 0.10})
        confidence_factors.append(0.70)
    else:
        signals.append({'indicator': 'ACCUMULATION_TREND', 'signal': 'STRONG_ACCUMULATION', 'weight': 0.20})
        confidence_factors.append(0.80)
    
    # Calculate weighted score
    total_weight = sum(s['weight'] for s in signals)
    avg_confidence = sum(confidence_factors) / len(confidence_factors)
    
    if total_weight >= 0.20:
        signal = 'BULLISH'
        score = min(0.80, 0.55 + total_weight)
    elif total_weight <= -0.10:
        signal = 'BEARISH'
        score = max(0.25, 0.45 + total_weight)
    else:
        signal = 'NEUTRAL'
        score = 0.50 + total_weight * 0.5
    
    result = {
        'agent': 'onchain',
        'timestamp': datetime.utcnow().isoformat(),
        'metrics': metrics,
        'signal': signal,
        'score': round(score, 3),
        'confidence': round(avg_confidence, 3),
        'key_indicators': {
            'mvrv': f"{mvrv} ({'undervalued' if mvrv < 1.5 else 'fair value'})",
            'realized_price_floor': f"${realized_floor:,}",
            'exchange_reserves': f"{reserves}% (7-year low)",
            'etf_flows_q1': f"${etf_flows}B",
            'supply_in_profit': f"{supply_profit}%"
        },
        'summary': f"MVRV {mvrv} indicates {'undervalued' if mvrv < 1.5 else 'fair value'}. "
                   f"Price above realized floor ${realized_floor:,}. "
                   f"Exchange reserves at {reserves}% (7-year low). "
                   f"Q1 2026 ETF inflows ${etf_flows}B (institutions buying correction)."
    }
    
    return result

if __name__ == '__main__':
    result = analyze()
    print(json.dumps(result, indent=2))
    sys.exit(0)