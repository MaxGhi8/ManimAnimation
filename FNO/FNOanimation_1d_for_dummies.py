from manim import *


class FNO_architecture_1d(Scene):
    def construct(self):
        # Set camera orientation for better viewing
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        etichette_font = 30
        text_font = 28
        title_font = 36
        label_font_small = 28
        label_font_big = 34
        d_input = 1
        n_points = 10
        d_v = 6
        k_max = 3
        d_output = 4

        ##=========================================================================================##
        #### add text for the title
        title = Text("FOURIER NEURAL OPERATOR", font_size=title_font)
        title.to_edge(UP)
        self.play(Create(title), run_time=2)
        self.wait(1)

        #### add image
        image = ImageMobject("input_hh.png")
        image.scale(1.5)
        text = Text("Take an input", font_size=text_font)
        text.to_edge(RIGHT)
        self.play(Create(text), run_time=1)
        self.play(FadeIn(image), run_time=1)
        self.wait(1)

        #### text
        text1 = Text("Evaluate the function \n on a uniform grid", font_size=text_font)
        text1.to_edge(RIGHT)
        self.play(ReplacementTransform(text, text1), run_time=1)

        self.wait(2)
        ##=========================================================================================##

        #### create the tensor
        tensor_size = (n_points, d_input, 1)  # tensor size
        length = 0.3  # side length of each cube
        spacing = 2 * length  # spacing between cubes
        tensor_group1_rotate = self.createTensor(tensor_size, length, spacing)
        tensor_group1_rotate.move_to(ORIGIN).scale(80 / 100)
        self.play(FadeOut(image), FadeIn(tensor_group1_rotate), run_time=2)
        self.wait(1)
        tensor_size = (d_input, n_points, 1)  # tensor size
        tensor_group1 = self.createTensor(tensor_size, length, spacing)
        tensor_group1.move_to(ORIGIN)
        self.play(ReplacementTransform(tensor_group1_rotate, tensor_group1), run_time=1)
        self.wait(1)

        ##=========================================================================================##
        # Move to left
        self.play(tensor_group1.animate.to_edge(LEFT))

        # Change text
        text2 = Text("Apply the FNO", font_size=text_font).to_edge(RIGHT)
        self.play(ReplacementTransform(text1, text2), run_time=1)
        self.wait()

        ##=========================================================================================##

        # Load the image
        image = (
            ImageMobject("FNO.png")
            .scale_to_fit_width(0.45 * config.frame_width)
            .move_to(ORIGIN)
        )
        ##=========================================================================================##

        arrow = Arrow(
            start=tensor_group1.get_right(),
            end=image.get_left(),
            buff=0.4,
            stroke_width=4,  # Adjust the width of the arrow
            tip_length=0.2,  # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1,  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow))

        # Animate the image
        self.play(FadeIn(image), run_time=2)
        self.wait()

        # ##=========================================================================================##

        self.play(FadeOut(text2), run_time=1)

        tensor_group_output = self.createTensor(
            (d_output, n_points, 1), length, spacing, color=BLUE
        )
        tensor_group_output.move_to(ORIGIN).scale(0.8).to_edge(RIGHT)
        arrow2 = Arrow(
            start=image.get_right(),
            end=tensor_group_output.get_left(),
            buff=0.4,
            stroke_width=4,  # Adjust the width of the arrow
            tip_length=0.2,  # Adjust the length of the arrow tip
            max_tip_length_to_length_ratio=0.1,  # Adjust the tip length to arrow length ratio
        )
        self.play(GrowArrow(arrow2))
        self.play(FadeIn(tensor_group_output), run_time=1)

        self.wait(2)
        # ##=========================================================================================##

        self.play(
            FadeOut(arrow),
            FadeOut(arrow2),
            FadeOut(image),
            FadeOut(tensor_group1),
            run_time=1,
        )
        self.play(
            tensor_group_output.animate.move_to(ORIGIN),
            run_time=1,
        )
        self.wait(1)

        #### output
        text13 = Text("We obtain the output", font_size=text_font)
        text13.to_edge(UP)
        self.play(ReplacementTransform(title, text13), run_time=1)

        image_output_1 = ImageMobject("v_hh.png")
        image_output_1.scale(0.85).to_edge(LEFT)
        image_output_2 = ImageMobject("m_hh.png")
        image_output_2.scale(0.85).next_to(image_output_1, RIGHT)
        image_output_3 = ImageMobject("h_hh.png")
        image_output_3.scale(0.85).next_to(image_output_2, RIGHT)
        image_output_4 = ImageMobject("n_hh.png")
        image_output_4.scale(0.85).next_to(image_output_3, RIGHT)

        # animation with arrange
        # self.play(tensor_group_output.animate.scale(0.8).arrange(RIGHT, buff=0.2))

        tensor_group_output_1_single = self.createTensor(
            (1, n_points, 1), length, spacing
        )
        tensor_group_output_1_single.scale(0.5).move_to(image_output_1.get_center())
        tensor_group_output_2_single = self.createTensor(
            (1, n_points, 1), length, spacing
        )
        tensor_group_output_2_single.scale(0.5).move_to(image_output_2.get_center())
        tensor_group_output_3_single = self.createTensor(
            (1, n_points, 1), length, spacing
        )
        tensor_group_output_3_single.scale(0.5).move_to(image_output_3.get_center())
        tensor_group_output_4_single = self.createTensor(
            (1, n_points, 1), length, spacing
        )
        tensor_group_output_4_single.scale(0.5).move_to(image_output_4.get_center())

        self.play(
            ReplacementTransform(
                tensor_group_output,
                VGroup(
                    tensor_group_output_1_single,
                    tensor_group_output_2_single,
                    tensor_group_output_3_single,
                    tensor_group_output_4_single,
                ),
            ),
            run_time=1,
        )

        self.wait(1)

        self.play(
            FadeOut(tensor_group_output_1_single),
            FadeOut(tensor_group_output_2_single),
            FadeOut(tensor_group_output_3_single),
            FadeOut(tensor_group_output_4_single),
            FadeIn(image_output_1),
            FadeIn(image_output_2),
            FadeIn(image_output_3),
            FadeIn(image_output_4),
            run_time=1,
        )

        self.wait(4)

    def createTensor(
        self, tensor_size, length, spacing, color=BLUE, opacity=1, angle=PI / 11
    ):
        tensor_group = VGroup()  # Create a group to hold all the cubes
        for i in range(tensor_size[0]):
            for j in range(tensor_size[1]):
                for k in range(tensor_size[2]):
                    # Create a small cube
                    cube = Square(
                        side_length=length,
                        fill_color=color,
                        fill_opacity=opacity,
                        stroke_color=WHITE,
                        stroke_width=1,
                        sheen_factor=0.5,  # Add sheen for a glossy effect
                        sheen_direction=UL,  # Direction of the sheen effect
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
    scene = FNO_architecture_1d()
    scene.render()
