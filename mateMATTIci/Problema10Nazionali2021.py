from manim import *
import numpy as np

class Problema(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta = 30 * DEGREES)
        cube = Cube(side_length=3, fill_opacity=0.2, color = WHITE)
        prism1 = Prism(dimensions=[2, 2, 1], fill_color = RED).shift([0.5,0.5,-1])
        prism2 = Prism(dimensions=[2, 1, 2], fill_color = GREEN).shift([0.5,-1,-0.5])
        prism3 = Prism(dimensions=[1, 2, 2], fill_color = PURPLE).shift([-1,-0.5,-0.5])
        prism4 = Prism(dimensions=[2, 2, 1], fill_color = RED).shift([-0.5,-0.5,1])
        prism5 = Prism(dimensions=[2, 1, 2], fill_color = GREEN).shift([-0.5,1,0.5])
        prism6 = Prism(dimensions=[1, 2, 2], fill_color = PURPLE).shift([1,0.5,0.5])

        self.play(DrawBorderThenFill(cube))
        self.play(DrawBorderThenFill(prism3))
        self.play(DrawBorderThenFill(prism2))
        self.play(DrawBorderThenFill(prism1))
        self.play(DrawBorderThenFill(prism4))
        self.play(DrawBorderThenFill(prism5))
        self.play(DrawBorderThenFill(prism6))
        self.wait(2)