from manim import *
from common import *


class Scene10ConstraintLogic(BaseSugarcaneScene):
    def construct(self):
        grid = self.grid(10, side=0.38)
        grid.set_fill(opacity=0)

        scene_09_neighbor_formula = MathTex(
            r"N(i,j) = \{",
            r"(i-1,j),",
            r"(i+1,j),",
            r"(i,j-1),",
            r"(i,j+1)",
            r"\}",
            font_size=34,
            color=TEXT,
        )
        scene_09_neighbor_formula.scale_to_fit_width(5.7)
        scene_09_boundary_formula = MathTex(
            r"N(1,1) = \{",
            r"(0,1),",
            r"(2,1),",
            r"(1,0),",
            r"(1,2)",
            r"\}",
            font_size=34,
            color=TEXT,
        )
        scene_09_boundary_formula.scale(
            scene_09_neighbor_formula.height / scene_09_boundary_formula.height
        )
        scene_09_formula_anchor = VGroup(
            scene_09_neighbor_formula,
            scene_09_boundary_formula,
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        VGroup(grid, scene_09_formula_anchor).arrange(RIGHT, buff=0.85).move_to(ORIGIN)

        neighbor_definition = MathTex(
            r"N(i,j) := \{(p,q)\in\{1,\ldots,n\}^2 : |p-i|+|q-j|=1\}",
            font_size=34,
            color=TEXT,
        )
        neighbor_definition.scale_to_fit_width(7.0)
        neighbor_definition.move_to(scene_09_formula_anchor).shift(UP * 0.18)

        constraint = MathTex(
            r"\sum_{(p,q)\in N(i,j)} (1-x_{p,q}) \ge x_{i,j}",
            font_size=34,
            color=TEXT,
        )
        water_indicator = MathTex(
            r"1-x_{p,q}="
            r"\begin{cases}"
            r"1, & \text{if neighbour has water}\\"
            r"0, & \text{if neighbour has sugarcane}"
            r"\end{cases}",
            font_size=34,
            color=TEXT,
        )
        valid_sum = MathTex(
            r"1+0+1+0 \ge 1",
            font_size=34,
            color=TEXT,
        )
        invalid_sum = MathTex(
            r"0+0+0+0 = 0",
            font_size=34,
            color=TEXT,
        )
        invalid_result = MathTex(
            r"0 \not\ge 1",
            font_size=34,
            color=BAD,
        )

        filtered_corner_formula = MathTex(
            r"N(1,1) = \{(2,1),(1,2)\}",
            font_size=34,
            color=TEXT,
        )
        filtered_corner_formula.scale(
            neighbor_definition.height / filtered_corner_formula.height
        )
        filtered_corner_formula.next_to(
            neighbor_definition,
            DOWN,
            buff=0.36,
            aligned_edge=LEFT,
        )

        neighbor_definition_target = neighbor_definition.copy().shift(UP * 0.95)
        constraint.next_to(
            neighbor_definition_target,
            DOWN,
            buff=0.36,
            aligned_edge=LEFT,
        )
        water_indicator.next_to(
            neighbor_definition_target,
            DOWN,
            buff=0.36,
            aligned_edge=LEFT,
        )
        valid_sum.next_to(constraint, DOWN, buff=0.48, aligned_edge=LEFT)
        invalid_sum.move_to(valid_sum)
        invalid_result.next_to(invalid_sum, DOWN, buff=0.3, aligned_edge=LEFT)

        check = Text("\u2713", font_size=60, color=SUGARCANE, font="Segoe UI Symbol")
        check.next_to(valid_sum, DOWN, buff=0.28)

        x_mark = Text("\u2717", font_size=60, color=BAD, font="Segoe UI Symbol")
        x_mark.next_to(invalid_result, DOWN, buff=0.22)

        row = 4
        col = 5
        center = self.cell(grid, row, col)
        north = self.cell(grid, row - 1, col)
        south = self.cell(grid, row + 1, col)
        east = self.cell(grid, row, col + 1)
        west = self.cell(grid, row, col - 1)

        center_label = MathTex(r"x_{i,j}", font_size=22, color=TEXT)
        center_label.next_to(center, UR, buff=0.08)
        center_label.set_z_index(5)

        center_value = Text("1", font_size=14, color="#102015")
        center_value.move_to(center)
        center_value.set_z_index(5)

        neighbors = [north, south, east, west]
        valid_neighbor_data = [
            (north, WATER, "0", "1"),
            (south, SUGARCANE, "1", "0"),
            (east, WATER, "0", "1"),
            (west, SUGARCANE, "1", "0"),
        ]

        cell_values = VGroup()
        for cell, color, value, _ in valid_neighbor_data:
            text_color = "#07131f" if color == WATER else "#102015"
            value_label = Text(value, font_size=14, color=text_color)
            value_label.move_to(cell)
            value_label.set_z_index(5)
            cell_values.add(value_label)

        valid_parts = MathTex(
            "1",
            "+",
            "0",
            "+",
            "1",
            "+",
            "0",
            r"\ge",
            "1",
            font_size=34,
            color=TEXT,
        )
        valid_parts.move_to(valid_sum)

        invalid_values = VGroup()
        for cell in neighbors:
            value_label = Text("1", font_size=14, color="#102015")
            value_label.move_to(cell)
            value_label.set_z_index(5)
            invalid_values.add(value_label)

        invalid_parts = MathTex(
            "0",
            "+",
            "0",
            "+",
            "0",
            "+",
            "0",
            "=",
            "0",
            font_size=34,
            color=TEXT,
        )
        invalid_parts.move_to(invalid_sum)

        corner = self.cell(grid, 0, 0)
        corner.set_fill(SUGARCANE, opacity=0.95)
        scene_09_valid_neighbors = VGroup(
            self.cell(grid, 1, 0),
            self.cell(grid, 0, 1),
        )
        scene_09_valid_neighbors.set_fill(WATER, opacity=0.95)
        corner_label = MathTex(r"x_{1,1}", font_size=22, color=TEXT)
        corner_label.next_to(corner, DR, buff=0.08)
        corner_label.set_z_index(4)

        self.add(
            grid,
            neighbor_definition,
            filtered_corner_formula,
            corner_label,
        )
        self.wait(0.65)
        self.play(
            FadeOut(filtered_corner_formula),
            FadeOut(corner_label),
            corner.animate.set_fill(opacity=0),
            scene_09_valid_neighbors.animate.set_fill(opacity=0),
            run_time=0.75,
        )
        self.wait(0.25)
        self.play(Transform(neighbor_definition, neighbor_definition_target), run_time=0.75)
        self.wait(0.3)
        self.play(Write(water_indicator), run_time=1.0)
        self.wait(0.8)
        self.play(FadeOut(water_indicator), run_time=0.45)
        self.wait(0.25)
        self.play(Write(constraint), run_time=0.8)
        self.play(
            center.animate.set_fill(SUGARCANE, opacity=0.95),
            FadeIn(center_value),
            Write(center_label),
            run_time=0.75,
        )
        self.play(FadeOut(center_label), run_time=0.35)

        for index, (cell, color, _, contribution) in enumerate(valid_neighbor_data):
            part_index = index * 2
            animations = [
                cell.animate.set_fill(color, opacity=0.95),
                FadeIn(cell_values[index]),
                Write(valid_parts[part_index]),
            ]
            if index > 0:
                animations.append(Write(valid_parts[part_index - 1]))
            self.play(*animations, run_time=0.52)

        self.play(Write(valid_parts[7]), Write(valid_parts[8]), run_time=0.5)
        self.play(Write(check), run_time=0.45)
        self.wait(0.65)

        self.play(
            FadeOut(valid_parts),
            FadeOut(check),
            FadeOut(cell_values),
            VGroup(*neighbors).animate.set_fill(opacity=0),
            run_time=0.55,
        )

        for index, cell in enumerate(neighbors):
            part_index = index * 2
            animations = [
                cell.animate.set_fill(SUGARCANE, opacity=0.95),
                FadeIn(invalid_values[index]),
                Write(invalid_parts[part_index]),
            ]
            if index > 0:
                animations.append(Write(invalid_parts[part_index - 1]))
            self.play(*animations, run_time=0.52)

        self.play(Write(invalid_parts[7]), Write(invalid_parts[8]), run_time=0.5)
        self.play(Write(invalid_result), Write(x_mark), run_time=0.55)
        self.wait(1.2)
