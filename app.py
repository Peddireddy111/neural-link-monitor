import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
from datetime import datetime, timedelta
import os

# --- 1. CONFIGURATION & STYLING ---
st.set_page_config(page_title="Neural Link Station", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #020617; color: #f8fafc; }
    .stMetric { background-color: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 8px; }
    .ai-box { background-color: #0f172a; border-left: 5px solid #22d3ee; padding: 20px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ PROJECT: NEURAL LINK FIELD MONITOR")

# --- 2. SIDEBAR & API KEY SETUP ---
st.sidebar.header("📡 Station Controls")

# ==========================================
# 🛑 PASTE YOUR API KEY RIGHT HERE 🛑
# Keep the quotation marks around your key!
api_key = "YOUR_API_KEY_GOES_HERE"
# ==========================================

if api_key == "YOUR_API_KEY_GOES_HERE":
    st.sidebar.warning("⚠️ API Key missing! Replace the placeholder in the code.")
else:
    st.sidebar.success("🔗 Neural Bridge: HARDWIRED")

city = st.sidebar.selectbox("Select Location", ["Paris", "London", "Tokyo", "Mumbai", "Pulivendula"])

# --- 3. DATA ENGINE ---
coords = {"Paris": (48.85, 2.35), "London": (51.50, -0.12), "Tokyo": (35.68, 139.65), "Mumbai": (19.07, 72.87), "Pulivendula": (14.422232, 78.226341)}
lat, lon = coords[city]

@st.cache_data(ttl=3600) # Caches data for 1 hour to make the app run faster
def fetch_weather_data(lat, lon):
    today = datetime.now()
    start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}&daily=temperature_2m_max,temperature_2m_min"
    res = requests.get(url).json()
    return pd.DataFrame({
        'Date': pd.to_datetime(res['daily']['time']),
        'Max Temp': res['daily']['temperature_2m_max'],
        'Min Temp': res['daily']['temperature_2m_min']
    })

df = fetch_weather_data(lat, lon)
latest_temp = df.iloc[-1]['Max Temp']

# --- 4. THE UI LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📹 Live Sensor Feed")
    video_path = 'D:\weather_analyzer\Video_Generation_With_Location_Temperature.mp4'
    
    if os.path.exists(video_path):
        # DYNAMIC HUD OVERLAY
        st.markdown(f"""
            <div style="position: relative; border-radius: 10px; overflow: hidden; border: 2px solid #22d3ee;">
                <video autoplay loop muted playsinline style="width: 100%; opacity: 0.8;">
                    <source src="http://localhost:8501/app/static/{video_path}" type="video/mp4">
                </video>
                <div style="position: absolute; top: 15px; right: 15px; background: rgba(0,0,0,0.8); 
                            color: #22d3ee; padding: 10px; border: 1px solid #22d3ee; font-family: monospace;">
                    <div style="font-size: 0.7rem; opacity: 0.7;">LIVE_DATA</div>
                    <div style="font-size: 1.4rem; font-weight: bold;">{latest_temp}°C</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        # Fallback in case the browser blocks the overlay trick
        st.video(open(video_path, 'rb').read()) 
    else:
        st.error(f"Station Video Missing! Make sure '{video_path}' is in the exact same folder as your app.py file.")

with col2:
    st.subheader("📊 Atmospheric Analysis")
    fig, ax = plt.subplots(facecolor='#020617')
    ax.set_facecolor('#020617')
    ax.plot(df['Date'], df['Max Temp'], color='#22d3ee', marker='o', label='Max')
    ax.plot(df['Date'], df['Min Temp'], color='#f472b6', marker='o', label='Min')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.1)
    plt.xticks(rotation=45, color='white')
    st.pyplot(fig)

# --- 5. THE INTELLIGENCE LAYER ---
st.divider()
st.subheader("🧠 Neural Link AI Analysis")

if st.button("ENGAGE NEURAL SCAN"):
    if api_key == "YOUR_API_KEY_GOES_HERE" or not api_key:
        st.error("⚠️ System Failure: Valid Gemini API Key required to run the scan.")
    else:
        with st.spinner("Decoding atmospheric patterns via Gemini 3 Flash..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-3-flash-preview')
                prompt = f"Analyze this 7-day weather for {city}: {df.to_string()}. Give a 2-sentence summary and one 'Neural Warning'."
                response = model.generate_content(prompt)
                st.markdown(f'<div class="ai-box">{response.text}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Neural Link Failed: {e}")

# --- 6. EXPORT SECTION ---
st.subheader("📝 Data Archive")
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 DOWNLOAD ARCHIVE (.CSV)", data=csv, file_name=f"{city}_weather.csv", mime="text/csv")