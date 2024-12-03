from fastapi import FastAPI
from fastapi.responses import JSONResponse
import yfinance as yf
app = FastAPI()

@app.get("/stock/{ticker}")
async def get_stock_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        company_name = info.get('longName')
        previous_close = info.get("previousClose")

        # Extract prices

        regular_market_price = (
        info.get("currentPrice")
        or info.get("regularMarketPrice")
        or info.get("previousClose")
        or "N/A"  # Default fallback
)

        # Calculate daily change percentage
        if regular_market_price and previous_close:
            daily_change_percent = round(((regular_market_price - previous_close) / previous_close) * 100, 2)
        else:
            daily_change_percent = "N/A"

        ndaily_change_percent = daily_change_percent
        ndaily_change_percent = int(ndaily_change_percent)
        ndaily_change_percent = daily_change_percent * 1000 # ndaily_change_percent is used here as an indicator, or form of dummy variable - inflated this to 1k as the JS front-end would only change the color if the percent change was >1%, for whatever reason, so implemented the * 1000 to inflate this backend metric to check if the number is negative or not. 
        daily_change_percent = (round(daily_change_percent, 2))
      
        if daily_change_percent >= 0:
            daily_change_percent = " or +" + str(daily_change_percent)
        else:
            daily_change_percent = " or " + str(daily_change_percent) 

        market_cap = 0
        # Handle market cap when it is None
        raw_market_cap = info.get("marketCap")
        if raw_market_cap is None:
            market_cap = "N/A"
        else:
            if raw_market_cap >= 1e12:
                market_cap = str(round(raw_market_cap / 1e12, 2)) + "T - Mega Cap"
            elif raw_market_cap >= 1e9:
                market_cap = str(round(raw_market_cap / 1e9, 2)) + "B - Large Cap"
            elif raw_market_cap >= 1e6:
                market_cap = str(round(raw_market_cap / 1e6, 2)) + "M - Small Cap"
            else:
                market_cap = str(raw_market_cap) + " - Nano Cap"

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

        year_low = info.get("fiftyTwoWeekLow")
        nyear_low = str(round(year_low, 2)) if year_low is not None else "N/A"

        year_high = info.get("fiftyTwoWeekHigh")
        nyear_high = str(round(year_high, 2)) if year_low is not None else "N/A"


        cprice = str(round(current_price, 2))
        volume = info.get("volume")
        avg_volume = info.get("averageVolume")
        combined = str(day_change) + daily_change_percent
        pe_trailing = info.get("trailingPE")
        if pe_trailing is not None:
            pe_trailing = str(round(pe_trailing, 2))
        else:
            pe_trailing = "N/A - not profitable"
        pe_forward = info.get("forwardPE")
        if pe_forward is not None:
            pe_forward = str(round(pe_forward, 2))
        else:
            pe_forward = "N/A"
        pe_total = pe_trailing + " / " + pe_forward

        if volume is not None:
            if volume > 1e9:  # Greater than 1 billion
                volume = str(round(volume / 1e9, 2)) + "B"
            elif 1e6 <= volume < 1e9:  # Between 1 million and 1 billion
                volume = str(round(volume / 1e6, 2)) + "M"
            elif 1e3 <= volume < 1e6:  # Between 1 thousand and 1 million
                volume = str(round(volume / 1e3, 2)) + "K"
            else:  # Below 1 thousand
                volume = str(volume)
        else:
            volume = "N/A"
        
        if avg_volume is not None:
            if avg_volume > 1e9:  # Greater than 1 billion
                avg_volume = str(round(avg_volume / 1e9, 2)) + "B"
            elif 1e6 <= avg_volume < 1e9:  # Between 1 million and 1 billion
                avg_volume = str(round(avg_volume / 1e6, 2)) + "M"
            elif 1e3 <= avg_volume < 1e6:  # Between 1 thousand and 1 million
                avg_volume = str(round(avg_volume / 1e3, 2)) + "K"
            else:  # Below 1 thousand
                avg_volume = str(avg_volume)
        else:
            avg_volume = "N/A"
        round_beta = info.get("beta")
        nround_beta = str(round(round_beta, 2)) if round_beta is not None else "N/A"

        if volume != "N/A" and avg_volume != "N/A":
            all_volume = volume + " / " + avg_volume
        else:
            all_volume = "N/A"

    
            # Fetch 5-day historical data
        # history = stock.history(period="5d")  # Last 5 days
        # history_data = history[['Close']].reset_index()
        # history_data = history_data.to_dict(orient="records")
        # Prepare response data
        data = {
            "company_name": company_name,
            "price": "{:.2f}".format(regular_market_price) if regular_market_price else "N/A",
            "daily_change": (day_change + daily_change_percent),
            "market_cap": market_cap,
            "volume": all_volume,
            "pe_ratio_total": pe_total,
            "beta": "{:.2f}".format(round_beta) if round_beta is not None else "N/A",
            "year_low": "{:.2f}".format(year_low) if year_low is not None else "N/A",
            "year_high": "{:.2f}".format(year_high) if year_high is not None else "N/A",
            "ndaily_change_percent": "{:.2f}".format(ndaily_change_percent) if ndaily_change_percent is not None else "N/A",
}
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)




