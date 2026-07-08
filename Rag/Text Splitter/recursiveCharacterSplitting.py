from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

#loading the pdf 
data = PyPDFLoader("dataset.pdf")
loaded_pdf = data.load()

# making the splitter 
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 2000,
    chunk_overlap = 10
)
#splitting the loaded document
chunks = splitter.split_documents(loaded_pdf)

print(len(chunks))
#printing all the chunks
for chunk in chunks:
    print(chunk.page_content)
    print("=="*50)