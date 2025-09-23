import os
import requests
import whois
from langchain.tools import tool
from serpapi import GoogleSearch

@tool
def domain_availability_checker(name: str) -> str:
    """
    Checks if a .com domain is available for a given name.
    It removes spaces and converts the name to lowercase.
    Returns 'available' or 'unavailable'.
    """
    if not name or not isinstance(name, str):
        return "Invalid input. Name must be a non-empty string."

    domain_name = name.replace(" ", "").lower() + ".com"
    try:
        w = whois.whois(domain_name)
        if w.status is None or w.registrar is None:
            return "available"
        return "unavailable"
    except whois.parser.PywhoisError:
        # This error often means the domain is not registered
        return "available"
    except Exception:
        # Catch other potential errors during the lookup
        return "unavailable"

@tool
def youtube_handle_checker(name: str) -> str:
    """
    Checks if a YouTube handle is available by making a GET request.
    It removes spaces and special characters from the name.
    Returns 'available' or 'unavailable'.
    """
    if not name or not isinstance(name, str):
        return "Invalid input. Name must be a non-empty string."

    handle = "".join(e for e in name if e.isalnum())
    if not handle:
        return "Invalid name for a handle."

    url = f"https://www.youtube.com/@{handle}"
    try:
        # Using a HEAD request is more efficient as we don't need the body
        response = requests.head(url, timeout=5)
        # YouTube returns 200 for existing handles and 404 for non-existing ones.
        if response.status_code == 404:
            return "available"
        else:
            return "unavailable"
    except requests.exceptions.RequestException:
        return "Error: Could not connect to YouTube to check handle."

@tool
def web_searcher(name: str) -> str:
    """
    Performs a web search to see if a company with the given name already exists.
    Looks for potential brand conflicts by searching for the name as a company.
    Returns a summary of the search results, highlighting potential conflicts.
    """
    if not name or not isinstance(name, str):
        return "Invalid input. Name must be a non-empty string."

    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key or api_key == "dummy_key_for_now":
        return "Web search skipped: SERPAPI_API_KEY is not configured."

    params = {
        "q": f'"{name}" company OR startup OR business',
        "engine": "google",
        "api_key": api_key,
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        if "error" in results:
            return f"Web search error: {results['error']}"

        if "organic_results" in results and len(results["organic_results"]) > 0:
            # Check if top results are highly relevant, indicating a direct conflict
            top_result = results["organic_results"][0]
            if name.lower() in top_result.get("title", "").lower():
                 return f"Conflict found: An entity named '{top_result.get('title')}' seems to exist. Link: {top_result.get('link')}"

            snippets = [res.get("snippet", "") for res in results["organic_results"][:3]]
            summary = "Potential conflicts found:\n" + "\n".join(f"- {s}" for s in snippets)
            return summary
        else:
            return "No significant conflicts found in web search."
    except Exception as e:
        return f"Web search error: {e}"
