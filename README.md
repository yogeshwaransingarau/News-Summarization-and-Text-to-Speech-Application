# 📰 News Sentiment Analysis & Hindi Audio Summary 🎙️

This project scrapes the latest news about a company, analyzes sentiment, extracts key topics, and generates a **Hindi** audio summary.

## 📌 Features
- ✅ **Scrape Google News** for company-related articles.
- ✅ **Perform Sentiment Analysis** (Positive, Negative, Neutral).
- ✅ **Extract Key Topics** from articles.
- ✅ **Translate Summary to Hindi** using Google Translate API.
- ✅ **Generate Hindi Audio Summary** with `gTTS`.
- ✅ **Flask API** to serve JSON results and the audio file.
- ✅ **Streamlit UI** to interact with the API.

---

## ⚙️ Setup Instructions

### **1️⃣ Install Dependencies**
Ensure you have **Python 3.8+** installed.

Run the following command to install required packages:
```bash

pip install -r requirements.txt
```
## Run the Flask API
```
python app.py
```
The server runs at:
📍 http://127.0.0.1:5000/

## Run the Streamlit App
```
streamlit run app_streamlit.py
```

🚀 Usage Guide

🌟 Using the Streamlit App
1️⃣ Open Streamlit UI in your browser.
2️⃣ Enter a company name (e.g., Google).
3️⃣ Click "Analyze Sentiment" to fetch news and perform analysis.
4️⃣ View:

✅ Sentiment Summary (Positive, Negative, Neutral).
✅ Extracted Key Topics.
✅ Comparative Sentiment Analysis.
✅ Hindi-translated summary. 5️⃣ Click "Play Audio" to listen to the Hindi summary.

📌 Expected Output

✅ JSON Response with:

Company News Summary
Sentiment Analysis
Key Topics
Comparative Sentiment Trends
Hindi-translated summary
Downloadable Hindi Audio
✅ Streamlit UI for interactive usage.


