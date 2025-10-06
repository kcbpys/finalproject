// Fetch and display stock data
async function fetchStockData() {
    const ticker = document.getElementById("ticker").value.trim();
    const resultsDiv = document.getElementById("results");
    const fetchButton = document.getElementById("fetchData");

    if (!ticker) {
        resultsDiv.innerHTML = "Please enter a stock ticker.";
        return;
    }
    if (!/^[A-Za-z0-9-.]+$/.test(ticker)) {
        resultsDiv.innerHTML = "Invalid ticker format. Use letters, numbers, or hyphens.";
        return;
    }

    resultsDiv.innerHTML = "Loading...";
    fetchButton.disabled = true;

    try {
        const response = await fetch(`https://your-app.onrender.com/stock/${ticker}`);
        if (!response.ok) {
            throw new Error("Ticker not found or server error");
        }
        const data = await response.json();
        if (data.error) {
            resultsDiv.innerHTML = `Error: ${data.error}`;
        } else {
            // Determine color based on daily change percentage
            let priceColor = "black"; // Default color
            if (data.daily_change_percent !== "N/A" && !isNaN(data.daily_change_percent)) {
                priceColor = data.daily_change_percent > 0 ? "green" : "red";
            }
            // Display data
            resultsDiv.innerHTML = `
                <b style="text-align: center;"><u>${data.company_name || "N/A"}</u></b>
                <p><strong>Price:</strong> <span style="color:${priceColor};">$${data.price || "N/A"}</span></p>
                <p><strong>Daily Change:</strong> ${data.daily_change_amount || "N/A"} (${data.daily_change_percent || "N/A"}%)</p>
                <p><strong>Market Cap:</strong> ${data.market_cap || "N/A"}</p>
                <p><strong>Vol/Avg:</strong> ${data.volume || "N/A"}</p>
                <p><strong>52 Week High:</strong> ${data.year_high || "N/A"}</p>
                <p><strong>52 Week Low:</strong> ${data.year_low || "N/A"}</p> 
                <p><strong>PE Ratio (TTM/FTM):</strong> ${data.pe_ratio_total || "N/A"}</p>
                <p><strong>Beta(5Y):</strong> ${data.beta || "N/A"}</p>
            `;
        }
    } catch (err) {
        resultsDiv.innerHTML = `Error: ${err.message}`;
    } finally {
        fetchButton.disabled = false;
    }
}

// Event listener for the "Get Data" button
document.getElementById("fetchData").addEventListener("click", () => {
    fetchStockData();
});

// Event listener for pressing Enter in the input field
document.getElementById("ticker").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        fetchStockData();
    }
});