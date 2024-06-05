from turtle import circle, width
from cairo import LineJoin
from manim import *
import numpy as np
from pyparsing import line

class Problema(Scene):
    def construct(self):
        image = ImageMobject('pikachu.png')
        image.scale(0.02)
        image2 = ImageMobject('team_rocket.png')
        image2.scale(0.1)

        #Assi
        axes = Axes(x_range=[-1,1], y_range=[-1,1])
        #Circonferenza
        r = 3.5
        circ = Circle(radius = r, color = WHITE)

        image.move_to(circ.get_top()+UP*0.3)
        image2.move_to(circ.get_bottom()-UP*0.3)

        riga1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(3*PI/2), color = YELLOW)

        riga2_1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(PI/2 + 1*PI/2) , color = YELLOW)
        riga2_2 = Line(circ.point_at_angle(PI/2 + 1*PI/2), circ.point_at_angle(PI/2 + 2*PI/2) , color = YELLOW)
        riga2 = VGroup(riga2_1, riga2_2)

        riga3_1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(PI/2 + 1*(PI/3)) , color = YELLOW)
        riga3_2 = Line(circ.point_at_angle(PI/2 + 1*(PI/3)), circ.point_at_angle(PI/2 + 2*(PI/3)) , color = YELLOW)
        riga3_3 = Line(circ.point_at_angle(PI/2 + 2*(PI/3)), circ.point_at_angle(PI/2 + 3*(PI/3)) , color = YELLOW)
        riga3 = VGroup(riga3_1, riga3_2, riga3_3)

        self.add(image, image2)
        self.play(Create(circ))
        self.wait()

        self.play(Create(riga1))
        self.wait()
        self.remove(riga1)

        self.play(Create(riga2))
        self.wait()
        self.remove(riga2)
        
        self.play(Create(riga3))
        self.wait()
        self.remove(riga3)

        for i in range(1, 9, 2):
            riga9_1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(PI/2 + 1*(i*PI/9)) , color = YELLOW)
            riga9_2 = Line(circ.point_at_angle(PI/2 + 1*(i*PI/9)), circ.point_at_angle(PI/2 + 2*(i*PI/9)) , color = YELLOW)
            riga9_3 = Line(circ.point_at_angle(PI/2 + 2*(i*PI/9)), circ.point_at_angle(PI/2 + 3*(i*PI/9)) , color = YELLOW)
            riga9_4 = Line(circ.point_at_angle(PI/2 + 3*(i*PI/9)), circ.point_at_angle(PI/2 + 4*(i*PI/9)) , color = YELLOW)
            riga9_5 = Line(circ.point_at_angle(PI/2 + 4*(i*PI/9)), circ.point_at_angle(PI/2 + 5*(i*PI/9)) , color = YELLOW)
            riga9_6 = Line(circ.point_at_angle(PI/2 + 5*(i*PI/9)), circ.point_at_angle(PI/2 + 6*(i*PI/9)) , color = YELLOW)
            riga9_7 = Line(circ.point_at_angle(PI/2 + 6*(i*PI/9)), circ.point_at_angle(PI/2 + 7*(i*PI/9)) , color = YELLOW)
            riga9_8 = Line(circ.point_at_angle(PI/2 + 7*(i*PI/9)), circ.point_at_angle(PI/2 + 8*(i*PI/9)) , color = YELLOW)
            riga9_9 = Line(circ.point_at_angle(PI/2 + 8*(i*PI/9)), circ.point_at_angle(PI/2 + 9*(i*PI/9)) , color = YELLOW)
            riga9 = VGroup(riga9_1, riga9_2, riga9_3, riga9_4, riga9_5, riga9_6, riga9_7, riga9_8, riga9_9)

            self.play(Create(riga9))
            self.wait()
            self.remove(riga9)   

        for i in range(1, 10, 2):
            if i != 5:
                riga10_1 = Line(circ.point_at_angle(PI/2), circ.point_at_angle(PI/2 + 1*(i*PI/10)) , color = YELLOW)
                riga10_2 = Line(circ.point_at_angle(PI/2 + 1*(i*PI/10)), circ.point_at_angle(PI/2 + 2*(i*PI/10)) , color = YELLOW)
                riga10_3 = Line(circ.point_at_angle(PI/2 + 2*(i*PI/10)), circ.point_at_angle(PI/2 + 3*(i*PI/10)) , color = YELLOW)
                riga10_4 = Line(circ.point_at_angle(PI/2 + 3*(i*PI/10)), circ.point_at_angle(PI/2 + 4*(i*PI/10)) , color = YELLOW)
                riga10_5 = Line(circ.point_at_angle(PI/2 + 4*(i*PI/10)), circ.point_at_angle(PI/2 + 5*(i*PI/10)) , color = YELLOW)
                riga10_6 = Line(circ.point_at_angle(PI/2 + 5*(i*PI/10)), circ.point_at_angle(PI/2 + 6*(i*PI/10)) , color = YELLOW)
                riga10_7 = Line(circ.point_at_angle(PI/2 + 6*(i*PI/10)), circ.point_at_angle(PI/2 + 7*(i*PI/10)) , color = YELLOW)
                riga10_8 = Line(circ.point_at_angle(PI/2 + 7*(i*PI/10)), circ.point_at_angle(PI/2 + 8*(i*PI/10)) , color = YELLOW)
                riga10_9 = Line(circ.point_at_angle(PI/2 + 8*(i*PI/10)), circ.point_at_angle(PI/2 + 9*(i*PI/10)) , color = YELLOW)
                riga10_10 = Line(circ.point_at_angle(PI/2 + 9*(i*PI/10)), circ.point_at_angle(PI/2 + 10*(i*PI/10)) , color = YELLOW)
                riga10 = VGroup(riga10_1, riga10_2, riga10_3, riga10_4, riga10_5, riga10_6, riga10_7, riga10_8, riga10_9, riga10_10)

                self.play(Create(riga10))
                self.wait()
                self.remove(riga10)

        self.wait(5)


class ProblemaCompleto(Scene):
    def construct(self):
        image1 = ImageMobject('pikachu.png')
        image1.scale(0.02)
        image2 = ImageMobject('team_rocket.png')
        image2.scale(0.1)

        #Assi
        axes = Axes(x_range=[-1,1], y_range=[-1,1])
        #Circonferenza
        r = 3.5
        circ = Circle(radius = r, color = WHITE)

        image1.move_to(circ.get_top()+UP*0.3)
        image2.move_to(circ.get_bottom()-UP*0.3)

        self.add(image1, image2)
        self.play(Create(circ))
        self.wait()

        for b in range(1, 11): # l'ultimo è escluso
            for a in range(1, 10, 2):
                if a < b and b%a != 0 or a == 1:
                    counter = 1
                    riga_tot_sx = VGroup()
                    riga_tot_dx = VGroup()
                    while counter <= b:
                        riga_sx = Line(circ.point_at_angle(PI/2 + (counter-1)*(a*PI/b)), circ.point_at_angle(PI/2 + counter*(a*PI/b)) , color = YELLOW)
                        riga_tot_sx = VGroup(riga_tot_sx, riga_sx)
                        riga_dx = Line(circ.point_at_angle(PI/2 - (counter-1)*(a*PI/b)), circ.point_at_angle(PI/2 - counter*(a*PI/b)) , color = YELLOW)
                        riga_tot_dx = VGroup(riga_tot_dx, riga_dx)
                        counter = counter + 1

                    if b == 1:
                        self.play(Create(riga_tot_sx))
                        self.wait()
                        self.remove(riga_tot_sx)
                    else:
                        self.play(Create(riga_tot_sx))
                        self.wait()
                        self.remove(riga_tot_sx)
                        self.play(Create(riga_tot_dx))
                        self.wait()
                        self.remove(riga_tot_dx)

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
