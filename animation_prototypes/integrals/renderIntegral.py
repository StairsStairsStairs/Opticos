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
    
    def createIntegralBox(self, x_lower, x_upper, ax, aproxWithLower=True):
        if aproxWithLower:
            rect = Polygon(
                ax.c2p(x_lower,0),
                ax.c2p(x_lower,userInfo.continuous_function(x_lower)),
                ax.c2p(x_upper,userInfo.continuous_function(x_lower)),
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

    def getSetOfNewBoxes(self, ax, numBoxesNow, aproxWithLower=True):
        xVals = self.createIntegralBoxXValues(numBoxesNow)
        allRects = []
        for i in range(numBoxesNow):
            rect = self.createIntegralBox(xVals[i], xVals[i+1], ax, aproxWithLower)
            allRects.append(rect)
        return allRects

    def animateAllBoxes(self, ax, allOldBoxes, allNewBoxes):
        if (len(allOldBoxes) != 0 and len(allNewBoxes) != 0):
            indexToStartCreating = min(len(allOldBoxes), len(allNewBoxes))
            while len(allOldBoxes) < len(allNewBoxes):
                newBox = self.createIntegralBox(userInfo.integral_xRange[1],userInfo.integral_xRange[1],ax)
                allOldBoxes.append(newBox)
                self.add(newBox)
            self.play(*[Transform(oldBox, newBox) for oldBox, newBox in zip(allOldBoxes, allNewBoxes)], run_time=0.50)
            return allOldBoxes
        if (len(allOldBoxes) != 0):
            self.play(*[Uncreate(box) for box in allOldBoxes], run_time=0.50)
            return []
        if (len(allNewBoxes) != 0):
            self.play(*[Create(box) for box in allNewBoxes], run_time=0.50)
            return allNewBoxes
        return None

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

        numBoxes = 5
        currentBoxes = []
        for i in range(5):
            numBoxes *= 2
            newBoxesToAdd = self.getSetOfNewBoxes(ax, numBoxes)
            currentBoxes = self.animateAllBoxes(ax, currentBoxes, newBoxesToAdd)
            self.wait(1)

        # self.play(Create(rect))
        self.wait(1)