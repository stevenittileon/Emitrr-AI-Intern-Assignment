# ner_extraction.py
from bootstrap import nlp, re

def extract_medical_info(text):
    doc = nlp(text)

    symptoms, treatments, diagnosis, prognosis = set(), set(), set(), set()

    for sent in doc.sents:
        s = sent.text.lower()

        if any(k in s for k in ["pain", "ache", "discomfort", "stiffness"]):
            symptoms.add(sent.text.strip())

        if any(k in s for k in ["physiotherapy", "therapy", "painkiller", "medication"]):
            treatments.add(sent.text.strip())

        if any(k in s for k in ["whiplash", "injury", "strain"]):
            diagnosis.add(sent.text.strip())

        if any(k in s for k in ["full recovery", "improving", "no long-term"]):
            prognosis.add(sent.text.strip())

    return {
        "Symptoms": list(symptoms),
        "Diagnosis": list(diagnosis),
        "Treatment": list(treatments),
        "Prognosis": list(prognosis)
    }


if __name__ == "__main__":
    sample = "I had a whiplash injury and physiotherapy. Pain is improving."
    print(extract_medical_info(sample))
