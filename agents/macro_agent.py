#!/usr/bin/env python3
"""
Macro Strategist Agent - BTC Max Profit Engine
Analyzes DXY, S&P500 correlation, Fed policy, geopolitical risk
"""

import json
import sys
from datetime import datetime

def analyze():
    """Run macro analysis on BTC"""
    
    # From research data
    metrics = {
        'btc_spx_correlation_30d': 0.74,
        'btc_nasdaq_correlation_30d': 0.72,
        'dxy': 98.7,
        'fed_rate_cut_expectation': '2027',  # pushed back from 2026
        ' Iran_war_risk': 'elevated',
        'sp500_record_highs': True,
        'nasdaq_record_highs': True,
        'btc_price': 76099,
        'risk_on_sentiment': 'cautious'
    }
    
    signals = []
    confidence_factors = []
    
    # 1. BTC-Equity Correlation Analysis
    corr = metrics['btc_spx_correlation_30d']
    if corr > 0.60:
        # High correlation - BTC trades like risk asset
        signals.append({'indicator': 'BTC_SPX_CORRELATION', 'signal': 'HIGH_CORRELATION_RISK_ASSET', 'weight': -0.10})
        confidence_factors.append(0.75)
        # If S&P500 at record highs, BTC should be higher too
        if metrics['sp500_record_highs']:
            signals.append({'indicator': 'SPX_AT_RECORD', 'signal': 'BTC_LAGGING_BULLISH', 'weight': 0.15})
            confidence_factors.append(0.70)
    elif corr < 0.30:
        signals.append({'indicator': 'BTC_SPX_CORRELATION', 'signal': 'DECOUPLED_BULLISH', 'weight': 0.15})
        confidence_factors.append(0.80)
    
    # 2. DXY Analysis (inverse correlation typical)
    dxy = metrics['dxy']
    if dxy > 100:
        signals.append({'indicator': 'DXY', 'signal': 'STRONG_DOLLAR_BEARISH_FOR_BTC', 'weight': -0.15})
        confidence_factors.append(0.70)
    elif dxy > 98:
        signals.append({'indicator': 'DXY', 'signal': 'ELEVATED_DOLLAR_HEADWIND', 'weight': -0.10})
        confidence_factors.append(0.65)
    elif dxy < 95:
        signals.append({'indicator': 'DXY', 'signal': 'WEAK_DOLLAR_BULLISH_FOR_BTC', 'weight': 0.20})
        confidence_factors.append(0.75)
    else:
        signals.append({'indicator': 'DXY', 'signal': 'NEUTRAL_DOLLAR', 'weight': 0.0})
        confidence_factors.append(0.50)
    
    # 3. Fed Rate Expectations
    fed_timing = metrics['fed_rate_cut_expectation']
    if fed_timing == '2027':
        signals.append({'indicator': 'FED_POLICY', 'signal': 'RATE_CUTS_DELAYED_BEARISH', 'weight': -0.10})
        confidence_factors.append(0.70)
    elif fed_timing == '2026_H2':
        signals.append({'indicator': 'FED_POLICY', 'signal': 'RATE_CUTS_LATER_THIS_YEAR', 'weight': 0.05})
        confidence_factors.append(0.65)
    else:
        signals.append({'indicator': 'FED_POLICY', 'signal': 'RATE_CUTS_IMMINENT', 'weight': 0.15})
        confidence_factors.append(0.75)
    
    # 4. Geopolitical Risk (Iran war)
    if metrics[' Iran_war_risk'] == 'elevated':
        signals.append({'indicator': 'GEOPOLITICAL', 'signal': 'RISK_OFF_ENVIRONMENT', 'weight': -0.05})
        confidence_factors.append(0.60)
        # However, BTC has shown resilience to Iran shocks
        signals.append({'indicator': 'GEOPOLITICAL', 'signal': 'BTC_RESILIENT_TO_IRAN_SHOCKS', 'weight': 0.10})
        confidence_factors.append(0.70)
    
    # 5. Risk-On Sentiment
    if metrics['nasdaq_record_highs'] and metrics['sp500_record_highs']:
        signals.append({'indicator': 'MARKET_MOOD', 'signal': 'RISK_ON_RECORD_HIGHS', 'weight': 0.15})
        confidence_factors.append(0.70)
    
    # 6. Bitcoin-specific bullish macro
    signals.append({'indicator': 'INSTITUTIONAL_ADOPTION', 'signal': 'MSTR_ETF_BUYING', 'weight': 0.10})
    confidence_factors.append(0.75)
    signals.append({'indicator': 'STRATEGIC_RESERVE', 'signal': 'GOVERNMENT_HOLDINGS_BULLISH', 'weight': 0.10})
    confidence_factors.append(0.70)
    
    # Calculate weighted score
    total_weight = sum(s['weight'] for s in signals)
    avg_confidence = sum(confidence_factors) / len(confidence_factors)
    
    if total_weight >= 0.15:
        signal = 'BULLISH'
        score = min(0.75, 0.50 + total_weight)
    elif total_weight <= -0.15:
        signal = 'BEARISH'
        score = max(0.25, 0.40 + total_weight)
    else:
        signal = 'NEUTRAL'
        score = 0.50 + total_weight * 0.3
    
    result = {
        'agent': 'macro',
        'timestamp': datetime.utcnow().isoformat(),
        'metrics': {
            'btc_spx_correlation': corr,
            'dxy': dxy,
            'fed_rate_cut_timing': fed_timing,
            'iran_war_risk': metrics[' Iran_war_risk'],
            'sp500_at_record_highs': metrics['sp500_record_highs']
        },
        'signal': signal,
        'score': round(score, 3),
        'confidence': round(avg_confidence, 3),
        'key_factors': {
            'correlation': f"BTC-S&P500 {corr} (high - trades like equity)",
            'dollar': f"DXY {dxy} (elevated - headwind for BTC)",
            'fed_timing': f"Rate cuts pushed to {fed_timing}",
            'geopolitical': "Iran war risk elevated, Strait of Hormuz",
            'equities': "S&P500 and Nasdaq at record highs (risk-on)"
        },
        'summary': f"BTC-S&P500 correlation {corr} - BTC tracking equities. "
                   f"DXY {dxy} elevated (dollar headwind). "
                   f"Fed rate cuts delayed to {fed_timing}. "
                   f"S&P500/Nasdaq at record highs = risk-on backdrop. "
                   f"BTC more resilient than oil/equities to Iran shocks."
    }
    
    return result

if __name__ == '__main__':
    result = analyze()
    print(json.dumps(result, indent=2))
    sys.exit(0)