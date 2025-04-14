from manim import *
import math
import sys

class limitAnimation(Scene):
    def construct(self):
        axes = Axes(
            x_range = [0, 6, 1],
            y_range = [0, 12, 2],
            axis_config={"include_numbers": True, "include_tip": False}
        )

        f = lambda x: x*x
        func = axes.plot(f, color = BLUE)
       

        x = ValueTracker(2)
        dx = ValueTracker(1)

        axes_labels = axes.get_axis_labels(x_label = "x", y_label = "y")

        def update_label(mob):
            mob.become(MathTex("slope = "+(str(calculate_slope(dot1, dot2, axes))))).to_corner(UP+RIGHT)

        def update_upperLabel(mob):
            mob.become(MathTex("f(x+h)").next_to(upperLine, UP))

        def calculate_slope(dot, end_dot, axis):
            x1, y1 = axes.point_to_coords(end_dot.get_center())[:2] #extract the first two elements
            x2, y2 = axes.point_to_coords(dot.get_center())[:2] #extract the first two elements
            
            slope = (y2 - y1)/(x2 - x1)
            return round(slope, 3)
            #return (dot.get_center()[1] - end_dot.get_center()[1])/(dot.get_center()[0] - end_dot.get_

        #BEGIN IMPORTANT SECTION
        secant = always_redraw(
            lambda: axes.get_secant_slope_group(
                x = x.get_value(),
                graph = func,
                dx = dx.get_value(),
                dx_line_color = RED,
                dy_line_color = BLUE,
                dx_label = MathTex("h").scale(2),
                dy_label = MathTex("f(x+h) - f(x)").scale(2),#MathTex("f(x+h) - f(x)").scale(2),
                secant_line_color = WHITE,
                secant_line_length = 8,
            )
        )
        #END IMPORTANT SECTION

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


        
        
        upperLine = always_redraw(
            lambda: DashedLine(axes.c2p(0, f(x.get_value() + dx.get_value())), axes.c2p(x.get_value() + dx.get_value(), f(x.get_value() + dx.get_value())), dash_length=0.25, color = YELLOW)
        )
        upperLineLabel = always_redraw(lambda: MathTex("f(x+h)").scale(0.8).next_to(upperLine, UP))
        upperLineCombined = VGroup(upperLine, upperLineLabel)

        lowerLine = always_redraw(
            lambda: DashedLine(axes.c2p(0, f(x.get_value())), axes.c2p(x.get_value(), f(x.get_value())), dash_length=0.25, color = YELLOW)
        )
        lowerLineLabel = MathTex("f(x)").scale(0.8).next_to(lowerLine, DOWN)

        #deltaLine = always_redraw(
         #   lambda: DashedLine(axes.c2p(x.get_value(), f(x.get_value())), axes.c2p(x.get_value() + dx.get_value(), f(x.get_value() + dx.get_value())), dash_length=0.25, color = GREEN)
        #)
        #deltaLineLabel = MathTex("f(x+h) - f(x)").next_to(deltaLine, LEFT)
        




        label = MathTex("slope = "+(str(calculate_slope(dot1, dot2, axes))))
        label.add_updater(update_label)
        label.to_corner(UP + RIGHT)
        label.add_updater(update_upperLabel)
        #self.add(label)
        print(type(x.get_value()), x.get_value())
        print(type(func.function(x.get_value())), func.function(x.get_value()))
        self.add(axes, axes_labels, func)
        self.play(Create(VGroup(dot1, dot2, secant)))
        self.play(Create(upperLine), Write(upperLineLabel))
        #self.add(upperLineCombined)
        self.play(Create(lowerLine), Write(lowerLineLabel))
        #self.play(Create(deltaLine), Write(deltaLineLabel))
        self.wait(1)
        self.play(dx.animate.set_value(0.0001), run_time = 2)
        #self.wait()
        #self.play(x.animate.set_value(1), run_time = 3)
        