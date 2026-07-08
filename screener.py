import os
import json
import yfinance as yf
import pandas as pd

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
    print("Downloading 5-year historical sequences...")
    
    for item in STOCK_POOL:
        ticker = item["ticker"]
        try:
            stock = yf.Ticker(ticker)
            # Pull 5 years of daily intervals
            hist = stock.history(period="5y")
            
            if len(hist) < 2:
                continue
                
            current_price = hist['Close'].iloc[-1]
            
            # Helper function to extract returns safely based on estimated trading days
            # 1D=Previous day, 1W=5 days ago, 1M=21 days ago, 1Y=252 days ago, etc.
            def get_return(trading_days_lookback):
                if len(hist) >= trading_days_lookback:
                    past_price = hist['Close'].iloc[-trading_days_lookback]
                    return round(((current_price - past_price) / past_price) * 100, 2)
                else:
                    # Fallback to the oldest available price if stock listing is younger than lookback
                    first_price = hist['Close'].iloc[0]
                    return round(((current_price - first_price) / first_price) * 100, 2)

            results.append({
                "ticker": ticker.replace(".NS", ""),
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
