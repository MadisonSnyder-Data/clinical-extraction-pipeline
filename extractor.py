import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Reading .env file
load_dotenv()


SCHEMA_KEYS = [
    "visit_date",
    "primary_complaint",
    "blood_pressure",
    "medication_name",
    "dosage_instructions",
]


# Unstructured Medical Note
unstructured_note = """
Patient presented today, Feb 18, 2026, complaining of a persistent cough. 
BP was 120/80. Prescribed Amoxicillin 500mg to be taken twice daily for 10 days. 
Follow-up in two weeks.
"""

# Extraction Function
def extract_clinical_data(text_input: str) -> dict:
    """
    Uses an LLM to extract structured clinical fields from raw notes.
    Returns a Python dict.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set. Cannot run live extraction.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a clinical data assistant...
...
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    return json.loads(content)


# Execution
# result = extract_clinical_data(unstructured_note)
# print(result)

def mock_extract_clinical_data(text_input: str) -> dict:
    """
    Simulates an AI response for testing purposes.
    """
    return {
        "visit_date": "2026-02-18",
        "primary_complaint": "persistent cough",
        "blood_pressure": "120/80",
        "medication_name": "Amoxicillin",
        "dosage_instructions": "500mg twice daily for 10 days",
    }


# Validation Layer with Logging
def validate_and_log(record):
    """
    Validates extracted clinical data.
    Accepts either a dict (preferred) or a JSON string (legacy).
    Logs errors to error_log.txt with timestamps.
    """
    # Accept dict or JSON string
    if isinstance(record, str):
        try:
            data = json.loads(record)
        except json.JSONDecodeError:
            data = {}
            errors = ["Invalid JSON: could not decode record"]
    elif isinstance(record, dict):
        data = record
        errors = []
    else:
        data = {}
        errors = [f"Invalid type: expected dict or str, got {type(record).__name__}"]

    # ---- Validation checks ----

    # 1) Date format check (YYYY-MM-DD)
    visit_date = data.get("visit_date")
    try:
        if visit_date:
            datetime.strptime(visit_date, "%Y-%m-%d")
        else:
            errors.append("Missing visit_date")
    except ValueError:
        errors.append(f"Invalid visit_date format: {visit_date}")

    # 2) Blood pressure basic format + numeric sanity
    bp = data.get("blood_pressure")
    if not bp:
        errors.append("Missing blood_pressure")
    else:
        if "/" not in bp:
            errors.append(f"Invalid blood_pressure format (missing '/'): {bp}")
        else:
            left, right = bp.split("/", 1)
            try:
                sys = int(left.strip())
                dia = int(right.strip())
                if sys <= dia:
                    errors.append(f"Blood pressure logic error (systolic <= diastolic): {bp}")
                if not (60 <= sys <= 250):
                    errors.append(f"Systolic out of expected range: {sys}")
                if not (30 <= dia <= 150):
                    errors.append(f"Diastolic out of expected range: {dia}")
            except ValueError:
                errors.append(f"Blood pressure must be numeric like '120/80': {bp}")

    # 3) Medication presence (light rule)
    med = data.get("medication_name")
    if not med or not str(med).strip():
        errors.append("Missing medication_name")

    # 4) Dosage presence (light rule)
    dose = data.get("dosage_instructions")
    if not dose or not str(dose).strip():
        errors.append("Missing dosage_instructions")

    # ---- Logging ----
    if errors:
        with open("logs/error_log.txt", "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for error in errors:
                log_file.write(f"[{timestamp}] {error} | record={data}\n")

        return False, f"Logged {len(errors)} error(s) to error_log.txt"

    return True, "Data is valid."

def main():
    use_mock = os.getenv("USE_MOCK", "true").lower() in ("true", "1", "yes")

    if use_mock:
        record = mock_extract_clinical_data(unstructured_note)
    else:
        record = extract_clinical_data(unstructured_note)

    is_valid, status_msg = validate_and_log(record)
    output_path = "outputs/structured.json"
    with open(output_path, "w") as f:
        json.dump(record, f, indent=2)

    print(f"Status: {status_msg}")
    print(f"Saved structured output to: {output_path}")
    if not is_valid:
        print("See logs/error_log.txt for details.")




if __name__ == "__main__":
    main()


