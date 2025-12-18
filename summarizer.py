import json
import re
import yake
import spacy
from transformers import pipeline

# Load models
nlp = spacy.load("en_core_web_sm")

ner_model = pipeline(
    "ner",
    model="d4data/biomedical-ner-all",
    aggregation_strategy="simple"
)

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

kw_extractor = yake.KeywordExtractor(top=15)

# ---------- HELPERS ----------

def extract_patient_text(text):
    return " ".join(
        line.split(":", 1)[-1].strip()
        for line in text.split("\n")
        if line.strip().lower().startswith("patient")
    )

def extract_entities(text):
    entities = {"Symptoms": set(), "Diagnosis": set(), "Treatment": set()}
    results = ner_model(text)

    for ent in results:
        label = ent["entity_group"].lower()
        value = ent["word"]

        if label in ["disease", "symptom"]:
            entities["Symptoms"].add(value)
        elif label in ["treatment", "procedure", "drug"]:
            entities["Treatment"].add(value)
        elif label in ["diagnosis"]:
            entities["Diagnosis"].add(value)

    return {k: list(v) for k, v in entities.items()}

def extract_current_status(patient_text):
    doc = nlp(patient_text)
    for sent in doc.sents:
        if any(tok.lemma_ in ["now", "currently", "still", "occasionally"] for tok in sent):
            return sent.text
    return ""

def extract_keywords(text):
    return [kw for kw, _ in kw_extractor.extract_keywords(text)]

def summarize(text):
    return summarizer(text, max_length=120, min_length=50, do_sample=False)[0]["summary_text"]

# ---------- MAIN PIPELINE ----------

def generate_medical_summary(transcript):
    patient_text = extract_patient_text(transcript)
    ents = extract_entities(transcript)

    return {
        "Patient_Name": "Unknown",
        "Symptoms": ents["Symptoms"],
        "Diagnosis": ents["Diagnosis"],
        "Treatment": ents["Treatment"],
        "Current_Status": extract_current_status(patient_text),
        "Prognosis": [],
        "Keywords": extract_keywords(transcript),
        "Clinical_Summary": summarize(transcript)
    }


if __name__ == "__main__":
    transcript = """
    Doctor: How are you feeling today?
    Patient: I had a car accident. My neck and back hurt a lot for four weeks.
    Doctor: Did you receive treatment?
    Patient: Yes, I had ten physiotherapy sessions, and now I only have occasional back pain.
    """

    print(json.dumps(generate_medical_summary(transcript), indent=2))
