import os
import google.generativeai as genai
import chromadb
from dotenv import load_dotenv
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
from config import EMBEDDING_MODEL, LLM_MODEL, DB_PATH

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def query_rag_pipeline(user_query: str, db_path: str = DB_PATH, k: int = 3) -> dict:
    client = chromadb.PersistentClient(path=db_path)
    embedding_fn = GoogleGenerativeAiEmbeddingFunction(
        api_key=api_key,
        model_name=EMBEDDING_MODEL
    )

    try:
        collection = client.get_collection(
            name="document_knowledge_base",
            embedding_function=embedding_fn
        )
    except Exception:
        return {
            "answer": "Error: Knowledge base is empty. Please run data ingestion first.",
            "citations": [],
            "raw_context": []
        }

    results = collection.query(
        query_texts=[user_query],
        n_results=k
    )

    if not results or not results['documents'] or not results['documents'][0]:
        return {
            "answer": "No relevant context found in documents.",
            "citations": [],
            "raw_context": []
        }

    context_blocks = []
    citations = []

    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        source_name = meta['source']
        page_num = meta['page']
        citation_str = f"Source: {source_name}, Page: {page_num}"

        context_blocks.append(f"[{citation_str}]\nContext: {doc}")
        citations.append(citation_str)

    context_payload = "\n\n---\n\n".join(context_blocks)

    system_prompt = (
        "You are a professional, accurate document Q&A assistant. "
        "Answer the user's question using ONLY the provided document context below. "
        "Cite the sources (filenames and pages) inline next to facts you cite. "
        "If the answer cannot be found in the context, clearly state: "
        "'I am sorry, but the provided documents do not contain the answer to your question.' "
        "Do not make up facts or use external knowledge sources."
    )

    prompt = (
        f"{system_prompt}\n\n"
        f"CONTEXT INFORMATION:\n{context_payload}\n\n"
        f"USER QUESTION: {user_query}\n\n"
        f"GROUNDED ANSWER:"
    )

    model = genai.GenerativeModel(LLM_MODEL)
    response = model.generate_content(prompt)

    return {
        "answer": response.text,
        "citations": citations,
        "raw_context": results['documents'][0]
    }