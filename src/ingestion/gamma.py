import requests
from src.config import GAMMA_API_URL

def get_market_from_token_id(token_id: str):
    """
    Fetch market details using the Token ID.
    Note: Gamma API doesn't have a direct 'get by token id' endpoint easily accessible 
    without querying markets and filtering, or using the CLOB.
    However, we can try to find the market that contains this token ID.
    """
    # This is inefficient if we query all markets. 
    # A better way is to cache markets or use the CLOB API if possible.
    # For MVP, we might just print the Token ID.
    
    # Let's try to use the CLOB endpoint which accepts asset_id (token_id)
    # But previous test showed it needs API key or failed.
    
    # Let's try filtering markets by query param?
    try:
        # We can try to guess the market slug or id if we had a map.
        # For now, return None if we can't easily resolve it without scraping.
        return None
    except Exception as e:
        print(f"Error fetching market for token {token_id}: {e}")
        return None

def get_market_by_id(market_id: str):
    url = f"{GAMMA_API_URL}/markets/{market_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None

