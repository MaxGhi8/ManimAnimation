import itertools as it
from typing import Dict

import numpy as np
from manim import *


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

        queries = self.ApplyParameters(label_embedding, DOWN, arrow_length=1.0)
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
        keys = self.ApplyParameters(key_label_embedding, RIGHT, arrow_length=1.0)

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
        cdot = MathTex("\cdot")
        cdot.move_to(grid[0][0].get_center())
        self.play(FadeIn(cdot))
        self.wait()

        queries_grid = queries.copy()
        queries_grid = queries_grid[2::3]
        for idx, query in enumerate(queries_grid):
            query.move_to(grid[0][idx + 1].get_center())
            self.play(Write(query), run_time=0.2)
        self.wait()

        keys_grid = keys.copy()
        keys_grid = keys_grid[2::3]
        for idx, key in enumerate(keys_grid):
            key.move_to(grid[idx + 1][0].get_center())
            self.play(Write(key), run_time=0.2)
        self.wait()

        # Populate the grid with the dot products
        for i, j in it.product(range(1, 8), range(1, 8)):
            dot_product = (
                MathTex(
                    f"\\vec{{ \\textbf{{Q}} }}_{i} \cdot \\vec{{ \\textbf{{K}} }}_{j}"
                )
                .move_to(grid[i][j].get_center())
                .scale(0.5)
            )
            self.play(Write(dot_product), run_time=0.1)
        self.wait()

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

    def ApplyParameters(self, mobject_list, dir, arrow_length=0.5, buff=0.2):
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
                label_group.add(arrow)

                # label right to the arrow
                if np.array_equal(dir, DOWN):
                    label = MathTex("W_{Q}")
                    label.next_to(arrow, RIGHT)
                elif np.array_equal(dir, RIGHT):
                    label = MathTex("W_{K}")
                    label.next_to(arrow, DOWN)

                label_group.add(label)

                # Create and position letter at end of arrow
                if np.array_equal(dir, DOWN):
                    letter_mob = MathTex(f"\\vec{{ \\textbf{{Q}} }}_{(i+1)//2}")
                elif np.array_equal(dir, RIGHT):
                    letter_mob = MathTex(f"\\vec{{ \\textbf{{K}} }}_{(i+1)//2}")
                letter_mob.next_to(arrow, dir, buff=buff * 0.5)
                label_group.add(letter_mob)

        return label_group

    def CreateGrid(self, rows, cols, buff=0.0):
        grid = VGroup()
        for i in range(rows):
            row = VGroup()
            for j in range(cols):
                rect = Rectangle(width=1, height=1)
                rect.move_to([j, i, 0])
                row.add(rect)
            row.arrange(RIGHT, buff=buff)
            grid.add(row)
        grid.arrange(DOWN, buff=buff)

        return grid
