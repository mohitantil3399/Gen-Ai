'''
Runnable Passthrough is used when we want to keep the original input or some intermediate data while passing it
through the pipeline. Normally, in a sequence, each step replaces the previous output, so earlier data gets lost. But in
many real-world scenarios, we need to carry multiple pieces of information together. RunnablePassthrough allows us to
forward the input as it is, without modifying it, so that it can be used along with other outputs in later steps. In simple
terms, it helps us preserve data while still continuing the flow of the pipeline.
'''
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough

#loading api keys
load_dotenv()
api_key = os.getenv("Grok_KEY")

#initializing model 
client = ChatOpenAI(
    api_key=api_key,
    model="openai/gpt-oss-20b",
    base_url="https://api.groq.com/openai/v1",
    max_completion_tokens=600,
    temperature=0.3
)
#lets write the code to see what is need of passthrough 
user_query = "Give a kotlin code example to explain the uses of lamda expressions."
#defining 1st prompt 
prompt1 = ChatPromptTemplate.from_messages([
    ("system","You are a developer.Write code on the user's query.Do not explain or add comments."),
    ("human","Write code for : {user_query}")
]
)
prompt2 = ChatPromptTemplate.from_messages([
    ("system","You are a senior developer.explain the code to the userin 550 tokens."),
    ("human","Explain code: {code}")
]
)
#This flow : in a single sequence
#prompt1-> Generates code -> prompt2 -> reviews the same code .No savings in between
structured_output = StrOutputParser()
sequence = prompt1 | client | structured_output | prompt2 | client | structured_output
#Final output is result of structured_output from prompt2 , nothing is saved from prompt1
result = sequence.invoke({"user_query":user_query})
print(result)
print("=="*50)
#In this method the generate code could not be saved , to do so we will use passthrough 


#Lets solve this problem here :
seq1 = prompt1 | client | structured_output
#creating parallel sequencies
seq2 = RunnableParallel({
    "generating_code":RunnablePassthrough(),#return the input as output with no changes 
    "review_code":prompt2 | client | structured_output
}) 
#connecting these both sequencies in single 
final_sequence = seq1 | seq2
#getting response 
response = final_sequence.invoke(user_query)
print("Code:\n",response['generating_code'],"\n\n")
print("\n\nExplaination:\n",response['review_code'])