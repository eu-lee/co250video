from manim import *
from common import *


class Scene03DiscreteChoices(BaseSugarcaneScene):
    def construct(self):
        title = Text(
            "each block may only be water or sugarcane",
            font_size=NARRATION_FONT_SIZE,
            color=TEXT,
            t2c={"water": WATER, "sugarcane": SUGARCANE},
        )
        self.place_as_top_narration(title)

        cell = Square(side_length=1.9, fill_color=WATER, fill_opacity=0.95)
        cell.set_stroke(opacity=0)
        cell.next_to(title, DOWN, buff=1.25)

        label = Text("Integer Program", font_size=42, color=TEXT, weight=BOLD)
        label.next_to(cell, DOWN, buff=0.75)

        self.play(Write(title))
        self.play(FadeIn(cell))
        self.play(cell.animate.set_fill(SUGARCANE), run_time=0.75)
        self.wait(0.35)
        self.play(Write(label))
        self.wait(1.2)
