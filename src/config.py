import os
from dotenv import load_dotenv

load_dotenv()

# Polygon RPC URL (Public)
RPC_URL = os.getenv("RPC_URL", "https://polygon-rpc.com")

# Gnosis Conditional Tokens Contract on Polygon
CONDITIONAL_TOKENS_ADDRESS = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"

# Gamma API Base URL
GAMMA_API_URL = "https://gamma-api.polymarket.com"

# List of addresses to watch (Whales)
WATCHLIST = [
    "0x8BD6C3D7a57D650A1870dd338234f90051fe9918", # Market Maker
    "0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E", # Active Whale 1
    "0x9B3dcD99eec7fE11602e6534e6302c0f318D7422", # Active Whale 2
    "0x92672c80D36dcd08172Aa1E51dFAce0F20b70F9A", # Active Whale 3
    "0xC5d563A36AE78145C45a50134d48A1215220f80a",
    "0xf68A281980f8c13828e84e147e3822381d6e5B1B",
    "0xee613B3FC183ee44F9Da9c05F53e2Da107E3DeBf"
]

# ABI for TransferSingle event
TRANSFER_SINGLE_ABI = {
    "anonymous": False,
    "inputs": [
        {"indexed": True, "internalType": "address", "name": "operator", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
        {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
        {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
        {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}
    ],
    "name": "TransferSingle",
    "type": "event"
}

# Full Minimal ABI for Contract Event Listening
CONTRACT_ABI = [
    TRANSFER_SINGLE_ABI
]
