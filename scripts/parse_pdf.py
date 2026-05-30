import fitz # PyMuPDF
import sys

pdf_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\DV1597_Assignment_2.pdf"
output_path = r"c:\Users\bilal\OneDrive - BTH Student\Canvas Kurser\Itelligentdata analys\Assigment 2\pdf_text.txt"

try:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n\n"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully extracted PDF text!")
except Exception as e:
    print(f"Error: {e}")
