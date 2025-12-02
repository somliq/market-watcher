import streamlit as st
import pandas as pd
import numpy as np

# 1. Title and Subheader
st.title("Market Watcher vs. Static Sites")
st.subheader("Real-time Data Dashboard")

# 2. Create Dummy Data (Just to prove we can graph)
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['AAPL', 'GOOGL', 'AMZN']
)

# 3. Plot the Data
st.line_chart(chart_data)

# 4. A subtle jab at the competition
st.caption("Live data rendering... unlike some static HTML projects we know.")