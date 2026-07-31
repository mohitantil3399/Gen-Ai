#Here we create the agents that will use those tools we created in Tools.py
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search ,tavily_search

#loading api keys
load_dotenv()

api_key = os.getenv("Groq_KEY")

#setting up the client 
groq_client = ChatOpenAI(
    api_key= api_key,
    base_url = "https://api.groq.com/openai/v1",
    model = "llama-3.3-70b-versatile",
    temperature=0.1,
    timeout=30,
) 
openrouter_api = os.getenv("OPENROUTER_API_KEY")
#creating client for openrouter
openrouter_client = ChatOpenAI(
    api_key= openrouter_api,
    base_url = "https://openrouter.ai/api/v1",
    model= "openrouter/free",
    temperature=0.1,
    timeout=30,
)
#mistral client 
mistral_key = os.getenv("MISTRAL_API_KEY")
mistral_client = ChatMistralAI(
    api_key= mistral_key,
    model= "mistral-medium-3-5",
    temperature=0.1,
    timeout=80,
)
#1st agent 
def search_agent():
    return create_agent(
        model = groq_client,
        tools = [tavily_search]
    )

#2nd agent 
def scrape_url_agent():
    return create_agent(
        model=mistral_client,
        tools=[web_search]
    )
#creating writer agent 

#initializing the prompt template
writer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a world-class technical writer"),
        ("human","""Write a detailed Research on the topic: '{topic}' \n
        Gathered data : '{gathered_data}'\n
        Structure the report as follows:
        1. Title: Clearly mention the topic name , headings , subheadings , etc.
        2. Summary: Briefly Summarize the content of the report.
        3. Body:  Use the gathered data to provide insights , details , and a thorough analysis of the topic. Synthesize information from multiple sources. Do not rely on just one source. Provide technical depth and thorough evaluation.
        4. Conclusion:Provide a concluding summary based on your analysis.
        5. Citations: Include proper citations for all the data used.Include proper URLs and sources.
        Do NOT add any extra information or formatting. Only provide the report.
        """)
    ]
)
#Writer sequence of runnables 
writer_sequence = writer_prompt|mistral_client|StrOutputParser()

#critic_sequence : to analyse my research and score it
critic_prompt = ChatPromptTemplate.from_messages([
    ("system","You are a World-class research report analyst and critic. Your job is to rigorously evaluate research reports and provide a clear, actionable critique."),
    ("human",
    """Critique this Research Report and assign a "final score" out of 10.
Topic: {topic}
Report:
{report}
Guidelines:
- Evaluate for accuracy, depth, clarity, structure, and proper citation.
- Provide a score from 0 to 10.
- If the score is below 7, suggest specific improvements.
- Return your critique and score clearly formatted.""")

])
#critic sequence 
critic_sequence = critic_prompt|groq_client|StrOutputParser()
