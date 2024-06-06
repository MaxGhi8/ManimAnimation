from manim import *

class Shapes(ThreeDScene):
    def construct(self):
        # Set camera orientation
        self.set_camera_orientation(phi=5/6 * PI, theta=PI/4)
        
        # Create a cube
        cube = Cube()
        self.play(Create(cube))
        self.wait(1)

        # Calculate the center of each face
        face_centers = [
            cube.get_center() + normal for normal in [
                UP, DOWN, LEFT, RIGHT, IN, OUT
            ]
        ]

        # Display the center of each face
        for center in face_centers:
            self.play(Create(Dot(center)))
            self.wait(1)