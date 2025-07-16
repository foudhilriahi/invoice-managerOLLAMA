# Offline Invoice Manager with Ollama and Kaggle OCR

## Overview

This is a fully offline, local Python desktop invoice management app using:

- **Kaggle OCR (Tesseract)** for text extraction from invoices (images or PDFs)  
- **Ollama LLM** for intelligent invoice parsing and JSON output  
- Local SQLite database to save and manage invoices  
- Tkinter GUI with invoice viewer, CSV export, and multi-model support  

---

## Requirements

- Windows 10/11 or compatible OS  
- Python 3.10 or newer  
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed and added to your system `PATH`  
- [PoppyOCR]
- [Ollama](https://ollama.com/) installed and running locally  

---

## Installation Steps

### 1. Clone the repository and set up the Python environment

```bash

cd invoice-manager/src
python -m venv .venv
# Activate virtual environment:
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
2. Install Tesseract OCR
Download the Windows installer from:
https://github.com/tesseract-ocr/tesseract/releases

Install it and add the Tesseract installation folder to your system PATH environment variable

Verify installation by running:

tesseract --version
3. Install Ollama and download the necessary models
Download and install Ollama from https://ollama.com/

Start the Ollama server by running models once (this downloads them):


ollama run llama3
ollama run llama2        # Optional
ollama run gpt4all       # Optional
Alternatively, pull models manually:


ollama pull llama3
ollama pull llama2
ollama pull gpt4all
Running the Application


From inside the src folder with your virtual environment activated, run:

python main.py
Use the "Select LLM Model" dropdown to choose the Ollama model to process invoices.

Click "Upload Invoice File" to select a PDF or image invoice.

The app will OCR the invoice, parse the text with the selected LLM, and save the extracted data.

Switch to the "View Invoices" tab to browse stored invoices.

Export all invoices to CSV using the "Export All to CSV" button.
