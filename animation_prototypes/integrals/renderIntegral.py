import math
from manim import *
import userInput_Integral as userInfo
from scipy.optimize import minimize_scalar
# wsl
# source manim-env/bin/activate
# manim ./animation_prototypes/integrals/renderIntegral.py

class hello(Scene):
    def construct(self):
        func = userInfo.continuous_function
        self.camera.background_color = ORANGE

        # Get Axis Ranges
        new_x_range = [userInfo.integral_xRange[0] - 1, userInfo.integral_xRange[1] + 1, 0]
        new_x_range[2] = math.ceil((new_x_range[1] - new_x_range[0]) / 10)

        min_res = minimize_scalar(func, bounds=(userInfo.integral_xRange[0], userInfo.integral_xRange[1]), method='bounded')
        max_res = minimize_scalar(lambda x: -func(x), bounds=(userInfo.integral_xRange[0], userInfo.integral_xRange[1]), method='bounded')

        custom_y_range = [func(min_res.x)-1, func(max_res.x)+1, 0]
        custom_y_range[2] = math.ceil((custom_y_range[1] - custom_y_range[0]) / 10)

        # Create Axes and Graph
        ax = Axes(
            x_range=new_x_range,
            y_range=custom_y_range,
            x_length=10,
            y_length=7.4,
            axis_config={"include_numbers": True, "include_tip": False},
        ).move_to((-1.75,0,0))
        parabola = ax.plot(lambda x: func(x), new_x_range[0:2], color=BLUE)

        # Make first box for integral (one x-step)
        dot = Dot().move_to(ax.coords_to_point(0, func(0)))
        rect = Polygon(
            ax.c2p(0,0),
            ax.c2p(0,func(0)),
            ax.c2p(new_x_range[2],func(0)),
            ax.c2p(new_x_range[2],0),
            color=RED
        )

        # Labels
        # equation_label = MathTex("y = x^2").to_edge(UP)
        
        # Animate
        self.play(Create(ax))
        self.play(Create(parabola))

        self.play(Create(dot))
        self.play(Create(rect))
        self.wait(1)