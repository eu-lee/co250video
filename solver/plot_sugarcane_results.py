from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from ortools.sat.python import cp_model

from sugarcaneSolver import sugarcaneSolver


N_VALUES = (3, 4, 6, 7, 8, 11, 12, 13)
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "sugarcane_results_stitched.png"


def solve_grid(n: int) -> tuple[list[list[int]], int, str]:
    solver = sugarcaneSolver(n)
    solver.set_variables()
    solver.set_constraint()
    solver.set_objective(solver.f)

    status = solver.solve()
    status_name = solver.solver.StatusName(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"Could not solve n={n}: {status_name}")

    grid = [
        [int(solver.solver.value(solver.x[(i, j)])) for j in range(n)]
        for i in range(n)
    ]
    return grid, int(solver.solver.objective_value), status_name


def draw_results() -> None:
    water_color = "#2878b5"
    sugarcane_color = "#38a65a"
    cmap = ListedColormap([water_color, sugarcane_color])
    fig, axes = plt.subplots(2, 4, figsize=(16, 9))
    fig.subplots_adjust(left=0.035, right=0.99, bottom=0.09, top=0.86, wspace=0.24, hspace=0.44)

    for ax, n in zip(axes.flat, N_VALUES):
        grid, objective, _status_name = solve_grid(n)
        coverage = objective / (n * n)

        ax.imshow(grid, cmap=cmap, vmin=0, vmax=1)
        ax.set_aspect("equal")

        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(range(1, n + 1), fontsize=7 if n >= 11 else 8)
        ax.set_yticklabels(range(1, n + 1), fontsize=7 if n >= 11 else 8)
        ax.xaxis.tick_top()
        ax.tick_params(axis="both", length=0)

        ax.set_xticks([x - 0.5 for x in range(1, n)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, n)], minor=True)
        ax.grid(which="minor", color="white", linewidth=0.9)
        ax.tick_params(which="minor", bottom=False, left=False)

        ax.set_title(
            f"n = {n}\n{objective} sugarcane ({coverage:.1%})",
            fontsize=12,
            pad=14,
        )

    fig.legend(
        handles=[
            Patch(facecolor=sugarcane_color, label="Sugarcane"),
            Patch(facecolor=water_color, label="Water"),
        ],
        loc="lower center",
        ncol=2,
        frameon=False,
        fontsize=11,
        bbox_to_anchor=(0.5, 0.018),
    )
    fig.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    draw_results()
    print(OUTPUT_PATH)
