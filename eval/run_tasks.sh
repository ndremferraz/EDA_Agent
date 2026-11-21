#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

task_ids=$(python -c 'import json; print("\n".join(json.loads(line)["id"] for line in open("eval/tasks.jsonl") if line.strip()))')

for run in 2 3; do
  while IFS= read -r task_id; do
    [[ -n "$task_id" ]] || continue
    printf 'Running task %s (run %s/3)\n' "$task_id" "$run"
    python -m eval.tasks "$task_id" --run "$run"
  done <<< "$task_ids"
done
