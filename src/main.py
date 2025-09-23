import os
import argparse
import sys
from src.agent import create_naming_agent

def main():
    """
    The main function for the Naming Collective CLI application.

    This function sets up the command-line argument parser, checks for
    necessary API keys, initializes and runs the agent, and prints the
    final output.
    """
    # Add the project root to the Python path to allow for absolute imports
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Check for API keys first
    if not os.getenv("GEMINI_API_KEY"):
        print("\033[91mError: GEMINI_API_KEY environment variable not set.\033[0m")
        print("Please create a .env file and add your key.")
        return

    print("\n\033[1m--- Welcome to the Naming Collective ---\033[0m")
    print("I am an AI agent that will help you find a name for your business.")

    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if not serpapi_key or serpapi_key == "dummy_key_for_now":
        print("\n\033[93mWarning: SERPAPI_API_KEY is not configured in your .env file.\033[0m")
        print("The agent will skip the web search step for brand conflicts.")

    parser = argparse.ArgumentParser(
        description="An agent-based system to find a creative and available name for your company."
    )
    parser.add_argument(
        "brief",
        type=str,
        help="A creative brief describing the company or product (e.g., 'a coffee shop that feels like a library').",
    )
    args = parser.parse_args()

    print("\n\033[94mInitializing agent...\033[0m")
    naming_agent = create_naming_agent()

    print(f"\n\033[1mCreative Brief:\033[0m \"{args.brief}\"")
    print("\n\033[92mThinking... (this may take a moment, agent's thoughts are below)\033[0m\n")

    try:
        # Invoke the agent with the creative brief
        result = naming_agent.invoke({"input": args.brief})

        print("\n\033[1m--- Agent Finished ---\033[0m")
        # The agent's final answer is in the 'output' key
        print(f"\033[96m{result['output']}\033[0m")

    except Exception as e:
        print(f"\n\033[91mAn error occurred during agent execution: {e}\033[0m")


if __name__ == "__main__":
    main()
