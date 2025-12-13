from manim import *
import numpy as np
import os



# Generates the definition of a deriative of a graph
# Used to plot the deriavtive line too but I got rid of that
class DefinitionOfADerivative(Scene):
    def construct(self):
        # Parse args only when manim executes this file
        a = float(os.environ.get("POLY_A", "2"))
        b = float(os.environ.get("POLY_B", "3"))
        c = float(os.environ.get("POLY_C", "2"))

        # creates the polynomial
        f = self.create_polynomial( a, b, c)
        label = f"f(x) = {a}x^2 + {b}x + {c}"

        # generates the axes
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

        #Generates the tangent line and places it on the graph
        slope = (f(1 + 1e-4) - f(1)) / 1e-4
        intercept = f(1) - slope * 1
        tangent = ax.plot(lambda x: slope*x + intercept, x_range=[-10, 10, 0.1], color=YELLOW)
        t_label = ax.get_graph_label(tangent, label="Tangent at x=1").shift(DOWN*2)

        self.play(Create(tangent, run_time=3))
        self.play(FadeIn(t_label))
        self.wait(1)

    def derivative_calc(self, func, x, h=1e-4):
        return (func(x + h) - func(x)) / h

    #Helper function to generate the tangent line of a polynomal at a certain point
    def plot_tangent_line(self, ax, func, x_point):
        slope = self.derivative_calc(func, x_point)
        intercept = func(x_point) - slope * x_point
        return ax.plot(lambda x: slope*x + intercept, x_range=[-10, 10, 0.1], color=YELLOW)
    
    def create_polynomial(self, a:float, b:float, c:float):
        def r(x):
            return a * x**2 + b * x + c
        return r

# Generates a releated Rates example, most importantly the FallingLadder Problem
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

        # changes the position of the ladder as its falling down
        self.ladder.add_updater(lambda mob: mob.become(
            Line(self.bottom.get_center(), self.top.get_center(), color=YELLOW)
        ))

        self.top.add_updater(self.update_top)

        ladder_label = always_redraw(self.make_ladder_label)
        self.add(ladder_label)

        # Displays the nature of the problem, subject to change
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

    # This puts the label for the ladder, perpendicularly to the ladder,
    # It looks "Nice", still took alot of time to do though
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
        label.shift(perp_unit * -0.25)  
        return label

    # This makes the "Ladder" fall, AKA value of the intersection between it and the X access incerases,
    # while the value between the interesection and the y access decreases
    def fall_ladder(self, speed: float):
        start_x = self.plane.p2c(self.bottom.get_center())[0]
        end_x = 4
        distance = end_x - start_x
        run_time = distance / speed
        self.play(self.bottom.animate.move_to(self.plane.c2p(end_x, 0)), run_time=run_time)

# This is still very buggy and unfinished, the movement of the ball is still slow and clunky, and the arrows
# of the graph are not attached to the ball, rather they are placed randomly

#Generates a unfinished motion problem example, where a point moves across a line
#where there given position is defined by an equation
class MotionProblem(Scene):
    def s(self, t):
        return t**3 - 3*t**2 - 8*t + 3

    def v(self, t):
        return 3*t**2 - 6*t - 8

    def a(self, t):
        return 6*t - 6

    def construct(self):
        ax = Axes(
            x_range=[-50, 50, 10],
            y_range=[-10, 10, 2],
            axis_config={"include_numbers": False, "stroke_color": GREY, "stroke_opacity": 0.3},
            tips=False
        )
        self.add(ax)

        ball = Dot(color=BLUE).scale(3.0)
        self.add(ball)

        # Keeps track of the ball's cordinates in real time and displays them on the graph
        time_tracker = ValueTracker(1)
        ball.add_updater(lambda m: m.move_to(ax.c2p(self.s(time_tracker.get_value()), 0)))
        self.play(time_tracker.animate.set_value(4), run_time=8, rate_func=linear)

        t_mid = time_tracker.get_value()

        # Generates the Velocity arrow
        vel_dir = np.sign(self.v(t_mid)) or 1
        vel_arrow = Arrow(
            start=ball.get_center() + UP*1.5,
            end=ball.get_center() + UP*1.5 + np.array([vel_dir*5, 0, 0]),
            buff=0,
            color=GREEN,
            stroke_width=10
        )
        vel_label = Text("Velocity", font_size=36, color=GREEN).next_to(vel_arrow, UP)

        # Generates the Accleration arrow
        acc_dir = np.sign(self.a(t_mid)) or 1
        acc_arrow = Arrow(
            start=ball.get_center() + DOWN*1.5,
            end=ball.get_center() + DOWN*1.5 + np.array([acc_dir*5, 0, 0]),
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


