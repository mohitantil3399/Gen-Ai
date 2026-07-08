from langchain_community.document_loaders import WebBaseLoader

url = "https://www.apple.com/in/newsroom/2026/03/apple-introduces-the-new-macbook-air-with-m5/"
data = WebBaseLoader(url)
loaded_webpage = data.load()
print(loaded_webpage[0].page_content)
