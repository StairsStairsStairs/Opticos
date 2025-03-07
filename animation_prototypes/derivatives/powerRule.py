#code heavily inspired by https://github.com/malhotra5/Manim-Tutorial?tab=readme-ov-file
#at this link, go to the graphing tutorial

from manim import *
import math

class Graphing(Scene):

    def construct(self):
        #Make graph
        axes = Axes(
            x_range = [-5, 5, 1],
            y_range = [-4, 4, 1],
            axis_config={"include_numbers": True}
        )

        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = axes.get_graph_label(graph, label="x^2")
        graph2 = axes.plot(lambda x: 2*x, color=BLUE)
        graph_label_2 = axes.get_graph_label(graph, label="2x")

        #Display graph
        self.play(Create(axes))
        self.wait(1)
        self.play(Create(graph))
        self.add(graph_label)
        self.wait(1)
        self.play(Transform(graph, graph2), Transform(graph_label, graph_label_2))
        self.wait(1)