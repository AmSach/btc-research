"""
BTC Max Profit Engine - Configuration
"""

# Agent weights for signal generation
AGENT_WEIGHTS = {
    'technical': 0.35,
    'onchain': 0.40,
    'macro': 0.25
}

# Signal thresholds
SIGNAL_THRESHOLDS = {
    'strong_buy': 0.75,
    'buy': 0.60,
    'neutral': 0.45,
    'sell': 0.30
}

# Market context (updated from research)
MARKET_CONTEXT = {
    'current_price': 76099,
    'ath': 125835,
    'down_from_ath_pct': -40.8,
    'key_support': 68900,
    'key_resistance': 75000,
    'rsi_14': 54,
    'ema_200': 82919,
    'btc_spx_correlation_30d': 0.74,
    'dxy': 98.7,
    'mvrv': 1.5,
    'realized_price_floor': 50000,
    'realized_price_ceiling': 62000,
    'exchange_reserves_pct': 11.9,
    'etf_flows_q1_2026_billions': 2.5
}

# Timing (UTC)
RUN_HOUR = 6  # 6 AM UTC = ~11:30 AM IST
RUN_MINUTE = 0

# Alert preferences
ALERT_METHOD = 'email'  # email or telegram
ALERT_EMAIL = 'i.amsachfr@gmail.com'