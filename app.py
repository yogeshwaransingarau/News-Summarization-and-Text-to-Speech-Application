import streamlit as st
import requests

# Streamlit App Title
st.title("📰 News Sentiment Analysis & Hindi Audio Summary 🎙️")

# Input field for company name
company = st.text_input("Enter Company Name:")

if st.button("Analyze Sentiment"):
    if company:
        with st.spinner("Fetching news and analyzing sentiment... ⏳"):
            try:
                response = requests.post("http://127.0.0.1:5000/analyze", json={"company": company})

                if response.status_code == 200:
                    result = response.json()

                    # Display response JSON
                    st.subheader("📌 Analysis Results")
                    st.subheader(company)
                    st.json(result)

                    # # Display sentiment summary
                    # st.subheader("🔍 Sentiment Summary")
                    # st.write(result["Overall Sentiment Summary"])


                    # Play Hindi audio summary
                    audio_url = result.get("Audio File")
                    if audio_url:
                        st.subheader("🎧 Listen to Hindi Summary")
                        st.audio(audio_url, format="audio/mp3")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")
    else:
        st.warning("⚠️ Please enter a company name.")
