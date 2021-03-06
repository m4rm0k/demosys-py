import math
import os

from demosys.effects import effect


class TextWriterEffect(effect.Effect):

    def __init__(self):
        super().__init__()

        with open(os.path.join(os.path.dirname(__file__), 'sample.txt'), 'r') as fd:
            lines = fd.readlines()

        TextWriter2D = self.get_effect_class('TextWriter2D', package_name='demosys.effects.text')

        self.writer = TextWriter2D(
            (105, len(lines)),
            aspect_ratio=self.window.aspect_ratio,
            text_lines=lines,
        )

    def draw(self, time, frametime, target):
        self.writer.draw(
            (0.05, 0.01 - math.fmod(time, 75.0) / 5.0),
            size=0.05,
        )
