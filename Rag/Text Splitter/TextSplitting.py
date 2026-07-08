from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

#loading the document 
data = TextLoader("notes_of_text.txt")
loaded_data = data.load()

#initializing the splitter 
splitter = CharacterTextSplitter(
    separator= "",
    chunk_size = 50,
    chunk_overlap = 2
)

#splitting the document 
chunks = splitter.split_documents(loaded_data)

# lets print the chunks 
for chunk in chunks:
    print(chunk.page_content+"\n")
