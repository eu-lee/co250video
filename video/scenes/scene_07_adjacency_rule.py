from manim import *
from common import *


class Scene07AdjacencyRule(BaseSugarcaneScene):
    def construct(self):
        correct_grid = self.grid(3, side=0.92)
        incorrect_grid = self.grid(3, side=0.92)
        correct_grid.set_fill(opacity=0)
        incorrect_grid.set_fill(opacity=0)

        grids = VGroup(correct_grid, incorrect_grid).arrange(RIGHT, buff=1.55)
        grids.move_to(ORIGIN + UP * 0.25)

        cardinal_positions = [(0, 1), (1, 0), (1, 2), (2, 1)]
        corner_positions = [(0, 0), (0, 2), (2, 0), (2, 2)]

        correct_center = self.cell(correct_grid, 1, 1)
        incorrect_center = self.cell(incorrect_grid, 1, 1)
        correct_water = VGroup(*[self.cell(correct_grid, row, col) for row, col in cardinal_positions])
        incorrect_water = VGroup(*[self.cell(incorrect_grid, row, col) for row, col in corner_positions])
        correct_cane = VGroup(*[self.cell(correct_grid, row, col) for row, col in corner_positions])
        incorrect_cane = VGroup(*[self.cell(incorrect_grid, row, col) for row, col in cardinal_positions])

        check = Text("✓", font_size=62, color=SUGARCANE, font="Segoe UI Symbol")
        check.next_to(correct_grid, DOWN, buff=0.45)

        x_mark = Text("✗", font_size=62, color=BAD, font="Segoe UI Symbol")
        x_mark.next_to(incorrect_grid, DOWN, buff=0.45)

        invalid_center = Square(side_length=incorrect_center.width)
        invalid_center.set_stroke(BAD, width=5)
        invalid_center.set_fill(opacity=0)
        invalid_center.move_to(incorrect_center)
        invalid_center.set_z_index(3)

        self.play(FadeIn(grids))
        self.play(
            correct_center.animate.set_fill(SUGARCANE, opacity=0.95),
            incorrect_center.animate.set_fill(SUGARCANE, opacity=0.95),
            run_time=0.55,
        )
        self.play(
            correct_water.animate.set_fill(WATER, opacity=0.95),
            incorrect_water.animate.set_fill(WATER, opacity=0.95),
            run_time=0.85,
        )
        self.play(
            correct_cane.animate.set_fill(SUGARCANE, opacity=0.95),
            incorrect_cane.animate.set_fill(SUGARCANE, opacity=0.95),
            run_time=0.75,
        )
        self.play(Create(invalid_center), run_time=0.45)
        self.play(Write(check), Write(x_mark), run_time=0.55)
        self.wait(1.2)
