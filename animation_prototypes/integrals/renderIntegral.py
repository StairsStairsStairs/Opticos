import math
from manim import *
import userInput_Integral as userInfo
from scipy.optimize import minimize_scalar
# wsl
# source manim-env/bin/activate
# manim ./animation_prototypes/integrals/renderIntegral.py

class hello(Scene):
    def createIntegralBoxXValues(self, numValues):
        totalRange = userInfo.integral_xRange[1] - userInfo.integral_xRange[0]
        toReturn = [userInfo.integral_xRange[0]]
        for i in range(numValues):
            toReturn.append(toReturn[-1]+(totalRange/numValues))
        return toReturn
    
    def createIntegralBox(self, x_lower, x_upper, function, ax, aproxWithLower=True):
        if aproxWithLower:
            rect = Polygon(
                ax.c2p(x_lower,0),
                ax.c2p(x_lower,function(x_lower)),
                ax.c2p(x_upper,function(x_lower)),
                ax.c2p(x_upper,0),
                color=userInfo.integral_box_color_outline,
                fill_color=userInfo.integral_box_color_fill,
                fill_opacity=1.0
            )
        else:
            rect = Polygon(
                ax.c2p(x_lower,0),
                ax.c2p(x_lower,function(x_upper)),
                ax.c2p(x_upper,function(x_upper)),
                ax.c2p(x_upper,0),
                color=userInfo.integral_box_color_outline,
                fill_color=userInfo.integral_box_color_fill,
                fill_opacity=1.0
            )
        return rect

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
        parabola.set_z_index(2)

        # Labels
        # equation_label = MathTex("y = x^2").to_edge(UP)
        
        # Animate
        self.play(Create(ax))
        self.play(Create(parabola))

        # Make All boxes
        xVals = createIntegralBoxXValues(10)
        for i in range(7):
            # offset = i * new_x_range[2]
            # rect = self.createIntegralBox(userInfo.integral_xRange[0] + offset, userInfo.integral_xRange[0] + offset + new_x_range[2], func, ax)
            rect = self.createIntegralBox(xVals[i], xVals[i+1], func, ax)
            self.play(Create(rect))
            self.wait(0.5)

        # self.play(Create(rect))
        self.wait(1)