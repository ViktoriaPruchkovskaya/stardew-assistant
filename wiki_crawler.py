import asyncio
from collections import deque
from typing import Tuple, Set

from bs4 import BeautifulSoup
import httpx

async def crawl_wiki(entrypoint: str):
    queue: deque[str] = deque([entrypoint]) 
    ignored: list[str] = ["Stardew Valley Wiki", "Getting Started"]
    visited: Set[str] = set()
    
    while len(queue) > 0:
        curr = queue.popleft()
        print(f"Visiting {curr}...")
        data = await make_wiki_request(f"https://stardewvalleywiki.com/Special:WhatLinksHere{curr}")
        if data:
            for href, title in data:
                if title in visited or title in ignored:
                    continue
                print(f"{title} -> {href}")
                visited.add(title)
                queue.append(href)
                
    with open("pages.csv", "w") as file:
        file.write(",".join(visited))
        
        
        
async def make_wiki_request(url: str) -> list[Tuple[str,str]] | None:
    """Make a request to the Stardew Valley wiki"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
    
            link_tags = soup.select("#mw-whatlinkshere-list li a")
            linked_pages: list[Tuple[str,str]] = []
            for tag in link_tags: 
                href = tag.get("href")
                title = tag.get("title")
                if href and title and ":" not in href and 'mediawiki' not in href:
                    linked_pages.append((href, title))
            return linked_pages
        except Exception:
            return None
        
asyncio.run(crawl_wiki("/Getting_Started"))