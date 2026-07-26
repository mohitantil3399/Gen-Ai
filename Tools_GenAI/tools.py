from dotenv import load_dotenv
import os
import datetime 
from langchain_tavily import TavilySearch 
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
#Tavily key 
Tavily_key = os.getenv("TAVILY_API_KEY")
#Model intialization
api_key = os.getenv("MISTRAL_API_KEY")
client = ChatMistralAI(
    model_name="mistral-small-latest",
    api_key=api_key
)

# Instantiate the search tool 

search_tool = TavilySearch(
    max_results=5,
    include_raw_content=True,
    include_images=False
)
#prompt template
prompt_template = ChatPromptTemplate.from_template(
    '''Act as a news anchor.
    State the new ai model launches with their features in 7 proper bullet points.
    News:{news}'''
)
# use today's date
today_date = datetime.date.today()

# build a direct, specific search query to ensure relevant and updated results
search_query_generation = client.invoke(f"Write a search query for the tavily search tool to fetch information related to New AI model launches as of date: {today_date.strftime('%B %Y')}.Returen only the search query string , no conversational bluff.")
search_query_text = search_query_generation.content

# running the search (the search tool expects a text query)
search_results = search_tool.run(search_query_text)

#create sequence of runnables
sequence = prompt_template | client | StrOutputParser()

#invoke for the results 
response = sequence.invoke({"news":search_results})
print(response)