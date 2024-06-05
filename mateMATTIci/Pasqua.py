from manim import *
import numpy as np

class UovoPasqua(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-7,7,1], y_range=[-4,4,1]).add_coordinates()

        #######COSTRUZIONE UOVO

        pentagono = RegularPolygon(n=5).scale(3)
        punti = pentagono.get_all_points()#da tutti i punti del pentagono, mette 4 punti per lato e parte dal punto in alto
        riga1 = Line(punti[0], punti[7])
        riga2 = Line(punti[0], punti[11])
        riga3 = Line(punti[3], punti[11])
        riga4 = Line(punti[3], punti[15])
        riga5 = Line(punti[7], punti[15])
        diagonali = VGroup(riga1, riga2, riga3, riga4, riga5)

        punto1 = line_intersection([ punti[3], punti[11] ], [ punti[7], punti[15] ])
        punto2 = line_intersection([ [-7, punto1[1], 0], [+7, punto1[1], 0] ],  [ punti[3], punti[7] ])
        punto3 = line_intersection([ [-7, punto1[1], 0], [+7, punto1[1], 0] ],  [ punti[11], punti[15] ])
        riga_orizzontale = Line(punto2, punto3)

        punto1_semicerchio2 = line_intersection([ punto2, punto3 ], [ punti[0], punti[7] ])
        punto2_semicerchio2 = line_intersection([ punto2, punto3 ], [ punti[0], punti[11] ])
        semicerchio2 = ArcBetweenPoints(start = punto1_semicerchio2, end = punto2_semicerchio2, angle = PI)

        punto1_semicerchio1 = line_intersection([ punti[0], punti[7] ], [ punti[3], punti[15] ])
        punto2_semicerchio1 = line_intersection([ punti[0], punti[11] ], [ punti[3], punti[15] ])
        centro_semicerchio1 = line_intersection([ punto2, punto2_semicerchio1 ], [ punto3, punto1_semicerchio1 ])
        raggio1 = Line(centro_semicerchio1, punto1_semicerchio1).get_length()
        angolo_centro1 = Angle(Line(centro_semicerchio1, punto2_semicerchio1), Line(centro_semicerchio1, punto1_semicerchio1)).get_value()
        semicerchio1 = Arc(radius = raggio1, arc_center = centro_semicerchio1, angle = angolo_centro1, start_angle = (PI-angolo_centro1)/2)

        raggio3 = Line(punto3, punto1_semicerchio1).get_length()
        riga_orizzontale_lunga = Line([-7, punto1[1], 0], [7, punto1[1], 0])
        angolo_centro3 = PI - Angle(Line(punto3, punto1_semicerchio1), riga_orizzontale_lunga).get_value()
        semicerchio3 = Arc(radius = raggio3, arc_center = punto3, angle = angolo_centro3, start_angle = PI)
        semicerchio4 = Arc(radius = raggio3, arc_center = punto2, angle = -angolo_centro3, start_angle = 0)

        ##### TESTI CON SPIEGAZIONE
        rectangle = RoundedRectangle(stroke_width = 8, stroke_color = WHITE,
        fill_color = BLUE_B, width = 4.5, height = 2).shift(UP*2.8+LEFT*4)

        text1_1 = Text("Costruite un").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text1_2 = Text("pentagono regolare").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text1 = VGroup(text1_1, text1_2).arrange(DOWN, buff = 0.3)
        text1.move_to(rectangle.get_center())

        text2_1 = Text(" Unite tutti ").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(3.7)
        text2_2 = Text(" i vertici ").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(3.2)
        text2 = VGroup(text2_1, text2_2).arrange(DOWN, buff = 0.3)
        text2.move_to(rectangle.get_center())

        text3_1 = Text("Tracciate la riga orizzontale").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text3_2 = Text("Passante per il punto verde").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text3 = VGroup(text3_1, text3_2).arrange(DOWN, buff = 0.3)
        text3.move_to(rectangle.get_center())

        text4_1 = Text("Tracciate il primo").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text4_2 = Text("arco di circonferenza").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text4 = VGroup(text4_1, text4_2).arrange(DOWN, buff = 0.3)
        text4.move_to(rectangle.get_center())

        text5_1 = Text("Unite i punti").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text5_2 = Text("dello stesso colore").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text5 = VGroup(text5_1, text5_2).arrange(DOWN, buff = 0.3)
        text5.move_to(rectangle.get_center())

        text6_1 = Text("Tracciate il secondo").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text6_2 = Text("arco di circonferenza").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text6 = VGroup(text6_1, text6_2).arrange(DOWN, buff = 0.3)
        text6.move_to(rectangle.get_center())

        text7_1 = Text("Tracciate il terzo arco di").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text7_2 = Text("circonferenza con i punti blu").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text7 = VGroup(text7_1, text7_2).arrange(DOWN, buff = 0.3)
        text7.move_to(rectangle.get_center())

        text8_1 = Text("Tracciate il quarto arco di").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text8_2 = Text("circonferenza con i punti rossi").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(4.3)
        text8 = VGroup(text8_1, text8_2).arrange(DOWN, buff = 0.3)
        text8.move_to(rectangle.get_center())

        text9 = Text("Buona Pasqua dai mateMATTIci").set_color_by_gradient(GREEN, PINK).scale_to_fit_width(10).shift(UP*3.1)


        self.play(FadeIn(rectangle))
        self.play(Write(text1), run_time=1)
        self.wait()
        self.play(Create(pentagono), run_time = 3)
        self.wait()

        self.play(ReplacementTransform(text1, text2), run_time=1)
        self.wait()
        self.play(Write(diagonali), run_time = 3)
        self.wait()

        dot1 = Dot(punto1, color = GREEN)
        self.play(Create(dot1))
        self.play(ReplacementTransform(text2, text3), run_time=1)
        self.wait()
        self.play(Write(riga_orizzontale), run_time = 2)

        dot2 = Dot(punto1_semicerchio2, color = RED)
        dot3 = Dot(punto2_semicerchio2, color = BLUE)
        self.play( Create(dot2), Create(dot3) )
        self.play(ReplacementTransform(text3, text4), run_time=1)
        self.play(Write(semicerchio2), run_time = 3)
        self.remove(dot1)

        dot4 = Dot(punto2, color = RED)
        dot5 = Dot(punto3, color = BLUE)
        self.play(ReplacementTransform(dot2, dot4), ReplacementTransform(dot3, dot5))
        dot6 = Dot(punto2_semicerchio1, color = RED)
        dot7 = Dot(punto1_semicerchio1, color = BLUE)
        self.play( Create(dot6), Create(dot7) )
        self.play(ReplacementTransform(text4, text5), run_time=1)
        linea1 = Line(punto3, punto1_semicerchio1)
        linea2 = Line(punto2, punto2_semicerchio1)
        self.play(Write(linea1))
        self.play(Write(linea2))

        dot8 = Dot(centro_semicerchio1, color = GREEN)
        self.play(Create(dot8))
        self.play(ReplacementTransform(text5, text6), run_time=1)
        self.play(Write(semicerchio1), run_time = 2)
        self.remove(dot8)
        
        dot9 = Dot(punto1_semicerchio2, color = BLUE)
        self.play(Create(dot9))
        self.play(ReplacementTransform(text6, text7), run_time=1)
        self.play(Write(semicerchio3), run_time = 2)
        self.remove(dot5, dot7, dot9)

        dot10 = Dot(punto2_semicerchio2, color = RED)
        self.play(Create(dot10))
        self.play(ReplacementTransform(text7, text8), run_time=1)
        self.play(Write(semicerchio4), run_time = 2)
        self.remove(dot4, dot6, dot10)
        self.play(pentagono.animate.set_opacity(0.2), diagonali.animate.set_opacity(0.2), riga_orizzontale.animate.set_opacity(0.2), linea1.animate.set_opacity(0.2), linea2.animate.set_opacity(0.2))
        self.remove(rectangle, text8)
        self.wait(2)
        self.play(Write(text9))
        
        self.wait(3)
