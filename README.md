# AI-Powered Weather Advisory and Recommendation System

## 🌦 Project Overview
This project is an **AI-powered Weather Advisory and Recommendation System** that leverages **NASA MERRA-2 historical Earth observation data** to provide personalized, interactive weather insights. Unlike traditional weather apps, which offer only 6–7 day forecasts, this system uses Earth data to **project weather patterns up to 7–8 months ahead**. The application combines **data analytics, AI/LLM reasoning, and interactive UI/UX** to suggest suitable activities, clothing, food, and essentials based on predicted weather conditions.

---

## 🚀 Features

- **Interactive Map Selection**: Users can drop a pin or search for any location worldwide.
- **Date & Parameter Selection**: Choose specific dates and weather parameters like temperature, rainfall, windspeed, humidity, snow, and dust/air quality.
- **Data Analysis**: Processes NASA MERRA-2 data to compute mean, max, min, and probability of extreme weather.
- **AI Recommendations**: Uses a free open-source LLM to dynamically generate:
  - Outdoor activities
  - Clothing suggestions
  - Essentials and food items
  - Safety precautions
- **Image Integration**: Fetches 1–3 relevant images per item from free APIs (Unsplash, Pexels, Pixabay) to enrich recommendations.
- **Visualization**: Charts, heatmaps, and probability trends.
- **Download Options**: Export results as CSV, JSON, or PDF.

---

## ⚡ Challenge Addressed
Traditional weather apps provide only **short-term forecasts** and lack **actionable guidance**. Users see temperatures or rainfall probabilities but do not know **how to act** on them. This system makes complex NASA climate data **understandable, visual, and actionable**, helping users make **smart, informed decisions**.

---

## 🌍 Importance
By combining **NASA-grade accuracy**, **AI reasoning**, and **intuitive UI**, the application promotes **sustainable, informed living**. Users can plan outdoor activities, dress appropriately, and prepare essentials while understanding **long-term climate trends**.

---

## 🛠 Tech Stack

- **Frontend**: React.js, Leaflet.js / Mapbox, Chart.js / Plotly.js
- **Backend**: Python, FastAPI / Flask
- **Data Processing**: xarray, netCDF4, pandas
- **AI / LLM Engine**: LLaMA 2, MPT-7B, or Falcon-7B (free/open-source)
- **Image Fetching**: Unsplash API, Pexels API, Pixabay API
- **Caching / DB (Optional)**: Redis / MongoDB

