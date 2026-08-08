from manim import *
from common import *


class Scene02OptimizationFramework(BaseSugarcaneScene):
    def construct(self):
        title = self.place_as_top_narration(self.narration_text("Elements of an optimization problem"))

        items = self.condition_list([
            "1. variables",
            "2. objective",
            "3. constraints",
        ])
        items.move_to(ORIGIN + DOWN * 0.05)

        self.play(Write(title))
        for item in items:
            self.play(Write(item), run_time=0.5)
        self.wait(1.2)
