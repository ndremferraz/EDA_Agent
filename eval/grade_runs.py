"""Grade saved runs with KiCAD_benchmark/benchmark.py.

    python eval/grade_runs.py

Writes eval/grades.json with per-run results and per-task means. Missing
schematics score zero; grading errors have no score and are counted separately.
Refusal tasks have no reference circuit and are reported as not applicable.
"""

import argparse
import importlib.util
import json
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_grader(benchmark):
    # benchmark.py imports its sibling circuit_comparison.py.
    sys.path.insert(0, str(benchmark))
    spec = importlib.util.spec_from_file_location("kicad_benchmark_grader", benchmark / "benchmark.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.grade_circuit


def find_schematic(run_dir, task_id):
    metadata = run_dir / "_run.json"
    if metadata.is_file():
        result = json.loads(metadata.read_text())
        saved_path = result.get("schematic")
        if saved_path:
            candidate = Path(saved_path)
            candidate = (candidate if candidate.is_absolute() else run_dir / candidate).resolve()
            if candidate.is_relative_to(run_dir) and candidate.is_file():
                return candidate
    # Also support interrupted runs and output directories moved to a new machine.
    candidate = run_dir / f"{task_id}.kicad_sch"
    if candidate.is_file():
        return candidate
    schematics = sorted(run_dir.glob("*.kicad_sch"))
    if len(schematics) > 1:
        raise ValueError("Multiple schematics found; no identifiable top-level schematic")
    return schematics[0] if schematics else None


def grade_run(task, run_dir, benchmark, grade_circuit):
    result = dict(task_id=task["id"], run=run_dir.name, run_dir=str(run_dir),
                  status=None, schematic=None, reference_netlist=None,
                  similarity=None, errors=None, warnings=None, grade=None)
    if task["type"] != "build":
        return dict(result, status="not_applicable", reason="Task has no reference circuit")
    try:
        reference = benchmark / task["reference_netlist"]
        result["reference_netlist"] = str(reference)
        if not reference.is_file():
            raise FileNotFoundError(f"Missing reference netlist: {reference}")
        schematic = find_schematic(run_dir, task["id"])
        if schematic is None:
            return dict(result, status="missing_schematic", grade=0.0)
        result["schematic"] = str(schematic)
        score = grade_circuit(str(schematic), str(reference))
        return dict(result, **score, status="graded")
    except Exception as exc:
        detail = str(exc)
        if isinstance(exc, subprocess.CalledProcessError):
            detail += "\n" + (exc.stderr or exc.stdout or "").strip()
        return dict(result, status="error", reason=detail.strip())


def summarize(results):
    scores = [r["grade"] for r in results if r["grade"] is not None]
    return dict(runs=len(results),
                graded=sum(r["status"] == "graded" for r in results),
                missing_schematic=sum(r["status"] == "missing_schematic" for r in results),
                errors=sum(r["status"] == "error" for r in results),
                not_applicable=sum(r["status"] == "not_applicable" for r in results),
                scored_runs=len(scores),
                mean_grade=statistics.mean(scores) if scores else None)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tasks", type=Path, default=HERE / "tasks.jsonl")
    parser.add_argument("--benchmark", type=Path, default=HERE.parent.parent / "KiCAD_benchmark")
    parser.add_argument("--output-root", type=Path, default=HERE / "output")
    parser.add_argument("--report", type=Path, default=HERE / "grades.json")
    args = parser.parse_args(argv)
    benchmark = args.benchmark.resolve()
    output = args.output_root.resolve()
    if not (benchmark / "benchmark.py").is_file():
        parser.error(f"Missing grader: {benchmark / 'benchmark.py'}")
    if not output.is_dir():
        parser.error(f"Run output directory does not exist: {output}")
    try:
        grader = load_grader(benchmark)
    except ImportError as exc:
        parser.error(f"Cannot import benchmark grader: {exc}. Install its dependencies (including networkx).")
    tasks = [json.loads(line) for line in args.tasks.read_text().splitlines() if line.strip()]
    results = []
    task_summaries = {}
    no_runs = []
    for task in tasks:
        run_dirs = sorted((p for p in (output / task["id"]).glob("run*")
                           if p.is_dir() and p.name[3:].isdigit()),
                          key=lambda p: int(p.name[3:]))
        if not run_dirs:
            no_runs.append(task["id"])
            continue
        task_results = []
        for run_dir in run_dirs:
            print(f"{task['id']}/{run_dir.name}: ", end="", flush=True)
            result = grade_run(task, run_dir, benchmark, grader)
            task_results.append(result)
            if result["status"] == "graded":
                print(f"grade={result['grade']:.2f} similarity={result['similarity']:.2f} "
                      f"ERC errors={result['errors']} warnings={result['warnings']}")
            else:
                print(result["status"] + (": " + result["reason"] if "reason" in result else " (grade=0)"))
        results.extend(task_results)
        task_summaries[task["id"]] = summarize(task_results)
    summary = summarize(results)
    report = dict(tasks_file=str(args.tasks.resolve()), benchmark=str(benchmark),
                  output_root=str(output),
                  scoring="benchmark.py grades; missing schematics score 0; grading errors and refusal tasks excluded from means",
                  summary=summary, tasks_without_runs=no_runs,
                  per_task=task_summaries, results=results)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    mean = summary["mean_grade"]
    print(f"\n{summary['graded']} graded, {summary['missing_schematic']} missing schematics, "
          f"{summary['errors']} grading errors, {summary['not_applicable']} not applicable.")
    print(f"Mean grade: {mean:.2f}" if mean is not None else "Mean grade: n/a")
    print(f"Report: {args.report.resolve()}")
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
