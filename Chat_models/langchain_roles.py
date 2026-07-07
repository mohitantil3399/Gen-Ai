from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import time
#using langchain message differentiation object methods
from langchain_core.messages import SystemMessage ,AIMessage,HumanMessage
load_dotenv()
api_key = os.getenv('OPENROUTER_API_KEY')
client = ChatOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="gpt-4o-mini",
    temperature=0.2,
    max_completion_tokens=600
)
print("The assistant is ready. Enter 'quit' or 'exit' to leave.")
messages = [
    SystemMessage(content="You are a helpful assistant , bound by ethics. Be concise in replying.")
]
while True:
    
    #taking user input 
    prompt = input("You : ").lower()
    #setting loop execution condition
    try:
        #termination condition 
        if prompt == 'quit' or prompt == 'exit':
            print("The conversation is over.")
            break
        #else block 
        else:
            #appending to the list messages 
            messages.append(
                HumanMessage(content=prompt)
            )
            #generating the response
            stream = client.stream(messages)
            #printing the response using streaming
            print("=="*50)
            reply = ""
            print("\nAssistant:",end=" ",flush=True)
            for chunk in stream:
                content = chunk.content
                print(content,end="",flush=True)
                reply += content
            print("\n","=="*50)

            #appending the response to the messages list of history 
            messages.append(
                AIMessage(content=reply)
            )
            time.sleep(2)
        
    except Exception as e :
        print("Error occured : ",e)
        break
print(f"\n The overall convo : {messages}")   
