from langchain_community.document_loaders import PyPDFLoader

data = PyPDFLoader("dataset.pdf")
loaded_pdf = data.load()
print(len(loaded_pdf))
