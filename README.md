# Automated_Daily_Crypto_Report

This Python application automatically fetches cryptocurrency data from the **CoinGecko API**, processes it to find the **top 10 best-performing** and **top 10 worst-performing** Crypto Currency, and sends the results by email every day at **8:00 AM**.  

The project saves the full dataset to CSV for historical tracking.

---

##  Features  

-  Fetches **real-time cryptocurrency data** from [CoinGecko](https://www.coingecko.com/) 

-  Identifies: 
    **Top 10 cryptos with highest 24h increase (positive movers)**  
    - **Top 10 cryptos with highest 24h decrease (negative movers)**  
    -  Saves **all data** (250 cryptos) as CSV file with timestamps  
    -  Sends a **daily email report** with:  
    -  CSV file attachment for full dataset  
    -  **Scheduled automation** at 8:00 AM every day using the `schedule` library  

---

##  Tech Stack  

- **Python** 
- **Libraries Used**:
  - `requests` → to fetch data from CoinGecko  
  - `pandas` → to clean & process data  
  - `smtplib`, `email.mime` → to send emails  
  - `schedule` → to run script at 8:00 AM daily  
  - `time`, `datetime` → timestamping & scheduling  

---

## How It Works

1. The script sends a request to the CoinGecko API to get the latest cryptocurrency data.
2. Data is converted into a Pandas DataFrame and relevant columns are selected.
3. Top 10 gainers and losers are identified based on the 24-hour price change percentage.
4. CSV files are saved locally:
   - `crypto_price_<timestamp>.csv` – full dataset
   - `crypto_price_positive_top10_<timestamp>.csv`
   - `crypto_price_negative_top10_<timestamp>.csv` 
5. Email is sent to configured recipients with the CSV report attached.
6. **Automation:** The script can run daily using **Windows Task Scheduler**.

 **Important Requirement: ** Computer must be running at the scheduled time** (e.g., 8:00 AM) for the script to execute automatically.
