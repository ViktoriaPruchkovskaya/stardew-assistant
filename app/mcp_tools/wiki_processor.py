from os.path import abspath

import httpx

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WikiProcessor")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"


async def make_wiki_request(title: str) -> str | None:
    """Make a request to the Stardew Valley wiki"""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    params = {
        "action": "query",
        "titles": title.replace(" ", "_"),
        "format": "json",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "formatversion": 2,
    }
    async with httpx.AsyncClient(base_url="https://stardewvalleywiki.com") as client:
        try:
            response = await client.get(
                "mediawiki/api.php",
                headers=headers,
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()

            data = response.json()
            info = ""
            pages = data.get("query", {}).get("pages", {})
            for page in pages:
                revisions = page.get("revisions", [])
                for revision in revisions:
                    content = revision.get("slots", {}).get("main", {}).get("content", "")
                    info += content
            return info
        except Exception:
            return None


@mcp.tool()
async def get_pages_content(name: str):
    """Get raw wiki page content for one Stardew Valley page title. Find response to a question in this text
    Args:
        name: Name of the page from Stardew Valley list of pages. List of names can be obtained from another tool.
    Returns:
        Raw page content from the wiki, without summarization
    """
    data = await make_wiki_request(name)
    if data:
        return data
    return "No content found for this page"


@mcp.tool()
def search_pages() -> str:
    """Return the full Stardew Valley page index from pages.csv.
    The assistant must use this index to infer the most relevant page titles for the user question
    Returns:
    CSV text containing all available page titles."""
    try:
        with open(abspath("pages.csv")) as file:
            return file.read()
    except Exception as e:
        return f"Failed to load pages.csv: {e}"


if __name__ == "__main__":
    mcp.run("stdio")
