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
        #labels = ax.get_axis_labels(x_label="x", y_label="f(x)") # Labels each axis

        # Labels precisely at the axis tips
        x_label = MathTex("x").to_edge(RIGHT).shift([0, 0.5, 0])
        y_label = MathTex("f(x)").to_edge(UP).shift([4, 0, 0])

        #Draw graph that plot out function defined by func()
        graph = ax.plot(lambda x: func(x), color = GREEN, discontinuities=[1])

        graph_group = VGroup(ax, graph)
        
        graph_group.to_edge(RIGHT)

        #075912
        rect = Rectangle(width=6, height=config.frame_height, color="#0a0a4a", fill_color = "#0a0a4a", fill_opacity = 1).to_edge(LEFT).shift([-0.5, 0, 0])
        limitTextLeft = MathTex(r"\lim \limits_{x \to 0^-} f(x) = 2").to_edge(UL).shift([0, -2.75, 0])
        self.add(ax, x_label, y_label, rect, limitTextLeft)
        self.wait(2)