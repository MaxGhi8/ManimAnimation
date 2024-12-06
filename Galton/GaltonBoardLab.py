from manim import *
import math


class PegScene(Scene):
    """
    This define a rectangular grid of pegs
    """

    def construct(self):
        # Configuration parameters
        n_rows = 3
        pegs_per_row = 5
        spacing = 1
        peg_radius = 0.2
        top_buff = 3.0

        # Create one row of pegs
        row = VGroup(
            *(
                Dot(radius=peg_radius).shift(x * spacing * RIGHT)
                for x in range(pegs_per_row)
            )
        )

        # Create all rows
        rows = VGroup(
            *(
                row.copy().shift(y * spacing * DOWN * math.sqrt(3) / 2)
                for y in range(n_rows)
            )
        )

        # Shift alternate rows for triangular lattice pattern
        rows[1::2].shift(0.5 * spacing * LEFT)

        # Style and position
        rows.set_fill(GREY, 1)
        # rows.set_shading(0.5, 0.5) #!
        rows.center()
        rows.to_edge(UP, buff=top_buff)

        # Animations
        self.play(FadeIn(rows))
        self.wait()
        self.play(FadeOut(rows))
        self.wait()


class get_buckets(Scene):
    """
    Construct the buckets
    """

    def construct(self):

        self.bucket_floor_buff = 1
        self.ball_radius = 0.2

        pegs = self.get_pegs()
        assert self.ball_radius < self.spacing
        # Center of the last row of pegs
        points = [dot.get_center() for dot in pegs[-1]]
        # height and width of each bucket's truss
        height = 0.5 * config.frame_height + pegs[-1].get_y() - self.bucket_floor_buff
        width = 0.5 * self.spacing - self.ball_radius
        buff = 0.75  # for the width, larger value for thiner truss

        buckets = VGroup()
        for idx, point in enumerate(points):
            # Construction of a truss here
            p0 = point + 0.5 * self.spacing * DOWN + buff * width * RIGHT
            p1 = p0 + height * DOWN
            p2 = p1 + (1 - buff) * width * RIGHT
            y = point[1] - 0.5 * self.spacing * math.sqrt(3) + self.ball_radius
            p3 = p2[0] * RIGHT + y * UP
            side1 = VMobject().set_points_as_corners([p0, p1, p2, p3, p0])
            side1.set_stroke(WHITE, 0)
            # side1.set_style(self.bucket_style) #!
            side1.set_fill(WHITE, opacity=1)  # Fill with white, fully opaque

            # Here copy and plit the truss to get a bucket
            side2 = side1.copy()
            side2.flip(about_point=point)
            side2.reverse_points()
            side2.shift(self.spacing * RIGHT)

            # Line for the floor
            floor = Line(side1.get_corner(DL), side2.get_corner(DR))
            floor.set_stroke(WHITE, 3)
            bucket = VGroup(side1, side2, floor)
            # bucket.set_shading(0.25, 0.25) #!

            # Add bottom reference
            bucket.bottom = VectorizedPoint(floor.get_center())
            bucket.add(bucket.bottom)

            # add external bucket (for n pegs I need n+1 buckets)
            if idx == 0:
                bucket_side = bucket.copy()
                bucket_side.flip(about_point=point)
                buckets.add(bucket_side)

            # Keep track of balls
            bucket.balls = Group()

            buckets.add(bucket)

        self.play(FadeIn(pegs))
        self.wait()
        self.play(FadeIn(buckets))
        self.wait(3)
        self.play(FadeOut(pegs), FadeOut(buckets))
        self.wait(3)

    def get_pegs(self):
        self.n_rows = 3
        self.pegs_per_row = 5
        self.spacing = 1
        self.peg_radius = 0.2
        self.top_buff = 3.0

        row = VGroup(
            *(
                Dot(radius=self.peg_radius).shift(x * self.spacing * RIGHT)
                for x in range(self.pegs_per_row)
            )
        )
        rows = VGroup(
            *(
                row.copy().shift(y * self.spacing * DOWN * math.sqrt(3) / 2)
                for y in range(self.n_rows)
            )
        )
        rows[1::2].shift(0.5 * self.spacing * LEFT)

        rows.set_fill(GREY, 1)
        # rows.set_shading(0.5, 0.5) #!
        rows.center()
        rows.to_edge(UP, buff=self.top_buff)

        return rows
