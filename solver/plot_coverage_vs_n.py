from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from ortools.sat.python import cp_model


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "sugarcane_coverage_vs_n.png"
DEFAULT_CSV = ROOT / "sugarcane_coverage_vs_n.csv"


@dataclass(frozen=True)
class CoverageResult:
    n: int
    sugarcane: int
    coverage: float
    status: str
    best_bound: float
    wall_time: float


def cardinal_neighbors(i: int, j: int, n: int) -> list[tuple[int, int]]:
    candidates = ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
    return [(p, q) for p, q in candidates if 0 <= p < n and 0 <= q < n]


def constructive_hint(n: int) -> list[list[int]]:
    grid = [[0 if (i + 2 * j) % 5 == 0 else 1 for j in range(n)] for i in range(n)]

    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if grid[i][j] == 0:
                    continue

                if not any(grid[p][q] == 0 for p, q in cardinal_neighbors(i, j, n)):
                    grid[i][j] = 0
                    changed = True

    return grid


def solve_coverage(n: int, time_limit: float, workers: int) -> CoverageResult:
    model = cp_model.CpModel()
    x = {(i, j): model.new_bool_var(f"x_{i}_{j}") for i in range(n) for j in range(n)}

    for i in range(n):
        for j in range(n):
            adjacent_water = sum(1 - x[p, q] for p, q in cardinal_neighbors(i, j, n))
            model.add(adjacent_water >= x[i, j])

    model.maximize(sum(x.values()))

    hint = constructive_hint(n)
    for i in range(n):
        for j in range(n):
            model.add_hint(x[i, j], hint[i][j])

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers

    status = solver.solve(model)
    status_name = solver.StatusName(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sugarcane = sum(sum(row) for row in hint)
        coverage = sugarcane / (n * n)
        return CoverageResult(
            n=n,
            sugarcane=sugarcane,
            coverage=coverage,
            status=f"{status_name} (constructive)",
            best_bound=0.8 * n * n,
            wall_time=solver.wall_time,
        )

    sugarcane = int(round(solver.objective_value))
    return CoverageResult(
        n=n,
        sugarcane=sugarcane,
        coverage=sugarcane / (n * n),
        status=status_name,
        best_bound=solver.best_objective_bound,
        wall_time=solver.wall_time,
    )


def write_csv(results: list[CoverageResult], csv_path: Path) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["n", "sugarcane", "coverage", "status", "best_bound", "wall_time"])
        for result in results:
            writer.writerow(
                [
                    result.n,
                    result.sugarcane,
                    f"{result.coverage:.8f}",
                    result.status,
                    f"{result.best_bound:.3f}",
                    f"{result.wall_time:.3f}",
                ]
            )


def plot_results(results: list[CoverageResult], output_path: Path) -> None:
    optimal = [result for result in results if result.status == "OPTIMAL"]
    feasible = [result for result in results if result.status != "OPTIMAL"]

    fig, ax = plt.subplots(figsize=(11, 6.2))

    ax.plot(
        [result.n for result in results],
        [100 * result.coverage for result in results],
        color="#212529",
        linewidth=1.0,
        zorder=1,
    )

    if optimal:
        ax.plot(
            [result.n for result in optimal],
            [100 * result.coverage for result in optimal],
            color="#2f9e44",
            marker="o",
            linewidth=2,
            label="proven optimal",
            zorder=2,
        )

    if feasible:
        ax.scatter(
            [result.n for result in feasible],
            [100 * result.coverage for result in feasible],
            color="#f2c94c",
            marker="o",
            s=36,
            label="feasible solution",
            zorder=3,
        )

    ax.set_title("% Coverage vs N", fontsize=18, weight="bold", pad=14)
    ax.set_xlabel("N")
    ax.set_ylabel("Coverage (%)")
    ax.set_xticks([result.n for result in results])
    ax.set_ylim(0, 100)
    ax.grid(True, axis="y", color="#dee2e6", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="lower right")

    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot optimal/best-known sugarcane coverage vs N.")
    parser.add_argument("--min-n", type=int, default=1)
    parser.add_argument("--max-n", type=int, default=25)
    parser.add_argument("--time-limit", type=float, default=5.0, help="CP-SAT seconds per N.")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    if args.min_n < 1:
        raise ValueError("--min-n must be at least 1")
    if args.max_n < args.min_n:
        raise ValueError("--max-n must be at least --min-n")

    results = [
        solve_coverage(n, time_limit=args.time_limit, workers=args.workers)
        for n in range(args.min_n, args.max_n + 1)
    ]

    write_csv(results, args.csv)
    plot_results(results, args.output)

    print(args.output)
    print(args.csv)
    for result in results:
        print(
            f"n={result.n:2d} coverage={100 * result.coverage:5.1f}% "
            f"sugarcane={result.sugarcane:4d} status={result.status}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
