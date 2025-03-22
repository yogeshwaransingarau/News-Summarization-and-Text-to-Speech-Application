from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gtts import gTTS
import os
from googletrans import Translator  # Import Google Translator
from utlis_ import scrape_articles, compare_articles  # Ensure the function exists

app = Flask(__name__)
CORS(app)  # Allow requests from Streamlit

translator = Translator()  # Initialize translator

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask API is running!"})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        company_name = data.get("company")
        if not company_name:
            return jsonify({"error": "Company name is required"}), 400
        
        # Fetch articles and sentiment distribution
        articles, sentiment_distribution, cumulative_summary = scrape_articles(company_name)

        if not articles:
            return jsonify({"error": "No articles found"}), 404

        # Perform comparative sentiment analysis
        comparative_analysis = compare_articles(articles)

        # 🔹 **Translate summary to Hindi**
        hindi_summary = translator.translate(cumulative_summary, src='en', dest='hi').text

        # 🔹 **Generate Hindi Audio**
        audio_path = "output.mp3"
        tts = gTTS(text=hindi_summary, lang="hi", slow=False)
        tts.save(audio_path)

        # Return JSON response with Hindi audio file link
        return jsonify({
            "Company": company_name,
            "Articles": articles,
            "Sentiment Distribution": sentiment_distribution,
            "Comparative Sentiment Analysis": comparative_analysis,
            "Overall Sentiment Summary": f"{company_name}'s latest news coverage is mostly {'positive' if sentiment_distribution['Positive'] > sentiment_distribution['Negative'] else 'negative'}.",
            "Final Sentiment Analysis": "Mostly positive" if sentiment_distribution["Positive"] > sentiment_distribution["Negative"] else "Mostly negative",
           
            "Audio File": "http://127.0.0.1:5000/audio"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/audio", methods=["GET"])
def get_audio():
    """Serve the generated Hindi audio file."""
    if os.path.exists("output.mp3"):
        return send_file("output.mp3", mimetype="audio/mp3")
    return jsonify({"error": "Audio file not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
