import os
import json
import yfinance as yf
import pandas as pd

STOCK_POOL = [
    # ---- LARGE CAP ----
    {"ticker": "RELIANCE.NS", "name": "Reliance Industries Ltd.", "cap": "Large", "sector": "Energy"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy Services Ltd.", "cap": "Large", "sector": "IT"},
    {"ticker": "HDFCBANK.NS", "name": "HDFC Bank Ltd.", "cap": "Large", "sector": "Banking & Finance"},
    {"ticker": "ITC.NS", "name": "ITC Ltd.", "cap": "Large", "sector": "FMCG"},
    {"ticker": "LT.NS", "name": "Larsen & Toubro Ltd.", "cap": "Large", "sector": "Capital Goods"},
    {"ticker": "TATAMOTORS.NS", "name": "Tata Motors Ltd.", "cap": "Large", "sector": "Automobile"},
    
    # ---- MID CAP ----
    {"ticker": "KPITTECH.NS", "name": "KPIT Technologies Ltd.", "cap": "Mid", "sector": "IT"},
    {"ticker": "TATACHEMICALS.NS", "name": "Tata Chemicals Ltd.", "cap": "Mid", "sector": "Chemicals"},
    {"ticker": "VOLTAS.NS", "name": "Voltas Ltd.", "cap": "Mid", "sector": "Consumer Durables"},
    {"ticker": "BHARATFORG.NS", "name": "Bharat Forge Ltd.", "cap": "Mid", "sector": "Capital Goods"},
    {"ticker": "FEDERALBANK.NS", "name": "The Federal Bank Ltd.", "cap": "Mid", "sector": "Banking & Finance"},
    {"ticker": "MRF.NS", "name": "MRF Ltd.", "cap": "Mid", "sector": "Automobile"},

    # ---- SMALL CAP ----
    {"ticker": "CDSL.NS", "name": "Central Depository Services (India) Ltd.", "cap": "Small", "sector": "Capital Markets"},
    {"ticker": "ANGELONE.NS", "name": "Angel One Ltd.", "cap": "Small", "sector": "Capital Markets"},
    {"ticker": "CYIENT.NS", "name": "Cyient Ltd.", "cap": "Small", "sector": "IT"},
    {"ticker": "CEATLTD.NS", "name": "CEAT Ltd.", "cap": "Small", "sector": "Automobile"},
    {"ticker": "CENTURYPLY.NS", "name": "Century Plyboards (India) Ltd.", "cap": "Small", "sector": "Materials"},
    {"ticker": "HFCL.NS", "name": "HFCL Ltd.", "cap": "Small", "sector": "Telecom"}
]

def analyze_stocks():
    results = []
    print("Downloading historical sequences...")
    
    for item in STOCK_POOL:
        ticker = item["ticker"]
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5y")
            
            if len(hist) < 2:
                continue
                
            current_price = hist['Close'].iloc[-1]
            
            def get_return(trading_days_lookback):
                if len(hist) >= trading_days_lookback:
                    past_price = hist['Close'].iloc[-trading_days_lookback]
                    return round(((current_price - past_price) / past_price) * 100, 2)
                else:
                    first_price = hist['Close'].iloc[0]
                    return round(((current_price - first_price) / first_price) * 100, 2)

            results.append({
                "ticker": ticker.replace(".NS", ""),
                "name": item["name"],
                "price": round(current_price, 2),
                "cap": item["cap"],
                "sector": item["sector"],
                "returns": {
                    "1D": get_return(2),
                    "1W": get_return(6),
                    "1M": get_return(22),
                    "1Y": get_return(253),
                    "2Y": get_return(505),
                    "3Y": get_return(758),
                    "4Y": get_return(1010),
                    "5Y": get_return(1262)
                }
            })
        except Exception as e:
            print(f"Failed handling {ticker}: {e}")
            
    os.makedirs("docs", exist_ok=True)
    with open("docs/data.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Multi-horizon processing completely exported.")

if __name__ == "__main__":
    analyze_stocks()
