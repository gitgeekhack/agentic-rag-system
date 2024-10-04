import pickle
from app.pdf_parser import extract_text_from_pdf, data_formatter

# File paths
pdf_path = 'data/iesc111.pdf'
output_path = 'models/text_chunks.pkl'

# Extract text from the PDF
print(f"Extracting text from {pdf_path}...")
raw_text = extract_text_from_pdf(pdf_path)

# Preprocess the text into manageable chunks
text_chunks = data_formatter(raw_text)

# Save the text chunks as a pickle file
with open(output_path, 'wb') as f:
    pickle.dump(text_chunks, f)

print(f"Text chunks saved to {output_path}")
