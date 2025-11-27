from web3 import Web3
from src.config import RPC_URL, CONDITIONAL_TOKENS_ADDRESS, CONTRACT_ABI, WATCHLIST
import time

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONDITIONAL_TOKENS_ADDRESS, abi=CONTRACT_ABI)

def get_latest_block():
    return w3.eth.block_number

def monitor_trades(start_block, end_block=None):
    """
    Scans for TransferSingle events where 'to' is in the watchlist.
    """
    if end_block is None:
        end_block = w3.eth.block_number

    if start_block > end_block:
        return []

    print(f"Scanning blocks {start_block} to {end_block}...")
    
    trades = []
    
    # We can filter by 'to' address to find buys/receipts
    # TransferSingle(operator, from, to, id, value)
    try:
        # Create a filter for the range
        # Note: Some RPCs limit the block range (e.g. 2000 blocks)
        # We'll assume the caller handles small ranges.
        
        events = contract.events.TransferSingle.get_logs(
            from_block=start_block,
            to_block=end_block,
            argument_filters={'to': WATCHLIST}
        )
        
        for event in events:
            trades.append({
                'tx_hash': event['transactionHash'].hex(),
                'block': event['blockNumber'],
                'trader': event['args']['to'],
                'token_id': str(event['args']['id']),
                'amount': event['args']['value'],
                'operator': event['args']['operator'],
                'from': event['args']['from']
            })
            
    except Exception as e:
        print(f"Error scanning blocks: {e}")
        
    return trades

