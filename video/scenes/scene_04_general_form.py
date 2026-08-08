from manim import *
from common import *


class Scene04GeneralForm(BaseSugarcaneScene):
    def construct(self):
        title = self.place_as_top_narration(self.narration_text("Integer Program"))
        form = VGroup(
            MathTex(r"\max f(x)", font_size=44, color=ACCENT),
            MathTex(r"\text{subject to}", font_size=32, color=MUTED),
            MathTex(
                r"g_i(x) \le b_i,\quad g_i(x) = b_i,\quad g_i(x) \ge b_i,\quad 1 \le i \le m",
                font_size=34,
                color=TEXT,
            ),
            MathTex(r"x_j \in \mathbb{Z}\ \text{for some } j", font_size=34, color=SUGARCANE),
        ).arrange(DOWN, buff=0.42)
        form.move_to(ORIGIN)

        self.play(Write(title))
        for mob in form:
            self.play(Write(mob), run_time=0.55)
        self.wait(1.2)
