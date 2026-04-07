import json
import ast
from pathlib import Path

INPUT = Path("data/train_original.jsonl")
OUTPUT = Path("data/train_syntax_clean.jsonl")
REPORT = Path("reports/filter_syntax_report.txt")

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
        try:
            obj = json.loads(line)
            prompt = obj.get("prompt", "")
            completion = obj.get("completion", "")
            full_code = prompt + completion
            ast.parse(full_code)
            fout.write(json.dumps(obj, ensure_ascii=False) + "\n")
            kept += 1
        except Exception as e:
            removed += 1
            if len(removed_examples) < 50:
                removed_examples.append((idx, str(e)))

with REPORT.open("w", encoding="utf-8") as f:
    f.write(f"Total samples: {total}\n")
    f.write(f"Kept (syntax valid): {kept}\n")
    f.write(f"Removed (syntax invalid): {removed}\n\n")
    f.write("Example removed rows:\n")
    for idx, err in removed_examples:
        f.write(f"Line {idx}: {err}\n")

print(f"Total samples: {total}")
print(f"Kept (syntax valid): {kept}")
print(f"Removed (syntax invalid): {removed}")
print(f"Saved cleaned dataset to: {OUTPUT}")
print(f"Saved report to: {REPORT}")

