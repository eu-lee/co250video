from manim import *
from common import *


class Scene06ObjectiveFunction(BaseSugarcaneScene):
    def construct(self):
        grid = self.grid(10, side=0.38)
        grid.set_fill(opacity=0)

        water_cols = {1, 4, 7, 9}
        water_cells = [(row, col) for row in range(10) for col in water_cols]
        cane_cells = [(row, col) for row in range(10) for col in range(10) if col not in water_cols]

        water_group = VGroup()
        cane_group = VGroup()

        for row, col in cane_cells:
            cell = self.cell(grid, row, col)
            cane_group.add(cell)
        for row, col in water_cells:
            cell = self.cell(grid, row, col)
            water_group.add(cell)

        objective = MathTex(
            r"\max\ \sum_{i=1}^{n}\sum_{j=1}^{n} x_{i,j}",
            font_size=44,
            color=TEXT,
        )

        layout = VGroup(grid, objective).arrange(RIGHT, buff=1.0)
        layout.move_to(ORIGIN)

        numbers = VGroup()
        for row, col in cane_cells:
            numbers.add(Text("1", font_size=14, color="#102015").move_to(self.cell(grid, row, col)))
        for row, col in water_cells:
            numbers.add(Text("0", font_size=14, color="#07131f").move_to(self.cell(grid, row, col)))

        self.play(FadeIn(grid))
        self.play(
            cane_group.animate.set_fill(SUGARCANE, opacity=0.95),
            water_group.animate.set_fill(WATER, opacity=0.95),
            run_time=1.1,
        )
        self.play(FadeIn(numbers), run_time=0.7)
        self.play(Write(objective))
        self.wait(1.2)
