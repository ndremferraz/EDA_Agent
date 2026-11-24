#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."

task_ids=$(python -c 'import json; print("\n".join(json.loads(line)["id"] for line in open("eval/tasks.jsonl") if line.strip()))')

# Default uses runs 1-3; ReAct uses 4-6; Plan-and-Replan uses 7-9.
run=4
for approach in react plan-and-replan; do
  for attempt in 1 2 3; do
    while IFS= read -r task_id; do
      [[ -n "$task_id" ]] || continue
      run_dir="eval/output/$task_id/run$run"
      if [[ -e "$run_dir" ]]; then
        printf 'Skipping task %s (%s, run %s): %s already exists\n' "$task_id" "$approach" "$run" "$run_dir"
        continue
      fi
      printf 'Running task %s (%s, attempt %s/3, run %s)\n' "$task_id" "$approach" "$attempt" "$run"
      python -m eval.tasks "$task_id" --run "$run" --approach "$approach"
    done <<< "$task_ids"
    run=$((run + 1))
  done
done
