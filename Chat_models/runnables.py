'''
# Runnables in LangChain

## Introduction
Runnables in LangChain are a powerful abstraction that allows users to define and execute 
a sequence of operations or tasks in a structured manner. They are particularly useful
for building complex workflows in applications that involve language models, data processing, and more.

## Key Concepts

### 1. Definition of Runnables
- Runnables are objects that encapsulate a specific task or operation.
- They can be composed together to create more complex workflows.
- Runnables can be synchronous or asynchronous.

### 2. Types of Runnables
- **Runnable Functions**: Basic functions that can be executed.
- **Runnable Chains**: A sequence of runnable functions executed in order.
- **Runnable Serializers**: Runnables that handle input/output serialization.

### 3. Composition of Runnables
- Runnables can be combined using various strategies:
  - **Sequential Execution**: Running one runnable after another.
  - **Parallel Execution**: Running multiple runnables simultaneously.
  - **Conditional Execution**: Executing runnables based on certain conditions.

## Implementation

### 1. Creating a Runnable
To create a runnable, you typically define a function that performs a specific task.

```python
from langchain.runnables import Runnable

def my_function(input_data):
    # Process the input data
    return processed_data

my_runnable = Runnable(my_function)
```

### 2. Composing Runnables
You can compose multiple runnables to create a chain.

```python
from langchain.runnables import RunnableChain

runnable_chain = RunnableChain([
    my_runnable,
    another_runnable,
    final_runnable
])
```

### 3. Executing Runnables
To execute a runnable or a chain of runnables, you simply call the `run` method.

```python
result = runnable_chain.run(input_data)
```

## Use Cases

### 1. Data Processing Pipelines
Runnables can be used to create data processing pipelines where each runnable represents a step in the data transformation process.

### 2. Workflow Automation
Automate complex workflows by chaining multiple tasks together, such as data retrieval, processing, and storage.

### 3. Machine Learning Workflows
Incorporate model inference, data preprocessing, and post-processing steps into a single runnable workflow.

## Best Practices

- **Modularity**: Keep runnables small and focused on a single task to enhance reusability.
- **Error Handling**: Implement error handling within runnables to manage exceptions gracefully.
- **Testing**: Test individual runnables to ensure they work correctly before composing them 
into chains.

## Conclusion
Runnables in LangChain provide a flexible and powerful way to define and execute workflows.
By leveraging the composition of runnables, developers can build complex applications 
that efficiently process data and interact with'''


#SequenceRunnables 
import os 
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


#loading environment variables
load_dotenv()
#API key setup 
api_key = os.getenv("MISTRAL_API_KEY")
#loading model 
client = ChatMistralAI(model="mistral-small-latest",api_key=api_key)
#prompt_template 
#user input 
query = input("Enter your query : ")
prompt_template =ChatPromptTemplate.from_template("Explain like a professor. Topic :{query} ")
final_prompt = prompt_template.format_messages(query=query) 
#Response formatting 
parser = StrOutputParser()
#response generation
response = client.invoke(final_prompt) 
#parsed output
parsed_output = parser.parse(response.content)
#print output
print(parsed_output)

'''
# **StrOutputParser() in LangChain: A Comprehensive Explanation**

## **1. Introduction to `StrOutputParser()`**
`StrOutputParser()` is a utility class from `langchain_core.output_parser` in the **LangChain** ecosystem. It is designed to **convert structured or complex outputs from a language model (LLM) into plain strings**.

### **Key Features:**
- **Simplifies LLM outputs** by extracting and formatting responses.
- **Works with various LLM outputs**, including `BaseMessage`, `AIMessage`, `HumanMessage`, or raw strings.
- **Integrates seamlessly** with LangChain's `Runnable` interface (e.g., `RunnablePassthrough`, `RunnableParallel`).

---

## **2. Why Use `StrOutputParser()`?**
LLMs often return structured outputs (e.g., JSON, lists, or `BaseMessage` objects). However, many applications require **human-readable or easily processable text**. `StrOutputParser()` helps by:
- Converting structured outputs into plain strings.
- Extracting the core content from messages.
- Making it easier to chain with other LangChain components.

---

## **3. How to Use `StrOutputParser()`**
### **Basic Usage**
```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define a prompt
prompt = PromptTemplate.from_template(
    "Tell me a joke about {topic}."
)

# Define the processing chain
chain = (
    {"topic": RunnablePassthrough()}  # Pass input directly
    | prompt  # Apply prompt
    | llm     # Call LLM
    | StrOutputParser()  # Convert output to string
)

# Run the chain
result = chain.invoke("cats")
print(result)
```
**Output:**
```
Why don't cats play poker in the jungle? Too many cheetahs!
```

---

### **Handling Different LLM Outputs**
#### **Case 1: LLM Returns `AIMessage` (Default in Chat Models)**
```python
from langchain_core.messages import AIMessage

# Simulate an AIMessage
ai_message = AIMessage(content="Hello, how can I help?")
parser = StrOutputParser()
parsed = parser.invoke(ai_message)
print(parsed)
```
**Output:**
```
Hello, how can I help?
```

#### **Case 2: LLM Returns a Structured Response (e.g., JSON)**
```python
from langchain_core.output_parsers import StrOutputParser
import json

# Simulate a structured response (e.g., from a JSON output)
structured_output = '{"joke": "Why did the AI break up with the human? It needed space!", "rating": 5}'
parser = StrOutputParser()
parsed = parser.invoke(structured_output)
print(parsed)
```
**Output:**
```
{"joke": "Why did the AI break up with the human? It needed space!", "rating": 5}
```

---

## **4. Integration with LangChain Runnables**
`StrOutputParser()` works well with LangChain's **`Runnable`** interface, allowing it to be chained with:
- **Prompts** (`PromptTemplate`)
- **LLMs** (`ChatOpenAI`, `OpenAI`)
- **Retrievers** (`RetrievalQA`)
- **Other parsers** (`JsonOutputParser`)

### **Example: Chaining with Retrieval**
```python
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

# Sample documents
docs = [
    Document(page_content="LangChain is a framework for building LLM apps."),
    Document(page_content="StrOutputParser converts LLM outputs to strings.")
]

# Create a vector store
vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())

# Define a retriever chain
retriever = vectorstore.as_retriever()
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | PromptTemplate.from_template(
        "Answer the question based on context: {question}\nContext: {context}"
    )
    | ChatOpenAI()
    | StrOutputParser()
)

# Query the chain
result = chain.invoke("What does StrOutputParser do?")
print(result)
```
**Output:**
```
StrOutputParser converts LLM outputs to strings.
```

---

## **5. When to Use `StrOutputParser()` vs Other Parsers**
| **Parser** | **Use Case** | **Example** |
|------------|-------------|-------------|
| `StrOutputParser()` | Extract plain text from LLM responses | `AIMessage` → `"Hello"` |
| `JsonOutputParser()` | Parse structured JSON outputs | `{"key": "value"}` → `dict` |
| `PydanticOutputParser()` | Extract typed structured data | `BaseModel` → `User(name="Alice")` |
| `MarkdownHeaderTextSplitter()` | Split Markdown by headers | Convert Markdown to chunks |

**Use `StrOutputParser()` when:**
✅ You need **raw text** from the LLM.
✅ The output is **not structured** (e.g., a simple answer).
✅ You want to **chain with text-processing steps**.

---

## **6. Advanced Usage: Custom Parsing Logic**
If you need **custom string extraction**, you can subclass `StrOutputParser`:
```python
from langchain_core.output_parsers import StrOutputParser

class CustomStrParser(StrOutputParser):
    def parse(self, text):
        # Example: Extract only the first sentence
        return text.split(".")[0] + "."

parser = CustomStrParser()
result = parser.invoke("Hello. How are you? I'm fine.")
print(result)  # Output: "Hello."
```

---

## **7. Best Practices**
1. **Always use `StrOutputParser()`** when working with chat models (`ChatOpenAI`, `ChatAnthropic`) to ensure clean text output.
2. **Combine with `RunnablePassthrough()`** to pass inputs directly to the prompt.
3. **For structured data**, consider `JsonOutputParser` or `PydanticOutputParser`.
4. **Test edge cases** (e.g., empty responses, multi-line outputs).

---

## **8. Conclusion**
`StrOutputParser()` is a **simple but powerful** tool in LangChain for converting LLM outputs into readable strings. It integrates smoothly with LangChain’s `Runnable` interface, making it ideal for:
- **Chaining LLMs with prompts and retrievers.**
- **Extracting clean text from structured responses.**
- **Building conversational AI pipelines.**

By mastering `StrOutputParser()`, you can **simplify your LangChain workflows** and ensure **consistent text-based processing**.

---

### **Further Reading**
- [LangChain Output Parsers Docs](https://python.langchain.com/docs/modules/model_io/output_parsers/)
- [LangChain Runnable Interface](https://python.langchain.com/docs/expression_language/)
- [Chat Models in LangChain](https://python.langchain.com/docs/modules/model_io/chat/)
'''