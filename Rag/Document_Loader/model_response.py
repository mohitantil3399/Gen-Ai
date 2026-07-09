import os 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
    max_completion_tokens=1000
)

#loading the document 
data = PyPDFLoader("dataset.pdf")
loaded_pdf = data.load()

#initializing splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000 , chunk_overlap=50)
#making chunks 
splitted_docs = splitter.split_documents(loaded_pdf)

#defining system prompt 
system_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     '''
    You are an assistant that extracts key details from a given document.
    Present the extracted details clearly in bullet points as summary of the given document.
     '''
     ),
    ("human",
      "{document}"
      )
])


# feeding the document to system prompt and getting response 
 
user_prompt = system_prompt.invoke({
    'document':splitted_docs #giving splitted documents to model
})
#getting the response 
reply = client.invoke(user_prompt).content

#printing the output 
print("The assistant says : ",reply)



 