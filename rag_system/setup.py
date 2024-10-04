import os
import subprocess
import time
import sys

# Ensure directories exist
if not os.path.exists('data/iesc111.pdf'):
    print("PDF file not found in 'data/' directory. Please add the PDF and rerun.")
    sys.exit(1)

# Step 1: Extract Text from the PDF
print("\nStep 1: Extracting text from NCERT PDF...")
try:
    if not os.path.exists('models/text_chunks.pkl'):
        subprocess.run(["python", "scripts/extract_text.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred during text extraction: {e}")
    sys.exit(1)

# Step 2: Generate Embeddings and Create FAISS Index
print("\nStep 2: Generating embeddings and creating FAISS index...")
try:
    if not os.path.exists('models/faiss_index.pkl'):
        subprocess.run(["python", "scripts/create_faiss_index.py"], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error occurred during FAISS index creation: {e}")
    sys.exit(1)

# Step 3: Run the FastAPI server
print("\nStep 3: Launching FastAPI server...")
try:
    subprocess.Popen(["python", "main.py"])
    print("FastAPI server is running at http://localhost:8000")
    print("Press Ctrl+C to stop the server.")
    # Allow server to run indefinitely
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("\nStopping FastAPI server...")
