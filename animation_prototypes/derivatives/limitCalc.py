from manim import *
import math
import sys

class limitAnimation(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-4, 4, 1],
            y_range = [-5, 5, 1],
            axis_config={"include_numbers": True, "include_tip": False}
        )

        func = axes.plot(lambda x: x**2 * (x-3))

        x = ValueTracker(3)
        dx = ValueTracker(2)

        axes_labels = axes.get_axis_labels(x_label = "x", y_label = "y")

        secant = always_redraw(
            lambda: axes.get_secant_slope_group(
                x = x.get_value(),
                graph = func,
                dx = dx.get_value(),
                dx_line_color = RED,
                dy_line_color = BLUE,
                dx_label = "dx",
                dy_label = "dy",
                secant_line_color = WHITE,
                secant_line_length = 5,
            )
        )

        dot1 = always_redraw(
            lambda: Dot()
            .move_to(axes.c2p(x.get_value()), func.function(x.get_value()))
        )

        dot2 = always_redraw(
            lambda: Dot()
            .move_to(
                axes.c2p(
                    x.get_value() + dx.get_value(), func.function(x.get_value() + dx.get_value())
                )
            )
        )

        self.add(axes, axes_labels, func)
        self.play(Create(VGroup(dot1, dot2, secant)))
        self.play(dx.animate.set_value(0.0001), run_time = 2)
        self.wait(2)