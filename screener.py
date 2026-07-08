import os
import json
import yfinance as yf
import pandas as pd

# Expanded stock pool with hardcoded Market Cap and Sector metadata
STOCK_POOL = [
    # ---- LARGE CAP ----
    {"ticker": "RELIANCE.NS", "cap": "Large", "sector": "Energy"},
    {"ticker": "TCS.NS", "cap": "Large", "sector": "IT"},
    {"ticker": "HDFCBANK.NS", "cap": "Large", "sector": "Banking & Finance"},
    {"ticker": "ITC.NS", "cap": "Large", "sector": "FMCG"},
    {"ticker": "LT.NS", "cap": "Large", "sector": "Capital Goods"},
    {"ticker": "TATAMOTORS.NS", "cap": "Large", "sector": "Automobile"},
    
    # ---- MID CAP ----
    {"ticker": "KPITTECH.NS", "cap": "Mid", "sector": "IT"},
    {"ticker": "TATACHEMICALS.NS", "cap": "Mid", "sector": "Chemicals"},
    {"ticker": "VOLTAS.NS", "cap": "Mid", "sector": "Consumer Durables"},
    {"ticker": "BHARATFORG.NS", "cap": "Mid", "sector": "Capital Goods"},
    {"ticker": "FEDERALBANK.NS", "cap": "Mid", "sector": "Banking & Finance"},
    {"ticker": "MRF.NS", "cap": "Mid", "sector": "Automobile"},

    # ---- SMALL CAP ----
    {"ticker": "CDSL.NS", "cap": "Small", "sector": "Capital Markets"},
    {"ticker": "ANGELONE.NS", "cap": "Small", "sector": "Capital Markets"},
    {"ticker": "CYIENT.NS", "cap": "Small", "sector": "IT"},
    {"ticker": "CEATLTD.NS", "cap": "Small", "sector": "Automobile"},
    {"ticker": "CENTURYPLY.NS", "cap": "Small", "sector": "Materials"},
    {"ticker": "HFCL.NS", "cap": "Small", "sector": "Telecom"}
]

def analyze_stocks():
    results = []
    print("Fetching updated market data...")
    
    for item in STOCK_POOL:
        ticker = item["ticker"]
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            
            if len(hist) < 5:
                continue
                
            current_price = hist['Close'].iloc[-1]
            price_1w_ago = hist['Close'].iloc[-5]
            
            weekly_return = ((current_price - price_1w_ago) / price_1w_ago) * 100
            score = round(weekly_return * 10, 1) 
            
            results.append({
                "ticker": ticker.replace(".NS", ""),
                "price": round(current_price, 2),
                "weekly_change": round(weekly_return, 2),
                "score": score,
                "cap": item["cap"],
                "sector": item["sector"]
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            
    # Sort everything by highest momentum score
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Analysis finished successfully!")

if __name__ == "__main__":
    analyze_stocks()
