from manim import *

class FNO(ThreeDScene):
    def construct(self):
        # Set camera orientation for better viewing
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        #### add text for the title
        title = Text("FOURIER NEURAL OPERATOR", font_size=36)
        title.to_edge(UP)
        self.play(Create(title), run_time=2)
        self.wait(1)
        
        #### add image
        image = ImageMobject('input.png')
        image.scale(2)
        text = Text("Take an input", font_size=24)
        text.to_edge(RIGHT)
        self.play(Create(text), run_time=1)
        self.play(FadeIn(image), run_time=1)
        self.wait(1) 

        #### text
        text1 = Text("Evaluate the function \n on an uniform grid", font_size=24)
        text1.to_edge(RIGHT)
        self.play(ReplacementTransform(text, text1), run_time=1)
        self.wait(1)
        
        #### create the tensor
        tensor_size = (1, 6, 6) # tensor size
        length = 0.3 # side length of each cube
        spacing = 3*length # spacing between cubes
        tensor_group1 = self.createTensor(tensor_size, length, spacing)
        tensor_group1.move_to(ORIGIN) # Center the entire tensor group
        self.play(FadeOut(image), FadeIn(tensor_group1), run_time=2)
        self.wait(2)
        
        #### text and move the tensor
        text2 = Text("Add the coordinate grid", font_size=24)
        text2.to_edge(RIGHT)
        self.play(ReplacementTransform(text1, text2), tensor_group1.animate.move_to(LEFT), run_time=1)
        self.wait(1)
        
        #### create the grid
        tensor_size = (1, 6, 6) # tensor size
        tensor_group2 = self.createTensor(tensor_size, length, spacing, GREEN)
        tensor_group3 = self.createTensor(tensor_size, length, spacing, RED)
        tensor_group2.move_to(tensor_group1.get_right())
        tensor_group3.move_to(tensor_group2.get_right())
        self.play(FadeIn(tensor_group2), FadeIn(tensor_group3), run_time=1)
        
        #### create a new tensor and remove the previous tensors
        tensor_size = (3, 6, 6)
        tensor_group_input = self.createTensor(tensor_size, length, spacing, color=BLUE)
        tensor_group_input.scale(0.5).move_to(2*LEFT)
        # For efficiency select the first one, for better visual select the second one
        # self.play(ReplacementTransform(tensor_group1, tensor_group_input), FadeOut(tensor_group2), FadeOut(tensor_group3), run_time=1)
        self.play(ReplacementTransform(Group(tensor_group1, tensor_group2, tensor_group3), tensor_group_input), run_time=1)

        #### text
        text3 = MathTex(r"\text{Apply lifting operator } \mathcal{P}", font_size=24)
        text3.to_edge(RIGHT)
        title1 = Text("LIFTING OPERATOR", font_size=36)
        title1.to_edge(UP)
        self.play(ReplacementTransform(title, title1), tensor_group_input.animate.shift(2*LEFT), ReplacementTransform(text2, text3), run_time=1)
        
        #### create the lifting operator
        # Highlight an input vector
        for i in range(1, tensor_size[0]+1):
            specific_cube = tensor_group_input[6*6*i-1] # Change this index to target a different cube
            self.play(specific_cube.animate.set_color(RED), run_time=0.4)

        # Create the lifted vector
        tensor_group_W1 = self.createTensor((5, 1, 1), length, spacing, color=RED)
        tensor_group_W1.scale(0.5).move_to(2*RIGHT)

        # create an arrow pointing from tensor_group_input to the new tensor
        arrow = Arrow(
            start=tensor_group_input.get_right(), 
            end=tensor_group_W1.get_left(), 
            buff=0.4,
            stroke_width=4, # Adjust the width of the arrow
            tip_length=0.2, # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow))
        
        # create a label above the arrow
        label1 = MathTex(r"W_{\mathcal{P}} \cdot x_{1, 1} + b_{\mathcal{P}}", font_size=36)
        label2 = MathTex(r"W_{\mathcal{P}} \in \mathbb{R}^{d_a \times d_v},\ b_{\mathcal{P}} \in \mathbb{R}^{d_v}", font_size=28)
        label1.next_to(arrow, UP, buff=0.2)
        label2.next_to(arrow, DOWN, buff=0.2)
        self.play(FadeIn(label1), FadeIn(label2), run_time=1)

        # Show the lifted vector
        self.play(FadeIn(tensor_group_W1), run_time=1)

        # Do the same as before but with another input vector            
        # reset BLUE color
        for i in range(1, tensor_size[0]+1):
            specific_cube = tensor_group_input[6*6*i-1] # Change this index to target a different cube
            self.play(specific_cube.animate.set_color(BLUE), run_time=0.4)
        for mobject in tensor_group_W1:
            self.play(mobject.animate.set_color(BLUE), run_time=0.4)
        self.play(tensor_group_W1.animate.shift(0.5*UP), run_time=1)
        # Highlight an input vector
        for i in range(1, tensor_size[0]+1):
            specific_cube = tensor_group_input[6*5*i + 6*(i-1) - 1] # Change this index to target a different cube
            self.play(specific_cube.animate.set_color(RED), run_time=0.4)
            if i == tensor_size[0]:
                # update label and color
                label1_2 = MathTex(r"W_{\mathcal{P}} \cdot x_{1, 2} + b_{\mathcal{P}}", font_size=36)
                label1_2.next_to(arrow, UP, buff=0.2)
                self.play(specific_cube.animate.set_color(RED), ReplacementTransform(label1, label1_2), run_time=1)

        # Create the lifted vector
        tensor_group_W2 = self.createTensor((5, 1, 1), length, spacing, color=RED)
        tensor_group_W2.scale(0.5).move_to(2*RIGHT)
        self.play(FadeIn(tensor_group_W2), run_time=1)
        self.wait(0.5)

        # create the lifted tensor
        tensor_group_W = self.createTensor((5, 6, 6), length, spacing, color=BLUE)
        tensor_group_W.move_to(2*RIGHT)
        tensor_group_W.scale(0.5)
        for i in range(1, tensor_size[0]+1):
            specific_cube = tensor_group_input[6*5*i + 6*(i-1) - 1] # Change this index to target a different cube
            self.play(specific_cube.animate.set_color(BLUE), run_time=0.4)
        self.play(ReplacementTransform(tensor_group_W1, tensor_group_W), FadeOut(tensor_group_W2), run_time=1) 
        
        # remove the input and move all to the left
        self.play(FadeOut(tensor_group_input), FadeOut(arrow), FadeOut(label1_2), FadeOut(label2), run_time=1)

        #### Affine transformation
        text4 = Tex(r"Apply an affine and \\ pointwise transformation", font_size=24)
        text4.to_edge(RIGHT)
        title2 = Text("FIRST FOURIER LAYER (L=1)", font_size=36)
        title2.to_edge(UP)
        self.play(tensor_group_W.animate.move_to(4*LEFT), ReplacementTransform(title1, title2), ReplacementTransform(text3, text4), run_time=1) 

        # Create the transformed tensor
        tensor_group_V1 = self.createTensor((5, 6, 6), length, spacing, color=GREEN)
        tensor_group_V1.move_to(2*RIGHT).scale(0.5)
        arrow = Arrow(
            start=tensor_group_W.get_right(), 
            end=tensor_group_V1.get_left(), 
            buff=0.4,
            stroke_width=4, # Adjust the width of the arrow
            tip_length=0.2, # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow))
        
        # create a label above the arrow
        label1 = MathTex(r"W_1 \cdot x + b_1, \quad \text{pointwise}", font_size=24)
        label2 = MathTex(r"W_1 \in \mathbb{R}^{d_v \times d_v}, b_1 \in \mathbb{R}^{d_v}", font_size=24)
        label1.next_to(arrow, UP, buff=0.2)
        label2.next_to(arrow, DOWN, buff=0.2)
        self.play(Create(label1), Create(label2), run_time=1)

        self.play(FadeIn(tensor_group_V1), run_time=1)
        self.wait(2)
        self.play(FadeOut(arrow), FadeOut(label1), FadeOut(label2), FadeOut(tensor_group_V1), run_time=1)
        
        #### FNO block
        text5 = MathTex(r"\text{The input represent} \\ \text{a function in } \mathbb{R}^{d_v}", font_size=24)
        text5.to_edge(RIGHT)
        self.play(ReplacementTransform(text4, text5), run_time=1)
        self.wait(2)
        
        text7 = MathTex(r"\text{Apply the Fourier transform}", font_size=24)
        text7.to_edge(RIGHT)
        self.play(ReplacementTransform(text5, text7), run_time=1)
        self.wait(1)
        
        # Fourier transform
        tensor_group_F = self.createTensor((5, 3, 3), length, spacing, color=BLUE)
        tensor_group_F.scale(0.5)
        tensor_group_F.move_to(2*RIGHT)
        arrow = Arrow(
            start=tensor_group_W.get_right(), 
            end=tensor_group_F.get_left(), 
            buff=0.4,
            stroke_width=4, # Adjust the width of the arrow
            tip_length=0.2, # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow))
        label = MathTex(r"\mathcal{F}", font_size=36)
        label.next_to(arrow, UP, buff=0.2)
        self.play(FadeIn(label), run_time=1)
        self.play(FadeIn(tensor_group_F), run_time=1)
        self.wait(2)
        self.play(FadeOut(arrow), FadeOut(label), FadeOut(tensor_group_W), run_time=1)
        text8 = Tex(r"Parameters multiplication", font_size=24)
        text8.to_edge(RIGHT)
        self.play(ReplacementTransform(text7, text8), tensor_group_F.animate.move_to(4*LEFT), run_time=1)

        # Parameters multiplication
        tensor_group_F_theta = self.createTensor((5, 3, 3), length, spacing, color=RED)
        tensor_group_F_theta.scale(0.5)
        tensor_group_F_theta.move_to(2*RIGHT)   
        arrow = Arrow(
            start=tensor_group_F.get_right(), 
            end=tensor_group_F_theta.get_left(), 
            buff=0.4,
            stroke_width=4, # Adjust the width of the arrow
            tip_length=0.2, # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow))
        label = MathTex(r"R_{\Theta, t} \in \mathbb{C}^{d_v \times d_v \times k_{max} \times k_{max}}", font_size=28)
        label.next_to(arrow, UP, buff=0.2)
        self.play(FadeIn(label), run_time=1) 
        self.play(text8.animate.shift(UP))
        text9 = MathTex(r"\hat{\mathbf{v}}_{2}(\mathbf{k}) = R_{\Theta, 1}(\mathbf{k}) \cdot \hat{\mathbf{v}}_{1}(\mathbf{k}) \\ \forall \mathbf{k} \in \mathbb{Z}_{k_{max}}", font_size=24)
        text9.to_edge(RIGHT)
        self.play(Create(text9), run_time=1)
        self.play(FadeIn(tensor_group_F_theta), run_time=1)
        self.wait()

        self.play(FadeOut(arrow), FadeOut(label), FadeOut(tensor_group_F), run_time=1)
        self.play(tensor_group_F_theta.animate.move_to(4*LEFT), run_time=1)
        self.wait(1)

        # anti Fourier transform
        text10 = Tex(r"Apply the inverse \\ Fourier transform", font_size=24)
        text10.to_edge(RIGHT)
        self.play(ReplacementTransform(text9, text10), FadeOut(text8), run_time=1)
        tensor_group_F_1 = self.createTensor((5, 6, 6), length, spacing, color=RED)
        tensor_group_F_1.scale(0.5)
        tensor_group_F_1.move_to(2*RIGHT)
        arrow = Arrow(
            start=tensor_group_F_theta.get_right(), 
            end=tensor_group_F_1.get_left(), 
            buff=0.4,
            stroke_width=4, # Adjust the width of the arrow
            tip_length=0.2, # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow))
        label = MathTex(r"\mathcal{F}^{-1}", font_size=36)
        label.next_to(arrow, UP, buff=0.2)
        self.play(FadeIn(label), run_time=1) 
        self.play(FadeIn(tensor_group_F_1), run_time=1) 
        self.wait()
        
        # add, sigma and output
        self.play(FadeOut(arrow), FadeOut(label), FadeOut(tensor_group_F_theta), FadeOut(text10), run_time=1)
        self.play(tensor_group_F_1.animate.move_to(4*LEFT), run_time=1)
        plus = MathTex(r"+", font_size=36)
        plus.next_to(tensor_group_F_1, RIGHT)
        self.play(FadeIn(plus), run_time=1)
        tensor_group_V1.next_to(plus, RIGHT)
        self.play(FadeIn(tensor_group_V1), run_time=1)
        self.wait()

        left_paren = MathTex(r"\left(", font_size=146)
        right_paren = MathTex(r"\right)", font_size=146)
        sigma = MathTex(r"\sigma", font_size=36)
        left_paren.next_to(tensor_group_F_1, LEFT, buff=0.5)
        right_paren.next_to(tensor_group_V1, RIGHT, buff=0.2)
        sigma.next_to(left_paren, LEFT, buff=0.2)
        self.play(FadeIn(left_paren), FadeIn(right_paren), FadeIn(sigma), run_time=1)
        self.wait(1)
        
        equal = MathTex(r"=", font_size=36)
        equal.next_to(right_paren, RIGHT)
        tensor_group_V = self.createTensor((5, 6, 6), length, spacing, color=BLUE)
        tensor_group_V.scale(0.5)
        tensor_group_V.next_to(equal, RIGHT)
        self.play(FadeIn(equal), FadeIn(tensor_group_V), run_time=1)

        #### text
        text11 = Tex(r"I repeat the Fourier layer $L$ times", font_size=30)
        text11.to_edge(DOWN)
        self.play(Create(text11), run_time=1)
        self.wait()
        
        #### Projection operator
        self.play(FadeOut(left_paren), FadeOut(right_paren), 
                  FadeOut(sigma), FadeOut(equal), FadeOut(plus), 
                  FadeOut(tensor_group_F_1), FadeOut(tensor_group_V1),
                  FadeOut(text11), run_time=1)
        title3 = Text("PROJECTION OPERATOR", font_size=36)
        title3.to_edge(UP)
        self.play(ReplacementTransform(title2, title3), run_time=1)
        self.play(tensor_group_V.animate.move_to(4*LEFT), run_time=1)
        text12 = MathTex(r"\text{Apply the projection operator } \mathcal{Q}", font_size=24)
        text12.to_edge(RIGHT)
        self.play(Create(text12), run_time=1)
        self.wait(1)
        
        tensor_group_output= self.createTensor((1, 6, 6), length, spacing, color=BLUE)
        tensor_group_output.move_to(2*RIGHT).scale(0.5)
        arrow = Arrow(
            start=tensor_group_V.get_right(), 
            end=tensor_group_output.get_left(), 
            buff=0.4,
            stroke_width=4, # Adjust the width of the arrow
            tip_length=0.2, # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow))
        
        # create a label above the arrow
        label1 = MathTex(r"W_{\mathcal{Q}} \cdot x + b_{\mathcal{Q}}, \quad \text{pointwise}", font_size=24)
        label2 = MathTex(r"W_{\mathcal{Q}} \in \mathbb{R}^{d_v \times d_o}, b_{\mathcal{Q}} \in \mathbb{R}^{d_o}", font_size=24)
        label1.next_to(arrow, UP, buff=0.2)
        label2.next_to(arrow, DOWN, buff=0.2)
        self.play(Create(label1), Create(label2), run_time=1)

        self.play(FadeIn(tensor_group_output), run_time=1)
        self.wait(2)
        self.play(FadeOut(arrow), FadeOut(label1), FadeOut(label2), FadeOut(tensor_group_V), FadeOut(text12), run_time=1)
        self.play(tensor_group_output.animate.shift(2*LEFT), run_time=1)
        self.wait(1)
        
        #### output
        image_output = ImageMobject('output.png')
        image_output.scale(2)
        text13 = Text("We got the output", font_size=24)
        text13.to_edge(RIGHT)
        self.play(Create(text13), run_time=1)
        self.play(FadeOut(tensor_group_output), FadeIn(image_output), run_time=1)

        self.wait(2)

    def createTensor(self, tensor_size, length, spacing, color=BLUE, opacity=1, angle=PI/11):
        tensor_group = Group() # Create a group to hold all the cubes
        for i in range(tensor_size[0]):
            for j in range(tensor_size[1]):
                for k in range(tensor_size[2]):
                    # Create a small cube
                    cube = Cube(
                        side_length=length,
                        fill_color=color,
                        fill_opacity=opacity,
                        stroke_color=WHITE,
                        stroke_width=1,
                        sheen_factor=0.5,  # Add sheen for a glossy effect
                        sheen_direction=UL  # Direction of the sheen effect
                    )
                    # Position the cube based on its indices in the tensor
                    cube.move_to(np.array([i * spacing, j * spacing, k * spacing]))
                    # Add the cube to the group
                    tensor_group.add(cube)
        tensor_group.rotate(-angle, axis=UP)
        return tensor_group
    
if __name__ == "__main__":
    from manim import config
    # config.background_color = WHITE
    # config.pixel_height = 720
    # config.pixel_width = 1280
    # config.frame_height = 7.0
    # config.frame_width = 14.0
    scene = FNO()
    scene.render()
