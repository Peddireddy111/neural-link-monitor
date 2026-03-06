# ⚡ Project: Neural Link - AI Weather Field Monitor

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

## 📌 Overview
The Neural Link Field Monitor is a next-generation data engineering dashboard. It bridges the gap between raw API telemetry and Artificial Intelligence. The application fetches live meteorological data, processes it into visual trends, and uses **Google's Gemini 3 Flash** model to generate real-time atmospheric analysis and custom warnings.

## 🚀 Features
* **Live API Ingestion:** Pulls rolling 7-day weather data via the Open-Meteo API.
* **Dynamic Digital Twin UI:** Simulates a live hardware sensor feed using CSS overlay techniques to float live API data over a looping video.
* **Data Transformation:** Cleans and processes JSON payloads into vectorized Pandas DataFrames.
* **AI Intelligence Layer:** Uses Gemini to read the dataframes and generate human-readable expert summaries based on the selected city.
* **One-Click Export:** Allows users to download the processed data archive as a CSV file.

## 🛠️ Tech Stack
* **Frontend:** Streamlit, Matplotlib, Custom CSS
* **Data Engineering:** Python, Pandas, Requests
* **AI/LLM:** Google Generative AI SDK (Gemini)

## 💻 How to Run Locally

1. **Clone this repository:**
   git clone https://github.com/Peddireddy111/neural-link-monitor.git
   
2. **Install dependencies:**
   pip install streamlit pandas matplotlib requests google-generativeai
   
3. **Add the Media:**
   Ensure your hardware looping video (`.mp4` or `.mov`) is placed in the root directory.
   
4. **Configure the AI:**
   Open `app.py`, locate Line 28, and replace `"YOUR_API_KEY_GOES_HERE"` with your actual Google AI Studio key. *(Note: Never commit your real API key to GitHub!)*
   
5. **Run the application:**
   streamlit run app.py

---
*Built as a live demonstration of modern Data Engineering, API integration, and LLM architectures.*
