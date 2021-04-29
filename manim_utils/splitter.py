from manim import *
import inspect
from pathlib import Path
import os.path
import json

class SplitterJson(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_animations = config.frame_rate < 60

    def stop_skipping(self):
        self.skip_animations = False

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cuts = []
        self.name = self.__class__.__name__
        self.cut_count = 0
        self.total_runtime = 0.0
        self.last_cut_time = 0.0
        filename = os.path.basename(
            os.path.splitext(inspect.getfile(self.__class__))[0]
        )
        self.output = Path(".") / "media" / "videos" / filename / (self.name + ".json")

        self.split_output = Path(".") / "media" / "split" / filename
        self.split_output.mkdir(parents=True, exist_ok=True)

    def play(self, *args, **kwargs):
        if self.skip_animations:
            config.from_animation_number = self.renderer.num_plays + 1
        else:
            config.from_animation_number = 0

        super().play(*args, **kwargs)
        if not self.skip_animations:
            self.total_runtime += self.duration

    def cut(self):
        if self.total_runtime - self.last_cut_time <= 0.2:
            return

        self.wait(0.2)
        t = self.total_runtime - self.last_cut_time

        self.cuts.append(
            {
                "start_time": float(self.last_cut_time),
                "length": float(t),
                "rename_to": str(
                    self.split_output / (self.name + "_" + str(self.cut_count) + ".mp4")
                ),
            }
        )
        self.cut_count += 1
        self.last_cut_time = self.total_runtime

        self.wait(0.2)

    def tear_down(self, *args, **kwargs):
        self.cut()

        with self.output.open("w") as out:
            data = {
                "splits": self.cuts,
                "filename": str(
                    Path(os.path.dirname(self.output))
                    / (str(config.pixel_height) + "p" + str(config.frame_rate))
                    / "Main.mp4"
                ),
            }
            json.dump(data, out)

        super().tear_down(*args, **kwargs)