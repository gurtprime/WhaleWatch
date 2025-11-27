# WhaleWatch: Polymarket Whale Detector

WhaleWatch is a real-time monitoring system that tracks "Top Traders" and "Whales" on prediction markets (specifically Polymarket on the Polygon blockchain). It analyzes their positions to detect high-confidence trades ("Sure Bets").

## How it Works

The system operates by directly connecting to the Polygon blockchain via an RPC node. It does not rely on slow or rate-limited web APIs for trade detection.

1.  **Data Ingestion (Live Blockchain Scanning)**: 
    *   The system monitors the **Gnosis Conditional Tokens** contract (used by Polymarket).
    *   It listens for `TransferSingle` events, which represent the movement of shares (buying/selling).
    *   It specifically filters for transactions involving wallet addresses in your **Watchlist** (`src/config.py`).

2.  **Analysis Engine**:
    *   It processes every trade found in the scanned blocks.
    *   It applies logic to detect significant patterns (Whale buys, multiple traders converging on the same outcome).

3.  **Signal Generator**:
    *   When a pattern matches, it outputs a signal to the console.

## Does it need to run 24/7?

**Yes.** The system is designed to be a live monitor. 

*   It polls the blockchain every 10 seconds for new blocks.
*   If you stop the script, it will stop monitoring. When you restart it, it currently defaults to scanning the last 20 blocks. Any activity that happened while the script was off (older than 20 blocks) will be missed unless you manually adjust the `start_block` in `main.py`.
*   For production use, you would run this on a server (VPS) using a process manager like `pm2` or `systemd`.

## How to Interpret Results

The system outputs two types of signals:

### 1. `[SUPER_WHALE]`
**Meaning:** A single trader on your watchlist has made a massive purchase.
*   **Threshold:** Currently set to >10,000 shares (configurable in `src/analysis/engine.py`).
*   **Interpretation:** This trader has high conviction in this specific outcome.

### 2. `[CONVERGENCE]`
**Meaning:** Multiple DIFFERENT traders on your watchlist have bought the exact same outcome token within the same scanning window.
*   **Interpretation:** This is a "Sure Bet" signal. When top traders independently move into the same position, it indicates strong market consensus among the "smart money."

## Setup & Usage

### 1. Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Find Whales (Optional)
If you don't know which addresses to watch, run the helper tool to find high-volume traders from recent blocks:
```bash
python3 src/utils/find_whales.py
```
Copy the interesting addresses (high volume) into `src/config.py`.

### 3. Run the Monitor
```bash
python3 main.py
```
Leave this running to receive real-time alerts.

## Configuration

Edit `src/config.py` to add/remove addresses:
```python
WATCHLIST = [
    "0x...", # Whale 1
    "0x...", # Whale 2
]
```
