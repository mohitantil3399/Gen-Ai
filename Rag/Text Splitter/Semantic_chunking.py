from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv

#loading the pdf 
data = PyPDFLoader("dataset.pdf")
loaded_pdf = data.load()

# Load your API key from .env
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

#making embeddings to find semantic meanings 
# Initialize embeddings client
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",   # or "text-embedding-3-large"
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"  # OpenRouter endpoint
)

#initializing splitter
splitter = SemanticChunker(embeddings)

#making chunks 
splitted_docs = splitter.split_documents(loaded_pdf)

#printing the chunks 
print(f"length of the splitted documents list : {len(splitted_docs)}\n")
for chunk in splitted_docs:
    print(chunk.page_content)
    print("=="*50 + "\n")