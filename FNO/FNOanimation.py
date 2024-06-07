from manim import *

from manim import *

class Tensor3D(ThreeDScene):
    def construct(self):
        # Set camera orientation for better viewing
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        #### add text for the title
        title = Text("FOURIER NEURAL OPERATOR", font_size=24)
        title.to_edge(UP)
        self.play(Create(title), run_time=2)
        self.wait(1)
        
        #### add image
        image = ImageMobject('input.png')
        # image.scale()
        self.add(image)
        self.wait(1) 

        #### text
        text1 = Text("Evaluate the function \n on an uniform grid", font_size=24)
        text1.to_edge(RIGHT)
        self.play(Create(text1), run_time=1)
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
        self.play(Transform(text1, text2), tensor_group1.animate.move_to(LEFT), run_time=1)
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
        tensor_group_input = self.createTensor(tensor_size, length, spacing, color=BLUE, opacity=0.9, angle=PI/15)
        tensor_group_input.scale(0.5).move_to(LEFT)
        # For efficiency select the first one, for better visual select the second one
        self.play(Transform(tensor_group1, tensor_group_input), FadeOut(tensor_group2), FadeOut(tensor_group3), run_time=1)
        # self.play(Transform(Group(tensor_group1, tensor_group2, tensor_group3), tensor_group_input), run_time=1)

        #### text
        text3 = Tex("Apply lifting operator $ \mathcal{P} $", font_size=24)
        text3.to_edge(RIGHT)
        self.play(Transform(text2, text3), run_time=1)
        
        #### create the lifting operator
        
        
        self.wait(2)
        
        
    def createTensor(self, tensor_size, length, spacing, color=BLUE, opacity=0.7, angle=PI/11):
        tensor_group = Group() # Create a group to hold all the cubes
        for i in range(tensor_size[0]):
            for j in range(tensor_size[1]):
                for k in range(tensor_size[2]):
                    # Create a small cube
                    cube = Cube(side_length=length, fill_color=color, fill_opacity=opacity, stroke_color=color, stroke_width=opacity)
                    # Position the cube based on its indices in the tensor
                    cube.move_to(np.array([i * spacing, j * spacing, k * spacing]))
                    # Add the cube to the group
                    tensor_group.add(cube)
        tensor_group.rotate(-angle, axis=UP)
        return tensor_group
        

if __name__ == "__main__":
    from manim import config
    config.background_color = WHITE
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_height = 7.0
    config.frame_width = 14.0
    scene = Tensor3D()
    scene.render()
