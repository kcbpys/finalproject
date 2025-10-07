from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

"""
A stock application/chrome extension that fetches stock data using yfinance (as yf), and FastAPI. 
"""
app = FastAPI()

# Add CORS middleware to allow Chrome extension requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stock/{ticker}")
async def get_stock_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        company_name = info.get("longName", "N/A")

        if info.get("previousClose") is not None:
            previous_close = info.get("previousClose")
        else:
            previous_close = "N/A"

        # Extract prices
        regular_market_price = (
            info.get("currentPrice")
            or info.get("navPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
            or "N/A"
        )
        # Calculate daily change percentage
        if regular_market_price != "N/A" and previous_close != "N/A":
            daily_change_percent = round(
                ((regular_market_price - previous_close) / previous_close) * 100, 2
            )
        else:
            daily_change_percent = "N/A"

        # Handle market cap
        raw_market_cap = info.get("marketCap", None)
        if raw_market_cap is not None:
            if raw_market_cap >= 1e12:
                market_cap = str(round(raw_market_cap / 1e12, 2)) + "T - Mega Cap"
            elif raw_market_cap >= 1e9:
                market_cap = str(round(raw_market_cap / 1e9, 2)) + "B - Large Cap"
            elif raw_market_cap >= 1e6:
                market_cap = str(round(raw_market_cap / 1e6, 2)) + "M - Small Cap"
            elif raw_market_cap >= 1e4:
                market_cap = str(raw_market_cap) + " - Nano Cap"
            else:
                market_cap = "N/A"
        else:
            market_cap = "N/A"

        prev_close = info.get("previousClose")
        current_price = info.get("currentPrice")
        if current_price is not None and prev_close is not None:
            day_change = current_price - prev_close
            if day_change > 0:
                day_change = "+" + str(round(day_change, 2))
            else:
                day_change = str(round(day_change, 2))
        else:
            day_change = "N/A"

        if info.get("fiftyTwoWeekLow") is not None:
            year_low = info.get("fiftyTwoWeekLow")
        else:
            year_low = "N/A"

        if info.get("fiftyTwoWeekHigh") is not None:
            year_high = info.get("fiftyTwoWeekHigh")
        else:
            year_high = "N/A"

        if info.get("trailingPE") is not None:
            pe_trailing = str(round(info.get("trailingPE"), 2))
        else:
            pe_trailing = "N/A"
        pe_forward = info.get("forwardPE")
        if pe_forward is not None and pe_forward >= 0:
            pe_forward = str(round(pe_forward, 2))
        else:
            pe_forward = "N/A"
        pe_total = pe_trailing + " / " + pe_forward

        if info.get("volume") is not None:
            volume = info.get("volume")
            if volume > 1e9:
                volume = str(round(volume / 1e9, 2)) + "B"
            elif 1e6 <= volume < 1e9:
                volume = str(round(volume / 1e6, 2)) + "M"
            elif 1e3 <= volume < 1e6:
                volume = str(round(volume / 1e3, 2)) + "K"
            else:
                volume = str(volume)
        else:
            volume = "N/A"

        if info.get("averageVolume") is not None:
            avg_volume = info.get("averageVolume")
            if avg_volume > 1e9:
                avg_volume = str(round(avg_volume / 1e9, 2)) + "B"
            elif 1e6 <= avg_volume < 1e9:
                avg_volume = str(round(avg_volume / 1e6, 2)) + "M"
            elif 1e3 <= avg_volume < 1e6:
                avg_volume = str(round(avg_volume / 1e3, 2)) + "K"
            else:
                avg_volume = str(avg_volume)
        else:
            avg_volume = "N/A"

        if info.get("beta") is not None:
            round_beta = info.get("beta")
        else:
            round_beta = "N/A"

        if volume != "N/A" and avg_volume != "N/A":
            all_volume = volume + " / " + avg_volume
        else:
            all_volume = "N/A"

        if day_change == "N/A":
            daily_change_percent = "Intraday price not available"
            day_change = ""

        data = {
            "company_name": company_name,
            "price": (
                "{:.2f}".format(regular_market_price) if regular_market_price != "N/A" else "N/A"
            ),
            "daily_change_amount": day_change,
            "daily_change_percent": (
                "{:.2f}".format(daily_change_percent) if daily_change_percent != "N/A" else "N/A"
            ),
            "market_cap": market_cap,
            "volume": all_volume,
            "pe_ratio_total": pe_total,
            "beta": (
                "{:.2f}".format(round_beta)
                if isinstance(round_beta, (int, float))
                else "N/A"
            ),
            "year_low": "{:.2f}".format(year_low) if year_low != "N/A" else "N/A",
            "year_high": "{:.2f}".format(year_high) if year_high != "N/A" else "N/A",
        }
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to fetch stock data: {str(e)}"}, status_code=400)