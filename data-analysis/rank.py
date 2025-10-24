import json
import re
from pathlib import Path
import numpy as np
from collections import defaultdict

# === CONFIG ===
JSON_PATH = Path("../output/report.json")
weights: dict[str, float] = {
        "success_rate": 0.4,
        "test_pass_rate": 0.4,
        "avg_coverage": 0.2,
        "norm_time": 0.1
}

# === LOAD ===
with open(JSON_PATH, "r") as f:
    data = json.load(f)

pattern = re.compile(
    r"(?P<complexity>low|medium|high)-complexity-"
    r"(?P<model>mistral|llama3|gemini|smollm2|deepseek-r1|qwen3)-"
    r"(?P<tests>AT|IT|UT|ATxIT|ATxUT|ITxUT|ATxITxUT)-"
    r"(?P<date>\d{8}_\d{6})"
)

# === COLLECT RAW STATS ===
entries = []
for key, entry in data.items():
    match = pattern.match(key)
    if not match:
        continue

    meta = match.groupdict()
    runs = entry.get("runs", [])
    if not runs:
        continue

    total_success = 0
    total_passed = 0
    total_tests = 0
    total_coverage = 0
    total_code_time = 0
    total_val_time = 0

    for run in runs:
        cg = run.get("code-generation", {})
        tv = run.get("test-validation", {})

        total_success += int(cg.get("success", False))
        total_code_time += cg.get("time-taken", 0)
        total_val_time += tv.get("time-taken", 0)
        total_passed += tv.get("passed-tests", 0)
        total_tests += tv.get("number-of-tests", 0)
        total_coverage += tv.get("coverage", 0)

    n = len(runs)
    entries.append({
        **meta,
        "success_rate": total_success / n if n else 0,
        "test_pass_rate": total_passed / total_tests if total_tests else 0,
        "avg_coverage": total_coverage / n if n else 0,
        "avg_code_time": total_code_time / n if n else 0,
        "avg_val_time": total_val_time / n if n else 0,
    })

# === NORMALIZE TIME ===
max_time = max(
    (e["avg_code_time"] + e["avg_val_time"]) for e in entries if e["avg_code_time"] + e["avg_val_time"] > 0
)
for e in entries:
    total_time = e["avg_code_time"] + e["avg_val_time"]
    e["norm_time"] = total_time / max_time if max_time else 0

# === COMPUTE SCORE ===
for e in entries:
    e["score"] = (
        weights["success_rate"] * e["success_rate"]
        + weights["test_pass_rate"] * e["test_pass_rate"]
        + weights["avg_coverage"] * e["avg_coverage"]
        - weights["norm_time"] * e["norm_time"]
    )

# === GROUP AND RANK ===
grouped = defaultdict(list)
for e in entries:
    key = (e["complexity"], e["tests"])
    grouped[key].append(e)

for (complexity, tests), group in grouped.items():
    ranked = sorted(group, key=lambda x: x["score"], reverse=True)
    print(f"\n=== {complexity.upper()} | {tests} ===")
    for i, e in enumerate(ranked, 1):
        print(
            f"{i}. {e['model']:10s} | Score: {e['score']:.3f} | "
            f"Success: {e['success_rate']:.2f} | Pass: {e['test_pass_rate']:.2f} | Coverage: {e['avg_coverage']:.2f}"
        )
