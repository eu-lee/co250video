from manim import *
from common import *


class Scene05CellVariables(BaseSugarcaneScene):
    def construct(self):
        grid = self.grid(10, side=0.38)
        grid.set_fill(opacity=0)

        definition = MathTex(
            r"x_{i,j} =",
            r"\begin{cases}"
            r"1, & \text{if block } (i,j) \text{ is sugarcane}\\"
            r"0, & \text{if block } (i,j) \text{ is water}"
            r"\end{cases}",
            font_size=34,
            color=TEXT,
        )
        definition.scale_to_fit_width(6.4)

        layout = VGroup(grid, definition).arrange(RIGHT, buff=0.85)
        layout.move_to(ORIGIN)

        selected = self.cell(grid, 4, 6)
        highlight = Square(side_length=selected.width)
        highlight.set_stroke(TEXT, width=3)
        highlight.set_fill(opacity=0)
        highlight.move_to(selected)
        highlight.set_z_index(2)
        var_label = MathTex(r"x_{i,j}", font_size=34, color=TEXT)
        var_label.next_to(selected, UP, buff=0.22)
        var_label.set_z_index(3)

        self.play(FadeIn(grid))
        self.play(Create(highlight), Write(var_label))
        self.play(highlight.animate.set_fill(SUGARCANE, opacity=0.95), run_time=0.8)
        self.wait(0.35)
        self.play(highlight.animate.set_fill(WATER, opacity=0.95), run_time=1.35)
        self.play(Write(definition))
        self.wait(1.2)
