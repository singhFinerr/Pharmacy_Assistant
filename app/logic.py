import pandas as pd
import re
from datetime import datetime

# Load patient data once
patients_df = pd.read_excel("data/fake_patient_records.xlsx", dtype=str)

# Normalize DOB
def normalize_dob(dob_str):
    if not dob_str:
        return None
    dob_str = dob_str.strip()
    formats = ["%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(dob_str, fmt)
            return dt.strftime("%m/%d/%Y")
        except ValueError:
            continue
    return dob_str

patients_df["DOB_norm"] = patients_df["DOB"].apply(normalize_dob)

def extract_dob_from_text(text: str):
    """Find DOB in free text."""
    match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    if match:
        return match.group(1)
    return None

def extract_name_from_text(text: str):
    """Find patient name in text (basic heuristic)."""
    match = re.search(r"(?:my name is|i am|this is)\s+([A-Za-z]+ [A-Za-z]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).title()
    return None

def find_patient(dob: str, name: str = None):
    """Look up patient in the Excel file."""
    dob_norm = normalize_dob(dob)
    matches = patients_df[patients_df["DOB_norm"] == dob_norm]

    if name and not matches.empty:
        exact = matches[matches["Customer"].str.lower() == name.lower()]
        if not exact.empty:
            return exact.iloc[0].to_dict()
    if not matches.empty:
        return matches.iloc[0].to_dict()
    return None

def handle_query(user_text: str, current_patient: dict = None):
    """Main assistant logic."""
    dob = extract_dob_from_text(user_text)
    name = extract_name_from_text(user_text)

    patient = None
    if dob:
        patient = find_patient(dob, name)
    elif current_patient:
        patient = current_patient

    controlled_keywords = [
        "oxycodone", "adderall", "xanax", "fentanyl",
        "morphine", "hydrocodone", "vicodin", "percocet"
    ]

    if any(word in user_text.lower() for word in controlled_keywords):
        return "For controlled medications, please speak directly with a pharmacist.", None

    if patient:
        if str(patient.get("Controlled", "")).lower() == "yes":
            return (
                f"Patient {patient['Customer']} ({patient['DOB']}): "
                "This is a controlled substance. Please contact the pharmacist directly."
            ), patient
        else:
            refill_info = patient.get("Refill", "No data")
            newrx_info = patient.get("NewRx", "No data")
            return (
                f"Patient {patient['Customer']} ({patient['DOB']}): "
                f"Refills: {refill_info}. New prescriptions: {newrx_info}."
            ), patient

    if any(kw in user_text.lower() for kw in ["refill", "prescription", "medication", "rx"]):
        return "I need your date of birth and full name to look up prescriptions.", None

    return "Hello, I am Hopkins Pharmacy Assistant. Can you provide your DOB and full name?", None
