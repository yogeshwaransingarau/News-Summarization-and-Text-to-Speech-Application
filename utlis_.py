import requests
from bs4 import BeautifulSoup
import urllib.parse
from textblob import TextBlob
from langdetect import detect
from collections import defaultdict
import json
from googletrans import Translator
from gtts import gTTS
import os
import platform
import sys

def analyze_sentiment(text):
    """Analyze the sentiment of a given text and return its polarity."""
    sentiment = TextBlob(text).sentiment.polarity
    return "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

def is_english(text):
    """Detect if the given text is in English."""
    try:
        return detect(text) == "en"
    except:
        return False

def extract_topics(text):
    """Extract relevant topics from the given text."""
    blob = TextBlob(text)
    return list(set(blob.noun_phrases))

def compare_articles(articles):
    """Conduct comparative sentiment analysis across the 10 articles."""
    sentiment_trend = {"Positive": 0, "Negative": 0, "Neutral": 0}
    topic_sentiment = defaultdict(lambda: defaultdict(int))
    coverage_differences = []
    for article in articles:
        sentiment_trend[article['Sentiment']] += 1
        for topic in article['Topics']:
            topic_sentiment[topic][article['Sentiment']] += 1
    sorted_topics = sorted(topic_sentiment.items(), key=lambda x: sum(x[1].values()), reverse=True)
    for i in range(len(articles) - 1):
        article1 = articles[i]
        article2 = articles[i + 1]
        comparison = {
            "Comparison": f"Article covers {article1['Topics']}, whereas Article {i+2} focuses on {article2['Topics']}.",
            "Sentiment Impact": f"Article has a {article1['Sentiment']} sentiment, while Article {i+2} has a {article2['Sentiment']} sentiment."
        }
        coverage_differences.append(comparison)
    return {
        "Sentiment Trend": sentiment_trend,
        "Top Topics Sentiment": dict(sorted_topics[:5]),
        "Coverage Differences": coverage_differences
    }

def scrape_articles(company_name):
    """Scrapes Google News for at least 10 articles about a company."""
    query = f"{company_name} news"
    encoded_query = urllib.parse.quote(query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"https://www.google.com/search?q={encoded_query}&tbm=nws&hl=en"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        sentiment_distribution = defaultdict(int)
        cumulative_summary = []
        for item in soup.select('div.SoaBEf'):
            try:
                title_elem = item.select_one('div.MBeuO')
                summary_elem = item.select_one('div.GI74Re')
                title = title_elem.text.strip() if title_elem else "No title found"
                summary = summary_elem.text.strip() if summary_elem else "No summary found"
                if is_english(summary):
                    sentiment = analyze_sentiment(summary)
                    topics = extract_topics(summary)
                    sentiment_distribution[sentiment] += 1
                    articles.append({
                        'Title': title,
                        'Summary': summary,
                        'Sentiment': sentiment,
                        'Topics': topics,
                    })
                    cumulative_summary.append(summary)
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        if len(articles) < 10:
            url_old = f"https://www.google.com/search?q={encoded_query}&tbm=nws&tbs=qdr:m&start=10"
            response_old = requests.get(url_old, headers=headers)
            response_old.raise_for_status()
            soup_old = BeautifulSoup(response_old.text, 'html.parser')
            for item in soup_old.select('div.SoaBEf'):
                if len(articles) >= 10:
                    break
                try:
                    title_elem = item.select_one('div.MBeuO')
                    summary_elem = item.select_one('div.GI74Re')
                    title = title_elem.text.strip() if title_elem else "No title found"
                    summary = summary_elem.text.strip() if summary_elem else "No summary found"
                    if is_english(summary):
                        sentiment = analyze_sentiment(summary)
                        topics = extract_topics(summary)
                        sentiment_distribution[sentiment] += 1
                        articles.append({
                            'Title': title,
                            'Summary': summary,
                            'Sentiment': sentiment,
                            'Topics': topics,
                        })
                        cumulative_summary.append(summary)
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue
        return articles, sentiment_distribution, " ".join(cumulative_summary)
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return [], {}, ""

translator = Translator()

def translate_to_hindi(text):
    """Translate English text to Hindi using Google Translate API."""
    try:
        translation = translator.translate(text, src='en', dest='hi')
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original text if translation fails

def play_audio(audio_file):
    """Play audio file based on OS."""
    if sys.platform.startswith("win"):  # Windows
        os.system(f"start {audio_file}")
    elif sys.platform.startswith("darwin"):  # macOS
        os.system(f"afplay {audio_file}")
    elif sys.platform.startswith("linux"):  # Linux
        os.system(f"mpg123 {audio_file}")  # Requires mpg123 installed
    else:
        print(f"Audio saved as {audio_file}. Please play manually.")

def text_to_speech_hindi(summary):
    """Convert the summary text into Hindi speech and save it."""
    try:
        hindi_summary = translate_to_hindi(summary)
        tts = gTTS(text=hindi_summary, lang="hi", slow=False)
        audio_file = "news_summary.mp3"
        tts.save(audio_file)
        print(f"\n✅ Hindi audio summary saved as: {audio_file}")
        play_audio(audio_file)
    except Exception as e:
        print(f"Error in TTS conversion: {e}")

def main():
    company_name = input("Enter company name: ")
    articles, sentiment_distribution, cumulative_summary = scrape_articles(company_name)
    if articles:
        comparative_analysis = compare_articles(articles)
        final_analysis = {
            "Company": company_name,
            "Articles": articles,
            "Comparative Sentiment Analysis": comparative_analysis,
            "Overall Sentiment Summary": f"{company_name}'s latest news coverage is mostly {'positive' if sentiment_distribution['Positive'] > sentiment_distribution['Negative'] else 'negative'}."
        }
        print(json.dumps(final_analysis, indent=4))
        text_to_speech_hindi(cumulative_summary) #added the audio function.
    else:
        print("No articles found or an error occurred.")

if __name__ == "__main__":
    main()