import os
import json
import yfinance as yf
import pandas as pd

# Define a starter list of popular liquid Indian stocks (Nifty 50 tokens)
# yfinance requires '.NS' at the end for the National Stock Exchange (NSE)
TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "BHARTIARTL.NS", "SBIN.NS", "LTIM.NS", "ITC.NS", "TATAMOTORS.NS",
    "BAJAJFINSV.NS", "NTPC.NS", "SUNPHARMA.NS", "TITAN.NS", "MARUTI.NS"
]

def analyze_stocks():
    results = []
    
    print("Fetching stock data...")
    for ticker in TICKERS:
        try:
            # Fetch 1 month of daily data to calculate short term trends
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1mo")
            
            if len(hist) < 5:
                continue
                
            current_price = hist['Close'].iloc[-1]
            price_1w_ago = hist['Close'].iloc[-5] if len(hist) >= 5 else hist['Close'].iloc[0]
            
            # Short-term momentum: % change over the last week
            weekly_return = ((current_price - price_1w_ago) / price_1w_ago) * 100
            
            # Simple scoring algorithm (higher momentum = higher score)
            score = round(weekly_return * 10, 1) 
            
            results.append({
                "ticker": ticker.replace(".NS", ""),
                "price": round(current_price, 2),
                "weekly_change": round(weekly_return, 2),
                "score": score
            })
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            
    # Sort stocks by highest short-term momentum score
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    # Ensure the output directory exists
    os.makedirs("docs", exist_ok=True)
    
    # Save results as a JSON data file for our frontend web app
    with open("docs/data.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Screener completed successfully. Data saved to docs/data.json")

if __name__ == "__main__":
    analyze_stocks()
