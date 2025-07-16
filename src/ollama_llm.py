import subprocess
import os
from config import SELECTED_MODEL

OLLAMA_EXE = r"C:\Users\DELL\AppData\Local\Programs\Ollama\ollama.exe"

def run_ollama(prompt, model_name=SELECTED_MODEL):
    if not os.path.exists(OLLAMA_EXE):
        return f"LLM Error: Could not find Ollama executable at {OLLAMA_EXE}"

    print(f"🧠 Sending prompt to Ollama with model {model_name}...")
    try:
        result = subprocess.run(
            [OLLAMA_EXE, "run", model_name],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=120
        )
        stdout = result.stdout.decode("utf-8").strip()
        stderr = result.stderr.decode("utf-8").strip()
        print("🧠 LLM STDOUT:", stdout)
        print("🧠 LLM STDERR:", stderr)
        return stdout or f"LLM Error: Empty output\n{stderr}"
    except Exception as e:
        return f"LLM Error: {e}"

def generate_invoice_json(text, model_name=None):
    if model_name is None:
        model_name = SELECTED_MODEL

    prompt = f"""
You are an expert invoice parser AI with excellent comprehension and reasoning skills.

Given the raw OCR text of an invoice, extract these fields as accurately as possible:

- supplier: Issuer company name
- customer: Recipient name
- invoice_number: Invoice ID
- date: Invoice date (YYYY-MM-DD)
- due_date: Payment due date (YYYY-MM-DD)
- items: List of purchased items with description, quantity, unit_price, total_price
- subtotal: Amount before tax
- taxes: Tax amount or percentage
- total_amount: Total invoice amount
- currency: Currency code (e.g., EUR, USD)
- payment_terms: Payment conditions or notes
- address_supplier: Supplier address
- address_customer: Customer address


Output a valid JSON object  
If a field is missing, try to infer it.

Format example:

{
  "supplier": "ABC Corp",
  "customer": "XYZ Ltd",
  "invoice_number": "INV-12345",
  "date": "2023-07-15",
  "due_date": "2023-08-15",
  "items": [
    {
      "description": "Product A",
      "quantity": 2,
      "unit_price": 50.0,
      "total_price": 100.0
    },
    {
      "description": "Service B",
      "quantity": 3,
      "unit_price": 100.0,
      "total_price": 300.0
    }
  ],
  "subtotal": 400.0,
  "taxes": 80.0,
  "total_amount": 480.0,
  "currency": "EUR",
  "payment_terms": "Net 30"
}

OCR text to analyze:

{text}

"""
    return run_ollama(prompt, model_name)
