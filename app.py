from flask import Flask, render_template, request, jsonify
from sentiment_analysis import analyze_sentiment
import json
import os
import collections

app = Flask(__name__)

accuracy = 85.5

def save_review(sentiment_data):
    """Append a new review to the reviews.json file in a valid JSON format."""
    if not os.path.exists('reviews.json'):
        # If the file does not exist, create it with an empty list
        with open('reviews.json', 'w') as file:
            json.dump([], file)
    
    with open('reviews.json', 'r+') as file:
        file_data = json.load(file)
        file_data.append(sentiment_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

def get_sentiment_counts():
    """Read the reviews.json file and count the occurrences of each sentiment."""
    if not os.path.exists('reviews.json'):
        return {"positive": 0, "negative": 0, "neutral": 0}
    
    with open('reviews.json', 'r') as file:
        reviews = json.load(file)
    
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    for review in reviews:
        if review['sentiment'] in sentiment_counts:
            sentiment_counts[review['sentiment']] += 1
    return sentiment_counts

def get_word_counts():
    """Count occurrences of each word in the reviews.json file."""
    if not os.path.exists('reviews.json'):
        return {}
    
    with open('reviews.json', 'r') as file:
        reviews = json.load(file)

    word_count = collections.Counter()
    for review in reviews:
        text = review['text']
        words = text.split()
        word_count.update(words)
    
    return dict(word_count)


@app.route('/')
def index():
    return render_template('feedback_form.html', accuracy=accuracy)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_route():
    text = request.form.get('text')
    
    # Debug print to check the input text
    print("Input Text:", text)

    sentiment = analyze_sentiment(text)

    # Debug print to check the detected sentiment
    print("Detected Sentiment:", sentiment)

    # Save review and sentiment to local storage
    review_data = {'text': text, 'sentiment': sentiment}
    save_review(review_data)

    return jsonify({'sentiment': sentiment, 'accuracy': accuracy})

@app.route('/sentiment_data')
def sentiment_data():
    data = get_sentiment_counts()
    return jsonify(data)

@app.route('/word_counts')
def word_counts():
    data = get_word_counts()
    # Sort the word counts from max to min
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    return jsonify(sorted_data)

@app.route('/positive_reviews')
def positive_reviews():
    if not os.path.exists('reviews.json'):
        return jsonify([])
    
    with open('reviews.json', 'r') as file:
        reviews = json.load(file)

    # Filter positive reviews
    positive_reviews = [review['text'] for review in reviews if review['sentiment'] == 'positive']
    
    # Get top 2-3 positive reviews
    top_positive_reviews = positive_reviews[:3]

    return jsonify(top_positive_reviews)

if __name__ == '__main__':
    app.run(debug=True)
