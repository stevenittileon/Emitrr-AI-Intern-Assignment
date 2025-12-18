# 🩺 Physician Notetaker – Medical NLP Pipeline

An end-to-end **Natural Language Processing (NLP) system** for analyzing
**physician–patient conversations** and converting them into structured,
clinically meaningful information using **pretrained Transformer models**.

This project runs **fully locally** and is designed to generalize across
different medical dialogue formats.

---

## 📌 Project Objectives

This project addresses the following tasks:

### 1. Medical NLP Summarization
- Extract key medical details:
  - Symptoms
  - Diagnosis
  - Treatment
  - Prognosis
- Generate structured medical summaries
- Identify important medical keywords

### 2. Sentiment & Intent Analysis
- Classify patient sentiment as:
  - **Anxious**
  - **Neutral**
  - **Reassured**
- Detect patient intent such as:
  - Reporting symptoms
  - Seeking reassurance
  - Expressing improvement

### 3. SOAP Note Generation (Bonus)
- Convert free-text medical conversations into **SOAP notes**:
  - **Subjective**
  - **Objective**
  - **Assessment**
  - **Plan**

---

## 🗂 Project Structure

emittr/
│
├── summarizer.py # Medical entity extraction & clinical summarization
├── sentiment_intent.py # Patient sentiment and intent analysis
├── soap_generator.py # SOAP note generation (bonus)
│
├── sample_transcript.txt # Example physician–patient conversation
├── requirements.txt # Project dependencies
└── README.md # Project documentation


---

## 📄 File Descriptions

### 🔹 `summarizer.py`
Implements the **Medical NLP Summarization** task.

**Responsibilities:**
- Biomedical Named Entity Recognition (NER)
- Extraction of:
  - Symptoms
  - Diagnosis
  - Treatment
  - Current patient status
- Keyword extraction using YAKE
- Clinical summarization using BART

**Output:**  
Structured medical summary in JSON format.

---

### 🔹 `sentiment_intent.py`
Implements **Sentiment & Intent Analysis**.

**Responsibilities:**
- Transformer-based sentiment classification
- Detection of patient intent

**Output Example:**
```json
{
  "Sentiment": "Reassured",
  "Intent": "Expressing improvement"
}

🔹 soap_generator.py

Implements SOAP Note Generation (Bonus).

Responsibilities:

Converts unstructured transcripts into structured SOAP format:

Subjective

Objective

Assessment

Plan

Output:
SOAP note in JSON format.

⚙️ Installation & Setup
Prerequisites

Python 3.10+ (Python 3.13 supported)

Works on Windows, Linux, and macOS

Step 1: Create Virtual Environment (Recommended)
python -m venv venv


Activate the environment:

Windows

venv\Scripts\activate


macOS / Linux

source venv/bin/activate

Step 2: Install Dependencies
pip install -r requirements.txt


If requirements.txt is not present:

pip install spacy transformers torch yake
python -m spacy download en_core_web_sm

▶️ How to Run
1️⃣ Medical Summarization
python summarizer.py


Output:
Structured medical summary in JSON format.

2️⃣ Sentiment & Intent Analysis
python sentiment_intent.py

3️⃣ SOAP Note Generation (Bonus)
python soap_generator.py

🧠 Pretrained Models Used
Task	Model
Biomedical NER	d4data/biomedical-ner-all
Summarization	facebook/bart-large-cnn
Sentiment Analysis	distilbert-base-uncased-finetuned-sst-2-english
Linguistic Parsing	spaCy en_core_web_sm
Keyword Extraction	YAKE

✔ No fine-tuning required
✔ Fully local execution

🧪 Generalization & Robustness

No hardcoded symptoms or diagnoses

Works on unseen physician–patient conversations

Model-driven extraction ensures robustness

Easily extendable to APIs or EHR systems

🎯 Academic & Interview Readiness

This project demonstrates:

End-to-end NLP pipeline design

Practical use of pretrained Transformer models

Medical text understanding and structuring

Robust handling of real-world clinical transcripts

🚀 Future Improvements

FastAPI backend for real-time usage

UMLS concept linking

Confidence scoring for extracted entities

Database or FHIR integration


---

If you want next:
- ✅ `requirements.txt`
- ✅ Clean sample input/output files
- ✅ Final code review for submission
- ✅ GitHub-ready project polish

Just tell me 👍
