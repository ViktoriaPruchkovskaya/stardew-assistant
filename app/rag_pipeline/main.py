import asyncio
import os

import chromadb
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2

from rag_pipeline.crawler import WikiCrawler, Page
from rag_pipeline.parser import Parser
from persistences.database import Database

chroma_client = chromadb.PersistentClient(path="./db")
ef = ONNXMiniLM_L6_V2(preferred_providers=["CoreMLExecutionProvider"])
collection = chroma_client.get_or_create_collection(name="articles", embedding_function=ef)

chroma_client.list_collections()


async def populate_vector_db():
    """Crawl wiki content and trigger vector database seeding."""
    crawler = WikiCrawler()
    pages = await crawler.crawl_wiki("Getting_Started")
    await seed_from_persistence(pages)


async def seed_from_persistence(pages: list[Page]):
    """Persist crawled pages, then index stored data into ChromaDB.

    Args:
        pages: Pages returned by the crawler.
    """
    db = await init_db()
    await db.insert_many("pages", pages)
    cursor = db.get_batch("pages")
    i = 1
    async for page in cursor:
        print(f"processing chunk N {i} {page["title"]}")
        parser = Parser()
        text = parser.get_paragraphs(page["text"])
        if text:
            store_article(page["title"], text)
        print(f"finished chunk N {i}")
        i += 1


def seed(pages: list[Page]):
    """Index a list of pages directly into ChromaDB.

    Args:
        pages: Pages to parse and upsert as vector documents.
    """
    i = 1
    parser = Parser()
    for page in pages:
        print(f"processing chunk N {i} {page["title"]}")
        text = parser.get_paragraphs(page["text"])
        store_article(page["title"], text)
        print(f"finished chunk N {i}")
        i += 1


def store_article(title: str, paragraphs: dict):
    """Store chunks in ChromaDB

    Args:
        title: page title.
        paragraphs: page paragraphs
    """
    for section, content in paragraphs.items():
        text = "".join(content)
        if not text.strip():
            continue

        collection.upsert(
            documents=[f"{title}\n{section}\n{text}"],
            metadatas=[{"article": title, "section": section}],
            ids=[f"{title}_{section}"],
        )


async def init_db() -> Database:
    connection_string = (
        f"mongodb://{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST", "localhost")}:27017/"
    )
    return Database(connection_string, os.getenv("DB_NAME"))


if __name__ == "__main__":
    asyncio.run(populate_vector_db())
