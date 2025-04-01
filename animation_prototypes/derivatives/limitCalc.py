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

        f = lambda x: (x-1)*(x-2)*(x-3)
        func = axes.plot(f, color = BLUE)
       

        x = ValueTracker(1)
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

        #dot1 = always_redraw(
         #   lambda: Dot().move_to(
          #  axes.c2p(x.get_value(), func.function(x.get_value()))
        #)

        dot1 = always_redraw(
            lambda: Dot().move_to(
                #axes.c2p(0,0)
                #print(type(func(x.get_value())))
                axes.c2p(x.get_value(), f(x.get_value()))
                
                
            )
        )

        dot2 = always_redraw(
            lambda: Dot().move_to(
                #axes.c2p(0,0)
                axes.c2p(x.get_value() + dx.get_value(), f(x.get_value() + dx.get_value()))
                #axes.c2p(x.get_value() + dx.get_value()), func.function(x.get_value() + dx.get_value())
            )
        )

        print(type(x.get_value()), x.get_value())
        print(type(func.function(x.get_value())), func.function(x.get_value()))
        self.add(axes, axes_labels, func)
        self.play(Create(VGroup(dot1, dot2, secant)))
        self.play(dx.animate.set_value(0.0001), run_time = 2)
        self.wait()
        self.play(x.animate.set_value(1), run_time = 3)
        self.wait(2)