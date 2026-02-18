# Clinical Note Extraction & Validation Pipeline

This project implements an end-to-end data pipeline that converts unstructured clinical notes into validated, structured JSON records using an LLM-based extraction layer combined with rule-based validation logic.

The system is designed with modular architecture, artifact generation, logging, and mock inference support to simulate a production-style data workflow.

---

## Overview

Unstructured medical documentation is difficult to search, validate, and analyze at scale.

This pipeline demonstrates how raw text can be transformed into analytics-ready structured data through:

1. LLM-based structured extraction  
2. Schema normalization  
3. Rule-based validation  
4. Error logging  
5. Artifact generation  

The result is a clean JSON output ready for downstream analytics or database storage.

---

## Features

### LLM-Powered Structured Extraction

Extracts the following clinical fields:

- `visit_date` (ISO format: YYYY-MM-DD)
- `primary_complaint`
- `blood_pressure`
- `medication_name`
- `dosage_instructions`

The extraction layer:
- Enforces structured JSON output  
- Returns null for missing fields  
- Supports live API or mock inference mode  

---

### Validation Layer

Implements rule-based quality checks:

- ISO date format validation  
- Blood pressure format validation (`systolic/diastolic`)  
- Numeric range checks for BP values  
- Logical validation (systolic > diastolic)  
- Medication presence checks  

Validation errors are automatically written to:

```
logs/error_log.txt
```

---

### Mock Inference Mode

Supports offline testing without API usage.

Run in mock mode (default):

```bash
python extractor.py
```

Run with live API extraction:

```bash
USE_MOCK=false python extractor.py
```

---

## Output Artifacts

Structured results are automatically saved to:

```
outputs/structured.json
```

This simulates real-world pipeline artifact generation.

---

## Project Structure

```
extractor.py
outputs/
  └── structured.json
logs/
  └── error_log.txt
.env.example
requirements.txt
README.md
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python extractor.py
```

### 3. Optional: Enable live API mode

```bash
USE_MOCK=false python extractor.py
```

---

## Technologies Used

- Python 3.x  
- OpenAI API  
- python-dotenv  
- JSON schema normalization  
- Rule-based validation framework  



