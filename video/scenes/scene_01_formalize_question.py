from manim import *
from common import *


class Scene01FormalizeQuestion(BaseSugarcaneScene):
    def construct(self):
        first_clause = self.narration_tex(
            r"Given an $n \times n$ plot,",
        )
        first_line_rest = self.narration_tex(
            r"how can we place sugarcane",
        )
        first_line = VGroup(first_clause, first_line_rest).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        self.place_as_top_narration(first_line)

        second_line = self.narration_tex(
            r"to maximize the amount produced?",
        )
        second_line.next_to(first_line, DOWN, buff=NARRATION_LINE_BUFF)

        grid = self.grid(8, side=0.52, fill=SUGARCANE)
        grid.next_to(second_line, DOWN, buff=VISUAL_AFTER_TEXT_BUFF)

        water_positions = [(row, col) for row in range(8) for col in (1, 4, 7)]
        for row, col in water_positions:
            self.fill_cell(grid, row, col, WATER)

        self.play(Write(first_clause))
        self.play(FadeIn(grid, shift=UP * 0.15))
        self.play(Write(first_line_rest))
        self.play(Write(second_line))
        self.wait(1.2)
