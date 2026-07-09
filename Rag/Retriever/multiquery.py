'''
User query: "What is AI?"
        ↓
ChatMistralAI generates 3 variations automatically:
  → "Define artificial intelligence"
  → "How do machines simulate human intelligence?"
  → "What are the applications of AI?"
        ↓
Each variation searches the vector store (k=2 each)
        ↓
All unique results are merged and returned

'''
import os
import logging
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_mistralai import ChatMistralAI
from langchain_classic.retrievers import MultiQueryRetriever

# enable logging to see the queries Mistral generates
logging.basicConfig()
logging.getLogger("langchain_classic.retrievers.multi_query").setLevel(logging.INFO)

# load api keys
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# sample documents
docs = [
    Document(page_content="The Taj Mahal is a massive mausoleum of white marble, built in Agra, India, by the Mughal emperor Shah Jahan in memory of his favorite wife, Mumtaz Mahal. Construction began around 1632 and was largely completed by 1648. It is widely regarded as one of the world's most beautiful buildings.",metadata={"source":"Taj Mahal"}),
    Document(page_content="The Eiffel Tower is an iconic wrought-iron lattice tower located on the Champ de Mars in Paris, France. Designed and built by Gustave Eiffel's company for the 1889 World's Fair, it stands 330 meters (1,083 feet) tall. It was the world's tallest man-made structure for 41 years and is a global cultural icon of France.",metadata={"source":"Eiffel Tower"}),
    Document(page_content="Python is a high level general purpose scripting and programming language. Python is widely used in the AI industry for ML , data science roles .",metadata={"source":"Python"}),
    Document(page_content="Artificial Intelligence (AI) refers to the simulation of human intelligence in machines, enabling them to perform tasks like learning, reasoning, problem-solving, perception, and decision-making.",metadata={"source":"AI"}),
    Document(page_content="Machine Learning (ML) is a subset of AI that involves training algorithms to learn patterns from data and make predictions or decisions without being explicitly programmed for every scenario.",metadata={"source":"ML"})
]

# initialize embedding model and vector store
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vectorstore = Chroma.from_documents(docs, embedding_model)

# initialize Mistral LLM
llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=mistral_api_key,
    temperature=0
)

# create MultiQuery retriever — Mistral will auto-generate 3 query variations
multiquery_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    llm=llm
)

# invoke with the original question
print("="*40, "MultiQuery Search Results", "="*40)
retrieved_docs = multiquery_retriever.invoke("What is AI?")

# print unique results
for i, doc in enumerate(retrieved_docs):
    print(f"\n Result {i+1} | Source: {doc.metadata['source']}")
    print(doc.page_content)
