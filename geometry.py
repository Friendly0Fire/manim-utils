from manim import *


class LinePath(VGroup):
    def __init__(self, vertices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(0, len(vertices) - 1):
            self.add(Line(vertices[i], vertices[i + 1], **kwargs))