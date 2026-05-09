#!/usr/bin/env python3
"""
Signal Generator - BTC Max Profit Engine
Combines agent outputs into final trading signals
"""

import json
import sys
from datetime import datetime

# Agent weights
WEIGHTS = {
    'technical': 0.35,
    'onchain': 0.40,
    'macro': 0.25
}

# Signal thresholds
THRESHOLDS = {
    'strong_buy': 0.75,
    'buy': 0.60,
    'neutral': 0.45,
    'sell': 0.30
}

def generate_signal(technical_result, onchain_result, macro_result):
    """Combine agent signals into final trading signal"""
    
    # Calculate weighted scores
    tech_score = technical_result['score'] * WEIGHTS['technical']
    onchain_score = onchain_result['score'] * WEIGHTS['onchain']
    macro_score = macro_result['score'] * WEIGHTS['macro']
    
    total_score = tech_score + onchain_score + macro_score
    
    # Calculate weighted confidence
    tech_conf = technical_result['confidence'] * WEIGHTS['technical']
    onchain_conf = onchain_result['confidence'] * WEIGHTS['onchain']
    macro_conf = macro_result['confidence'] * WEIGHTS['macro']
    
    total_confidence = tech_conf + onchain_conf + macro_conf
    
    # Determine signal type
    if total_score >= THRESHOLDS['strong_buy']:
        signal_type = 'STRONG_BUY'
        action = 'Take full position (50-100% of capital)'
    elif total_score >= THRESHOLDS['buy']:
        signal_type = 'BUY'
        action = 'Take partial position (25-50% of capital)'
    elif total_score >= THRESHOLDS['neutral']:
        signal_type = 'NEUTRAL'
        action = 'Hold current position / no new entries'
    elif total_score >= THRESHOLDS['sell']:
        signal_type = 'SELL'
        action = 'Reduce position by 25-50%'
    else:
        signal_type = 'STRONG_SELL'
        action = 'Exit all positions (or short if available)'
    
    # Determine key drivers
    drivers = []
    if technical_result['score'] >= 0.65:
        drivers.append(f"Technical: {technical_result['signal'].lower()} ({technical_result['score']})")
    if onchain_result['score'] >= 0.65:
        drivers.append(f"On-Chain: {onchain_result['signal'].lower()} ({onchain_result['score']})")
    if macro_result['score'] >= 0.65:
        drivers.append(f"Macro: {macro_result['signal'].lower()} ({macro_result['score']})")
    
    # Risk assessment
    risk_factors = []
    current_price = technical_result['price']
    
    if current_price < 70000:
        risk_factors.append("Price near key support ($68,900)")
    if current_price > 80000:
        risk_factors.append("Price approaching 200 EMA resistance ($82,919)")
    
    result = {
        'timestamp': datetime.utcnow().isoformat(),
        'signal_type': signal_type,
        'total_score': round(total_score, 3),
        'confidence': round(total_confidence, 3),
        'action': action,
        'current_price': current_price,
        'agent_scores': {
            'technical': round(technical_result['score'], 3),
            'onchain': round(onchain_result['score'], 3),
            'macro': round(macro_result['score'], 3)
        },
        'weighted_contribution': {
            'technical': round(tech_score, 3),
            'onchain': round(onchain_score, 3),
            'macro': round(macro_score, 3)
        },
        'key_drivers': drivers,
        'risk_factors': risk_factors,
        'levels': {
            'support': 68900,
            'resistance': 75000,
            'ema_200': 82919,
            'ath': 125835
        },
        'summary': f"{signal_type} signal. Score: {total_score:.2f}. {action}."
    }
    
    return result

def save_signal(signal, filepath='signals/daily_signals.json'):
    """Save signal to file"""
    with open(filepath, 'w') as f:
        json.dump(signal, f, indent=2)

if __name__ == '__main__':
    # Test with current data
    technical = {
        'score': 0.58,
        'confidence': 0.65,
        'signal': 'NEUTRAL_BULLISH',
        'price': 76099
    }
    onchain = {
        'score': 0.72,
        'confidence': 0.76,
        'signal': 'BULLISH'
    }
    macro = {
        'score': 0.55,
        'confidence': 0.69,
        'signal': 'NEUTRAL'
    }
    
    signal = generate_signal(technical, onchain, macro)
    print(json.dumps(signal, indent=2))
    sys.exit(0)