# Here we will make the logic of retrievel and answer generation

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


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

