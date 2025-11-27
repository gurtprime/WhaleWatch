from web3 import Web3
from collections import defaultdict
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from src.config import RPC_URL, CONDITIONAL_TOKENS_ADDRESS, CONTRACT_ABI

def find_active_whales(blocks_to_scan=50):
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    contract = w3.eth.contract(address=CONDITIONAL_TOKENS_ADDRESS, abi=CONTRACT_ABI)
    
    latest_block = w3.eth.block_number
    start_block = latest_block - blocks_to_scan
    
    print(f"Scanning last {blocks_to_scan} blocks for whales...")
    
    # Fetch all TransferSingle events (no address filter)
    # Note: This might be heavy.
    try:
        events = contract.events.TransferSingle.get_logs(
            from_block=start_block,
            to_block=latest_block
        )
        
        volume_by_trader = defaultdict(int)
        
        for event in events:
            trader = event['args']['to']
            value = event['args']['value']
            volume_by_trader[trader] += value
            
        # Sort by volume
        sorted_traders = sorted(volume_by_trader.items(), key=lambda x: x[1], reverse=True)
        
        print("\n--- Top Active Traders (by Volume) ---")
        for i, (trader, volume) in enumerate(sorted_traders[:10]):
            # Volume is in atomic units. Assuming 1e6 for USDC.
            readable_vol = volume / 1_000_000
            print(f"{i+1}. {trader}: {readable_vol:,.2f} shares")
            
        print("\nCopy these addresses to src/config.py WATCHLIST if desired.")
        
    except Exception as e:
        print(f"Error scanning for whales: {e}")

if __name__ == "__main__":
    find_active_whales()

