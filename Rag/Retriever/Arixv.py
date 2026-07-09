import arxiv
from langchain_core.documents import Document

# create client (v2.x API)
client = arxiv.Client()

# define search
search = arxiv.Search(
    query="What is the use of Artificial intelligence",
    max_results=2,
    sort_by=arxiv.SortCriterion.Relevance
)

# fetch results and wrap into LangChain Documents
retrieved_docs = [
    Document(
        page_content=result.summary,
        metadata={
            "source": result.entry_id,
            "title": result.title,
            "authors": [str(a) for a in result.authors],
            "published": str(result.published)
        }
    )
    for result in client.results(search)
]

# print results
for i, doc in enumerate(retrieved_docs):
    print("\n results : ", i + 1)
    print("\n Source  : ", doc.metadata["source"])
    print("\n Title   : ", doc.metadata["title"])
    print("\n Content : ", doc.page_content[:100])