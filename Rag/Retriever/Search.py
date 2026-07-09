from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

docs = [
    Document(page_content="The Taj Mahal is a massive mausoleum of white marble, built in Agra, India, by the Mughal emperor Shah Jahan in memory of his favorite wife, Mumtaz Mahal. Construction began around 1632 and was largely completed by 1648. It is widely regarded as one of the world’s most beautiful buildings.",metadata={"source":"Taj Mahal"}),
    Document(page_content="The Eiffel Tower is an iconic wrought-iron lattice tower located on the Champ de Mars in Paris, France. Designed and built by Gustave Eiffel’s company for the 1889 World’s Fair, it stands 330 meters (1,083 feet) tall. It was the world’s tallest man-made structure for 41 years and is a global cultural icon of France.",metadata={"source":"Eiffel Tower"}),
    Document(page_content="Python is a high level general purpose scripting and programming language. Python is widely used in the AI industry for ML , data science roles .",metadata={"source":"Python"}),
    Document(page_content="Artificial Intelligence (AI) refers to the simulation of human intelligence in machines, enabling them to perform tasks like learning, reasoning, problem-solving, perception, and decision-making.",metadata={"source":"AI"}),
    Document(page_content="Machine Learning (ML) is a subset of AI that involves training algorithms to learn patterns from data and make predictions or decisions without being explicitly programmed for every scenario.",metadata={"source":"ML"})
]

embedding_model = HuggingFaceEmbeddings()

vectorstore = Chroma.from_documents(docs,embedding_model)
#defining similarity search retrieval 
similarity_retreiver = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k":2}
)
#making a similarity search for a query
similar_docs = similarity_retreiver.invoke("What is AI.")

#printing the results of similarity search
print("="*40,"Similarity Search results","="*40)
#using loop to loop over the similarity docs
for doc in similar_docs:
    print(doc.page_content)

#defining MMR search retrieval 
mmr_retreiver = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k":2,
    "lambda_mult":0.6}
)
#making a MMR search for a query
mmr_docs = mmr_retreiver.invoke("What is AI.")

#printing the results of similarity search
print("="*40,"MMR Search results","="*40)
#using loop to loop over the similarity docs
for doc in mmr_docs:
    print(doc.page_content)