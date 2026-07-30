from Agents import search_agent , scrape_url_agent , writer_sequence , critic_sequence

#creatiing pipeline function to run the final overall loop of the system
def research_pipeline(topic:str)->dict:
    #shared state dictionary to maintain a persistent memory of calls, input passings and output generations
    state={}#initialized as empty dictionary
    #search agent 
    print("Researching topic : ",topic)
    print("=="*50)
    searching_agent=search_agent()
    search_result = searching_agent.invoke({
"messages":[("user",f"Search for comprehensive and diverse sources (at least 3-4 distinct perspectives) on the topic: {topic}.")]
    })
    #adding the extracted details to state 
    state["search_results"]=search_result["messages"][-1].content
    print("Search results added to state","\nSearch results:\n",state['search_results'])
    print("=="*50)
    #next function is scrape url agent 
    print("Scraping urls for more details about topic.")
    print("=="*50)
    web_searcher=scrape_url_agent()
    web_results=web_searcher.invoke({
        "messages":[("user",f"""
        Based on the following results about the topic :{topic}.
        Pick the most relevant urls and etract deep details respectively.
        Search results are : \n {state['search_results']}""")]
    })
    state['scraped_content']=web_results['messages'][-1].content
    print("Content scraped successfully as :\n",state['scraped_content'][:4000])
    print("=="*50)
    #writer chain
    print("\n","Writer on the work.\n")
    #combining the results of both the tools 
    combined_results = (
        f"Search Results: {state['search_results']}\n\n"
        f"Scraped Content: {state['scraped_content']}"
    )
    #invoking writer chain
    state['report']=writer_sequence.invoke({
        "topic":topic,
        "gathered_data":combined_results
    })
    print("\nFinal Report:\n",state['report'])
    #reviewing chain
    print("=="*50)
    print("Report in being reviewed.")
    #invoke the chain
    state['feedback']=critic_sequence.invoke({
        "topic":topic,
        "report":state['report']
    })
    print("\nFinal reviews: \n",state['feedback'])

    return state

if __name__=="__main__":
    topic=input("Enter the topic of research: ")
    research_pipeline(topic)

