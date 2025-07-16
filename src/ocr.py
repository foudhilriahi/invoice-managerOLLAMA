import pytesseract
import cv2
from PIL import Image
from pdf2image import convert_from_path
import os
import shutil

if not shutil.which("tesseract"):
    raise EnvironmentError("⚠️ Tesseract-OCR is not installed or not in PATH. Please install and add to PATH.")
def extract_text_from_image(img_path):
    image = cv2.imread(img_path)
    if image is None:
        raise ValueError(f"Failed to read image: {img_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray)

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text_output = ""
    for page in images:
        text_output += pytesseract.image_to_string(page)
    return text_output

def extract_text(file_path):
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    else:
        return extract_text_from_image(file_path)
def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Text extracted and saved to {output_path}")