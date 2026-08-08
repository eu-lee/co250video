from manim import *
from common import *


class Scene08NeighborEdgeCases(BaseSugarcaneScene):
    def construct(self):
        grid = self.grid(10, side=0.38)
        grid.set_fill(opacity=0)

        neighbor_formula = MathTex(
            r"N(i,j) = \{",
            r"(i-1,j),",
            r"(i+1,j),",
            r"(i,j-1),",
            r"(i,j+1)",
            r"\}",
            font_size=34,
            color=TEXT,
        )
        neighbor_formula.scale_to_fit_width(5.7)

        boundary_formula = MathTex(
            r"N(1,1) = \{",
            r"(0,1),",
            r"(2,1),",
            r"(1,0),",
            r"(1,2)",
            r"\}",
            font_size=34,
            color=TEXT,
        )
        boundary_formula[1].set_color(BAD)
        boundary_formula[3].set_color(BAD)
        boundary_formula.scale(neighbor_formula.height / boundary_formula.height)

        formula_stack = VGroup(neighbor_formula, boundary_formula).arrange(
            DOWN,
            buff=0.38,
            aligned_edge=LEFT,
        )
        layout = VGroup(grid, formula_stack).arrange(RIGHT, buff=0.85)
        layout.move_to(ORIGIN)

        row = 4
        col = 5
        selected = self.cell(grid, row, col)
        neighbors = VGroup(
            self.cell(grid, row - 1, col),
            self.cell(grid, row + 1, col),
            self.cell(grid, row, col - 1),
            self.cell(grid, row, col + 1),
        )

        selected_label = MathTex(r"x_{i,j}", font_size=24, color=TEXT)
        selected_label.next_to(selected, UR, buff=0.08)
        selected_label.set_z_index(4)

        self.play(FadeIn(grid))
        self.play(
            selected.animate.set_fill(SUGARCANE, opacity=0.95),
            Write(selected_label),
            run_time=0.7,
        )
        self.wait(0.2)
        self.play(
            AnimationGroup(
                *[
                    cell.animate.set_fill(WATER, opacity=0.95)
                    for cell in neighbors
                ],
                lag_ratio=0.08,
            ),
            run_time=0.9,
        )
        self.play(Write(neighbor_formula), run_time=1.0)
        self.wait(1.2)

        self.play(
            FadeOut(selected_label),
            selected.animate.set_fill(opacity=0),
            neighbors.animate.set_fill(opacity=0),
            run_time=0.65,
        )

        corner = self.cell(grid, 0, 0)
        valid_corner_neighbors = VGroup(
            self.cell(grid, 1, 0),
            self.cell(grid, 0, 1),
        )

        invalid_up = Square(side_length=corner.width)
        invalid_up.set_stroke(opacity=0)
        invalid_up.set_fill("#ff2d2d", opacity=0.42)
        invalid_up.move_to(corner.get_center() + UP * corner.height)

        invalid_left = invalid_up.copy()
        invalid_left.move_to(corner.get_center() + LEFT * corner.width)

        invalid_cells = VGroup(invalid_up, invalid_left)
        invalid_cells.set_z_index(2)

        corner_label = MathTex(r"x_{1,1}", font_size=22, color=TEXT)
        corner_label.next_to(corner, DR, buff=0.08)
        corner_label.set_z_index(4)

        self.play(
            corner.animate.set_fill(SUGARCANE, opacity=0.95),
            Write(corner_label),
            run_time=0.65,
        )
        self.play(
            valid_corner_neighbors.animate.set_fill(WATER, opacity=0.95),
            FadeIn(invalid_cells),
            run_time=0.85,
        )
        self.play(Write(boundary_formula), run_time=1.0)
        self.wait(1.2)
