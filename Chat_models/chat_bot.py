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
    max_completion_tokens=400
)
# prompt = input("You : ")
messages = [{
    "role":"system",
    "content":"You are a helpful assistant , bound by ethics."
}]
messages.append({
    "role":"user",
    "content":prompt
})
response = client.invoke(messages)
print(response.content)