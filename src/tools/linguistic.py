import os
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAi

@tool
def name_idea_generator(creative_brief: str) -> list[str]:
    """
    Generates a list of creative company or product names based on a creative brief.
    The brief should describe the company, its values, and its target audience.
    Returns a list of 10 names.
    """
    try:
        llm = ChatGoogleGenerativeAi(model="gemini-pro", temperature=0.9)
        prompt = f"""
        Based on the following creative brief, generate a list of 10 creative and unique names.
        The names should be catchy, memorable, and relevant to the brief.
        Return the names as a single comma-separated string. Do not include any other text, numbers, or bullet points in your response.

        Creative Brief: "{creative_brief}"

        Example output: Name One, Name Two, Name Three, Name Four, Name Five, Name Six, Name Seven, Name Eight, Name Nine, Name Ten
        """
        response = llm.invoke(prompt)
        # The response content will be a string like "Name One, Name Two, ..."
        names = [name.strip() for name in response.content.split(',')]
        return names
    except Exception as e:
        return [f"Error generating names: {e}"]
