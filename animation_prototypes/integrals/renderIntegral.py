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
            self.var_sum += userInfo.continuous_function(x_lower) * abs(x_upper - x_lower)
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
            self.var_sum += userInfo.continuous_function(x_upper) * (x_upper - x_lower)
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
        self.var_sum = 0
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

    def copyAllBoxes(self, boxes):
        newBoxes = []
        for box in boxes:
            newBoxes.append(box.copy())
            # turn boxes blue
            newBoxes[-1].set_color(userInfo.sum_of_integral_boxes_outline)
            newBoxes[-1].set_fill(userInfo.sum_of_integral_boxes_fill, opacity=0)
            newBoxes[-1].set_z_index(1)
        return newBoxes

    def construct(self):
        self.var_sum = 0
        self.camera.background_color = ORANGE
        func = userInfo.continuous_function

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

        # Show Box of Area sum
        Area_box = Square(side_length=3, color=userInfo.box_of_area_under_curve_outline, fill_color=userInfo.box_of_area_under_curve_fill, fill_opacity=1.0)
        Area_box.move_to(RIGHT * 5.25)
        Area_box.set_z_index(2)
        #   Add text to box
        Area_text = MathTex(r"\text{Area}").scale(1.5).move_to(Area_box.get_center())
        Area_text.shift(UP * 1)
        Area_text.set_z_index(2)

        # Area_number = DecimalNumber(self.var_sum, num_decimal_places=4)
        # Area_MathTex = MathTex("0")
        # Area_MathTex[0].become(Area_number)
        # Area_MathTex.move_to(Area_box.get_center()).shift(DOWN * 0.25)
        # Area_MathTex.set_z_index(2)
        equation = MathTex("x =")
        number = DecimalNumber(0, num_decimal_places=0)
        number.next_to(equation, RIGHT)
        equation_group = VGroup(equation, number)
        equation_group.move_to(Area_box.get_center()).shift(DOWN * 0.25)
        equation_group.set_z_index(2)
        
        # Animate
        self.play(Create(ax), Create(Area_box))
        self.play(Create(parabola), Create(Area_text), Create(equation_group))

        numBoxes = 5
        currentBoxes = []
        for i in range(2):
            numBoxes *= 2
            newBoxesToAdd = self.getSetOfNewBoxes(ax, numBoxes)
            currentBoxes = self.animateAllBoxes(ax, currentBoxes, newBoxesToAdd)
            self.wait(1)

            CopiedToShowArea = self.copyAllBoxes(currentBoxes)
            self.add(*[box for box in CopiedToShowArea])
            self.play(*[box.animate.set_opacity(1) for box in CopiedToShowArea], run_time=0.3)
            self.play(*[Transform(box, Area_box) for box in CopiedToShowArea], run_time=0.50)
            print(self.var_sum)
            self.play(number.animate.set_value(self.var_sum), run_time=0.50)
            number.set_z_index(2)
            self.remove(*[box for box in CopiedToShowArea])

        self.wait(1)