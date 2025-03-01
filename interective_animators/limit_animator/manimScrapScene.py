from manim import *
class hello(Scene):
    def construct(self):
        def func(x):
            return x ** 2
        
        boundScale = 30
        ax = Axes(
            x_range=[-1*boundScale, boundScale, int(boundScale/5)], y_range=[-1*boundScale, boundScale, int(boundScale/5)], axis_config={"include_tip": True},
            x_length = 7,
            y_length = 7,
            x_axis_config={"numbers_to_include": range(-1*boundScale, boundScale, int(boundScale/5))},  # Auto number x-axis
            y_axis_config={"numbers_to_include": range(-1*boundScale, boundScale, int(boundScale/5))},  # Auto number y-axis
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)") # Labels each axis

        #Draw graph that plot out function defined by func()
        graph = ax.plot(lambda x: func(x), color = GREEN, discontinuities=[1])

        graph_group = VGroup(ax, graph)
        
        graph_group.to_edge(RIGHT)
        self.add(ax)
        self.wait(2)