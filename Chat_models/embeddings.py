import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Load your API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize embeddings client
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",   # or "text-embedding-3-large"
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"  # OpenRouter endpoint
)

# Example texts
texts = [
    "LangChain makes LLM orchestration easy.",
    "FAISS is great for similarity search.",
    "OpenRouter lets you access multiple models."
]

# Create embeddings
vector_list = embeddings.embed_documents(texts)

print(vector_list,"\n\n")
print("Number of vectors:", len(vector_list))
print("\nDimension of each vector:", len(vector_list[0]))
print("\nFirst vector (truncated):", vector_list[0][:10])  # show first 10 values
