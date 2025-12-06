from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI
from rag_utils import create_vector_store, load_and_split_pdf, get_retriever

import os

import random

def create_podcast_crew(pdf_path, api_key, persona_description, host_name):
    """Creates and runs the CrewAI workflow."""
    os.environ["OPENAI_API_KEY"] = api_key
    
    # 1. Setup RAG Tool
    chunks = load_and_split_pdf(pdf_path)
    vector_store = create_vector_store(chunks, api_key)
    retriever = get_retriever(vector_store)
    
    @tool("Search PDF")
    def search_pdf_tool(query: str):
        """Search the PDF for relevant information. Always use this tool to find facts in the paper."""
        docs = retriever.invoke(query)
        return "\n\n".join([d.page_content for d in docs])

    # 2. Setup LLM
    llm = ChatOpenAI(model="gpt-4o", api_key=api_key, temperature=0.7)

    # 3. Define Agents
    researcher = Agent(
        role='Senior Academic Researcher',
        goal='Extract comprehensive and accurate information from the provided PDF, including the Lead Author\'s name.',
        backstory="You are an expert academic researcher. Your job is to read papers and extract key findings, methodologies, and limitations. You are rigorous and fact-based. You verify everything against the text.",
        tools=[search_pdf_tool],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    host = Agent(
        role='Podcast Host',
        goal='Create an engaging podcast script based on the research findings.',
        backstory=f"You are a charismatic podcast host. {persona_description} You turn dry academic facts into entertaining conversations. You are talking to the Researcher.",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # 4. Define Tasks
    
    research_task = Task(
        description='Search the PDF and extract the main arguments, methodology, results, and limitations. ALSO, explicitly find the name of the Lead Author (first author) of the paper. Be detailed and cite specific sections if possible.',
        agent=researcher,
        expected_output='A detailed summary of the paper with key facts, citations, AND the name of the Lead Author.'
    )

    script_task = Task(
        description=f"""Write a dialogue script for a podcast episode between the Host (named {host_name}) and the Guest (the Lead Author found in the research). 
        
        Use the research findings to inform the conversation. 
        The Host ({host_name}) should introduce herself and the Guest by name.
        The Guest should be referred to as 'Dr. [Last Name]' or by their full name.
        
        IMPORTANT FORMATTING RULES:
        1. The output must START IMMEDIATELY with the dialogue. Do NOT include any title, 'Podcast Script', or markdown headers at the top.
        2. Use strictly 'Host:' and 'Guest:' as the speaker labels for the dialogue blocks, even though they use their names in the text.
        Example:
        Host: Welcome back everyone, I'm {host_name}...
        Guest: Thanks for having me, {host_name}.
        """,
        agent=host,
        context=[research_task],
        expected_output='A podcast script in dialogue format starting immediately with "Host:".',
        async_execution=True
    )

    # 5. Create Crew
    crew = Crew(
        agents=[researcher, host],
        tasks=[research_task, script_task],
        process=Process.sequential,
        verbose=True
    )

    # 6. Kickoff
    result = crew.kickoff()
    
    # Extract outputs
    # result is a CrewOutput object, but we can also access task outputs directly if needed.
    # However, CrewAI's kickoff returns the output of the LAST task by default if we just take the string.
    # But result object has 'tasks_output'.
    
    script_output = script_task.output.raw
    
    return script_output
