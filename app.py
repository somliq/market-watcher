import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Configuration (The "UI" polish)
st.set_page_config(page_title="Market Watcher", page_icon="📈")

st.title("📈 Real-Time Market Watcher")

# 2. Input: Let the user choose the stock (Interactivity!)
# We default to 'AAPL' (Apple), but the user can type any ticker.
ticker = st.text_input("Enter Stock Ticker:", "AAPL")

# 3. Fetch Data (The "Backend" Logic)
# We use a try/except block to handle invalid tickers so the app doesn't crash.
try:
    st.write(f"Fetching data for: **{ticker}**")
    
    # Download 6 months of data
    stock_data = yf.download(ticker, period="6mo")
    
    # Check if data is empty (Invalid ticker)
    if stock_data.empty:
        st.error("No data found. Check the ticker symbol.")
    else:
        # 4. Visualization
        # We only care about the 'Close' price for the line chart
        st.line_chart(stock_data['Close'])

        # 5. Raw Data (For the "nerds" who want numbers)
        with st.expander("See Raw Data"):
            st.dataframe(stock_data.tail())

except Exception as e:
    st.error(f"An error occurred: {e}")

st.caption("Data provided by Yahoo Finance API")