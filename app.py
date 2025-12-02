import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Market Watcher", page_icon="📈")
st.title("📈 Real-Time Market Watcher")

# 2. Input
ticker = st.text_input("Enter Stock Ticker:", "AAPL")

# --- CACHING MECHANISM (The Rate Limit Fix) ---
# This function will only run ONCE every hour for the same ticker.
# If the user clicks a button, it grabs the data from memory, NOT Yahoo.
@st.cache_data(ttl=3600) 
def fetch_stock_data(symbol):
    # Added auto_adjust=True to fix the warning you saw
    data = yf.download(symbol, period="6mo", auto_adjust=True)
    
    # Flatten MultiIndex if necessary
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    return data
# ---------------------------------------------

# 3. Fetch Data
try:
    st.write(f"Fetching data for: **{ticker}**")
    
    # CALL THE CACHED FUNCTION INSTEAD OF DIRECT DOWNLOAD
    stock_data = fetch_stock_data(ticker)

    # Check if data is empty
    if stock_data.empty:
        st.error("No data found. Check the ticker symbol.")
    else:
        # --- CALCULATIONS ---
        stock_data['50-Day SMA'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['20-Day SMA'] = stock_data['Close'].rolling(window=20).mean()

        # --- USER CONTROLS ---
        col1, col2 = st.columns(2)
        with col1:
            show_sma_50 = st.checkbox("Show 50-Day SMA")
        with col2:
            show_sma_20 = st.checkbox("Show 20-Day SMA")

        # --- PLOTTING LOGIC ---
        columns_to_show = ['Close']
        
        if show_sma_50:
            columns_to_show.append('50-Day SMA')
            
        if show_sma_20:
            columns_to_show.append('20-Day SMA')

        st.line_chart(stock_data[columns_to_show])

        with st.expander("See Raw Data"):
            st.dataframe(stock_data.tail())

except Exception as e:
    # If we get rate limited, show a friendly message
    if "Too Many Requests" in str(e):
        st.warning("Yahoo Finance is busy (Rate Limit). Please wait 1 minute and hit Rerun.")
    else:
        st.error(f"An error occurred: {e}")

st.caption("Data provided by Yahoo Finance API")