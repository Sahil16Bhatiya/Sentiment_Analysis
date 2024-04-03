from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    # Create a SentimentIntensityAnalyzer object
    analyzer = SentimentIntensityAnalyzer()

    # Analyze the sentiment of the text
    sentiment_score = analyzer.polarity_scores(text)

    # Classify the sentiment based on the compound score
    if sentiment_score['compound'] >= 0.05:
        return 'positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'negative'
    else:
        # If compound score is between -0.05 and 0.05, consider it as neutral
        return 'neutral'
