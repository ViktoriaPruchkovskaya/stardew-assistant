import asyncio
from collections import deque
from dataclasses import dataclass
from typing import Set
import httpx


@dataclass
class Page:
    page_id: int
    title: str
    text: str


class WikiCrawler:
    async def crawl_wiki(self, entrypoint: str) -> list[Page]:
        queue: deque[str] = deque([entrypoint])
        ignored: list[str] = ["Stardew Valley Wiki", "Getting Started", ".png", "Modding", ":"]
        visited: Set[str] = set()
        pages: list[Page] = []
        i = 0

        while len(queue) > 0 and i < 3:
            curr = queue.popleft()
            print(f"Visiting {curr}...")
            data = await self.__make_wiki_request(curr)
            if data is None:
                continue
            parse = data.get("parse", {})
            pages.append(
                {
                    "page_id": parse.get("pageid"),
                    "text": parse.get("text", {}).get("*"),
                    "title": parse.get("title", ""),
                }
            )
            i += 1
            links = parse.get("links", [])
            for link in links:
                title = link.get("*")
                if any(sub in title for sub in ignored) or title in visited:
                    continue
                print(f"  - {title}")
                visited.add(title)
            queue.append(title.replace(" ", "_"))
            await asyncio.sleep(0.4)
        return pages

    async def __make_wiki_request(self, page: str) -> dict:
        headers = {
            "Accept": "application/json",
        }

        params = {
            "action": "parse",
            "page": page,
            "prop": "text|links",
            "format": "json",
        }
        async with httpx.AsyncClient(base_url="https://stardewvalleywiki.com") as client:
            try:
                response = await client.get("mediawiki/api.php", headers=headers, params=params, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except Exception as err:
                print(f"Unexpected error:{err}")
            return None
