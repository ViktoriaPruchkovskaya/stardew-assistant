from abc import ABC, abstractmethod
import os
from typing import Literal, TypedDict

from langchain_deepseek import ChatDeepSeek
from langchain.messages import HumanMessage
from openai import RateLimitError
from sentence_transformers import CrossEncoder
from tenacity import retry, retry_if_exception_type, wait_exponential

class JudgementResult(TypedDict):
    verdict: bool
    reason: str
         
class JudgeStrategy(ABC):
    @abstractmethod
    async def judge_answer(self, question: str, expected: str, output: str) -> JudgementResult:
        pass 
  
class Judge:
    judge: JudgeStrategy
    def __init__(self, type: Literal["nli", "llm"]):
        try:
            if type == "nli":
                self.judge = JudgeNLI()
            else:
                self.judge = JudgeLLM()
        except Exception as e:
            raise Exception(f"Fail to init {type} judge: {e}")
    
    async def check_answer(self, question: str, expected: str, output: str) -> JudgementResult:
        result = await self.judge.judge_answer(question, expected, output)
        return result
            
class JudgeNLI(JudgeStrategy):
    label_mapping = ["contradiction", "entailment", "neutral"]
    def __init__(self):
        self.model = CrossEncoder("cross-encoder/nli-deberta-v3-base", device="mps") 
        
    async def judge_answer(self, _question: str, expected: str, output: str)-> JudgementResult:
        scores = self.model.predict([(output, expected), (expected, output)])
        for score in scores:
            label = self.label_mapping[score.argmax()]
            if label == "entailment":
                return JudgementResult(verdict=True)
        return JudgementResult(verdict=False)
        
class JudgeLLM(JudgeStrategy):
    def __init__(self):
        model = ChatDeepSeek(
            base_url=os.getenv("JUDGE_ENDPOINT"),
            api_key=os.getenv("JUDGE_SUBSCRIPTION_KEY"),
            model="DeepSeek-V3.2",
            temperature=0
            )
        self.model = model.with_structured_output(JudgementResult)
        
    @retry(
        retry=retry_if_exception_type(RateLimitError),
        wait=wait_exponential(multiplier=1, min=4, max=60),
    )
    async def judge_answer(self, question: str, expected: str, output: str) -> JudgementResult:
        messages = [
            HumanMessage(
                content=(
                    "You are a factual grader. The reference answer is a minimum requirement — "
                    "it contains the core fact that must be present in the given answer.\n\n"
                    
                    "PASS if:\n"
                    "- Given answer contains all facts from the reference\n"
                    "- Extra details are allowed even if not in reference\n\n"
                    
                    "FAIL if:\n"
                    "- Given answer is missing a core fact from the reference\n"
                    "- Given answer directly contradicts the reference\n"
                    "- Given answer addresses a different aspect or refuses to answer\n\n"
                    f"Question: {question}\n"
                    f"Reference answer: {expected}\n"
                    f"Given answer: {output}\n"
                    "Reply only PASS or FAIL, and shortly explain a reason"
                )
            ),
        ]
        res = await self.model.ainvoke(messages)
        return res