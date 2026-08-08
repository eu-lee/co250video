from manim import *
from common import *


class Scene11BinaryRestrictions(BaseSugarcaneScene):
    def construct(self):
        formula_size = 30

        objective = MathTex(
            r"\max\quad \sum_{i=1}^{n}\sum_{j=1}^{n} x_{i,j}",
            font_size=formula_size,
            color=TEXT,
        )

        subject_to = MathTex(
            r"\text{subject to}",
            font_size=formula_size,
            color=MUTED,
        )

        adjacency_row = MathTex(
            r"\sum_{(p,q)\in N(i,j)} (1-x_{p,q}) \ge x_{i,j}",
            r",\qquad \forall\ 1\le i,j\le n,\ i,j\in\mathbb{Z}",
            font_size=formula_size,
            color=TEXT,
        )

        neighbor_definition = MathTex(
            r"N(i,j) := \{(p,q)\in\{1,\ldots,n\}^2 : |p-i|+|q-j|=1\}",
            font_size=formula_size,
            color=TEXT,
        )

        binary_row = MathTex(
            r"x_{i,j}\in\{0,1\}",
            r",\qquad \forall\ 1\le i,j\le n,\ i,j\in\mathbb{Z}",
            font_size=formula_size,
            color=TEXT,
        )

        model = VGroup(
            objective,
            subject_to,
            adjacency_row,
            neighbor_definition,
            binary_row,
        ).arrange(DOWN, buff=0.34)
        model.move_to(ORIGIN)
        subject_to.align_to(adjacency_row, LEFT)

        self.play(Write(objective), run_time=0.8)
        self.play(Write(subject_to), run_time=0.55)
        self.play(Write(adjacency_row), run_time=0.9)
        self.play(Write(neighbor_definition), run_time=0.9)
        self.play(Write(binary_row), run_time=0.8)
        self.wait(1.3)
