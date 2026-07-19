from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

# You named it Grok_KEY in .env, so we're retrieving that
api_key = os.getenv('Grok_KEY')

client = ChatOpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",
    model="openai/gpt-oss-120b",
    temperature=0.2,
    max_completion_tokens=2048
)

prompts = [
    "Explain in detail how LangChain's RunnableSequence (LCEL) works and why it is preferred over legacy chains like LLMChain.",
    "Describe the step-by-step process of building a Retrieval-Augmented Generation (RAG) pipeline using LangChain, including document loaders, text splitters, embeddings, and vector stores.",
    "What are LangChain Agents? Explain the difference between a zero-shot ReAct agent and a conversational retrieval agent, providing use cases for each.",
    "Compare and contrast the different types of memory available in LangChain (e.g., ConversationBufferMemory, ConversationSummaryMemory, and VectorStoreRetrieverMemory). When should I use which?",
    "How does LangChain handle tool calling and function calling with modern LLMs? Provide a conceptual overview of binding tools to a ChatModel.",
    "Discuss the concept of 'Callbacks' in LangChain. How can they be used to stream output to a user interface and monitor token usage?",
    "What are the best practices for structuring a complex, multi-agent application using LangGraph? Explain the concepts of state, nodes, and conditional edges."
]

for i, prompt in enumerate(prompts, 1):
    print(f"\n--- Prompt {i}/7 ---")
    print(f"You: {prompt}")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant, bound by ethics."},
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = client.invoke(messages)
        print(f"Bot: {response.content.strip()}")
    except Exception as e:
        print(f"Error during request {i}: {e}")
        break  # Stop if we hit an error (like a rate limit)
    
    # Adding a small 1-second delay so we don't bombard the API too aggressively
    time.sleep(0)