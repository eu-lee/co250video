from manim import *
from common import *


class Scene04GeneralForm(BaseSugarcaneScene):
    def construct(self):
        title = self.place_as_top_narration(self.narration_text("Integer Program"))
        objective = MathTex(
            r"\max\quad c_1x_1+c_2x_2+\cdots+c_nx_n",
            font_size=44,
            color=ACCENT,
        )
        subject_to = MathTex(r"\text{subject to}", font_size=32, color=MUTED)
        constraints = MathTex(
            r"\begin{aligned}"
            r"a_{1,1}x_1+a_{1,2}x_2+\cdots+a_{1,n}x_n &\le b_1\\"
            r"a_{2,1}x_1+a_{2,2}x_2+\cdots+a_{2,n}x_n &\le b_2\\"
            r"&\vdots\\"
            r"a_{m,1}x_1+a_{m,2}x_2+\cdots+a_{m,n}x_n &\le b_m"
            r"\end{aligned}",
            font_size=34,
            color=TEXT,
        )
        integer_restriction = MathTex(
            r"x_j \in \mathbb{Z}\quad \text{for some } j",
            font_size=34,
            color=SUGARCANE,
        )
        form = VGroup(
            objective,
            subject_to,
            constraints,
            integer_restriction,
        ).arrange(DOWN, buff=0.42)
        form.move_to(ORIGIN)
        subject_to.align_to(constraints, LEFT)

        self.play(Write(title))
        self.wait(0.35)
        self.play(Write(objective), run_time=0.75)
        self.wait(0.6)
        self.play(Write(subject_to), run_time=0.55)
        self.wait(0.45)
        self.play(Write(constraints), run_time=1.0)
        self.wait(0.65)
        self.play(Write(integer_restriction), run_time=0.7)
        self.wait(1.2)
