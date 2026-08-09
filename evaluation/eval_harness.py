# =============================================================================================
# Evaluation Harness
# Runs Task 1 and Task 2 tests and generates JSON + Markdown reports.
# =============================================================================================
import json
from pathlib import Path

from evaluation.test_cases import TASK1_TESTS, TASK2_TESTS
from evaluation.llm_judge import judge_output

from src.triage import triage_ticket
from src.account_summary import generate_account_brief

results = {"task1": [], "task2": []}

# Score calculator
def calculate_score(matches, total):
    score = matches / total if total else 1.0
    return round(score, 2), score == 1.0

# -----------------------------------------------------------------------------
# Task 1 evaluation
# -----------------------------------------------------------------------------

for test in TASK1_TESTS:
    output = triage_ticket(test["subject"], test["body"])
    expected = test["expected"]
    matches = sum(
        getattr(output, key) == value
        for key, value in expected.items()
    )

    score, passed = calculate_score(matches, len(expected))

    llm_result = judge_output(
        "Task1",
        test["id"],
        output.model_dump_json(indent=2)
    )

    results["task1"].append({
        "id": test["id"],
        "pass": passed,
        "score": score,
        "llm_judge": llm_result
    })

# -----------------------------------------------------------------------------
# Task 2 evaluation
# -----------------------------------------------------------------------------

for test in TASK2_TESTS:
    if test.get("expect_error"):
        try:
            generate_account_brief(test["account_id"])
            passed, score = False, 0.0
        except Exception:
            passed, score = True, 1.0
        llm_result = {
            "pass": passed,
            "score": score,
            "reason": "Invalid account handled correctly" if passed else "Expected error not raised"
        }
    else:
        brief = generate_account_brief(test["account_id"])
        criteria = test["criteria"]
        matches = sum(c in brief for c in criteria)
        score, passed = calculate_score(matches, len(criteria))
        llm_result = judge_output(
            "Task2",
            test["id"],
            brief
        )
    results["task2"].append({
        "id": test["id"],
        "pass": passed,
        "score": score,
        "llm_judge": llm_result
    })

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
summary = {}
for task_name in ["task1", "task2"]:
    task_results = results[task_name]
    avg_score = round(
        sum(r["score"] for r in task_results) / len(task_results),
        2
    )
    passed = sum(r["pass"] for r in task_results)
    summary[task_name] = {
        "passed": passed,
        "total": len(task_results),
        "average_score": avg_score
    }
results["summary"] = summary

# -----------------------------------------------------------------------------
# Save reports
# -----------------------------------------------------------------------------
Path("evaluation").mkdir(exist_ok=True)
with open("evaluation/report.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
md = ["# Evaluation Report", ""]
for task_name in ["task1", "task2"]:
    md.append(f"## {task_name.upper()}")
    md.append("| Test | Pass | Score |")
    md.append("|---|---|---|")
    for r in results[task_name]:
        md.append(
            f"| {r['id']} | {'PASS' if r['pass'] else 'FAIL'} | {r['score']} |"
        )
    s = summary[task_name]
    md.append("")
    md.append(f"**Passed:** {s['passed']}/{s['total']}  ")
    md.append(f"**Average score:** {s['average_score']}")
    md.append("")

Path("evaluation/report.md").write_text(
    "\n".join(md),
    encoding="utf-8"
)

print(json.dumps(summary, indent=2))
print("Evaluation completed.")
