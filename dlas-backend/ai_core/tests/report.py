from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json


@dataclass
class TestResult:
    query: str
    expected: str
    predicted: str
    confidence: float
    reasoning: str
    passed: bool


class ReportGenerator:

    def __init__(self):
        self.results: list[TestResult] = []

    def add(self, result: TestResult):
        self.results.append(result)

    @property
    def total(self):
        return len(self.results)

    @property
    def passed(self):
        return sum(r.passed for r in self.results)

    @property
    def failed(self):
        return self.total - self.passed

    @property
    def accuracy(self):
        if self.total == 0:
            return 0
        return round(self.passed / self.total * 100, 2)

    def print_summary(self):

        print("\n" + "=" * 80)
        print("FINAL REPORT")
        print("=" * 80)

        print(f"Total Tests : {self.total}")
        print(f"Passed      : {self.passed}")
        print(f"Failed      : {self.failed}")
        print(f"Accuracy    : {self.accuracy}%")

        print("=" * 80)

    def save_json(self):

        Path("reports").mkdir(exist_ok=True)

        filename = (
            f"reports/intent_report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        data = {
            "accuracy": self.accuracy,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "results": [
                {
                    "query": r.query,
                    "expected": r.expected,
                    "predicted": r.predicted,
                    "confidence": r.confidence,
                    "reasoning": r.reasoning,
                    "passed": r.passed,
                }
                for r in self.results
            ],
        }

        with open(filename, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4)

        print(f"\nJSON report saved -> {filename}")