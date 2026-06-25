import fitz

pdf_path = "MLE.pdf"   # replace with your actual PDF filename

doc = fitz.open(pdf_path)

text = ""

for page in doc:
    text += page.get_text()

print(text)

with open("pymupdf_output.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("\nSaved output to pymupdf_output.txt")