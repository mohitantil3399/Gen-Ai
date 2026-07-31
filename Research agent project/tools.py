import os 
import requests
from langchain.tools import tool
from dotenv import load_dotenv
from tavily import TavilyClient
from bs4 import BeautifulSoup

load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")

#loading tavily client
tavily = TavilyClient(api_key=tavily_key)

@tool
def tavily_search(query:str)->str:
    """Search the web for information using Tavily.It returns Title,Snippet and URLs of the related sites."""
    results = tavily.search(
        query=query,
        max_results=5,
        include_images=False,
        include_raw_content=False,
        search_depth='fast',
        timeout = 15.0
        )
    out = []
    for r in results['results']:
        title = r['title']
        url = r['url']
        content = r['content'][:800]#taking only 200 words of content
        out.append(f"Title: {title} \nUrl: {url} \nContent: {content}")
    return "\n=================\n".join(out)#joining to an empty string , to make the list a string 

#print(tavily_search.invoke("What are plans of google with manifest v3 in google chrome?"))
#web search tool
@tool
def web_search(url:str)->str:
    """Get complete web page content from a URL."""
    try:
        response = requests.get(url, timeout = 8,headers={"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
        response.raise_for_status()  # HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted tags
        for tag in ['script', 'style', 'header', 'footer', 'nav', 'aside']:
            for element in soup.find_all(tag):
                element.decompose()
        
        return soup.get_text(separator=" ", strip=True)[:10000]
    except Exception as e:
        return f"Error fetching URL: {e}"

#print(web_search.invoke("https://www.youtube.com/watch?v=P22qI2RnNjA&list=PLaldQ9PzZd9oXR4PMGR4pr_DX4wFHkFwR&index=4"))