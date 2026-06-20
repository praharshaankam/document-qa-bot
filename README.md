# document-qa-bot

# AI-Driven Document Q&A Assistant

An intelligent RAG (Retrieval-Augmented Generation) pipeline built to extract text from custom PDF documents, process the context, and provide fully grounded answers using the Gemini API.

## 🚀 Features
* **Full PDF Ingestion:** Automating text extraction dynamically across multi-page PDFs using `pypdf`.
* **Strict Grounding Guardrails:** Custom system prompts to prevent hallucinations and strictly restrict the model to local document context.
* **Interactive Q&A Loop:** Clean, terminal-based user interface for continuous querying.

## 🏗️ Architecture & Implementation Details
* **Language:** Python
* **Core Models:** `gemini-2.5-flash` for optimized, high-speed text synthesis.
* **Pipeline Design:** Transitioned from a vector-store chunking index to a direct memory context extraction system to safely handle library endpoint shifts.

## ⚙️ Setup Instructions
1. Clone the repository: `git clone https://github.com/praharshaankam/document-qa-bot`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `.\venv\Scripts\Activate.ps1`
4. Install dependencies: `pip install pypdf google-generativeai python-dotenv`
5. Run the application: `python run_all.py`
