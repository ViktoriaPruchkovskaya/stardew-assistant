import asyncio
import json
import os
from typing import TypedDict

from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from openai import RateLimitError
from tenacity import retry, retry_if_exception_type, wait_exponential

from persistences.ioc import PersistenceContainer
from langchain_core.messages import SystemMessage, HumanMessage

DATASET_PATH = "evaluations/dataset.jsonl"

class QAPair(TypedDict):
    question: str
    expected: str


class QAList(TypedDict):
    pairs: list[QAPair]

async def prepare():
    """Create file of generated Q&A dataset for pages collection"""
    model = ChatOpenAI(
            base_url=os.getenv("ENDPOINT"),
            api_key=os.getenv("SUBSCRIPTION_KEY"),
            model=os.getenv("API_VERSION"),
            )
    structured = model.with_structured_output(QAList)

    db = PersistenceContainer.init_db()
    collection = db.connection["pages"]
    records = await collection.aggregate([{"$sample": {"size": 250}}]).to_list()
    with open(DATASET_PATH, "a", newline="\n") as file:
        for record in records:
            print(f"Generating for {record["title"]}")
            if record["title"] == "Animals":
                continue
            text = get_text(record["text"])
            if not text:
                continue
            res = await generate_questions(structured, text)
            if res["pairs"]:
                file.writelines([json.dumps(el) + "\n" for el in res["pairs"]])
            await asyncio.sleep(2)
            
            
@retry(
    retry=retry_if_exception_type(RateLimitError),
    wait=wait_exponential(multiplier=1, min=4, max=60),
)
async def generate_questions(model: ChatOpenAI, article_text: str) -> QAList:
    messages = [
        SystemMessage(
            content=(
                "You are given a Stardew Valley wiki article.\n"
                "Formulate 1-2 factual questions where:\n"
                "- The answer is a short sentence that states exactly one fact from the article.\n"
                "- The answer should be phrased naturally, but must be factually grounded in the article.\n"
                "- The question must be fully and directly answered by that sentence.\n"
                "- Skip questions where the answer requires multiple facts, a range, or is ambiguous.\n"
                "Ignore sections: Portraits, Quotes, Timeline, Gallery, History, Fish Infograph, Location Tables, Fishing Zones."
            )
        ),
        HumanMessage(content=article_text),
    ]
    return await model.ainvoke(messages)


def get_text(page: str) -> str|None:
    soup = BeautifulSoup(page, "html.parser")
    container = soup.select_one(".mw-parser-output")
    if container.find("div", class_="redirectMsg"):
            return None
    return container.get_text()
