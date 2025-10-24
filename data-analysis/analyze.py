import json
import re
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

JSON_PATH = Path("../output/report.json")

with open(JSON_PATH, "r") as f:
    data = json.load(f)

results = []

pattern = re.compile(
    r"(?P<complexity>low|medium|high)-complexity-"
    r"(?P<model>mistral|llama3|gemini|smollm2|deepseek-r1|qwen3)-"
    r"(?P<tests>AT|IT|UT|ATxIT|ATxUT|ITxUT|ATxITxUT)-"
    r"(?P<date>\d{8}_\d{6})"
)

for key, entry in data.items():
    match = pattern.match(key)
    if not match:
        print(f"⚠️ Skipping unexpected key: {key}")
        continue

    meta = match.groupdict()
    model = meta["model"]
    complexity = meta["complexity"]
    tests = meta["tests"]

    runs = entry.get("runs", [])
    if not runs:
        print(f"⚠️ Skipping unexpected empty runs: {key}")
        continue

    total_coverage = 0
    total_passed = 0
    total_tests = 0
    total_successes = 0
    total_code_time = 0
    total_validation_time = 0

    for run in runs:
        cg = run.get("code-generation", {})
        tv = run.get("test-validation", {})

        total_successes += int(cg.get("success", False))
        total_code_time += cg.get("time-taken", 0)
        total_validation_time += tv.get("time-taken", 0)
        total_passed += tv.get("passed-tests", 0)
        total_tests += tv.get("number-of-tests", 0)
        total_coverage += tv.get("coverage", 0)

    n = len(runs)
    if n == 0:
        continue

    avg_coverage = total_coverage / n
    avg_code_time = total_code_time / n
    avg_validation_time = total_validation_time / n
    success_rate = total_successes / n
    test_pass_rate = total_passed / total_tests if total_tests else 0

    results.append({
        "model": model,
        "complexity": complexity,
        "tests": tests,
        "avg_coverage": avg_coverage,
        "avg_code_time": avg_code_time,
        "avg_validation_time": avg_validation_time,
        "success_rate": success_rate,
        "test_pass_rate": test_pass_rate,
    })

by_model = {}
for r in results:
    model = r["model"]
    by_model.setdefault(model, []).append(r)

avg_by_model = {}
for model, vals in by_model.items():
    avg_by_model[model] = {
        "avg_coverage": np.mean([v["avg_coverage"] for v in vals]),
        "success_rate": np.mean([v["success_rate"] for v in vals]),
        "avg_code_time": np.mean([v["avg_code_time"] for v in vals]),
    }

# === VISUALIZE ===
models = list(avg_by_model.keys())
coverage = [avg_by_model[m]["avg_coverage"] for m in models]
success = [avg_by_model[m]["success_rate"] for m in models]
code_time = [avg_by_model[m]["avg_code_time"] for m in models]

fig, ax1 = plt.subplots(figsize=(10, 6))
x = np.arange(len(models))
bar_width = 0.25

ax1.bar(x - bar_width, coverage, width=bar_width, label="Coverage")
ax1.bar(x, success, width=bar_width, label="Success rate")
ax1.bar(x + bar_width, code_time, width=bar_width, label="Code time (s)")

ax1.set_xticks(x)
ax1.set_xticklabels(models)
ax1.set_ylabel("Value")
ax1.set_title("Model Performance Overview")
ax1.legend()
plt.tight_layout()
plt.show()
