import os 
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


#loading environment variables
load_dotenv()
#API key setup 
api_key = os.getenv("MISTRAL_API_KEY")
#loading model 
client = ChatMistralAI(model="mistral-small-latest",api_key=api_key)
#prompt_template 
#user input 
query = input("Enter your query : ")
prompt_template =ChatPromptTemplate.from_template("Explain like a professor. Topic :{query} ")
#chain setting
chain = prompt_template | client | StrOutputParser()
for chunk in chain.stream({"query": query}):
    print(chunk, end="", flush=True)