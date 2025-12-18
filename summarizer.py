import json
import yake
import spacy
from transformers import pipeline

# Load models
nlp = spacy.load("en_core_sci_md")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
kw_extractor = yake.KeywordExtractor(top=15, stopwords=None)

# ---------- HELPERS ----------

def extract_patient_text(text):
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if line.lower().startswith("patient"):
            lines.append(line.split(":", 1)[-1].strip())
    return " ".join(lines)

def medical_ner(text):
    doc = nlp(text)
    entities = {
        "Symptoms": set(),
        "Diagnosis": set(),
        "Treatment": set()
    }

    for ent in doc.ents:
        label = ent.label_.lower()

        if label in ["disease", "symptom"]:
            entities["Symptoms"].add(ent.text)
        elif label in ["procedure", "treatment"]:
            entities["Treatment"].add(ent.text)
        elif label in ["diagnosis"]:
            entities["Diagnosis"].add(ent.text)

    return {k: list(v) for k, v in entities.items()}

def extract_current_status(patient_text):
    doc = nlp(patient_text)
    for sent in doc.sents:
        if sent.root.lemma_ in ["be", "feel", "have"] and any(
            t.lemma_ in ["now", "currently", "still", "occasionally"] for t in sent
        ):
            return sent.text
    return ""

def extract_keywords(text):
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords]

def summarize(text):
    return summarizer(text, max_length=130, min_length=50, do_sample=False)[0]["summary_text"]

# ---------- MAIN PIPELINE ----------

def generate_medical_summary(transcript):
    patient_text = extract_patient_text(transcript)
    ner_results = medical_ner(transcript)

    structured = {
        "Patient_Name": "Unknown",
        "Symptoms": ner_results["Symptoms"],
        "Diagnosis": ner_results["Diagnosis"],
        "Treatment": ner_results["Treatment"],
        "Current_Status": extract_current_status(patient_text),
        "Prognosis": [],
        "Keywords": extract_keywords(transcript),
        "Clinical_Summary": summarize(transcript)
    }

    return structured


if __name__ == "__main__":
    transcript = """
    Doctor: How are you feeling today?
    Patient: I had a car accident. My neck and back hurt a lot for four weeks.
    Doctor: Did you receive treatment?
    Patient: Yes, I had ten physiotherapy sessions, and now I only have occasional back pain.
    """

    print(json.dumps(generate_medical_summary(transcript), indent=2))
