from manim import *
import numpy as np

class Problema(Scene):
    def construct(self):
        image = ImageMobject('pikachu.png')
        image.scale(0.02)
        #Assi
        axes = Axes(x_range=[-1,1], y_range=[-1,1])
        #Circonferenza
        r = 3.5
        circ = Circle(radius = r, color = WHITE)

        image.move_to(circ.get_top()+UP*0.3)

        riga1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(3*PI/2), color = YELLOW)

        riga2_1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(PI) , color = YELLOW)
        riga2_2 = Line(circ.point_at_angle(PI), circ.point_at_angle(3*PI/2) , color = YELLOW)
        riga2 = VGroup(riga2_1, riga2_2)

        riga3_1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(5*PI/6) , color = YELLOW)
        riga3_2 = Line(circ.point_at_angle(5*PI/6), circ.point_at_angle(7*PI/6) , color = YELLOW)
        riga3_3 = Line(circ.point_at_angle(7*PI/6), circ.point_at_angle(3*PI/2) , color = YELLOW)
        riga3 = VGroup(riga3_1, riga3_2, riga3_3)

        self.add(image)
        self.play(Create(circ))
        self.wait()
        self.play(Create(riga1))
        self.wait()
        self.remove(riga1)
        self.play(Create(riga2))
        self.wait()
        self.remove(riga2)
        self.play(Create(riga3))
        self.wait(5)

class HeatDiagramPlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 40, 5],
            y_range=[-8, 32, 5],
            x_length=9,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 40, 5)},
            y_axis_config={"numbers_to_include": np.arange(-5, 34, 5)},
            tips=False,
        )
        labels = ax.get_axis_labels(
            x_label=Tex("$\Delta Q$"), y_label=Tex("T[$^\circ C$]")
        )

        x_vals = [0, 8, 38, 39]
        y_vals = [20, 0, 0, -5]
        graph = ax.plot_line_graph(x_values=x_vals, y_values=y_vals)

        self.play(Create(ax))
        self.play(Create(graph))
        self.wait(2)
