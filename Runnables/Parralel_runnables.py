'''In real world we might want multiple outputs or multiple works at the same time.
We can use parrallel runnables to so so :
In this approach we define multiple sequence runnables in a dictionay , and all of them run
on the same input simaltaneously.Each pipeline has its own output that in the end is returned 
as proper structure.'''

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnableLambda

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
user_query= "Tell me about steam."
#prompt template initializing short output
prompt_template_short= ChatPromptTemplate.from_template(
   "As a gamer answer to user queries about gaming in 3 sentences.Query :{user_query}"
)
#prompt template initializing for longer output 
prompt_template_long= ChatPromptTemplate.from_template(
   "As a gamer answer to user queries about gaming in 10 sentences.Query :{user_query}"
)
#output parser 
parser = StrOutputParser()

print("=="*50,"\n","Same prompts")
#definig the sequence pipelines in a dictionary for same input in both
parallel_running = RunnableParallel({
"pipeline1": prompt_template_short | client | parser,
"pipeline2": prompt_template_long | client | parser
})
#getting result
response = parallel_running.invoke({"user_query":user_query})
print(response["pipeline1"],"\n\n\n",response["pipeline2"])

print("=="*50,"\n","Different prompts")
#definig the sequence pipelines in a dictionary for different input in both
parallel_running = RunnableParallel({
"pipeline1": RunnableLambda(lambda x: x["pipeline1"])| prompt_template_short | client | parser,
"pipeline2": RunnableLambda(lambda x: x["pipeline2"])| prompt_template_long | client | parser
})
'''
# RunnableLambda is used to extract each branch's nested input before the prompt template runs.
# It converts the outer dictionary into the specific sub-dictionary that the downstream runnable expects.
# This allows pipeline1 and pipeline2 to receive different prompt inputs while sharing the same parallel runner.
# In effect, RunnableLambda adapts the top-level payload so each pipeline sees only its own {"user_query": ...} data.
'''
#getting result
response = parallel_running.invoke({
    "pipeline1":{"user_query":"Tell me about steam."},
    "pipeline2":{"user_query":"Tell me about Xbox."}
    })
# The invoke payload is a nested dict where keys match pipeline names and values are each pipeline's own input dict.
print(response["pipeline1"],"\n\n\n",response["pipeline2"])
'''
Now sometimes in our pipeline, we don’t just want to pass data forward, we might want to slightly modify it or pick
a specific part of it before sending it to the next step. This is where RunnableLambda comes in. It allows us to write
a simple Python function and insert it inside our pipeline as a runnable. For example, if our input is a dictionary with
multiple keys, and we only want to send one specific part of it to a particular pipeline, we can use RunnableLambda
to extract that part. So instead of the entire input going everywhere, we can control exactly what each component
receives. In simple terms, RunnableLambda lets us add custom logic inside our runnable flow, making our pipelines
more flexible and powerful.
'''