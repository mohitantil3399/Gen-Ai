# Here we will make the logic of retrievel and answer generation
'''FLow ->
take user query -> create embeddings -> query these embeddings to vectorstore->Fetch 
relevant chunks out of the Db -> send the context to the chat model ->
bind the query of user with it , not the query embeddings -> get reponse and print to console.'''
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


#loading environment varibales
load_dotenv()
#defining api key 
api_key = os.getenv('OPENROUTER_API_KEY')

#calling the chat model from openrouter api
client = ChatOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
    temperature=0.2,
    max_completion_tokens=500
)
#defining embedding model
embedding_model = OpenAIEmbeddings(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="text-embedding-3-small"
)
#initializing the vectorstore
vectorStore = Chroma(
    embedding_function=embedding_model,
    persist_directory="Chroma_DB"#This points to the pre-created vectorDb
)
#using retriever
retriever = vectorStore.as_retriever(#using vectorstore retreiver function
    search_type="mmr",#This is type of embeddings search 
    search_kwargs={
        "k":4,#How many chunks to pick up
        "fetch_k":10,
        "lambda_mult":0.6
    }
)
#prompt template 
prompt_template = ChatPromptTemplate.from_messages([
    ("system",'''
    You are a helpful assistant.Answer the question based on the context provided.
    If the answer does not exist in the context , reply "Answer could not be generated".
    Do not answer any other type of question rather the question based on the context.
    '''),
    ("user","Context: {context}\n\n Question: {question}\n Answer:")
])
print("=="*50)
print("\nRag System is ready to take your queries down on Data-Science.\n")
print("=="*50)
print("Enter 'quit'or 'exit' to leave the chat")
print("=="*50)

#creating a chatting system using while loop
while True:
    user_input = input("Ask your query: ")
    if user_input.lower() == "quit" or user_input.lower() == "exit":
        print("Thanks for using the Rag System")
        break
    #retrieve the context from the vectordb

    #convert the user input to embeddings 
    retrieved_docs = retriever.invoke(user_input)
    #storing context as a string
    context = "\n".join([doc.page_content for doc in retrieved_docs])#looped over the retrieved docs to extract page_content and join to the string
    #final prompt 
    final_prompt = prompt_template.invoke({
        "context":context,
        "question":user_input
    })
    #generating the response
    response = client.stream(final_prompt)
    #looping over the response to print the response
    print("assistant says: ")
    for chunk in response:
        print(chunk.content,end="",flush=True)
    print("\n")
    print("=="*50)
