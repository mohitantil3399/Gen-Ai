from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#loading environment variables
load_dotenv()

#api keys 
api_key = os.getenv("OPENROUTER_API_KEY")

#intializing client 
client = ChatOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
    temperature=0.2,
    max_completion_tokens=600
)

#prompt template 
prompt_template = ChatPromptTemplate.from_messages([
    ("system", 
     '''
    You are an assistant that gives the notes of the topic asked by the students of Btech cse.
      '''
     ),
    ("human",
      "{paragraph}"
      )
])

#output parsing
parser = StrOutputParser()

#creating chain 
chain = prompt_template | client | parser

reponse = chain.invoke("Runnables in langchain.Give proper structured notes.")

print(reponse)