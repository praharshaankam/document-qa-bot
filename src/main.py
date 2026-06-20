import sys
import os

# Ensure Python can find our custom modules when running from the root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from query import query_rag_pipeline

def start_interactive_bot():
    print("====================================================")
    print("🤖 Welcome to your AI Document Q&A Assistant!")
    print("Ask questions based on your loaded custom files.")
    print("Type 'exit' or 'quit' to close the program.")
    print("====================================================\n")

    while True:
        try:
            user_query = input("\n👤 Ask a question: ").strip()
            if not user_query:
                continue
            if user_query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                sys.exit(0)
                
            print("🔍 Searching database and synthesizing response...")
            result = query_rag_pipeline(user_query)
            
            print("\n🤖 ANSWER:")
            print(result["answer"])
            
            if result["citations"]:
                print("\n📚 REFERENCED SOURCES:")
                for citation in set(result["citations"]):
                    print(f" -> {citation}")
                
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    start_interactive_bot()