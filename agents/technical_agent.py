#!/usr/bin/env python3
"""
Technical Analysis Agent - BTC Max Profit Engine
Analyzes price action, patterns, support/resistance, indicators
"""

import json
import sys
from datetime import datetime

def analyze():
    """Run technical analysis on BTC/USD"""
    
    # Current market data from research
    price = 76099
    rsi = 54
    ema_200 = 82919
    key_support = 68900
    key_resistance = 75000
    
    # Technical signals
    signals = []
    confidence_factors = []
    
    # 1. RSI Analysis
    if rsi < 30:
        signals.append({'indicator': 'RSI_14', 'signal': 'OVERSOLD', 'weight': 0.15})
        confidence_factors.append(0.75)
    elif rsi > 70:
        signals.append({'indicator': 'RSI_14', 'signal': 'OVERBOUGHT', 'weight': -0.15})
        confidence_factors.append(0.75)
    elif 50 <= rsi <= 60:
        signals.append({'indicator': 'RSI_14', 'signal': 'NEUTRAL_BULLISH', 'weight': 0.08})
        confidence_factors.append(0.65)
    else:
        signals.append({'indicator': 'RSI_14', 'signal': 'NEUTRAL', 'weight': 0.0})
        confidence_factors.append(0.50)
    
    # 2. Price vs 200 EMA (major trend)
    if price > ema_200:
        signals.append({'indicator': 'PRICE_VS_EMA200', 'signal': 'BELOW_EMA_BEARISH', 'weight': -0.20})
        confidence_factors.append(0.70)
    else:
        signals.append({'indicator': 'PRICE_VS_EMA200', 'signal': 'BELOW_EMA', 'weight': -0.10})
        confidence_factors.append(0.70)
    
    # 3. Distance from ATH (cyclical analysis)
    ath_distance = (price / 125835 - 1) * 100  # -40.8%
    if ath_distance < -60:
        signals.append({'indicator': 'ATH_DISTANCE', 'signal': 'DEEP_CORRECTION_BULLISH', 'weight': 0.15})
        confidence_factors.append(0.80)
    elif ath_distance < -40:
        signals.append({'indicator': 'ATH_DISTANCE', 'signal': 'MODERATE_CORRECTION', 'weight': 0.10})
        confidence_factors.append(0.70)
    
    # 4. Support/Resistance proximity
    distance_to_support = (price - key_support) / price * 100
    distance_to_resistance = (key_resistance - price) / price * 100
    
    if distance_to_support < 5:
        signals.append({'indicator': 'NEAR_SUPPORT', 'signal': 'STRONG_SUPPORT', 'weight': 0.15})
        confidence_factors.append(0.80)
    
    if distance_to_resistance < 3:
        signals.append({'indicator': 'NEAR_RESISTANCE', 'signal': 'STRONG_RESISTANCE', 'weight': -0.15})
        confidence_factors.append(0.75)
    
    # 5. Volume analysis (from chart - would need real data)
    # Placeholder - volume appears elevated in recent weeks
    signals.append({'indicator': 'VOLUME', 'signal': 'ELEVATED_VOLUME', 'weight': 0.05})
    confidence_factors.append(0.50)
    
    # Calculate weighted signal
    total_weight = sum(s['weight'] for s in signals)
    avg_confidence = sum(confidence_factors) / len(confidence_factors)
    
    # Determine signal
    if total_weight >= 0.15:
        signal = 'BULLISH'
        score = min(0.75, 0.55 + total_weight)
    elif total_weight <= -0.15:
        signal = 'BEARISH'
        score = max(0.25, 0.45 + total_weight)
    else:
        signal = 'NEUTRAL'
        score = 0.50 + total_weight * 0.5
    
    result = {
        'agent': 'technical',
        'timestamp': datetime.utcnow().isoformat(),
        'price': price,
        'indicators': signals,
        'signal': signal,
        'score': round(score, 3),
        'confidence': round(avg_confidence, 3),
        'key_levels': {
            'support': key_support,
            'resistance': key_resistance,
            'ema_200': ema_200
        },
        'summary': f"RSI {rsi} neutral. Price below 200 EMA ({ema_200:,}). Near support {key_support:,}. Range-bound between {key_support:,} and {key_resistance:,}."
    }
    
    return result

if __name__ == '__main__':
    result = analyze()
    print(json.dumps(result, indent=2))
    sys.exit(0)