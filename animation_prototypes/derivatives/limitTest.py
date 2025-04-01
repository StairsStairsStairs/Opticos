from manim import *

class FunctionExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1, 5],
            y_range=[-5, 5],
            axis_config={"include_tip": False},
        )

        # Define function and plot
        f = lambda x: (x-1)*(x-4)
        func = axes.plot(f, color=BLUE)

        # Get y-value at a specific x
        x_value = 2
        y_value = f(x_value)
        dot = Dot(axes.c2p(x_value, y_value), color=RED)  # Convert coordinates to scene coordinates

        self.add(axes, func, dot)
        self.wait()