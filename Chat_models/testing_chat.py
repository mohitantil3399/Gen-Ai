import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    max_completion_tokens= 200,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"  # OpenRouter endpoint
)

response = llm.invoke("List me steps on how to use mistral api with langchain ?")
print(response.content)
