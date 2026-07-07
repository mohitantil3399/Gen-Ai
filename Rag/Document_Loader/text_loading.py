from langchain_community.document_loaders import TextLoader

data = TextLoader("notes.txt")
loadedData = data.load()
print(loadedData[0].page_content)
