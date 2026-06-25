from parser import extract_text_from_pdf

text = extract_text_from_pdf("MLE.pdf")

print(text[:1000])