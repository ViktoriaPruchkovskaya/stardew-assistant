from dataclasses import dataclass
from typing import Any

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent, AgentState
from langgraph.runtime import Runtime
from services.tools.wiki_tool import search_pages_vector
from langchain.messages import RemoveMessage, HumanMessage

# from langchain_core.messages.utils import trim_messages as trim_messages_util
from langgraph.checkpoint.mongodb.saver import MongoDBSaver
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import REMOVE_ALL_MESSAGES

from services.tools.wiki_tool import search_pages_vector
from langchain.agents.middleware import before_model


@dataclass
class Config:
    version: str
    endpoint: str
    api_key: str
    deployment: str


@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

    # trimmed = trim_messages_util(
    #     messages,
    #     max_tokens=10000,
    #     strategy="last",
    #     token_counter="approximate",
    #     start_on="human",
    #     include_system=True,
    #     allow_partial=False,
    # )
    if len(messages) <= 3:
        return None 
    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *new_messages]}


class QueryService:
    def __init__(self, config: Config, checkpointer: MongoDBSaver | InMemorySaver):
        self.model = ChatOpenAI(
            base_url=config.endpoint,
            api_key=config.api_key,
            model=config.deployment,
        )
        self.chat_agent = create_agent(
            self.model,
            name="Chat_Agent",
            tools=[search_pages_vector],
            system_prompt=(
                "You are a Stardew Valley assistant.\n"
                "Use conversation memory and user preferences from context. Avoid mentioning game name\n"
                "Workflow:\n"
                "1) For factual gameplay questions, call search_pages_vector with the user's question first.\n"
                "2) Use tool evidence as the primary source of truth for factual claims.\n"
                "3) For follow-up questions with implicit references (for example, pronouns), resolve them from conversation memory.\n"
                "4) Answer with the gist only: max 70-100 words total, unless the user asks for more detail.\n"
                "5) If evidence is missing or conflicting, say so briefly and ask one clarifying question.\n"
            ),
            middleware=[trim_messages],
            checkpointer=checkpointer,
        )


    async def process_query(self, chat_id: str, message: str) -> str:
        """Process a query using the chat agent with per-chat short-term memory."""
        result = await self.chat_agent.ainvoke(
            {"messages": [HumanMessage(content=message)]},
            config={"configurable": {"thread_id": chat_id}},
        )
        return result["messages"][-1].content
