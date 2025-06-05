from manim import *


class RotationTransition(MovingCameraScene):
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
        self.camera.background_color = WHITE

        image = ImageMobject("titolo.jpeg").scale_to_fit_width(config.frame_width)

        self.play(FadeIn(image))
        self.wait(2)
        # self.play(
        #     LaggedStart(
        #         Rotate(image, angle=PI / 2, about_point=ORIGIN),
        #         FadeOut(image),
        #         lag_ratio=0.5,
        #         run_time=1,
        #     ),
        # )
        self.play(
            ClockwiseTransform(
                image,
                image.copy().rotate(PI, about_point=ORIGIN).scale(0.1).set_opacity(0),
            ),
        )

        self.wait(2)
