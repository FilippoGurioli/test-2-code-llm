import json
import re
from pathlib import Path
from collections import defaultdict
from tabulate import tabulate
import pandas as pd

# === CONFIG ===
# path to the report
JSON_PATH = Path("../output/report.json")
# weights to compute the formula
weights: dict[str, float] = {
        "success_rate": 0.4,
        "test_pass_rate": 0.4,
        "avg_coverage": 0.2,
        "norm_time": 0.1
}
# display order
sort: list[str] = ["Score", "Complexity"]

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

# === BUILD RAW OUTPUT ===
output_lines = []
for (complexity, tests), group in grouped.items():
    ranked = sorted(group, key=lambda x: x["score"], reverse=True)
    output_lines.append(f"=== {complexity.upper()} | {tests} ===")
    for i, e in enumerate(ranked, 1):
        output_lines.append(
            f"{i}. {e['model']:10s} | Score: {e['score']:.3f} | "
            f"Success: {e['success_rate']:.2f} | Pass: {e['test_pass_rate']:.2f} | Coverage: {e['avg_coverage']:.2f}"
        )
    output_lines.append("")

# === PARSE RAW OUTPUT INTO TABLE ===
raw_data = "\n".join(output_lines)
pattern_header = re.compile(r"=== (\w+) \| ([\w+x]+) ===")
pattern_entry = re.compile(r"\d+\.\s+([\w\-]+)\s+\|\s+Score:\s+([\-0-9\.]+)")

data = []
current_complexity, current_test = None, None

for line in raw_data.splitlines():
    header_match = pattern_header.match(line.strip())
    if header_match:
        current_complexity, current_test = header_match.groups()
        continue

    entry_match = pattern_entry.match(line.strip())
    if entry_match and current_complexity and current_test:
        llm, score = entry_match.groups()
        data.append([current_complexity, current_test, llm, float(score)])

df = pd.DataFrame(data, columns=["Complexity", "Test kind", "LLM", "Score"])

# === PRINT FINAL TABLE ===
print(tabulate(df.sort_values(by=sort, ascending=False), headers="keys", tablefmt="github"))
