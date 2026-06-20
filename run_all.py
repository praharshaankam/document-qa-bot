import os
import sys
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Setup API Keys and Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = "AQ.Ab8RN6JLEytXitck3VUHcrgfj-q_lR4GQHmaqJ4YDZ9vy3m0cA"

genai.configure(api_key=api_key)

DATA_DIR = "./data"
PDF_NAME = "svp answers.pdf"
pdf_path = os.path.join(DATA_DIR, PDF_NAME)

print("====================================================")
print("🔍 Loading and Analyzing the Full Document...")
print("====================================================")

# 2. Automatically read the entire PDF file dynamically
if not os.path.exists(pdf_path):
    print(f"❌ Error: Could not find '{PDF_NAME}' inside the '{DATA_DIR}' folder.")
    print("Please make sure your PDF file is dropped inside D:\\document-qa-bot\\data\\")
    sys.exit(1)

full_document_text = ""
try:
    reader = PdfReader(pdf_path)
    for index, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            full_document_text += f"\n--- PAGE {index + 1} ---\n{text}"
    print(f"✅ Successfully parsed {len(reader.pages)} pages from {PDF_NAME}!")
except Exception as e:
    print(f"❌ Error reading the PDF file: {e}")
    sys.exit(1)

# 3. Define the Strict System Prompt Guardrails
system_prompt = (
    "You are a professional, accurate document Q&A assistant.\n"
    "Answer the user's question using ONLY the provided document context below.\n"
    "Cite the specific page numbers inline next to the facts you mention.\n"
    "If the exact answer cannot be found in the context, clearly state:\n"
    "'I am sorry, but the provided documents do not contain the answer to your question.'\n"
    "Do not make up facts or use external knowledge sources."
)

print("\n====================================================")
print("🤖 Interactive Q&A Session Started!")
print("Type 'exit' or 'quit' to close the program.")
print("====================================================\n")

# 4. Interactive Chat Loop
while True:
    try:
        user_query = input("\n👤 Ask a question: ").strip()
        if not user_query:
            continue
        if user_query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        print("🔍 Analyzing document contents via Gemini...")
        
        # Assemble the payload with the entire document text included dynamically
        prompt = (
            f"{system_prompt}\n\n"
            f"CONTEXT INFORMATION:\n{full_document_text}\n\n"
            f"USER QUESTION: {user_query}\n\n"
            f"GROUNDED ANSWER:"
        )
        
        # Using the standard updated generation model
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        print("\n🤖 ANSWER:")
        print(response.text)
        print("-" * 50)
            
    except Exception as e:
        print(f"\n❌ Error encountered during processing: {e}")