from dataclasses import dataclass
from typing import Literal, Optional, TypedDict

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from services.tools.wiki_tool import search_pages_vector
from langchain.messages import SystemMessage, HumanMessage, AIMessage


@dataclass
class Config:
    version: str
    endpoint: str
    api_key: str
    deployment: str


class Message(TypedDict):
    role: Literal["user", "assistant", "system"]
    content: str


class QueryService:
    def __init__(self, config: Config):
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
                "5) Apply user preferences and constraints when formatting and prioritizing the answer.\n"
                "6) If evidence is missing or conflicting, say so briefly and ask one clarifying question.\n"
            ),
        )
        self.summary_agent = create_agent(
            self.model,
            name="Summary_Agent",
            system_prompt=(
                "Summarize into compact memory.\n"
                "Output exactly these sections:\n"
                "1) Assistant facts: key factual answers only.\n"
                "2) User intent/constraints: preferences, goals, corrections.\n"
                "3) Open threads: unanswered or pending items.\n"
                "4) Important entities: item names, NPCs, seasons, places.\n"
                "Keep it concise, max ~180 words."
            ),
        )

    async def process_query(self, context: list[Message]) -> str:
        """Process a query using OpenAI and available MCP tools"""
        # messages = self.to_messages(summary, history, new_message)
        result = await self.chat_agent.ainvoke({"messages": context})
        # result = await Runner.run(self.agent, messages)
        # usage = result.context_wrapper.usage
        # print("Requests:", usage.requests)
        # print("Input tokens:", usage.input_tokens)
        # print("Output tokens:", usage.output_tokens)
        # print("Total tokens:", usage.total_tokens)
        return result["messages"][-1].content

    async def summarize_context(self, context: list[Message]) -> str:
        result = await self.summary_agent.ainvoke({"messages": context})
        return result["messages"][-1].content

    def to_messages(self, summary: Optional[Message], history: list[Message], new_message: str) -> list:
        messages = [SystemMessage(summary["content"])] if summary else []
        for msg in history:
            messages.append(AIMessage(msg["content"]) if msg["role"] == "assistant" else HumanMessage(msg["content"]))
        messages.append(HumanMessage(new_message))
        return messages
