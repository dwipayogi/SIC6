import streamlit as st
import requests
import pandas as pd
import json
import time

st.set_page_config(page_title="EduDetect - History", layout="wide")

# Add sidebar
st.sidebar.header("Data History")
st.sidebar.write("This page displays historical data.")

# Main content
st.title("Data History")
st.subheader("Historical Data")
st.write("This section shows historical data points.")

placeholder = st.empty()

# Function to fetch data from the server
@st.cache_data(ttl=300)  # Cache the data for 5 minutes
def fetch_data():
    try:
        response = requests.get("https://samsung.yogserver.web.id/data")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Create a container for displaying last refresh time
refresh_info = st.container()
last_refresh = st.empty()

# Add a refresh button
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("Refresh Data"):
        # Clear the cache to force a fresh data fetch
        fetch_data.clear()
        # Update the last refresh time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        last_refresh.text(f"Last refreshed: {current_time}")

# Fetch and display data
data = fetch_data()

if data:
    # Display the data in the placeholder
    with placeholder.container():
      df = pd.DataFrame(data)
      st.dataframe(df)
else:
    with placeholder.container():
        st.warning("No data available. Please check the server connection.")