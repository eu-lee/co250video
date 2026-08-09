from manim import *


WATER = "#38a3ff"
SAND = "#d8b46a"
SUGARCANE = "#58c76f"
GRID_STROKE = "#2f2f2f"
TEXT = "#f5f1e8"
MUTED = "#b9c0c7"
ACCENT = "#ffd166"
BAD = "#ff6b6b"

REGULAR_FONT_SIZE = 30
BOLD_FONT_SIZE = 30
NARRATION_FONT_SIZE = REGULAR_FONT_SIZE
TOP_NARRATION_BUFF = 0.75
NARRATION_LINE_BUFF = 0.26
VISUAL_AFTER_TEXT_BUFF = 0.36
LIST_ITEM_BUFF = 0.42


class BaseSugarcaneScene(Scene):
    def setup(self):
        self.camera.background_color = "#111418"

    def narration_text(self, text, font_size=NARRATION_FONT_SIZE, color=TEXT):
        return Text(text, font_size=font_size, color=color)

    def narration_tex(self, text, font_size=NARRATION_FONT_SIZE, color=TEXT):
        return Tex(text, font_size=font_size, color=color)

    def place_as_top_narration(self, mob, buff=TOP_NARRATION_BUFF):
        mob.to_edge(UP, buff=buff)
        return mob

    def condition_list(self, items, font_size=NARRATION_FONT_SIZE, buff=LIST_ITEM_BUFF):
        return VGroup(
            *[self.narration_text(item, font_size=font_size) for item in items]
        ).arrange(DOWN, buff=buff, aligned_edge=LEFT)

    def title(self, text):
        title = Text(text, font_size=BOLD_FONT_SIZE, color=TEXT, weight=BOLD)
        title.to_edge(UP, buff=0.35)
        return title

    def caption(self, text, width=11.5, font_size=REGULAR_FONT_SIZE):
        caption = Text(text, font_size=font_size, color=MUTED, line_spacing=0.85)
        caption.scale_to_fit_width(width)
        caption.to_edge(DOWN, buff=0.35)
        return caption

    def formula(self, text, font_size=REGULAR_FONT_SIZE, color=TEXT):
        return Text(text, font_size=font_size, color=color)

    def grid(self, n=5, side=0.62, fill=SAND):
        cells = VGroup()
        for i in range(n):
            row = VGroup()
            for j in range(n):
                cell = Square(side_length=side)
                cell.set_stroke(GRID_STROKE, width=2)
                cell.set_fill(fill, opacity=0.9)
                cell.row = i
                cell.col = j
                row.add(cell)
            row.arrange(RIGHT, buff=0)
            cells.add(row)
        cells.arrange(DOWN, buff=0)
        return cells

    def cell(self, grid, row, col):
        return grid[row][col]

    def fill_cell(self, grid, row, col, color):
        self.cell(grid, row, col).set_fill(color, opacity=0.95)

    def labeled_box(self, label, color=ACCENT, width=3.2, height=0.65):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.06,
            stroke_color=color,
            fill_color="#1b2128",
            fill_opacity=0.95,
        )
        text = Text(label, font_size=REGULAR_FONT_SIZE, color=TEXT)
        text.scale_to_fit_width(width - 0.3)
        return VGroup(box, text)

    def fade_all(self):
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)
