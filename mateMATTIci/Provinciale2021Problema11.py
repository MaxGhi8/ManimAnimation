from manim import *
import numpy as np

class Problema(Scene):
    def construct(self):
        #Assi
        #axes = Axes(x_range=[-1,1], y_range=[-3/2,3/2], x_length=10, y_length=10)
        theta = ValueTracker((5/6)*np.pi)
        
        #tr1 = Triangle(color = WHITE).scale(3/2).shift(UP*0.75)
        #tr2 = Triangle(color = WHITE).scale(3/2).rotate(PI).shift(DOWN*0.75)
        tr1 = Polygon([-np.sqrt(3)/2, 0,0], [np.sqrt(3)/2, 0,0], [0, 3/2,0])

        tr2 = always_redraw(lambda: Polygon([-np.sqrt(3)/2, 0,0], [np.sqrt(3)/2, 0,0], [np.cos(theta.get_value()), np.sin(theta.get_value())-1/2,0]))
        segmentoPy = always_redraw(lambda: Line([np.cos(theta.get_value()), np.sin(theta.get_value())-1/2,0], [ 1/((np.sin(theta.get_value()-1)/np.cos(theta.get_value()))+ (3/np.sqrt(3))), 1/2 + (np.sin(theta.get_value()-1)/np.cos(theta.get_value()))/((np.sin(theta.get_value()-1)/np.cos(theta.get_value()))+ (3/np.sqrt(3)))  , 0]))

        #self.play(Create(axes))
        self.play(Write(tr1))
        self.play(LaggedStart(Create(tr2), Create(segmentoPy)))
        self.play(theta.animate.set_value((3/2)*np.pi), run_time = 10)
        self.wait(5)
        
class Tute4(Scene):
    def construct(self):

        r = ValueTracker(0.5) #Tracks the value of the radius
        
        circle = always_redraw(lambda : 
        Circle(radius = r.get_value(), stroke_color = YELLOW, 
        stroke_width = 5), )

        self.play(LaggedStart(Create(circle)))
        self.play(r.animate.set_value(2), run_time = 5)
