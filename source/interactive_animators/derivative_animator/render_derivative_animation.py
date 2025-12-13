from manim import *
import numpy as np
import argparse
import os

class LogScalingExample(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 6, 1],
            tips=False,
            axis_config={"include_numbers": True},
            y_axis_config={"scaling": LogBase(custom_labels=True)},
        )

        # x_min must be > 0 because log is undefined at 0.
        graph = ax.plot(lambda x: x ** 2, x_range=[0.001, 10], use_smoothing=False)
        self.add(ax, graph)


class NegitiveTest(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-10, 10, 1],
            y_range=[-1000, 1000, 100],
            tips=False,
            axis_config={"include_numbers": True},
        )

        # x_min must be > 0 because log is undefined at 0.
        graph = ax.plot(lambda x: (-1 * x) ** 3, x_range=[-10, 10], use_smoothing=False)
        self.add(ax, graph)


class DefinitionOfADerivative(Scene):
    def construct(self):
        # Parse args only when manim executes this file
        a = float(os.environ.get("POLY_A", "2"))
        b = float(os.environ.get("POLY_B", "3"))
        c = float(os.environ.get("POLY_C", "2"))

        f = self.create_polynomial( a, b, c)
        label = f"f(x) = {a}x^2 + {b}x + {c}"

        ax = Axes(
            x_range=[-10, 10, 1],
            y_range=[-10, 10, 1],
            tips=False,
            axis_config={"include_numbers": True},
        )
        poly = ax.plot(f, x_range=[-10, 10, 0.1], color=BLUE)
        poly_label = ax.get_graph_label(poly, label=label)

        self.add(ax)
        self.play(Create(poly, run_time=3))
        self.play(FadeIn(poly_label))

        slope = (f(1 + 1e-4) - f(1)) / 1e-4
        intercept = f(1) - slope * 1
        tangent = ax.plot(lambda x: slope*x + intercept, x_range=[-10, 10, 0.1], color=YELLOW)
        t_label = ax.get_graph_label(tangent, label="Tangent at x=1").shift(DOWN*2)

        self.play(Create(tangent, run_time=3))
        self.play(FadeIn(t_label))
        self.wait(1)

    def derivative_calc(self, func, x, h=1e-4):
        return (func(x + h) - func(x)) / h

    def plot_tangent_line(self, ax, func, x_point):
        slope = self.derivative_calc(func, x_point)
        intercept = func(x_point) - slope * x_point
        return ax.plot(lambda x: slope*x + intercept, x_range=[-10, 10, 0.1], color=YELLOW)
    
    def create_polynomial(self, a:float, b:float, c:float):
        def r(x):
            return a * x**2 + b * x + c
        return r


class FallingLadder(Scene):
    def construct(self):
        self.L = 5

        self.plane = NumberPlane(
            x_range=[0, 6],
            y_range=[0, 6],
            axis_config={"include_numbers": True}
        ).scale(0.9)

        labels = self.plane.get_axis_labels("x", "y")
        self.add(self.plane, labels)

        self.bottom = Dot(self.plane.c2p(1, 0), color=BLUE)
        y0 = np.sqrt(self.L**2 - 1**2)
        self.top = Dot(self.plane.c2p(0, y0), color=RED)
        self.ladder = Line(self.bottom.get_center(), self.top.get_center(), color=YELLOW)
        self.add(self.bottom, self.top, self.ladder)

        self.ladder.add_updater(lambda mob: mob.become(
            Line(self.bottom.get_center(), self.top.get_center(), color=YELLOW)
        ))

        self.top.add_updater(self.update_top)

        ladder_label = always_redraw(self.make_ladder_label)
        self.add(ladder_label)

        rate_label = Text("Falling down at 1/2 ft per second", font_size=24, color=WHITE)
        rate_label.next_to(self.plane, DOWN)
        rate_label.shift(UP * 0.3)
        self.add(rate_label)

        self.fall_ladder(speed=0.5)

        self.wait(2)

    def update_top(self, mob):
        x = self.plane.p2c(self.bottom.get_center())[0]
        y = np.sqrt(max(self.L**2 - x**2, 0))
        mob.move_to(self.plane.c2p(0, y))

    def make_ladder_label(self):
        vec = self.ladder.get_end() - self.ladder.get_start()
        angle = np.arctan2(vec[1], vec[0])

        if angle > np.pi / 2:
            angle -= np.pi
        elif angle < -np.pi / 2:
            angle += np.pi

        perp = np.array([-vec[1], vec[0], 0])
        norm = np.linalg.norm(perp)
        perp_unit = perp / norm if norm > 0 else np.array([0, 1, 0])

        label = Text("5 ft ladder", font_size=28, color=WHITE)
        label.move_to(self.ladder.get_center())
        label.rotate(angle, about_point=label.get_center())
        label.shift(perp_unit * -0.25)  # offset above line
        return label

    def fall_ladder(self, speed: float):
        start_x = self.plane.p2c(self.bottom.get_center())[0]
        end_x = 4
        distance = end_x - start_x
        run_time = distance / speed
        self.play(self.bottom.animate.move_to(self.plane.c2p(end_x, 0)), run_time=run_time)


class MotionProblem(Scene):
    def s(self, t):
        return t**3 - 3*t**2 - 8*t + 3

    def v(self, t):
        return 3*t**2 - 6*t - 8

    def a(self, t):
        return 6*t - 6

    def construct(self):
        ax = Axes(
            x_range=[-10, 10, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_numbers": False, "stroke_color": GREY, "stroke_opacity": 0.3},
            tips=False
        )
        self.add(ax)

        ball = Dot(ax.c2p(self.s(0), 0), color=BLUE).scale(3.0)
        self.add(ball)

        def ball_path(t):
            return ax.c2p(self.s(t), 0)

        self.play(MoveAlongPath(ball, ParametricFunction(lambda t: ball_path(t), t_range=[0, 4])), run_time=6)

        t_mid = 2
        ball.move_to(ax.c2p(self.s(t_mid), 0))

        vel_value = self.v(t_mid)
        vel_arrow = Arrow(
            start=ball.get_center() + np.array([0.5, 0, 0]),  
            end=ball.get_center() + np.array([vel_value*0.5, 0, 0]),  
            buff=0,
            color=GREEN,
            stroke_width=10
        )
        vel_label = Text("Velocity", font_size=36, color=GREEN).next_to(vel_arrow, UP)

        acc_value = self.a(t_mid)
        acc_arrow = Arrow(
            start=ball.get_center() - np.array([0.5, 0, 0]), 
            end=ball.get_center() + np.array([acc_value*0.5, 0, 0]),  
            buff=0,
            color=RED,
            stroke_width=10
        )
        acc_label = Text("Acceleration", font_size=36, color=RED).next_to(acc_arrow, DOWN)

        self.play(Create(vel_arrow), Create(acc_arrow), FadeIn(vel_label), FadeIn(acc_label))
        self.wait(3)



if __name__=="__main__":
    main()


def main():
    DefinitionOfADerivitive.derivative_calc(2, 3, 4)


