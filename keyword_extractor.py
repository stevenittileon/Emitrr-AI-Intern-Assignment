# keyword_extractor.py
from rake_nltk import Rake

def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    # Return top-ranked keyword phrases
    return r.get_ranked_phrases()[:10]

if __name__ == "__main__":
    transcript = """I had a car accident. My neck and back hurt a lot for four weeks. 
I had ten physiotherapy sessions, and now I only have occasional back pain."""
    keywords = extract_keywords(transcript)
    print(keywords)
