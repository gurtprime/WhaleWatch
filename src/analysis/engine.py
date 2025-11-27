from collections import defaultdict

def analyze_trades(trades):
    """
    Analyzes a list of trades for signals.
    """
    signals = []
    
    # Group by Token ID
    token_activity = defaultdict(list)
    
    for trade in trades:
        token_activity[trade['token_id']].append(trade)
        
        # Check for Super Whale (Single large trade)
        # Assuming 6 decimals for USDC-collateralized outcomes, but shares are atomic units?
        # Usually Polymarket shares are 1e6 based if collateral is USDC (6 decimals).
        # Let's assume threshold is 5000 shares (5000 * 1e6 if strictly atomic, but let's just look at raw value)
        # Actually, value is the raw integer amount.
        # If I buy 10 YES shares, value is 10 * 10^6? Or just 10?
        # It's usually matched to collateral decimals. USDC is 6. 
        # So 1 share = 1,000,000 units.
        # A whale bet of 5000 shares = 5,000,000,000 units.
        
        amount = trade['amount']
        # Threshold: 10,000 shares = 10,000 * 1,000,000 = 10^10
        THRESHOLD = 10_000 * 1_000_000 
        
        if amount >= THRESHOLD:
             signals.append({
                 "type": "SUPER_WHALE",
                 "description": f"Whale {trade['trader']} bought {amount / 1_000_000} shares of Token {trade['token_id']}",
                 "trade": trade
             })

    # Check for Convergence (Multiple Whales on same Token)
    for token_id, trade_list in token_activity.items():
        traders = set(t['trader'] for t in trade_list)
        if len(traders) > 1:
            signals.append({
                "type": "CONVERGENCE",
                "description": f"Multiple Top Traders ({len(traders)}) converging on Token {token_id}",
                "traders": list(traders),
                "token_id": token_id
            })
            
    return signals

