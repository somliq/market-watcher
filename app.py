import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Market Watcher", page_icon="📈")
st.title("📈 Real-Time Market Watcher")

# 2. Input
ticker = st.text_input("Enter Stock Ticker:", "AAPL")

# 3. Fetch Data
try:
    st.write(f"Fetching data for: **{ticker}**")
    
    # Download 6 months of data
    stock_data = yf.download(ticker, period="6mo")
    
    # --- FIX: Flatten MultiIndex (The yfinance bug fix) ---
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)
    # ------------------------------------------------------

    # Check if data is empty
    if stock_data.empty:
        st.error("No data found. Check the ticker symbol.")
    else:
        # --- CALCULATIONS ---
        # Calculate 50-Day SMA
        stock_data['50-Day SMA'] = stock_data['Close'].rolling(window=50).mean()
        
        # Calculate 20-Day SMA (Extra Credit)
        stock_data['20-Day SMA'] = stock_data['Close'].rolling(window=20).mean()

        # --- USER CONTROLS ---
        col1, col2 = st.columns(2) # Make them sit side-by-side
        with col1:
            show_sma_50 = st.checkbox("Show 50-Day SMA")
        with col2:
            show_sma_20 = st.checkbox("Show 20-Day SMA")

        # --- PLOTTING LOGIC ---
        # Always start with the Close price
        columns_to_show = ['Close']
        
        # Add 50-Day if checked
        if show_sma_50:
            columns_to_show.append('50-Day SMA')
            
        # Add 20-Day if checked
        if show_sma_20:
            columns_to_show.append('20-Day SMA')

        # Draw ONE chart with all selected columns
        st.line_chart(stock_data[columns_to_show])

        # Raw Data Expander
        with st.expander("See Raw Data"):
            st.dataframe(stock_data.tail())

except Exception as e:
    st.error(f"An error occurred: {e}")

st.caption("Data provided by Yahoo Finance API")