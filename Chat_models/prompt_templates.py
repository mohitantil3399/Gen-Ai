import os 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')

client = ChatOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
    temperature=0.2,
    max_completion_tokens=600
)
#defining system prompt 
system_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     '''
    You are an assistant that extracts key details from a given paragraph about laptops.
    Focus on specifications, brand, performance, battery life, and price.
    Present the extracted details clearly in bullet points.
     '''
     ),
    ("human",
      "{paragraph}"
      )
])
sample_paragraph='''
The Dell XPS 15 is a premium laptop featuring a 15.6-inch 4K display, 
Intel Core i7 processor, 16GB of RAM, and a 512GB SSD. 
It offers excellent performance for both productivity and creative tasks. 
Battery life averages around 10 hours, and the price starts at $1,499.
'''
paragraph = input("Enter your paragraph : ")

# feeding the paragraph to system prompt and getting response 
user_prompt = system_prompt.invoke({
    'paragraph':paragraph
})
#getting the response 
reply = client.invoke(user_prompt).content

#printing the output 
print("The assistant says : ",reply)
