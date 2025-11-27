import time
from src.ingestion.blockchain import get_latest_block, monitor_trades
from src.analysis.engine import analyze_trades
from src.ingestion.gamma import get_market_from_token_id

def main():
    print("Starting WhaleWatch System...")
    
    # Start from a few blocks back to catch immediate recent activity for testing
    current_block = get_latest_block()
    start_block = current_block - 20 
    
    print(f"Current Block: {current_block}. Scanning from {start_block}...")

    while True:
        try:
            latest_block = get_latest_block()
            
            if latest_block > start_block:
                trades = monitor_trades(start_block, latest_block)
                
                if trades:
                    print(f"Found {len(trades)} trades from watched wallets.")
                    signals = analyze_trades(trades)
                    
                    if signals:
                        print("\n--- SIGNALS DETECTED ---")
                        for signal in signals:
                            print(f"[{signal['type']}] {signal['description']}")
                            # Try to resolve market info
                            if 'token_id' in signal:
                                # TODO: Implement actual market resolution
                                pass
                        print("------------------------\n")
                
                start_block = latest_block + 1
            
            time.sleep(10) # Poll every 10 seconds
            
        except KeyboardInterrupt:
            print("Stopping...")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()

