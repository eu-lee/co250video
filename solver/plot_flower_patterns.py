from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from ortools.sat.python import cp_model

from sugarcaneSolver import sugarcaneSolver


N = 13
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "sugarcane_13x13_flowers.png"


def solve_grid(n: int) -> tuple[list[list[int]], int]:
    solver = sugarcaneSolver(n)
    solver.solver.parameters.num_search_workers = 8
    solver.solver.parameters.random_seed = 1
    solver.solver.parameters.max_time_in_seconds = 20
    solver.set_variables()
    solver.set_constraint()
    solver.set_objective(solver.f)

    status = solver.solve()
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"Could not solve n={n}: {solver.solver.StatusName(status)}")

    grid = [
        [int(solver.solver.value(solver.x[(i, j)])) for j in range(n)]
        for i in range(n)
    ]
    return grid, int(solver.solver.objective_value)


def flower_cells(grid: list[list[int]], i: int, j: int) -> set[tuple[int, int]] | None:
    n = len(grid)
    neighbors = ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
    if grid[i][j] != 0:
        return None
    if any(not (0 <= p < n and 0 <= q < n) for p, q in neighbors):
        return None
    if any(grid[p][q] != 1 for p, q in neighbors):
        return None
    return {(i, j), *neighbors}


def draw_cell_outline(ax: plt.Axes, cells: set[tuple[int, int]]) -> None:
    edges: dict[tuple[tuple[float, float], tuple[float, float]], int] = {}

    for i, j in cells:
        x0, x1 = j - 0.5, j + 0.5
        y0, y1 = i - 0.5, i + 0.5
        cell_edges = (
            ((x0, y0), (x1, y0)),
            ((x1, y0), (x1, y1)),
            ((x0, y1), (x1, y1)),
            ((x0, y0), (x0, y1)),
        )

        for start, end in cell_edges:
            key = tuple(sorted((start, end)))
            edges[key] = edges.get(key, 0) + 1

    for (start, end), count in edges.items():
        if count == 1:
            ax.plot(
                [start[0], end[0]],
                [start[1], end[1]],
                color="#e03131",
                alpha=0.28,
                linewidth=4.2,
                solid_capstyle="round",
                zorder=5,
            )
            ax.plot(
                [start[0], end[0]],
                [start[1], end[1]],
                color="#e03131",
                linewidth=1.4,
                solid_capstyle="round",
                zorder=6,
            )


def select_non_overlapping_flowers(grid: list[list[int]]) -> list[set[tuple[int, int]]]:
    flowers: list[set[tuple[int, int]]] = []
    used: set[tuple[int, int]] = set()

    for i in range(len(grid)):
        for j in range(len(grid)):
            cells = flower_cells(grid, i, j)
            if cells is None:
                continue
            if cells & used:
                continue

            flowers.append(cells)
            used.update(cells)

    return flowers


def draw_figure() -> None:
    grid, objective = solve_grid(N)
    coverage = objective / (N * N)

    water_color = "#2878b5"
    sugarcane_color = "#38a65a"
    cmap = ListedColormap([water_color, sugarcane_color])

    fig, ax = plt.subplots(figsize=(8.2, 8.7))
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=1)
    ax.set_aspect("equal")

    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.set_xticklabels(range(1, N + 1), fontsize=11)
    ax.set_yticklabels(range(1, N + 1), fontsize=11)
    ax.xaxis.tick_top()
    ax.tick_params(axis="both", length=0)

    ax.set_xticks([x - 0.5 for x in range(1, N)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, N)], minor=True)
    ax.grid(which="minor", color="#a4d3a8", linewidth=1.0)
    ax.tick_params(which="minor", bottom=False, left=False)

    for cells in select_non_overlapping_flowers(grid):
        draw_cell_outline(ax, cells)

    ax.set_xlabel(f"Optimal: {objective} sugarcane, coverage {coverage:.1%}", labelpad=18)

    fig.legend(
        handles=[
            Patch(facecolor=sugarcane_color, label="Sugarcane"),
            Patch(facecolor=water_color, label="Water"),
            Patch(facecolor="none", edgecolor="#e03131", linewidth=1.5, label="Optimal tile"),
        ],
        loc="lower center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, 0.01),
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=0.87, bottom=0.14)
    fig.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    draw_figure()
    print(OUTPUT_PATH)
