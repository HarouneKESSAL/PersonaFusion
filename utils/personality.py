from textblob import TextBlob

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity  # Returns float between -1 (negative) and +1 (positive)
