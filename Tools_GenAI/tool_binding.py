from rich import print 
import os
import datetime
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

'''Tool binding is connecting the tools to the LLM for it can use it whenever needed.
We give the tools to the LLM and it knows what is has and how can it use them for the work.'''
'''
Steps ->
  *Tool defining ->We define tool with @Tool annotation in the form of a function.
  *Tool Binding ->We tell the llm about the available tools so it can use them.
  *Tool Calling ->LLM chooses to use the tool.
  *Tool Execution ->The tool is actually running after having chosen.
  *Response generation -> The tool results are analyzed by the llm to return the response.
  '''

#Finding today's date 
date = datetime.date.today()

#loading environment variables
load_dotenv()
api_key = os.getenv("Groq_KEY")
#Initializing the client 
client = ChatOpenAI(
    api_key=api_key,
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    temperature=0.7,
    max_completion_tokens=4096
)
# Instantiate the search tool predefined tools

search_tool = TavilySearch(
    max_results=5,
    include_raw_content=False,
    include_images=False
)
#self created tool 
@tool
def length_string(text:str)->int:
    """This tool returns the number of characters in a given string."""#Tool description
    return len(text)
#tool binding 
client_with_tool = client.bind_tools([search_tool,length_string])

# Lets invoke twice without tool call and find out input tokens and tool calls.
response_without_tool = client.invoke("What is python? In 120 words")

print(response_without_tool)
print("\n\n\n\n\n")

response_with_tool = client_with_tool.invoke("What is python?In 120 words")

print(response_with_tool)
print("\n\n\n\n\n")

# Now call with tool and compare the responses. 
response1_without_tool = client.invoke("Tell me new launched ai models.Only names")
print(response1_without_tool)
print("\n\n\n\n\n")

response1_with_tool = client_with_tool.invoke("Tell me new launched ai models.Only names")
print(response1_with_tool) #its knows to call a tool but can not use it by its own
 #TO help the llm use the tool : 
# 1. Ask the model
response2_with_tool = client_with_tool.invoke("Tell me new launched ai models.Only names")

# 2. Check if model requested a tool
if response2_with_tool.tool_calls:#tool calls are returned by the model in response
    for tool_call in response2_with_tool.tool_calls:
        # Execute the tool yourself in Python
        if tool_call["name"] == "tavily_search":
            result = search_tool.invoke(tool_call["args"])#args contain the tool query 
            
            # 3. Pass result back to model
            final_response = client_with_tool.invoke([#using template to clarify that this is tool reponse container prompt 
                HumanMessage(content="Tell me new launched ai models.Only names"),
                response2_with_tool,
                ToolMessage(content=str(result), tool_call_id=tool_call["id"])#parsed tostring and sent with tool id 
            ])
            print(final_response.content)#final result with tool call results 

