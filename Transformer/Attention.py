import itertools as it
from typing import Dict

import numpy as np
from manim import *

np.random.seed(0)


class AttentionPatterns(Scene):
    def construct(self):
        # Add sentence
        phrase = "A nice seminar inside this cute room"
        phrase_mob = Text(phrase)
        phrase_mob.move_to(2 * UP)

        words = list(filter(lambda s: s.strip(), phrase.split(" ")))
        word2mob: Dict[str, VMobject] = {}
        for idx, word in enumerate(words):
            word2mob[word] = Text(word)
            if idx == 0:
                word2mob[word].move_to(2 * UP).to_edge(LEFT)
            else:
                word2mob[word].move_to(2 * UP).next_to(
                    word2mob[words[idx - 1]], RIGHT
                ).align_to(word2mob[words[0]], DOWN)

        word_mobs = VGroup(*word2mob.values())
        self.play(LaggedStartMap(FadeIn, word_mobs, shift=0.5 * UP, lag_ratio=0.25))
        self.wait()

        # Create word rectangles
        word2rect: Dict[str, VMobject] = dict()
        SMALL_BUFF_HEIGHT = 0.2
        SMALL_BUFF_WIDTH = 0.05
        for word in words:
            rect = SurroundingRectangle(word2mob[word])
            rect.set(
                width=word2mob[word].width + SMALL_BUFF_WIDTH,
                height=phrase_mob.height + SMALL_BUFF_HEIGHT,
            )
            rect.match_y(phrase_mob)
            rect.set_stroke(GREY, 2)
            rect.set_fill(GREY, 0.2)
            word2rect[word] = rect

        # Adjectives updating noun
        adjs = ["nice", "cute"]
        nouns = ["seminar", "room"]
        others = ["A", "inside", "this"]
        adj_mobs, noun_mobs, other_mobs = [
            VGroup(word2mob[substr] for substr in group)
            for group in [adjs, nouns, others]
        ]
        adj_rects, noun_rects, other_rects = [
            VGroup(word2rect[substr] for substr in group)
            for group in [adjs, nouns, others]
        ]
        adj_rects.set_color(GREEN)
        noun_rects.set_color(GREY_BROWN)
        other_rects.set_color(YELLOW)

        self.play(
            LaggedStartMap(DrawBorderThenFill, adj_rects),
            # Animation(adj_mobs),
        )
        self.wait()

        self.play(
            LaggedStartMap(DrawBorderThenFill, noun_rects),
            # Animation(noun_mobs),
        )
        self.wait()

        self.play(
            LaggedStartMap(DrawBorderThenFill, other_rects),
            # Animation(other_mobs),
        )
        self.wait()

        # Makes arrows
        adj_to_noun_arrows = VGroup(
            CurvedArrow(
                word2rect[adj].get_top(),
                word2rect[noun].get_top(),
                angle=-PI / 4,
                color=BLUE,
                # stroke_width=0.2,
                tip_length=0.15,
            )
            for adj, noun in zip(adjs, nouns)
        )
        self.play(
            LaggedStartMap(Create, adj_to_noun_arrows, lag_ratio=0.2, run_time=1.5),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, adj_to_noun_arrows, lag_ratio=0.2, run_time=1.5),
        )
        self.wait()

        for other in others:
            other_arrows = VGroup(
                CurvedArrow(
                    word2rect[other].get_top(),
                    word2rect[noun].get_top(),
                    angle=-PI / 4,
                    tip_length=0.15,
                )
                for noun in nouns + adjs
            )
            self.play(
                LaggedStartMap(Create, other_arrows, lag_ratio=0.2, run_time=1.5),
            )
            self.play(
                LaggedStartMap(FadeOut, other_arrows, lag_ratio=0.2, run_time=1.5),
            )

        self.wait()

        # Print the embedding and queries
        all_rects = VGroup(*adj_rects, *noun_rects, *other_rects)
        all_rects.sort(lambda p: p[0])

        numeric_embedding = self.NumericEmbedding(all_rects, DOWN)
        self.play(LaggedStartMap(Write, numeric_embedding, run_time=1.5))
        self.wait()

        label_embedding = self.LetterEmbedding(numeric_embedding, DOWN)
        self.play(LaggedStartMap(Create, label_embedding, run_time=2))
        self.wait()

        queries = self.ApplyParameters(label_embedding, DOWN, "Q", arrow_length=1.0)
        self.play(LaggedStartMap(Create, queries, run_time=2))
        self.wait()

        # Create a copy for the keys
        rect_numeric_embedding_queries = VGroup(*all_rects, *word_mobs)
        rect_numeric_embedding_keys = rect_numeric_embedding_queries.copy()
        rect_numeric_embedding_keys.rotate(PI / 2).move_to(ORIGIN).to_edge(
            LEFT
        ).to_edge(DOWN)

        # Scale and move the queries
        rect_to_queries = VGroup(
            *rect_numeric_embedding_queries,
            *numeric_embedding,
            *label_embedding,
            *queries,
        )
        self.play(
            rect_to_queries.animate.scale(0.4).shift(0.4 * RIGHT).to_edge(UP),
            run_time=1.5,
        )
        self.wait()

        # Apply embeddings and keys
        key_numeric_embedding = self.NumericEmbedding(
            rect_numeric_embedding_keys, RIGHT
        )
        key_label_embedding = self.LetterEmbedding(key_numeric_embedding, RIGHT)
        keys = self.ApplyParameters(key_label_embedding, RIGHT, "K", arrow_length=1.0)

        rect_to_keys = VGroup(
            *rect_numeric_embedding_keys,
            *key_numeric_embedding,
            *key_label_embedding,
            *keys,
        )
        rect_to_keys.scale(0.4).to_edge(DOWN)
        self.play(LaggedStartMap(Create, rect_to_keys), run_time=5.0)
        self.wait()

        # Make the grid
        grid = self.CreateGrid(8, 8)
        grid.scale(0.6)
        grid.next_to(keys[-1], RIGHT, aligned_edge=UP, buff=1)
        self.play(Create(grid), run_time=2)
        self.wait()

        # Populate the grid with Queries and Keys
        cdot = MathTex("\\cdot")
        cdot.move_to(grid[0][0].get_center())
        self.play(FadeIn(cdot))
        self.wait()

        queries_grid = queries.copy()
        queries_grid = queries_grid[2::3]
        for idx, query in enumerate(queries_grid):
            query.move_to(grid[0][idx + 1].get_center()).set_color(GREEN).scale(1.1)
            self.play(Write(query), run_time=0.2)
        self.wait()

        keys_grid = keys.copy()
        keys_grid = keys_grid[2::3]
        for idx, key in enumerate(keys_grid):
            key.move_to(grid[idx + 1][0].get_center()).set_color(YELLOW).scale(1.1)
            self.play(Write(key), run_time=0.2)
        self.wait()

        # Populate the grid with the dot products
        text_dot_product = (
            Text("Compute the dot\n products between\n queries and keys")
            .scale(0.5)
            .to_edge(RIGHT)
        )
        self.play(Write(text_dot_product))
        self.wait()

        dot_product_group_letters = VGroup()
        for i, j in it.product(range(1, 8), range(1, 8)):
            dot_product = (
                MathTex(
                    f"\\vec{{ \\textbf{{Q}} }}_{j} \\cdot \\vec{{ \\textbf{{K}} }}_{i}"
                )
                .move_to(grid[i][j].get_center())
                .scale(0.3)
            )
            self.play(Write(dot_product), run_time=0.07)
            dot_product_group_letters.add(dot_product)
        self.wait(2)

        self.play(FadeOut(dot_product_group_letters))
        self.wait()

        # Replace the dot-products with some random values
        dot_product_group_numbers = VGroup()
        numpy_random = (
            np.random.rand(7, 7) * 10 - 5
        )  # Uniform random numbers between -5 and 5
        for i, j in it.product(range(1, 8), range(1, 8)):
            dot_product = (
                (MathTex("{}".format(np.round(numpy_random[i - 1][j - 1], 2))))
                .move_to(grid[i][j].get_center())
                .scale(0.4)
            )
            self.play(
                Write(dot_product),
                run_time=0.025,
            )
            dot_product_group_numbers.add(dot_product)
        self.wait(2)

        # Apply softmax at each column
        text_softmax = Text("Apply softmax at\n each column").scale(0.5).to_edge(RIGHT)
        self.play(ReplacementTransform(text_dot_product, text_softmax))
        self.wait()

        self.play(FadeOut(dot_product_group_numbers))
        self.wait()

        numpy_random_softmax = np.exp(numpy_random) / np.sum(
            np.exp(numpy_random), axis=0
        )
        dot_product_group_softmax = VGroup()
        for i, j in it.product(range(1, 8), range(1, 8)):
            dot_product = (
                (MathTex("{}".format(np.round(numpy_random_softmax[i - 1][j - 1], 2))))
                .move_to(grid[i][j].get_center())
                .scale(0.4)
            )
            self.play(
                Write(dot_product),
                run_time=0.025,
            )
            dot_product_group_softmax.add(dot_product)
        self.wait()

        # Create the values
        values = self.ApplyParameters(key_label_embedding, RIGHT, "V", arrow_length=1.0)

        for idx, value in enumerate(values[1::3]):
            value.next_to(keys[0::3][idx], DOWN, buff=0.1)
        for idx, value in enumerate(values[2::3]):
            value.next_to(keys[0::3][idx], RIGHT, buff=0.1)

        self.play(
            ReplacementTransform(keys[1::3], values[1::3]),
            ReplacementTransform(keys[2::3], values[2::3]),
            run_time=2,
        )
        self.wait()

        # Makes a single columns examples with the values
        text_values = Text("Apply the values").scale(0.5).to_edge(RIGHT)
        self.play(ReplacementTransform(text_softmax, text_values))
        self.wait()

        softmax_column_1 = VGroup()
        softmax_column_helper = VGroup()
        j = 1
        for i in range(1, 8):
            dot_product = (
                (MathTex("{}".format(np.round(numpy_random_softmax[i - 1][j - 1], 2))))
                .scale(0.3)
                .next_to(grid[i][j].get_left(), RIGHT, buff=0.05)
            )
            softmax_column_1.add(dot_product)
            softmax_column_helper.add(dot_product)

            if i > 0 and i < 7:
                plus_symbol = (
                    MathTex("\\textbf{+}")
                    .scale(0.3)
                    .move_to(grid[i][j].get_bottom())
                    .set_color(RED)
                )
                softmax_column_1.add(plus_symbol)

            elif i == 7:
                result = (
                    MathTex(f"\\vec{{ \\textbf{{A}} }}_{j}")
                    .scale(0.3)
                    .next_to(grid[i][j].get_bottom(), DOWN, buff=0.1)
                    .set_color(RED)
                )
                softmax_column_1.add(result)

        self.play(
            ReplacementTransform(dot_product_group_softmax, softmax_column_1),
            run_time=1.5,
        )
        self.wait()

        values_grid = values.copy()
        values_grid = values_grid[2::3]
        for idx, value in enumerate(values_grid):
            value.scale(0.9).next_to(
                softmax_column_helper[idx], RIGHT, buff=0.02
            ).set_color(RED)
            self.play(Write(value), run_time=0.2)
        self.wait()

        # makes the others grid multiplication
        for j in range(2, 8):
            softmax_column = VGroup()
            softmax_column_helper = VGroup()
            for i in range(1, 8):
                dot_product = (
                    (
                        MathTex(
                            "{}".format(np.round(numpy_random_softmax[i - 1][j - 1], 2))
                        )
                    )
                    .scale(0.3)
                    .next_to(grid[i][j].get_left(), RIGHT, buff=0.05)
                )
                softmax_column.add(dot_product)
                softmax_column_helper.add(dot_product)

                if i > 0 and i < 7:
                    plus_symbol = (
                        MathTex("\\textbf{+}")
                        .scale(0.3)
                        .move_to(grid[i][j].get_bottom())
                        .set_color(RED)
                    )
                    softmax_column_1.add(plus_symbol)

                elif i == 7:
                    result = (
                        MathTex(f"\\vec{{ \\textbf{{A}} }}_{j}")
                        .scale(0.3)
                        .next_to(grid[i][j].get_bottom(), DOWN, buff=0.1)
                        .set_color(RED)
                    )
                    softmax_column.add(result)

            self.play(
                FadeIn(softmax_column),
                run_time=1.5,
            )
            self.wait(0.1)

            values_grid = values.copy()
            values_grid = values_grid[2::3]
            for idx, value in enumerate(values_grid):
                value.scale(0.9).next_to(
                    softmax_column_helper[idx], RIGHT, buff=0.02
                ).set_color(RED)
                self.play(Write(value), run_time=0.03)
            self.wait(0.1)

        self.wait(5)

    def NumericEmbedding(self, mobject_list, dir, buff=0.2):
        number_group = VGroup()

        for i, mob in enumerate(mobject_list):
            if np.array_equal(dir, RIGHT):
                if i < len(mobject_list) // 2:
                    number = Text(str(i + 1))
                    number.next_to(mob, dir, buff=buff)
                    number_group.add(number)
            else:
                number = Text(str(i + 1))
                number.next_to(mob, dir, buff=buff)
                number_group.add(number)

        return number_group

    def LetterEmbedding(self, mobject_list, dir, arrow_length=0.5, buff=0.2):
        label_group = VGroup()

        for i, mob in enumerate(mobject_list):
            # Create arrow pointing in direction 'dir'
            if np.array_equal(dir, DOWN):
                start_point = mob.get_bottom() + buff * dir * 0.3
            elif np.array_equal(dir, RIGHT):
                start_point = mob.get_right() + buff * dir * 0.3

            end_point = start_point + arrow_length * dir
            arrow = Arrow(start_point, end_point, buff=0, stroke_width=2)
            label_group.add(arrow)

            # Create and position letter at end of arrow
            letter_mob = MathTex(f"\\vec{{ \\textbf{{E}} }}_{i+1}")
            letter_mob.next_to(arrow, dir, buff=buff * 0.5)
            label_group.add(letter_mob)

        return label_group

    def ApplyParameters(self, mobject_list, dir, letter, arrow_length=0.5, buff=0.2):
        label_group = VGroup()

        for i, mob in enumerate(mobject_list):
            if i % 2 == 1:  # I want to do it only for E and not for the arrows
                # Create arrow pointing in direction 'dir'
                if np.array_equal(dir, DOWN):
                    start_point = mob.get_bottom() + buff * dir * 0.3
                elif np.array_equal(dir, RIGHT):
                    start_point = mob.get_right() + buff * dir * 0.3
                end_point = start_point + arrow_length * dir
                arrow = Arrow(start_point, end_point, buff=0, stroke_width=2)
                if letter == "V":
                    arrow.scale(0.4)
                label_group.add(arrow)

                # label right to the arrow
                label = MathTex(f"W_{{{letter}}}")
                if letter == "V":
                    label.scale(0.4)
                if np.array_equal(dir, DOWN):
                    label.next_to(arrow, RIGHT)
                elif np.array_equal(dir, RIGHT):
                    label.next_to(arrow, DOWN)
                label_group.add(label)

                # Create and position letter at end of arrow
                letter_mob = MathTex(f"\\vec{{ \\textbf{{{letter}}} }}_{(i+1)//2}")
                if letter == "V":
                    letter_mob.scale(0.4)
                letter_mob.next_to(arrow, dir, buff=buff * 0.5)
                label_group.add(letter_mob)

        return label_group

    def CreateGrid(self, rows, cols, buff=0.0):
        grid = VGroup()
        for i in range(rows):
            row = VGroup()
            for j in range(cols):
                rect = Rectangle(width=1.0, height=1.0)
                rect.set_stroke(WHITE, 2)
                rect.move_to([j, i, 0])
                row.add(rect)
            row.arrange(RIGHT, buff=buff)
            grid.add(row)
        grid.arrange(DOWN, buff=buff)

        return grid
