from cgitb import text
from manim import *
import numpy as np

class Problema(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta = 30 * DEGREES, zoom = 0.7)
        cube = Cube(side_length=3, color = WHITE).shift([0,3,0])
        prism1 = Prism(dimensions=[2, 2, 1], fill_color = RED).shift([2,-2,0])
        prism2 = Prism(dimensions=[2, 2, 1], fill_color = RED).shift([-2,-2,0])
        prism3 = Prism(dimensions=[2, 2, 1], fill_color = GREEN).shift([-2,-5,0])
        prism4 = Prism(dimensions=[2, 2, 1], fill_color = GREEN).shift([2,-5,0])
        prism5 = Prism(dimensions=[2, 2, 1], fill_color = PURPLE).shift([-2,-8,0])
        prism6 = Prism(dimensions=[2, 2, 1], fill_color = PURPLE).shift([2,-8,0])
        prismi = VGroup(prism1, prism2, prism3, prism4, prism5, prism6)

        text1= Text("Riesci a far stare sei parallelepipedi \n2x2x1 in un cubo 3x3x3?", font_size=30).shift([2.5,2.5,0])
        text2= Text("Li puoi ruotare, ma sempre tenendo le \nfacce parallele a quelle del cubo", font_size=30).shift([2.5,2.5,0])
        text3= Text("Hint: guarda i colori ;)", font_size=30).shift([2.5,2.5,0])

        self.play(DrawBorderThenFill(cube))
        self.play(DrawBorderThenFill(prismi))
        #self.add_fixed_in_frame_mobjects(text1)
        self.wait(6)
        #self.remove(text1)
        #self.add_fixed_in_frame_mobjects(text2)
        self.play(Rotate(prism1, PI/2, [0,1,0]),)
        self.wait()
        self.play(Rotate(prism1, -PI/2, [0,1,0]))
        self.play(Rotate(prism1, -PI/2, [1,0,0]))
        self.wait()
        self.play(Rotate(prism1, PI/2, [1,0,0]))
        #self.remove(text2)
        #self.add_fixed_in_frame_mobjects(text3)
        self.wait(5)