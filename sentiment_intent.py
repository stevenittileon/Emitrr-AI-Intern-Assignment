# sentiment_intent.py
from bootstrap import pipeline

sentiment_model = pipeline("sentiment-analysis")
intent_model = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

def analyze_sentiment_intent(text):
    sentiment_raw = sentiment_model(text)[0]["label"]

    sentiment_map = {
        "NEGATIVE": "Anxious",
        "POSITIVE": "Reassured"
    }

    sentiment = sentiment_map.get(sentiment_raw, "Neutral")

    intent_labels = [
        "Seeking reassurance",
        "Reporting symptoms",
        "Expressing concern"
    ]

    intent = intent_model(text, intent_labels)["labels"][0]

    return {
        "Sentiment": sentiment,
        "Intent": intent
    }


if __name__ == "__main__":
    text = "I'm worried about my back pain."
    print(analyze_sentiment_intent(text))
