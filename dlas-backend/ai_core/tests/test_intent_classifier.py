from langchain_core.messages import HumanMessage

from ai_core.graph import get_graph
from ai_core.state import get_postgres_checkpointer

from ai_core.tests.test_cases import TEST_CASES
from ai_core.tests.report import (
    ReportGenerator,
    TestResult,
)


def run_tests():

    report = ReportGenerator()

    print("=" * 100)
    print("Intent Classification Test Suite")
    print("=" * 100)

    with get_postgres_checkpointer() as checkpointer:

        workflow = get_graph(checkpointer)

        for i, case in enumerate(TEST_CASES, start=1):

            initial_state = {
                "task_id": f"test-{i}",
                "messages": [
                    HumanMessage(content=case.query)
                ]
            }

            result = workflow.invoke(
                initial_state,
                config={
                    "configurable": {
                        "thread_id": f"intent-test-{i}"
                    }
                }
            )

            predicted = result.get("intent", "unknown")
            confidence = result.get("confidence", 0.0)
            reasoning = result.get("reasoning", "")

            passed = predicted == case.expected

            report.add(
                TestResult(
                    query=case.query,
                    expected=case.expected,
                    predicted=predicted,
                    confidence=confidence,
                    reasoning=reasoning,
                    passed=passed,
                )
            )

            print()
            print("=" * 100)
            print(f"Test #{i}")

            print(f"Query      : {case.query}")
            print(f"Expected   : {case.expected}")
            print(f"Predicted  : {predicted}")
            print(f"Confidence : {confidence:.2f}")
            print(f"Status     : {'PASS' if passed else 'FAIL'}")
            print(f"Reason     : {reasoning}")

            print("=" * 100)

    report.print_summary()
    report.save_json()