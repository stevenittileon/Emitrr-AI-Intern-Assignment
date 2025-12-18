# bootstrap.py
import sys
import subprocess
import importlib
import json
import re

REQUIRED_PACKAGES = [
    "spacy",
    "nltk",
    "rake-nltk",
    "transformers",
    "torch"
]

SPACY_MODEL = "en_core_web_sm"


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def safe_import(pkg):
    try:
        return importlib.import_module(pkg)
    except ImportError:
        print(f"[INFO] Installing {pkg}...")
        install(pkg)
        return importlib.import_module(pkg)


# Install + import core libraries
spacy = safe_import("spacy")
nltk = safe_import("nltk")
rake_nltk = safe_import("rake_nltk")
transformers = safe_import("transformers")
torch = safe_import("torch")

# Download NLTK resources
try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")
    nltk.download("stopwords")

# Load spaCy model safely
try:
    nlp = spacy.load(SPACY_MODEL)
except:
    print(f"[INFO] Downloading spaCy model {SPACY_MODEL}...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", SPACY_MODEL])
    nlp = spacy.load(SPACY_MODEL)

# Export commonly used classes
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from rake_nltk import Rake
from transformers import pipeline

print("✅ Environment ready")
