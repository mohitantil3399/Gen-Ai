#sequence : Prompt -> model -> reponse-> parser -> print
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#loading api keys
load_dotenv()
api_key = os.getenv("Grok_KEY")

#initializing model 
client = ChatOpenAI(
    api_key=api_key,
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    max_completion_tokens=500,
    temperature=0.3
)
#taking user input
user_query = input("Enter your query : ")
#prompt template initializing
prompt_template = ChatPromptTemplate.from_template(
   "As a gamer answer to user queries about gaming.Query :{user_query}"

)
#structured output 
structured_output = StrOutputParser()

#Sequence of runnables 
sequence = prompt_template | client | structured_output

#invoking the reponse 
response = sequence.invoke(user_query)
print(response)