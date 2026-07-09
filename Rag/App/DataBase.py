'''
Loading the pdf 
Split into chunks 
Create embeddings 
Store the embeddings into ChromaDb
'''

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import os
import time
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma


#loading api keys 
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

#loading our documents 
data = PyPDFLoader("Data_Science.pdf")
loaded_pdf = data.load()

#initializing splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 3000,
    chunk_overlap = 200
)

#splitting the documents 
splitted_docs = splitter.split_documents(loaded_pdf)
print(f"No. of chunks : {len(splitted_docs)}")

#calling the chat model from openrouter api
embedding_model = OpenAIEmbeddings(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="text-embedding-3-small"
)

#intializing vector store
vectorStore = Chroma(
    embedding_function=embedding_model,
    persist_directory="Chroma_DB"
)
# Process in batches
BATCH_SIZE = 50  # tune this down if still hitting limits
DELAY = 10       # seconds to wait between batches
for i in range(0, len(splitted_docs), BATCH_SIZE):
    batch = splitted_docs[i : i + BATCH_SIZE]#definig the documents in batch of 50 ,using list split method
    vectorStore.add_documents(batch)#adding the document into vector db
    #printing until it happens to finish
    print(f"✅ Batch {i // BATCH_SIZE + 1} done ({i + len(batch)}/{len(splitted_docs)})")

    # Don't sleep after the last batch
    if i + BATCH_SIZE < len(splitted_docs):
        time.sleep(DELAY)
print("🎉 All chunks embedded and stored!")