import os 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

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
#defining system prompt 
system_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     '''
    You are an assistant that extracts key details from a given document.
    Present the extracted details clearly in bullet points.
     '''
     ),
    ("human",
      "{document}"
      )
])
#loading the document 
data = PyPDFLoader("dataset.pdf")
loaded_pdf = data.load()

# feeding the document to system prompt and getting response 
user_prompt = system_prompt.invoke({
    'document':loaded_pdf
})
#getting the response 
reply = client.invoke(user_prompt).content

#printing the output 
print("The assistant says : ",reply)

 