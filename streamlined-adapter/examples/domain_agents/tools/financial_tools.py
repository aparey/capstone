########################################################
# Financial Tools for MCP Integration
# ========================================
# Tools that Claude can use to fetch and analyze stock data.
########################################################

import yfinance as yf
from datetime import datetime
from typing import Dict, Any, List

def get_stock_info(ticker: str, period: str = "3mo") -> Dict[str, Any]:
    """
    Get comprehensive stock information for a single ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)
        period: Time period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
    
    Returns:
        Dictionary containing current price, historical data, and key metrics
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        
        if hist.empty:
            return {"error": f"No data available for {ticker}"}
        
        current_price = hist['Close'].iloc[-1]
        price_change = ((current_price - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
        
        return {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "price_change_pct": round(price_change, 2),
            "period": period,
            "avg_volume": int(hist['Volume'].mean()),
            "company_name": info.get('longName', ticker),
            "sector": info.get('sector', 'N/A'),
            "market_cap": info.get('marketCap', 'N/A'),
            "pe_ratio": info.get('trailingPE', 'N/A'),
            "52_week_high": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52_week_low": info.get('fiftyTwoWeekLow', 'N/A'),
            "dividend_yield": info.get('dividendYield', 0),
            "recommendation": info.get('recommendationKey', 'N/A'),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}


def get_historical_prices(ticker: str, start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Get historical stock prices for a specific date range.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        Dictionary with historical price data
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.download(start=start_date, end=end_date)
        
        if hist.empty:
            return {"error": f"No historical data for {ticker} between {start_date} and {end_date}"}
        
        return {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "data_points": len(hist),
            "open_price": round(hist['Open'].iloc[0], 2),
            "close_price": round(hist['Close'].iloc[-1], 2),
            "high": round(hist['High'].max(), 2),
            "low": round(hist['Low'].min(), 2),
            "avg_volume": int(hist['Volume'].mean()),
            "price_change_pct": round(((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100, 2)
        }
    except Exception as e:
        return {"error": f"Failed to fetch historical data: {str(e)}"}


def compare_stocks(tickers: List[str], period: str = "3mo") -> Dict[str, Any]:
    """
    Compare multiple stocks side by side.
    
    Args:
        tickers: List of stock ticker symbols
        period: Time period for comparison
    
    Returns:
        Dictionary with comparative analysis data
    """
    try:
        comparison = {
            "period": period,
            "stocks": {},
            "timestamp": datetime.now().isoformat()
        }
        
        for ticker in tickers:
            stock_data = get_stock_info(ticker, period)
            if "error" not in stock_data:
                comparison["stocks"][ticker] = stock_data
        
        return comparison
    except Exception as e:
        return {"error": f"Failed to compare stocks: {str(e)}"}


# MCP Tool Definitions for Claude
FINANCIAL_TOOLS = [
    {
        "name": "get_stock_info",
        "description": "Get comprehensive current stock information including price, volume, market cap, P/E ratio, and key metrics for a single stock ticker.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol (e.g., AAPL for Apple, GOOGL for Google, MSFT for Microsoft)"
                },
                "period": {
                    "type": "string",
                    "description": "Time period for historical data analysis. Options: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max. Default is 3mo.",
                    "default": "3mo"
                }
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "get_historical_prices",
        "description": "Get detailed historical stock prices for a specific date range. Useful for analyzing trends over custom time periods.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Stock ticker symbol"
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date in YYYY-MM-DD format (e.g., 2024-01-01)"
                },
                "end_date": {
                    "type": "string",
                    "description": "End date in YYYY-MM-DD format (e.g., 2024-12-31)"
                }
            },
            "required": ["ticker", "start_date", "end_date"]
        }
    },
    {
        "name": "compare_stocks",
        "description": "Compare multiple stocks side-by-side to identify relative performance, best opportunities, and risk profiles.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tickers": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of stock ticker symbols to compare (e.g., ['AAPL', 'MSFT', 'GOOGL'])"
                },
                "period": {
                    "type": "string",
                    "description": "Time period for comparison. Options: 1mo, 3mo, 6mo, 1y, etc. Default is 3mo.",
                    "default": "3mo"
                }
            },
            "required": ["tickers"]
        }
    }
]