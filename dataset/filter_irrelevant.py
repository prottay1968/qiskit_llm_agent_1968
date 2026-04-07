import json
from pathlib import Path

INPUT = Path("data/train_syntax_clean.jsonl")
OUTPUT = Path("data/train_filtered_v1.jsonl")
REPORT = Path("reports/filter_irrelevant_report.txt")

BAD_KEYWORDS = [
    "qiskit_chemistry",
]

total = 0
kept = 0
removed = 0
removed_examples = []

with INPUT.open("r", encoding="utf-8") as fin, OUTPUT.open("w", encoding="utf-8") as fout:
    for idx, line in enumerate(fin, start=1):
        line = line.strip()
        if not line:
            continue
        total += 1
        obj = json.loads(line)

        text = (obj.get("prompt", "") + "\n" + obj.get("completion", "")).lower()

        if any(keyword in text for keyword in BAD_KEYWORDS):
            removed += 1
            if len(removed_examples) < 50:
                removed_examples.append((idx, obj.get("task_id", "N/A")))
            continue

        fout.write(json.dumps(obj, ensure_ascii=False) + "\n")
        kept += 1

with REPORT.open("w", encoding="utf-8") as f:
    f.write(f"Total samples: {total}\n")
    f.write(f"Kept: {kept}\n")
    f.write(f"Removed due to irrelevant imports: {removed}\n\n")
    f.write("Example removed rows:\n")
    for idx, task_id in removed_examples:
        f.write(f"Line {idx}: {task_id}\n")

print(f"Total samples: {total}")
print(f"Kept: {kept}")
print(f"Removed due to irrelevant imports: {removed}")
print(f"Saved cleaned dataset to: {OUTPUT}")
print(f"Saved report to: {REPORT}")
