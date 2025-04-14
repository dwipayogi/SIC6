import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime

st.set_page_config(page_title="EduDetect", layout="wide")

# Function to fetch data from API
def fetch_latest_data():
    try:
        response = requests.get("https://samsung.yogserver.web.id/data/latest")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data: Status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to fetch historical data (10 latest entries)
def fetch_historical_data():
    try:
        response = requests.get("https://samsung.yogserver.web.id/data")
        if response.status_code == 200:
            data = response.json()
            # Get the 10 most recent entries
            recent_data = data[-10:] if len(data) > 10 else data
            return recent_data
        else:
            st.error(f"Error fetching historical data: Status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
        return None

# Add sidebar
st.sidebar.header("About EduDetect")
st.sidebar.write("EduDetect is a monitoring system that tracks environmental conditions in educational spaces.")

# Main content
st.title("EduDetect")
st.subheader("Environmental Monitoring Dashboard")

# Fetch latest data
latest_data = fetch_latest_data()

# Display metrics with real data or fallback values
a, b, c = st.columns(3)

if latest_data:
    temp_value = f"{latest_data['temperature']}°C"
    humidity_value = f"{latest_data['humidity']}%"
    motion_value = "Active" if latest_data['motion'] == 1 else "Inactive"
    timestamp = latest_data['timestamp']
    
    # Format timestamp for display
    st.caption(f"Last updated: {timestamp}")
else:
    temp_value = "30°C"
    humidity_value = "77%"
    motion_value = "Active"

a.metric("Temperature", temp_value, border=True)
b.metric("Humidity", humidity_value, border=True)
c.metric("Motion Sensor", motion_value, border=True)

# Fetch historical data for charts
historical_data = fetch_historical_data()

# Process historical data for charts
if historical_data:
    # Convert to DataFrame
    df = pd.DataFrame(historical_data)
    
    # Convert timestamps to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort by timestamp (newest last for proper chart display)
    df = df.sort_values('timestamp')
    
    # Create temperature dataframe
    temp_df = df[['timestamp', 'temperature']].rename(columns={'timestamp': 'Time', 'temperature': 'Temperature'})
    
    # Create humidity dataframe
    humidity_df = df[['timestamp', 'humidity']].rename(columns={'timestamp': 'Time', 'humidity': 'Humidity'})

# Temperature chart
st.subheader("Temperature Data")
st.write("This chart shows the 10 latest temperature readings.")
st.line_chart(temp_df, x='Time', y='Temperature', use_container_width=True)

# Humidity chart
st.subheader("Humidity Data")
st.write("This chart shows the 10 latest humidity readings.")
st.line_chart(humidity_df, x='Time', y='Humidity', use_container_width=True)

# Note: The generate_temperature_data and generate_humidity_data functions are kept as fallbacks
def generate_temperature_data(num_points=10):
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=num_points, freq='1s')
    base_temp = 30
    temperatures = base_temp + np.random.normal(0, 1, size=num_points)
    return pd.DataFrame({
        'Time': timestamps,
        'Temperature': temperatures
    })

def generate_humidity_data(num_points=10):
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=num_points, freq='1s')
    base_humidity = 50
    humidity = base_humidity + np.random.normal(0, 5, size=num_points)
    return pd.DataFrame({
        'Time': timestamps,
        'Humidity': humidity
    })