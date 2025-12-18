## Physician Notetaker Assignment

An end-to-end **Natural Language Processing (NLP) system** for analyzing **physician–patient conversations** and converting them into information using **pretrained Transformer models**.

This project runs **locally** and is designed to generalize across different medical dialogue formats.

## Core Capabilities

- **Medical summarization**: extract symptoms, diagnoses, treatments, current status, prognosis cues, and keywords from transcripts.
- **Sentiment & intent analysis**: map raw model outputs into clinical-friendly labels (e.g. **Anxious**, **Reassured**, **Seeking reassurance**).
- **SOAP note generation**: convert free-text conversations into a structured **SOAP** representation.


## Project Structure

```text
emittr/
├── bootstrap.py            # Environment bootstrap (installs core NLP libs & models)
├── summarizer.py           # Medical entity extraction, keywords, and clinical summary
├── sentiment_intent.py     # Patient sentiment and intent analysis
├── ner_extraction.py       # Rule-based medical info extraction using spaCy
├── keyword_extractor.py    # Simple keyword extraction with RAKE
├── soap_note_generator.py  # SOAP note generation from transcripts
└── README.md               # Project documentation
```

## Module Overview

### **`bootstrap.py`**
- Ensures required Python packages (`spacy`, `nltk`, `rake-nltk`, `transformers`, `torch`) are installed.
- Downloads the `en_core_web_sm` spaCy model and NLTK resources as needed.
- Exposes commonly used NLP utilities (e.g. `pipeline`, `nlp`, tokenizers).

### **`summarizer.py`**
- Uses **spaCy**, **HuggingFace Transformers**, and **YAKE** to:
  - Run biomedical NER (`d4data/biomedical-ner-all`).
  - Extract **Symptoms**, **Diagnosis**, and **Treatment** entities.
  - Detect **current status** from patient statements.
  - Generate **keywords** (`yake`).
  - Produce a **clinical summary** using `facebook/bart-large-cnn`.
- **Output**: a JSON object with fields like `Symptoms`, `Diagnosis`, `Treatment`, `Current_Status`, `Keywords`, and `Clinical_Summary`.

### **`sentiment_intent.py`**
- Builds two HuggingFace pipelines:
  - `sentiment-analysis` → mapped to **Anxious / Reassured / Neutral**.
  - `zero-shot-classification` (`facebook/bart-large-mnli`) for intent.
- **Output example**:

```json
{
  "Sentiment": "Reassured",
  "Intent": "Seeking reassurance"
}
```

### **`ner_extraction.py`**
- Uses `bootstrap.nlp` (spaCy) and simple keyword heuristics over sentences to collect:
  - **Symptoms**
  - **Treatment**
  - **Diagnosis**
  - **Prognosis**
- Returns a small structured JSON dictionary, useful for quick rule-based extraction/baselines.

### **`keyword_extractor.py`**
- Uses **RAKE (rake-nltk)** to extract the **top N keyword phrases** from a transcript.
- Contains a small `__main__` example you can run directly for testing.

### **`soap_note_generator.py`**
- Uses regex-based pattern matching on transcripts to fill a SOAP structure:
  - **Subjective**: chief complaint & history of present illness.
  - **Objective**: physical exam & observations.
  - **Assessment**: diagnosis & severity.
  - **Plan**: treatment & follow-up recommendations.
- **Output**: a SOAP note as a JSON-like dictionary (printable via `json.dumps`).


## Installation & Setup

### **Prerequisites**
- **Python 3.10.x or 3.11.x**
- OS: Windows, macOS, or Linux with internet access for the first model downloads.

### **1. Create & Activate a Virtual Environment (recommended)**

```bash
python -m venv venv
```

On **Windows**:

```bash
venv\Scripts\activate
```

On **macOS / Linux**:

```bash
source venv/bin/activate
```

### **2. Install Dependencies**

If you already have a `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

If not, minimally install:

```bash
pip install spacy nltk rake-nltk transformers torch yake
python -m spacy download en_core_web_sm
```

**Note:** Running `bootstrap.py` once will also attempt to auto-install core dependencies and the spaCy model.

## How to Run

All scripts can be run directly with Python once dependencies are installed.

- **Medical summarization & entities**

```bash
python summarizer.py
```

- **Sentiment & intent analysis**

```bash
python sentiment_intent.py
```

- **Rule-based medical info extraction**

```bash
python ner_extraction.py
```

- **Keyword extraction demo**

```bash
python keyword_extractor.py
```

- **SOAP note generation**

```bash
python soap_note_generator.py
```

Each script contains a small inline example in its `__main__` block; replace the sample transcript strings with your own conversation text.

## Models & Libraries

- **spaCy**: `en_core_web_sm` for sentence splitting and linguistic features.
- **HuggingFace Transformers**:
  - `d4data/biomedical-ner-all` for biomedical NER.
  - `facebook/bart-large-cnn` for summarization.
  - `facebook/bart-large-mnli` for zero-shot intent classification.
  - Default `sentiment-analysis` model (e.g. `distilbert-base-uncased-finetuned-sst-2-english`) for sentiment.
- **YAKE** and **RAKE**: keyword and keyphrase extraction.

No fine-tuning is required; everything uses pretrained models.

## Possible Next Steps

- Add a `FastAPI` or `Streamlit` front-end for interactive use.
- Persist outputs to a database or FHIR-compatible schema.
- Enhance rule-based components with more robust clinical ontologies (e.g. UMLS).
- Add tests and benchmark scripts against real or synthetic medical dialogues.
