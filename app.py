import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns

# Set page title
st.set_page_config(page_title="Calgary Traffic Incidents Dashboard", layout="wide")

# Load the cleaned dataset
file_path = "/Users/sohamsolanki/Desktop/Calgary_Traffic_Analysis/data/Cleaned_Traffic_data.csv"
df = pd.read_csv(file_path)

# Sidebar Filters
st.sidebar.header("Filter Options")
selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()), index=0)
selected_category = st.sidebar.multiselect("Select Incident Type", df["Incident_Category"].unique(), default=df["Incident_Category"].unique())

# Filter Data Based on Selection
filtered_df = df[(df["Year"] == selected_year) & (df["Incident_Category"].isin(selected_category))]

# Main Dashboard Title
st.title("🚦 Calgary Traffic Incidents Dashboard")

# Show basic stats
st.markdown(f"### 📊 Year: {selected_year}")
st.write(f"Total incidents: **{len(filtered_df)}**")

# Create two columns layout
col1, col2 = st.columns([2, 1])

# 🔥 Heatmap Visualization
with col1:
    st.subheader("Traffic Incident Heatmap")
    
    # Create Folium Map
    heatmap = folium.Map(location=[51.0447, -114.0719], zoom_start=11)
    heat_data = list(zip(filtered_df["Latitude"], filtered_df["Longitude"]))
    HeatMap(heat_data).add_to(heatmap)
    
    # Display Map
    folium_static(heatmap)

# 📊 Quadrant-based Incident Distribution
with col2:
    st.subheader("Incidents by Quadrant")
    plt.figure(figsize=(5, 4))
    sns.countplot(x=filtered_df["QUADRANT"], hue=filtered_df["QUADRANT"], palette="viridis", legend=False)
    plt.xlabel("Quadrant")
    plt.ylabel("Incident Count")
    plt.title("Traffic Incidents by Quadrant")
    st.pyplot(plt)

# 📅 Monthly Traffic Incidents
st.subheader("Monthly Trends")
plt.figure(figsize=(10, 5))
sns.countplot(x=filtered_df["Month"], hue=filtered_df["Month"], palette="coolwarm", legend=False)
plt.xlabel("Month")
plt.ylabel("Incident Count")
plt.title("Traffic Incidents by Month")
st.pyplot(plt)

# 🕒 Hourly Trends
st.subheader("Hourly Trends")
plt.figure(figsize=(10, 5))
sns.countplot(x=filtered_df["Hour"], hue=filtered_df["Hour"], palette="magma", legend=False)
plt.xlabel("Hour (24-hour format)")
plt.ylabel("Incident Count")
plt.title("Traffic Incidents by Hour")
st.pyplot(plt)

# 🚗 Incident Types Breakdown
st.subheader("Incident Types")
plt.figure(figsize=(8, 4))
sns.countplot(y=filtered_df["Incident_Category"], hue=filtered_df["Incident_Category"], palette="pastel", legend=False)
plt.xlabel("Count")
plt.ylabel("Incident Type")
plt.title("Traffic Incidents by Type")
st.pyplot(plt)

# 🎯 Summary
st.markdown(f"#### ✅ Data from {selected_year} displayed based on selected incident categories.")
