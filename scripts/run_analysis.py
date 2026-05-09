#!/usr/bin/env python3
"""
BTC Max Profit Engine - Main Analysis Runner
Runs all agents in parallel and generates final signal
"""

import json
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.technical_agent import analyze as technical_analyze
from agents.onchain_agent import analyze as onchain_analyze
from agents.macro_agent import analyze as macro_analyze
from scripts.signal_generator import generate_signal, save_signal

def run_analysis():
    """Run all agents and generate final signal"""
    
    print("=" * 60)
    print("BTC MAX PROFIT ENGINE - Analysis Run")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print("=" * 60)
    
    # Run all agents
    print("\n[1/4] Running Technical Analysis Agent...")
    technical = technical_analyze()
    print(f"  Signal: {technical['signal']} | Score: {technical['score']} | Conf: {technical['confidence']}")
    
    print("\n[2/4] Running On-Chain Analyst Agent...")
    onchain = onchain_analyze()
    print(f"  Signal: {onchain['signal']} | Score: {onchain['score']} | Conf: {onchain['confidence']}")
    
    print("\n[3/4] Running Macro Strategist Agent...")
    macro = macro_analyze()
    print(f"  Signal: {macro['signal']} | Score: {macro['score']} | Conf: {macro['confidence']}")
    
    print("\n[4/4] Generating Combined Signal...")
    signal = generate_signal(technical, onchain, macro)
    
    # Display results
    print("\n" + "=" * 60)
    print("FINAL SIGNAL")
    print("=" * 60)
    print(f"Signal Type: {signal['signal_type']}")
    print(f"Total Score: {signal['total_score']}")
    print(f"Confidence:  {signal['confidence']}")
    print(f"Action:      {signal['action']}")
    print(f"Price:       ${signal['current_price']:,}")
    
    print("\nAgent Scores:")
    for agent, score in signal['agent_scores'].items():
        weight = {'technical': 0.35, 'onchain': 0.40, 'macro': 0.25}[agent]
        print(f"  {agent.capitalize():12} {score:.3f} (weight: {weight})")
    
    print("\nKey Drivers:")
    for driver in signal['key_drivers']:
        print(f"  • {driver}")
    
    print("\nRisk Factors:")
    for risk in signal['risk_factors']:
        print(f"  • {risk}")
    
    print("\nKey Levels:")
    for level, value in signal['levels'].items():
        print(f"  {level.capitalize():12} ${value:,}")
    
    # Save signal
    save_signal(signal)
    print(f"\nSignal saved to signals/daily_signals.json")
    
    # Also save agent results
    results = {
        'timestamp': signal['timestamp'],
        'technical': technical,
        'onchain': onchain,
        'macro': macro,
        'final_signal': signal
    }
    
    with open('signals/detailed_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return signal

if __name__ == '__main__':
    signal = run_analysis()
    sys.exit(0)