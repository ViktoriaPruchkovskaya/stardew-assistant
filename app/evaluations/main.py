import asyncio
import csv
import argparse

from enum import Enum
import json
import os
from typing import Literal, TypedDict
from uuid import uuid4

from langgraph.checkpoint.memory import InMemorySaver
from evaluations.prepare_dataset import DATASET_PATH, prepare, QAPair
from evaluations.judge import Judge

from services.query_service import Config, QueryService

EVALS_PATH = "evaluations/results/"

Verdict = Literal["PASS", "FAIL"]

class ScoreResult(TypedDict):
    verdict: Verdict
    reasons: str
    
class EvalResult(TypedDict, ScoreResult):
    answers: list[str]
    verdict: Verdict
    
class CsvResult(TypedDict):
    question: str
    expected: str
    actual_1: str
    actual_2: str
    actual_3: str
    verdict: str
    reasons: str
    
class Mode(Enum):
    PREP = "prep"
    RUN = "run"
    RERUN = "rerun"
    def __str__(self):
        return self.value

    @staticmethod
    def from_string(s):
        try:
            return Mode(s)
        except KeyError:
            raise ValueError()

class JudgeMode(Enum):
    NLI = "nli"
    LLM = "llm"
    def __str__(self):
        return self.value

    @staticmethod
    def from_string(s):
        try:
            return JudgeMode(s)
        except KeyError:
            raise ValueError()

async def evaluate(agent: QueryService, dataset: QAPair, judge: Judge) -> EvalResult:
    results = []
    id = str(uuid4())
    for i in range(3):
        answer = await agent.process_query(
            chat_id=f"{id}-{i}",
            message=dataset["question"],
        )
        results.append(answer)
    res = await score_results(dataset, results, judge)
    return EvalResult(answers=[*results], verdict=res["verdict"], reasons=res["reasons"])

async def score_results(dataset: QAPair, results: list[str], judge: Judge) -> ScoreResult:
    score = 0
    reasoning = []
    for res in results:
        judgement = await judge.check_answer(dataset["question"], dataset["expected"], res)
        if judgement["verdict"] is True:
            score+=1
        else:
            score -=1
        reasoning.append(judgement["reason"])
    return ScoreResult(verdict="PASS" if score > 0 else "FAIL", reasons=" ".join(f"{i}: {item}" for i, item in enumerate(reasoning)))

async def run_evals(judge_type: JudgeMode):
    """Run agent reference-based evaluations and save results to the file"""
    config: Config = Config(
        version=os.getenv("API_VERSION"),
        endpoint=os.getenv("ENDPOINT"),
        api_key=os.getenv("SUBSCRIPTION_KEY"),
        deployment=os.getenv("DEPLOYMENT"),
    )
    query_service = QueryService(
        config=config,
        checkpointer=InMemorySaver(),
    )
    judge = Judge(judge_type.value)
    full_path = os.path.join(EVALS_PATH, f"results_{judge_type.value}.csv")
    
    with open(DATASET_PATH, mode="r") as dataset_file, open(full_path, mode="a") as results_file:
        fieldnames = list(CsvResult.__annotations__.keys())
        writer = csv.DictWriter(results_file, fieldnames=fieldnames)
        writer.writeheader()
        lines = dataset_file.readlines()
        lines_count = len(lines)
        for i, line in enumerate(lines, 1):
            data = json.loads(line)
            print(f"processing {i}/{lines_count}")
            result = await evaluate(query_service, data, judge)
            writer.writerow(CsvResult(question=data["question"],
                                      expected=data["expected"],
                                      actual_1=result["answers"][0],
                                      actual_2=result["answers"][1],
                                      actual_3=result["answers"][2], verdict=result["verdict"], reasons=result["reasons"]))

async def rerun_evals(judge_type: JudgeMode):
    """Rerun evaluations on previous results, compare the changes"""
    judge = Judge(judge_type.value)
    full_path = os.path.join(EVALS_PATH, f"results_{judge_type.value}.csv")
    
    with open(full_path, mode="r") as results_file:
        fieldnames = list(CsvResult.__annotations__.keys())
        reader = csv.DictReader(results_file, fieldnames=fieldnames)
        next(reader)
        changed = 0
        for row in reader:
            print(row["question"])
            result = await score_results(QAPair(question=row["question"], expected=row["expected"]), [row["actual_1"], row["actual_2"], row["actual_3"]], judge)
            print(f"Processing {reader.line_num}")
            if result["verdict"] != row["verdict"]:
                changed+=1
                print(f"Question: {row["question"]}, {row["verdict"]} -> {result["verdict"]}")
                print(f"Reasons:{result["reasons"]}")
        print(f"\n{changed} verdict(s) changed")

            
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=Mode.from_string, choices=list(Mode))   
    parser.add_argument("-j", "--judge", type=JudgeMode.from_string, choices=list(JudgeMode), default=JudgeMode.NLI) 
    args = parser.parse_args()
    match args.mode:
        case Mode.PREP:
            await prepare()
        case Mode.RUN:
            await run_evals(args.judge)
        case Mode.RERUN:
            await rerun_evals(args.judge)
    
if __name__ == "__main__":
    asyncio.run(main())
