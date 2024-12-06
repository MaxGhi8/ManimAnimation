from manim import *
import math


def gauss_func(x, mu, sigma):
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(
        -((x - mu) ** 2) / (2 * sigma**2)
    )


class GaltonBoard(Scene):
    random_seed = 1
    pegs_per_row = 9
    n_rows = 5
    spacing = 1.0
    top_buff = 0.5
    peg_radius = 0.1
    ball_radius = 0.1
    bucket_floor_buff = 1.0
    stack_ratio = 1.0
    fall_factor = 0.6
    clink_sound = "tick.mp3"
    mode_corner = "vertical"

    def construct(self):
        # ------------------------------------------------
        # Create the pegs and buckets
        # ------------------------------------------------
        pegs = self.get_pegs()
        buckets = self.get_buckets(pegs)
        # Save the bottom of the buckets without balls and labels
        bottom_bucket_no_label = []
        for bucket in buckets:
            tmp_bottom = VectorizedPoint(bucket.get_bottom())
            bottom_bucket_no_label.append(tmp_bottom)

        # Stagger animation of the pegs and buckets
        self.play(
            LaggedStartMap(Write, buckets),
            LaggedStartMap(Write, pegs),
        )
        self.wait()

        # ------------------------------------------------
        # Animation of some balls falling
        # ------------------------------------------------
        # balls = self.drop_n_balls(5, pegs, buckets, sound=True)  #!
        balls = self.drop_n_balls(25, pegs, buckets, sound=True)  #!

        self.wait()
        # Reverse the order of the balls and FadeOut one by one
        animations = []
        for ball in balls:
            animations.append(FadeOut(ball))
        self.play(AnimationGroup(*animations, lag_ratio=0.05))

        # Reset the bucket attributes
        for idx, bucket in enumerate(buckets):
            bucket.balls = Group()
            bucket.bottom = bottom_bucket_no_label[idx]

        # ------------------------------------------------
        # Single ball bouncing, step-by-step
        # ------------------------------------------------
        ball = self.get_ball()
        bits = np.random.randint(0, 2, self.n_rows)
        _, pieces = self.random_trajectory(ball, pegs, buckets, bits)

        all_arrows = VGroup()
        # Makes all the bounces animation
        for piece, bit in zip(pieces, bits):
            ball.move_to(piece.get_end())  # Makes one jump
            pm_arrows = self.get_pm_arrows(ball)  # Creates arrow
            all_arrows.add(pm_arrows)
            # animations
            self.play(self.falling_anim(ball, piece))
            self.add_single_clink_sound()
            self.play(FadeIn(pm_arrows, lag_ratio=0.1))
            self.wait()
            self.play(
                pm_arrows[1 - bit].animate.set_opacity(0.25)
            )  # Makes the unused arrow less visible

        # Last jump inside the bucket
        for piece in pieces[-2:]:
            self.play(self.falling_anim(ball, piece))
        self.wait()

        # Makes the sum of the directions
        corner_sum_anim, corner_sum_fade = self.show_corner_sum(
            all_arrows, bits, mode=self.mode_corner
        )
        self.play(corner_sum_anim)
        self.wait()

        # Show buckets as sums
        sums = range(-self.n_rows, self.n_rows + 1, 2)
        sum_labels = VGroup(
            *(Integer(s, font_size=24, include_sign=True) for s in sums)
        )
        tot_buckets = len(buckets)
        diff = (tot_buckets - (self.n_rows + 1)) // 2
        for bucket, label in zip(buckets[diff:], sum_labels):
            label.next_to(bucket, DOWN, SMALL_BUFF)

        # animate the labels
        sum_labels.set_stroke(WHITE, 1)
        self.play(Write(sum_labels))
        self.wait()

        for bucket, label in zip(buckets, sum_labels):
            bucket.add(label)

        # Remove all the stuffs of direction
        self.play(FadeOut(all_arrows, lag_ratio=0.025), corner_sum_fade)

        # ------------------------------------------------
        # Show a few more trajectories with cumulative sum
        # ------------------------------------------------
        for _ in range(3):
            ball = self.get_ball()
            bits = np.random.randint(0, 2, self.n_rows)
            _, pieces = self.random_trajectory(ball, pegs, buckets, bits)

            all_arrows = VGroup()

            self.add(all_arrows)
            for piece, bit in zip(pieces, bits):
                ball.move_to(piece.get_end())
                arrows = self.get_pm_arrows(ball)
                all_arrows.add(arrows[:])
                self.play(self.falling_anim(ball, piece))
                self.add_single_clink_sound()
                arrows[1 - bit].set_opacity(0.25)

            self.play(self.falling_anim(ball, pieces[-2]))
            # self.add_single_clink_sound() # click when hit the bucket
            corner_sum_anim, corner_sum_fade = self.show_corner_sum(
                all_arrows, bits, mode=self.mode_corner
            )
            self.play(
                self.falling_anim(ball, pieces[-1]),
                corner_sum_anim,
            )
            self.wait()
            self.play(FadeOut(all_arrows, lag_ratio=0.025), corner_sum_fade)

        # ------------------------------------------------
        # Drops balls and show the number distribution
        # ------------------------------------------------
        # self.drop_n_balls(5, pegs, buckets, sound=True)  #!
        self.drop_n_balls(25, pegs, buckets, sound=True)  #!

        # Fade out irrelevant parts
        n = self.pegs_per_row // 2
        to_fade = VGroup()
        peg_triangle = VGroup()
        for row in range(self.n_rows):
            r2 = row // 2
            low = n - r2
            high = n + 1 + r2 + (row % 2)
            to_fade.add(pegs[row][:low])
            to_fade.add(pegs[row][high:])
            peg_triangle.add(pegs[row][low:high])

        to_fade.add(buckets[:diff])
        to_fade.add(buckets[diff + self.n_rows + 1 :])

        self.play(to_fade.animate.set_opacity(0.25), lag_ratio=0.01)

        # Show relevant probabilities
        point = (
            peg_triangle[0][0].get_top() + MED_SMALL_BUFF * UP
        )  # First peg position (top of the triangle)
        v1 = (
            peg_triangle[1][0].get_center() - peg_triangle[0][0].get_center()
        )  # DR direction
        v2 = (
            peg_triangle[1][1].get_center() - peg_triangle[1][0].get_center()
        )  # DL direction

        last_labels = VGroup(self.get_peg_label(0, 0, point, v1, v2, split=False))
        self.play(FadeIn(last_labels))
        for n in range(1, self.n_rows + 1):
            split_labels = VGroup(
                *(
                    self.get_peg_label(n, k, point, v1, v2, split=True)
                    for k in range(n + 1)
                )
            )
            unsplit_labels = VGroup(
                *(
                    self.get_peg_label(n, k, point, v1, v2, split=False)
                    for k in range(n + 1)
                )
            )
            anims = [
                TransformFromCopy(last_labels[0], split_labels[0]),
                TransformFromCopy(last_labels[-1], split_labels[-1]),
            ]
            for k in range(1, n):
                anims.append(TransformFromCopy(last_labels[k - 1], split_labels[k][0]))
                anims.append(TransformFromCopy(last_labels[k], split_labels[k][1]))

            self.play(*anims)
            self.play(
                *(
                    FadeTransformPieces(sl1, sl2)
                    for sl1, sl2 in zip(split_labels, unsplit_labels)
                )
            )

            last_labels = unsplit_labels

        # ------------------------------------------------
        # Show an example with a lot of balls
        # ------------------------------------------------
        # Remove the balls
        all_balls = Group()
        for idx, bucket in enumerate(buckets):
            all_balls.add(*bucket.balls)

        self.play(LaggedStartMap(FadeOut, all_balls, run_time=1))

        # reset buckets
        buckets = self.get_buckets(pegs)
        # Drop a lot of balls
        self.stack_ratio = 0.125
        np.random.seed(0)
        # self.drop_n_balls(5, pegs, buckets, lr_factor=2)  #!
        self.drop_n_balls(250, pegs, buckets, lr_factor=2)  #!
        self.wait(2)

    def get_pegs(self) -> VGroup:
        """
        This define a rectangular grid of pegs

        Returns:
            VGroup: A VGroup of VGroup of pegs
        """
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
        rows.center()
        rows.to_edge(UP, buff=self.top_buff)

        return rows

    def get_peg_label(self, n: int, k: int, point, v1, v2, split=False):
        """
        Methods to write the probability of each peg as a label

        Args:
            n: int
                The index of the row

            k: int
                The index of the peg

            point:
                The position of the first peg

            v1:
                Direction 1

            v2:
                Direction 2

            split: bool
                Whether to split the label into two parts
        """
        kw = dict(font_size=16)

        if n == 0:
            label = Tex("1", font_size=24)

        elif split and 0 < k < n:
            label = VGroup(
                Tex(f"{choose(n - 1, k - 1)}/{2**n}", **kw),
                Tex(f" + {{{choose(n - 1, k)}/{2**n}}}", **kw),
            )
            label.arrange(RIGHT, buff=0.75 * label[0].get_width())

        else:
            label = VGroup(Tex(f"{choose(n, k)}/{2**n}", **kw))

        label.move_to(point + n * v1 + k * v2)

        return label

    def get_buckets(self, pegs: VGroup) -> VGroup:
        """
        Construct the buckets

        Args:
            pegs: VGroup
                The pegs VGroup return from get_pegs method

        Returns:
            VGroup: A VGroup of buckets

        The method construct the self.bucket_floor_buff and self.ball_radius
        """
        assert self.ball_radius < self.spacing

        # Center of the last row of pegs
        points = [dot.get_center() for dot in pegs[-1]]

        # height and width of each bucket's truss
        height = 0.5 * config.frame_height + pegs[-1].get_y() - self.bucket_floor_buff
        width = 0.5 * self.spacing - self.ball_radius
        buff = 0.75  # for the width of buckets' truss, larger value for thicker truss

        buckets = VGroup()
        for idx, point in enumerate(points):
            # Construction of a truss here
            p0 = point + 0.5 * self.spacing * DOWN + buff * width * RIGHT
            p1 = p0 + height * DOWN
            p2 = p1 + (1 - buff) * width * RIGHT
            y = point[1] - 0.5 * self.spacing * math.sqrt(3) + self.ball_radius
            p3 = p2[0] * RIGHT + y * UP
            side1 = VMobject().set_points_as_corners([p0, p1, p2, p3, p0])
            side1.set_stroke(GREY, 0)
            side1.set_fill(GREY, opacity=1)  # Fill with color, fully opaque

            # Here copy and split the truss to get a bucket
            side2 = side1.copy()
            side2.flip(about_point=point)
            side2.reverse_points()
            side2.shift(self.spacing * RIGHT)

            # Line for the floor
            floor = Line(side1.get_corner(DL), side2.get_corner(DR))
            floor.set_stroke(GREY, 3)
            bucket = VGroup(side1, side2, floor)

            # Add bottom reference
            bucket.bottom = VectorizedPoint(floor.get_center())

            # Keep track of balls
            bucket.balls = Group()

            # add external bucket (for n pegs I need n+1 buckets)
            if idx == 0:
                bucket_side = bucket.copy()
                bucket_side.flip(about_point=point)
                buckets.add(bucket_side)

            buckets.add(bucket)

        return buckets

    def get_ball_arrows(
        self, ball, labels: list, sub_labels: list = [], colors: list = [RED, BLUE]
    ) -> VGroup:
        """
        Function to create arrows pointing to the left and right of the ball

        Args:
            ball:
                The ball to which the arrows point

            labels: list
                The labels to be placed above the arrows

            sub_labels: list (optional)
                The labels to be placed below the arrows

            colors: list (optional)
                The colors of the arrows
        """
        arrows = VGroup()
        for vect, color, label in zip([LEFT, RIGHT], colors, labels):
            # Create the arrow next to the ball
            arrow = Vector(
                0.5 * self.spacing * vect,
                max_tip_length_to_length_ratio=0.25,
                stroke_color=color,
            )
            arrow.next_to(ball, vect, buff=0.1)
            arrows.add(arrow)
            # Add label above the arrow
            text = Tex(label, font_size=24)
            text.next_to(arrow, UP, SMALL_BUFF)
            arrow.add(text)

        # Possibly add smaller labels below the arrow
        for arrow, label in zip(arrows, sub_labels):
            text = Text(label, font_size=16)
            text.next_to(arrow, DOWN, SMALL_BUFF)
            arrow.add(text)

        return arrows

    def get_fifty_fifty_arrows(self, ball) -> VGroup:
        """
        Show 50-50 arrows, with get_ball_arrows function
        """
        return self.get_ball_arrows(ball, ["50%", "50%"])

    def get_pm_arrows(self, ball, show_prob: bool = True) -> VGroup:
        """
        Show +1-1 arrows with sub-labels 50-50 if show_prob is equal to True,
        with get_ball_arrows function
        """
        return self.get_ball_arrows(
            ball, ["$-1$", "$+1$"], sub_labels=(["50%", "50%"] if show_prob else [])
        )

    def show_corner_sum(self, pm_arrows, bits, font_size=48, mode="vertical"):
        """
        The function animates a visual transformation of arrows (pm_arrows) and
        associated bits into a summation term. This term is displayed at the
        top-left corner of the screen.
        """
        parts = VGroup(*(arrow[bit][0].copy() for arrow, bit in zip(pm_arrows, bits)))
        parts.target = parts.generate_target()

        if mode == "vertical":
            parts.target.arrange(DOWN, buff=0.1)  # next to each other
        else:
            parts.target.arrange(RIGHT, buff=0.1)

        # parts.target.scale(font_size / 28) # upscale the font
        parts.target.to_edge(UP, buff=MED_SMALL_BUFF)
        parts.target.to_edge(LEFT)

        # Makes the animation from the original position/colors/fonts to the target one
        anim1 = MoveToTarget(parts, lag_ratio=0.01)

        # Calculate the sum term of the selected directions
        sum_term = Tex(
            f"= {2 * sum(bits) - len(bits)}", font_size=font_size
        )  # bits are 0 or 1

        if mode == "vertical":
            sum_term.next_to(parts.target, DOWN, buff=0.3, aligned_edge=DOWN)
        else:
            sum_term.next_to(parts.target, RIGHT, buff=0.1, aligned_edge=RIGHT)

        # Lagged animation (i.e. a sequence of animations)
        anim2 = LaggedStart(
            *(
                ReplacementTransform(
                    part.copy().set_opacity(0), sum_term, path_arc=-30 * DEGREES
                )
                for part in parts.target
            )
        )

        return Succession(anim1, anim2), FadeOut(VGroup(parts, sum_term))

    def get_ball(self, color=YELLOW_E):
        """
        This function creates and returns a stylized "ball" object for use in animations.
        """
        ball = Dot(radius=self.ball_radius, color=color)
        return ball

    def single_bounce_trajectory(self, ball, peg, direction):
        """
        This method models the motion of a ball after a single bounce off a peg.
        The resulting trajectory is visually represented using a parabolic curve.
        """
        sgn = np.sign(direction[0])
        # Create a parabolic trajectory
        trajectory = FunctionGraph(
            lambda x: -x * (x - 1),
            x_range=(0, 2, 0.1),
        )

        # Get the starting and ending points of the trajectory
        p1 = peg.get_top()
        p2 = p1 + self.spacing * np.array([sgn * 0.5, -math.sqrt(3) / 2, 0])

        # Stretch and shift the trajectory to fit the starting and ending points
        vect = trajectory.get_end() - trajectory.get_start()
        for i in (0, 1):
            trajectory.stretch((p2[i] - p1[i]) / vect[i], i)
        trajectory.shift(p1 - trajectory.get_start() + self.ball_radius * UP)

        return trajectory

    def random_trajectory(self, ball, pegs, buckets, bits=None):
        """
        The random_trajectory method defines the motion of a ball falling through a pegboard and eventually landing in a bucket.
        It creates a visually appealing trajectory by chaining multiple segments of motion:
        an initial drop, bounces off pegs, and a final descent into a bucket.
        """
        index = len(pegs[0]) // 2  # Start in the middle
        radius = self.ball_radius
        peg = pegs[0][index]

        ## Create a straight line to represent the initial drop
        top_line = ParametricFunction(
            lambda t: t**2 * DOWN, t_range=[0, 1], color=WHITE
        )
        top_line.move_to(
            peg.get_top() + radius * UP, DOWN
        )  # Start slightly above the first peg

        ## Create a list to store the trajectory segments in the pegs board
        bounces = []
        # Determines the ball's bounce direction at each row (0 for left, 1 for right). If not provided, it's randomly generated.
        if bits is None:
            bits = np.random.randint(0, 2, self.n_rows)
        # Create a bounce trajectory for each row
        for row, bit in enumerate(bits):
            peg = pegs[row][index]
            bounces.append(self.single_bounce_trajectory(ball, peg, [LEFT, RIGHT][bit]))
            index += bit
            # Adjusts the index for staggered rows, as the pegs are offset alternately.
            if row % 2 == 1:
                index -= 1

        ## Create a final line to represent the ball falling into the bucket
        bucket = buckets[index + (-1 if self.n_rows % 2 == 0 else 0)]
        final_line = Line(
            bounces[-1].get_end(), bucket.bottom.get_center() + self.ball_radius * UP
        )
        final_line.insert_n_curves(int(8 * final_line.get_length()))  #!
        bucket.bottom.shift(2 * self.ball_radius * self.stack_ratio * UP)
        bucket.balls.add(ball)

        ## Combine all the trajectory segments into a single VMobject
        result = VMobject()  # full trajectory as a single VMobject
        pieces = VGroup(top_line, *bounces, final_line)  # trajectory pieces as a VGroup
        for vmob in pieces:
            if result.get_num_points() > 0:
                vmob.shift(result.get_end() - vmob.get_start())
            result.append_vectorized_mobject(vmob)

        return result, pieces

    def falling_anim(self, ball, trajectory):
        """
        Method to animate the ball falling along a given trajectory.
        """
        return MoveAlongPath(
            ball,
            trajectory,
            rate_func=linear,
            run_time=self.fall_factor * trajectory.get_arc_length(),
        )

    def add_single_clink_sound(self, time_offset=0, gain=0):
        """
        Add a single clink randomized sound to the animation.
        """
        self.add_sound(
            sound_file="tick.mp3",
            time_offset=time_offset,
            gain=gain,
        )

    def add_falling_clink_sounds(self, trajectory_pieces, time_offset=0, gain=0):
        """
        Add clink sounds to the animation at each bounce with appropriate timing.
        """
        total_len = trajectory_pieces[0].get_arc_length()
        for piece in trajectory_pieces[1:-1]:
            self.add_single_clink_sound(
                time_offset + self.fall_factor * total_len, gain
            )
            total_len += piece.get_arc_length()

    def drop_n_balls(self, n, pegs, buckets, lr_factor=1, sound=False):
        """
        Function to animate the falling of n balls through the pegboard.
        """
        # Animate n balls falling
        balls = Group(*(self.get_ball() for _ in range(n)))
        trajs = [self.random_trajectory(ball, pegs, buckets) for ball in balls]
        anims = (self.falling_anim(ball, traj[0]) for ball, traj in zip(balls, trajs))
        full_anim = LaggedStart(*anims, lag_ratio=lr_factor / n)

        # Add sounds
        if sound:
            start_times = [tup[1] for tup in full_anim.anims_with_timings]
            for time, traj in zip(start_times, trajs):
                self.add_falling_clink_sounds(traj[1], time, gain=0)

        # Render the animation
        self.play(full_anim)

        return balls


class EmphasizeMultipleSums(GaltonBoard):
    def construct(self):
        pegs = self.get_pegs()
        buckets = self.get_buckets(pegs)
        self.add(pegs, buckets)

        # Show a trajectories with cumulative sum
        for x in range(20):
            ball = self.get_ball()
            bits = np.random.randint(0, 2, self.n_rows)
            full_trajectory, pieces = self.random_trajectory(ball, pegs, buckets, bits)

            all_arrows = VGroup()

            self.add(all_arrows)
            for piece, bit in zip(pieces, bits):
                ball.move_to(piece.get_end())
                arrows = self.get_pm_arrows(ball)
                all_arrows.add(arrows)
                self.play(self.falling_anim(ball, piece))
                self.add_single_clink_sound()
                arrows[1 - bit].set_opacity(0.25)

            self.play(self.falling_anim(ball, pieces[-2]))
            self.add_single_clink_sound()
            self.play(self.falling_anim(ball, pieces[-1]), FadeOut(all_arrows))


class GaltonTrickle(GaltonBoard):
    def construct(self):
        pegs = self.get_pegs()
        buckets = self.get_buckets(pegs)
        self.add(pegs, buckets)

        ball = self.get_ball()
        peg = pegs[0][len(pegs[0]) // 2]
        ball.move_to(peg.get_top(), DOWN)
        arrows = self.get_pm_arrows(ball)

        # Drops
        n = 25

        balls = Group(*(self.get_ball() for x in range(n)))
        all_bits = [np.random.randint(0, 2, self.n_rows) for x in range(n)]
        trajs = [
            self.random_trajectory(ball, pegs, buckets, bits)
            for ball, bits in zip(balls, all_bits)
        ]
        falling_anims = (
            self.falling_anim(ball, traj[0]) for ball, traj in zip(balls, trajs)
        )

        arrow_copies = VGroup()
        for bits in all_bits:
            ac = arrows.copy()
            ac[1 - bits[0]].set_opacity(0.2)
            arrow_copies.add(ac)

        rt = 60
        arrows.set_opacity(1)
        self.add(arrows)
        self.play(
            LaggedStart(*falling_anims, lag_ratio=0.4, run_time=rt),
            # ShowSubmobjectsOneByOne(arrow_copies, run_time=1.0 * rt),
        )
        self.wait()


class BiggerGaltonBoard(GaltonBoard):
    random_seed = 0
    pegs_per_row = 30
    n_rows = 13
    spacing = 0.5
    top_buff = 0.5
    peg_radius = 0.025
    ball_radius = 0.05
    bucket_floor_buff = 0.5
    stack_ratio = 0.1
    n_balls = 800

    def construct(self):
        # Setup
        pegs = self.get_pegs()
        buckets = self.get_buckets(pegs)
        self.add(pegs, buckets)

        # Drop!
        self.drop_n_balls(self.n_balls, pegs, buckets, lr_factor=2)
        self.wait()

        # Show low bell cuve
        full_rect = FullScreenFadeRectangle()
        full_rect.set_fill(BLACK, 0.5)
        balls = self.mobjects[-1]
        curve = FunctionGraph(lambda x: gauss_func(x, 0, 1))
        curve.set_stroke(YELLOW)
        curve.move_to(balls, DOWN)
        curve.match_height(balls, stretch=True, about_edge=DOWN)
        formula = Tex(R"{1 \over \sqrt{2\pi}} e^{-x^2 / 2}", font_size=60)
        formula.move_to(balls, LEFT)
        formula.shift(1.25 * LEFT)
        formula.set_backstroke(width=8)

        self.add(full_rect, balls)
        self.play(FadeIn(full_rect), ShowCreation(curve, run_time=2), Write(formula))
        self.wait()


class SingleDropBigGaltonBoard(BiggerGaltonBoard):
    spacing = 0.55
    ball_radius = 0.075

    def construct(self):
        # Setup
        pegs = self.get_pegs()
        buckets = self.get_buckets(pegs)
        self.add(pegs, buckets)

        # Single ball bouncing, step-by-step
        ball = self.get_ball()
        full_trajectory, pieces = self.random_trajectory(ball, pegs, buckets)
        self.add_falling_clink_sounds(pieces)
        self.play(self.falling_anim(ball, full_trajectory))
        self.wait()


class NotIdenticallyDistributed(GaltonBoard):
    def construct(self):
        # Setup
        pegs = self.get_pegs()
        buckets = self.get_buckets(pegs)
        self.add(pegs, buckets)

        # Arrows to show distributions
        max_arrow_len = 0.5

        def get_peg_arrow(peg, angle, length, color=RED_E):
            vect = np.array([-math.sin(angle), math.cos(angle), 0])
            arrow = Vector(
                ORIGIN,
                length * vect,
                buff=0,
                fill_color=color,
                max_tip_length_to_length_ratio=0.25,
                thickness=0.025,
            )
            arrow.shift(peg.get_center() + vect * peg.get_radius())
            arrow.set_fill(opacity=0.8 * length / max_arrow_len)
            return arrow

        def get_bounce_distribution(peg, sigma=30 * DEGREES):
            ds = sigma / 2
            angles = np.arange(-2 * sigma, 2 * sigma + ds, ds)
            denom = math.sqrt(2 * PI) * sigma
            arrows = VGroup(
                *(
                    get_peg_arrow(
                        peg, angle, denom * gauss_func(angle, 0, sigma) * max_arrow_len
                    )
                    for angle in angles
                )
            )
            return arrows

        # Show many distributions
        all_dists = VGroup(
            *(get_bounce_distribution(peg) for row in pegs for peg in row)
        )

        all_dists.set_fill(RED_E, 0.8)
        self.play(LaggedStart(*(LaggedStartMap(GrowArrow, dist) for dist in all_dists)))
        self.wait()

        # Zoom in to top one
        ball = self.get_ball()
        peg1 = pegs[0][len(pegs[0]) // 2]
        peg2 = pegs[1][len(pegs[1]) // 2]
        peg1_dist = get_bounce_distribution(peg1)
        peg2_dist = get_bounce_distribution(peg2)
        peg1_dist.rotate(30 * DEGREES, about_point=peg1.get_center())
        peg2_dist.rotate(-30 * DEGREES, about_point=peg2.get_center())

        full_trajectory, pieces = self.random_trajectory(
            ball, pegs, buckets, [0, 1, 0, 0, 0]
        )
        pieces[0].move_to(peg1.pfp(3 / 8) + ball.get_radius() * UP, DOWN)
        pieces[1].stretch(0.7, 0)
        pieces[1].shift(pieces[0].get_end() - pieces[1].get_start())
        pieces[2].stretch(0.9, 0)
        pieces[2].stretch(0.97, 1)
        pieces[2].shift(pieces[1].get_end() - pieces[2].get_start())

        self.play(
            FadeOut(all_dists, lag_ratio=0.01),
            self.falling_anim(ball, pieces[0]),
            run_time=2,
        )
        self.add(peg1_dist, ball)
        self.play(LaggedStartMap(FadeIn, peg1_dist))
        self.wait()
        self.play(self.falling_anim(ball, pieces[1]), run_time=1)
        self.play(LaggedStartMap(FadeIn, peg2_dist))
        self.wait()
        self.play(self.falling_anim(ball, pieces[2]), run_time=1)
        self.wait(2)
