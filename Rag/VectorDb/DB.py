from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

#loading api keys 
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

#creating sample documents for practicing 
documents = [
    Document(page_content = "The Taj Mahal is a massive mausoleum of white marble, built in Agra, India, by the Mughal emperor Shah Jahan in memory of his favorite wife, Mumtaz Mahal. Construction began around 1632 and was largely completed by 1648. It is widely regarded as one of the world’s most beautiful buildings.",metadata ={"source":"Taj Mahal"} ),
    Document(page_content = "The Eiffel Tower is an iconic wrought-iron lattice tower located on the Champ de Mars in Paris, France. Designed and built by Gustave Eiffel’s company for the 1889 World’s Fair, it stands 330 meters (1,083 feet) tall. It was the world’s tallest man-made structure for 41 years and is a global cultural icon of France.",metadata={"source":"Eiffel Tower"}),
    Document(page_content="Python is a high level general purpose scripting and programming language. Python is widely used in the AI industry for ML , data science roles .",metadata={"source":"Python"}),
    Document(page_content="Artificial Intelligence (AI) refers to the simulation of human intelligence in machines, enabling them to perform tasks like learning, reasoning, problem-solving, perception, and decision-making.",metadata={"source":"AI"}),
    Document(page_content="Machine Learning (ML) is a subset of AI that involves training algorithms to learn patterns from data and make predictions or decisions without being explicitly programmed for every scenario.",metadata={"source":"ML"})
]

#intializing embedding model : 
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",   # or "text-embedding-3-large"
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"  # OpenRouter endpoint
)

#intializing vector store
vectorStore = Chroma.from_documents(
    embedding = embedding_model,
    documents = documents,
    persist_directory="Chroma_DB"#this creates a vector db for the above mentioned text documents.
)
 
