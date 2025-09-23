# Naming Collective Agent

The Naming Collective is an AI agent-based system designed to help users find a creative and available name for a new product or company. It leverages a large language model for creative brainstorming and a suite of tools to perform real-world validation checks.

This project is an implementation of the agent architecture discussed in a conversation with Gemini, demonstrating a hierarchical approach to problem-solving where an agent orchestrates multiple specialized tools.

## Features

-   **Creative Name Generation:** Uses Google's Gemini Pro to brainstorm a list of relevant and creative names based on a user's brief.
-   **Domain Availability Check:** Automatically checks for the availability of the `.com` domain for each suggested name.
-   **YouTube Handle Check:** Checks if a corresponding YouTube handle (`@name`) is available.
-   **Brand Conflict Search:** Performs a web search to identify if any major companies or brands already exist with the same name (requires a `SERPAPI_API_KEY`).
-   **Autonomous Workflow:** The agent follows a strict, multi-step process to vet each name, stopping and reporting the first one that passes all checks.

## Setup and Installation

Follow these steps to set up and run the Naming Collective agent on your local machine.

### 1. Clone the Repository

First, clone this repository to your local machine.

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate it (on macOS/Linux)
source venv/bin/activate

# Or on Windows
# venv\Scripts\activate
```

### 3. Install Dependencies

Install all the required Python packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

The agent requires API keys to function. Create a `.env` file in the root of the project directory by copying the example file.

```bash
cp .env.example .env
```

Now, open the `.env` file with a text editor and add your API keys:

-   **`GEMINI_API_KEY` (Required):** Your API key for the Google Gemini API.
-   **`SERPAPI_API_KEY` (Optional):** Your API key from [SerpApi](https://serpapi.com/). This is needed for the `web_searcher` tool to check for brand conflicts. If you leave this blank, the agent will skip this step.

## Usage

You can run the agent from the command line. Pass the creative brief for your company as a single string argument. The agent's thoughts will be printed to the console as it works.

### Example

```bash
python src/main.py "a cozy bookstore cafe that specializes in fantasy novels"
```

The agent will start its process, and once it finds a suitable name, it will present its final answer.

### Example Output

```
--- Welcome to the Naming Collective ---
I am an AI agent that will help you find a name for your business.

Initializing agent...

Creative Brief: "a cozy bookstore cafe that specializes in fantasy novels"
Thinking... (this may take a moment, agent's thoughts are below)

> Entering new AgentExecutor chain...
I need to generate a list of names for a cozy bookstore cafe specializing in fantasy novels.
Action: name_idea_generator
Action Input: a cozy bookstore cafe that specializes in fantasy novels
...
(Agent's thoughts and tool usage will appear here)
...
> Finished chain.

--- Agent Finished ---
Final Answer: I have found a name for you: The Fabled Page
```
