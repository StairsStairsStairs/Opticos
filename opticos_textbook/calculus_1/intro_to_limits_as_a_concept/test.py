import sys
import math
from manim import *
del sys.modules["manim"]
del sys.modules["math"]
class DiscontinuousGraph(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1], 
            y_range=[-2, 4, 1], 
            axis_config={"include_numbers": True}
        )
        val = math.cos(2)
        # Define the function f(x) = (x^2 - 1) / (x - 1)
        def func(x):
            if x == 2:
                return 0
            return (x**2 - 1) / (x - 1)
        
        # Plot graph for x < 1
        left_graph = axes.plot(func, x_range=[-2.9, 0.96], color=BLUE)

        # Plot graph for x > 1
        right_graph = axes.plot(func, x_range=[1.04, 2.9], color=BLUE)

        # Create a circular hole at (1,2)
        hole = Circle(radius=0.08, color=BLUE, fill_opacity=0, stroke_width=3)
        hole.move_to(axes.c2p(1, 2)) 

        # Labels
        graph_label = MathTex("f(x) = \\frac{x^2 - 1}{x - 1}").to_edge(UP)
        
        # Add elements to scene
        self.play(Create(axes))
        self.play(Create(left_graph), Create(right_graph))
        self.play(FadeIn(hole))  # Show hole
        self.play(Write(graph_label))
        self.wait(2)