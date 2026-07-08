from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
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
messages = [{
    "role":"system",
    "content":"You are a helpful assistant , bound by ethics. Be concise in replying."
}]
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
            messages.append({
                "role":"user",
                "content":prompt
            })
            #generating the response as stream
            print("=="*50)
            print("\nAssistant:",end="",flush=True)
            
            #printing the response 
            reply =""
            for chunk in client.stream(messages):
                print(chunk.content,end="",flush=True)
                reply+=chunk.content
            print("\n","=="*50)

            #appending the response to the messages list of history 
            messages.append({
                "role":"ai",
                "content":reply
            })
        
    except Exception as e :
        print("Error occured : ",e)
        break
    
