from os.path import abspath

import httpx
from bs4 import BeautifulSoup

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"


async def make_wiki_request(url: str) -> str | None:
    """Make a request to the Stardew Valley wiki"""
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/xml"}
    async with httpx.AsyncClient() as client:
        try:
            print("request is made by {url}")
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            text_only = soup.get_text()
            parsed = text_only.replace("\n", " ")
            return parsed
        except Exception:
            return None


@mcp.tool()
async def get_res(name: str):
    """Get information from Stardew Valley wiki. Response is a plain unedited text. Find response to a question in this text
    Args:
        name: Name of the page from Stardew Valley list of pages. List of names can be obtained from another tool.
    """
    url = f"https://stardewvalleywiki.com/{name.replace(" ", "_")}"
    data = await make_wiki_request(url)
    return f"Reply this briefly {data}"


@mcp.tool()
def get_stardew_pages_list() -> str:
    """Get information about list of pages from JSON file"""
    try:
        with open(abspath("pages.csv")) as file:
            return f"Here's list of pages in CSV format, return value from text back to the user: {str(file.read())}"
    except Exception as e:
        return f"Something bad happened! Provide this to the user exactly as-is: {str(e)}"


if __name__ == "__main__":
    mcp.run("stdio")
