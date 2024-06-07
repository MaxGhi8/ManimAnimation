from manim import *

from manim import *

class Tensor3D(ThreeDScene):
    def construct(self):
        tensor_size = (4, 3, 4) # tensor size
        spacing = 1 # spacing between elements
        length = 0.5 # side length of each cube
        # Create a group to hold all the cubes
        tensor_group = Group()

        # Loop over each element in the tensor
        for i in range(tensor_size[0]):
            for j in range(tensor_size[1]):
                for k in range(tensor_size[2]):
                    # Create a small cube
                    cube = Cube(side_length=length, fill_color=BLUE, fill_opacity=0.5, stroke_color=BLUE, stroke_width=0.5)
                    # Position the cube based on its indices in the tensor
                    cube.move_to(np.array([i * spacing, j * spacing, k * spacing]))
                    # Add the cube to the group
                    tensor_group.add(cube)
        
        # Center the entire tensor group
        tensor_group.move_to(ORIGIN)

        self.add(tensor_group)
        
        # Set camera orientation for better viewing
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

if __name__ == "__main__":
    from manim import config
    config.background_color = WHITE
    config.pixel_height = 720
    config.pixel_width = 1280
    config.frame_height = 7.0
    config.frame_width = 14.0
    scene = Tensor3D()
    scene.render()
