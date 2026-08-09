from manim import *
from common import *


class Scene09DistanceNeighbors(BaseSugarcaneScene):
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

        corner = self.cell(grid, 0, 0)
        corner.set_fill(SUGARCANE, opacity=0.95)
        valid_neighbors = VGroup(
            self.cell(grid, 1, 0),
            self.cell(grid, 0, 1),
        )
        valid_neighbors.set_fill(WATER, opacity=0.95)

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

        final_definition = MathTex(
            r"N(i,j) := \{(p,q)\in\{1,\ldots,n\}^2 : |p-i|+|q-j|=1\}",
            font_size=34,
            color=TEXT,
        )
        final_definition.scale_to_fit_width(7.0)
        final_definition.move_to(formula_stack).shift(UP * 0.18)

        filtered_corner_formula = MathTex(
            r"N(1,1) = \{(2,1),(1,2)\}",
            font_size=34,
            color=TEXT,
        )
        filtered_corner_formula.scale(
            final_definition.height / filtered_corner_formula.height
        )
        filtered_corner_formula.next_to(
            final_definition,
            DOWN,
            buff=0.36,
            aligned_edge=LEFT,
        )

        point_domain = MathTex(
            r"(p,q)\in\{1,\ldots,n\}^2",
            font_size=34,
            color=TEXT,
        )
        manhattan_distance = MathTex(
            r"|p-i|+|q-j|",
            font_size=34,
            color=TEXT,
        )
        expression_stack = VGroup(point_domain, manhattan_distance).arrange(
            DOWN,
            buff=0.42,
            aligned_edge=LEFT,
        )
        expression_stack.move_to(formula_stack)

        row = 4
        col = 5
        selected = self.cell(grid, row, col)
        selected_label = MathTex(r"x_{i,j}", font_size=22, color=TEXT)
        selected_label.next_to(selected, UR, buff=0.08)
        selected_label.set_z_index(5)

        distance_labels = VGroup()
        far_labels = VGroup()
        one_labels = VGroup()
        one_cells = VGroup()
        for dr in range(-3, 4):
            for dc in range(-3, 4):
                r = row + dr
                c = col + dc
                if not (0 <= r < 10 and 0 <= c < 10):
                    continue

                dist = abs(dr) + abs(dc)
                color = TEXT if dist == 0 else WATER if dist == 1 else MUTED
                label = MathTex(str(dist), font_size=15, color=color)
                label.move_to(self.cell(grid, r, c))
                label.set_z_index(5)
                distance_labels.add(label)

                if dist == 1:
                    one_labels.add(label)
                    one_cells.add(self.cell(grid, r, c))
                elif dist != 0:
                    far_labels.add(label)

        self.add(grid, invalid_cells, neighbor_formula, boundary_formula, corner_label)
        self.wait(0.45)
        self.play(
            FadeOut(invalid_cells),
            FadeOut(corner_label),
            FadeOut(neighbor_formula),
            FadeOut(boundary_formula),
            corner.animate.set_fill(opacity=0),
            valid_neighbors.animate.set_fill(opacity=0),
            run_time=0.8,
        )
        self.play(
            selected.animate.set_fill(SUGARCANE, opacity=0.95),
            Write(selected_label),
            Write(point_domain),
            run_time=0.9,
        )
        self.wait(0.45)
        self.play(Write(manhattan_distance), run_time=0.8)
        self.wait(0.35)
        self.play(FadeOut(selected_label), run_time=0.35)
        self.play(FadeIn(distance_labels), run_time=1.0)
        self.wait(0.35)
        self.play(
            one_cells.animate.set_fill(WATER, opacity=0.95),
            far_labels.animate.set_opacity(0.28),
            run_time=0.8,
        )
        self.wait(0.25)
        self.play(
            FadeOut(expression_stack),
            FadeOut(distance_labels),
            run_time=0.65,
        )
        self.wait(0.15)
        self.play(Write(final_definition), run_time=1.0)
        self.wait(0.9)
        self.play(
            selected.animate.set_fill(opacity=0),
            one_cells.animate.set_fill(opacity=0),
            corner.animate.set_fill(SUGARCANE, opacity=0.95),
            valid_neighbors.animate.set_fill(WATER, opacity=0.95),
            Write(corner_label),
            run_time=0.9,
        )
        self.play(Write(filtered_corner_formula), run_time=0.8)
        self.wait(1.2)
