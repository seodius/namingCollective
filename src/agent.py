import os
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAi
from langchain_core.prompts import PromptTemplate

from src.tools.linguistic import name_idea_generator
from src.tools.research import domain_availability_checker, youtube_handle_checker, web_searcher

# Load environment variables from .env file at the beginning
load_dotenv()

def create_naming_agent():
    """
    Creates and returns the Naming Collective agent executor.

    This function initializes the LLM, gathers the necessary tools,
    and constructs the agent with a detailed prompt that guides its
    reasoning process.
    """
    # 1. Initialize the LLM
    # We use a low temperature because the agent's reasoning should be predictable
    llm = ChatGoogleGenerativeAi(model="gemini-pro", temperature=0)

    # 2. Gather the tools
    tools = [
        name_idea_generator,
        domain_availability_checker,
        youtube_handle_checker,
        web_searcher,
    ]

    # 3. Define the prompt template
    # This prompt is the core of the agent's logic. It's a zero-shot prompt
    # that tells the agent how to behave, what its goal is, and how to use the tools
    # in a specific sequence.
    template = """
You are the "Naming Collective", an expert agent that helps users find a creative and available name for their company or product.

Your goal is to find a name that meets all the following criteria:
1. The .com domain is available.
2. The YouTube handle is available.
3. The web search does not reveal any major conflicts.

Here is your non-negotiable workflow:
1.  Receive the user's creative brief.
2.  Use the `name_idea_generator` tool to brainstorm a list of 10 potential names.
3.  For each name in the list, you MUST verify its availability by performing the following checks in this exact order:
    a. Use `domain_availability_checker`. If it returns 'unavailable', you MUST immediately stop and move to the next name on the list. Do not proceed with other checks for this name.
    b. If the domain is available, use `youtube_handle_checker`. If it returns 'unavailable', you MUST immediately stop and move to the next name.
    c. If the domain and YouTube handle are available, use `web_searcher` to check for conflicts. If the search result indicates a direct conflict (e.g., an existing company with that exact name), you MUST stop and move to the next name.
4.  The very FIRST name that passes ALL THREE checks is the final answer. You must immediately stop your work and provide the answer in the following format:

"I have found a name for you: [The Winning Name]"

If you exhaust the entire list of names and none of them pass all the checks, you MUST conclude with this exact message:

"I generated and checked 10 names, but unfortunately, none were available across all platforms. You could try running the process again with a different creative brief."

You have access to the following tools:
{tools}

Let's begin!

User's Creative Brief: {input}

Thought Process:
{agent_scratchpad}
"""

    # 4. Create the prompt from the template
    prompt = PromptTemplate.from_template(template)

    # 5. Create the agent using the ReAct framework
    agent = create_react_agent(llm, tools, prompt)

    # 6. Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True, # Set to True to see the agent's thought process
        handle_parsing_errors=True, # Helps with robustness on unexpected LLM outputs
        max_iterations=15, # Prevent potential infinite loops
    )

    return agent_executor
