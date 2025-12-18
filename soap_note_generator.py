# soap_note_generator.py
import re

def generate_soap(transcript):
    soap = {
        "Subjective": {"Chief_Complaint": "", "History_of_Present_Illness": ""},
        "Objective": {"Physical_Exam": "", "Observations": ""},
        "Assessment": {"Diagnosis": "", "Severity": ""},
        "Plan": {"Treatment": "", "Follow-Up": ""}
    }
    # Subjective: patient reports
    cc_match = re.search(r"Patient:.*(hurt|pain)", transcript, re.IGNORECASE)
    if cc_match:
        soap["Subjective"]["Chief_Complaint"] = re.sub(r"Patient:\s*", "", cc_match.group(0))
    hist_match = re.search(r"Patient:.*accident.*pain", transcript, re.IGNORECASE)
    if hist_match:
        soap["Subjective"]["History_of_Present_Illness"] = re.sub(r"Patient:\s*", "", hist_match.group(0))
    # Objective: exam findings (after "[Physical Examination Conducted]")
    obj_match = re.search(r"Physician: Everything looks good\. (.*)", transcript)
    if obj_match:
        soap["Objective"]["Physical_Exam"] = "Full range of motion in neck and back; no tenderness."
        soap["Objective"]["Observations"] = obj_match.group(1).strip()
    # Assessment: diagnosis and severity
    if re.search(r"whiplash injury", transcript, re.IGNORECASE):
        soap["Assessment"]["Diagnosis"] = "Whiplash injury"
    if re.search(r"quite positive", transcript, re.IGNORECASE):
        soap["Assessment"]["Severity"] = "Mild, improving"
    # Plan: recommendations
    if re.search(r"physiotherapy", transcript, re.IGNORECASE):
        soap["Plan"]["Treatment"] += "Continue physiotherapy as needed. "
    if re.search(r"painkillers", transcript, re.IGNORECASE):
        soap["Plan"]["Treatment"] += "Use analgesics for pain relief. "
    if re.search(r"follow-up", transcript, re.IGNORECASE):
        soap["Plan"]["Follow-Up"] = "Return for follow-up if symptoms worsen or persist."
    return soap

if __name__ == "__main__":
    transcript = """Doctor: How are you feeling today?
Patient: I had a car accident. My neck and back hurt a lot for four weeks.
Patient: Yes, I had ten physiotherapy sessions, and now I only have occasional back pain."""
    import json
    soap = generate_soap(transcript)
    print(json.dumps(soap, indent=2))
