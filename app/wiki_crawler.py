import asyncio
from collections import deque
from typing import Set, Tuple

import httpx


async def crawl_wiki(entrypoint: str):
    queue: deque[str] = deque([entrypoint])
    ignored: list[str] = ["Stardew Valley Wiki", "Getting Started"]
    visited: Set[str] = set()

    while len(queue) > 0:
        curr = queue.popleft()
        print(f"Visiting {curr}...")
        data = await make_backlinks_request(curr)
        if data:
            for href, title in data:
                if title in visited or title in ignored:
                    continue
                print(f"{title} -> {href}")
                visited.add(title)
                queue.append(href)
        await asyncio.sleep(1)
    with open("pages.csv", "w") as file:
        file.write(",".join(visited))


async def make_backlinks_request(page: str) -> list[Tuple[str, str]] | None:
    headers = {
        "Accept": "application/json",
    }

    params = {
        "action": "query",
        "list": "backlinks",
        "bltitle": page,
        "blnamespace": 0,  # main/article namespace only
        "blfilterredir": "nonredirects",
        "bllimit": "max",
        "format": "json",
        "formatversion": 2,
    }
    async with httpx.AsyncClient(base_url="https://stardewvalleywiki.com") as client:
        try:
            response = await client.get("mediawiki/api.php", headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            backlinks = data.get("query", {}).get("backlinks", [])
            linked_pages: list[Tuple[str, str]] = []
            for link in backlinks:
                title = link.get("title")
                if title:
                    linked_pages.append((title.replace(" ", "_"), title))
            return linked_pages
        except Exception as err:
            print(f"Unexpected error:{err}")
            return None


asyncio.run(crawl_wiki("Getting_Started"))
