import math
from manim import *
import userInput_Integral as userInfo
from scipy.optimize import minimize_scalar
from scipy.integrate import quad
# wsl
# source manim-env/bin/activate
# manim ./animation_prototypes/integrals/renderIntegral.py

class hello(Scene):
    def clampYPos(self, value):
        return max(self.min_y, min(value, self.max_y))

    def createIntegralBoxXValues(self, numValues):
        totalRange = userInfo.integral_xRange[1] - userInfo.integral_xRange[0]
        toReturn = [userInfo.integral_xRange[0]]
        for i in range(numValues):
            toReturn.append(toReturn[-1]+(totalRange/numValues))
        return toReturn
    
    def createIntegralBox(self, x_lower, x_upper, ax, aproxWithLower=True):
        if aproxWithLower:
            self.var_sum += userInfo.continuous_function(x_lower) * abs(x_upper - x_lower)
            self.var_sum_pos += max(0, userInfo.continuous_function(x_lower) * abs(x_upper - x_lower))
            self.var_sum_neg += min(0, userInfo.continuous_function(x_lower) * abs(x_upper - x_lower))
            rect = Polygon(
                ax.c2p(x_lower,0),
                ax.c2p(x_lower,self.clampYPos(userInfo.continuous_function(x_lower))),
                ax.c2p(x_upper,self.clampYPos(userInfo.continuous_function(x_lower))),
                ax.c2p(x_upper,0),
                color=userInfo.integral_box_color_outline,
                fill_color=userInfo.integral_box_color_fill,
                fill_opacity=1.0
            )
        else:
            self.var_sum += userInfo.continuous_function(x_upper) * (x_upper - x_lower)
            self.var_sum_pos += max(0, userInfo.continuous_function(x_lower) * abs(x_upper - x_lower))
            self.var_sum_neg += min(0, userInfo.continuous_function(x_lower) * abs(x_upper - x_lower))
            rect = Polygon(
                ax.c2p(x_lower,0),
                ax.c2p(x_lower,self.clampYPos(userInfo.continuous_function(x_upper))),
                ax.c2p(x_upper,self.clampYPos(userInfo.continuous_function(x_upper))),
                ax.c2p(x_upper,0),
                color=userInfo.integral_box_color_outline,
                fill_color=userInfo.integral_box_color_fill,
                fill_opacity=1.0
            )
        return rect

    def getSetOfNewBoxes(self, ax, numBoxesNow, aproxWithLower=True):
        self.var_sum = 0
        self.var_sum_pos = 0
        self.var_sum_neg = 0
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
            newBoxes[-1].set_color(userInfo.sum_of_integral_boxes_outline_positive)
            newBoxes[-1].set_fill(userInfo.sum_of_integral_boxes_fill_positive, opacity=0)
            if (newBoxes[-1].get_center()[1] < 0):
                newBoxes[-1].set_color(userInfo.sum_of_integral_boxes_outline_negative)
                newBoxes[-1].set_fill(userInfo.sum_of_integral_boxes_fill_negative, opacity=0)
            newBoxes[-1].set_z_index(1)
        return newBoxes

    def setPositionOfAreaBoxPositiveAndNegative(self, Area_box, Area_box_positive, Area_box_negative, totalPositive, totalNegative):
        # Normalize ratio
        total = totalPositive + abs(totalNegative)
        ratio_positive = totalPositive / total
        ratio_negative = totalNegative / total
        
        # Resize boxes
        height_positive = 3 * ratio_positive
        height_negative = 3 * ratio_negative
        toReturn = [Rectangle(width=3, height=height_positive, fill_color=userInfo.sum_of_integral_boxes_fill_positive, fill_opacity=1.0).set_stroke(RED, width=0).set_z_index(2),\
                Rectangle(width=3, height=height_negative, fill_color=userInfo.sum_of_integral_boxes_fill_negative, fill_opacity=1.0).set_stroke(RED, width=0).set_z_index(2)]
        
        # Move boxes
        toReturn[0].move_to(RIGHT * 5.25).shift(UP*(1.5-(height_positive/2)))
        toReturn[1].move_to(RIGHT * 5.25).shift(DOWN*(1.5-(height_negative/2)))
        return toReturn

    def construct(self):
        self.var_sum = 0
        self.var_sum_pos = 0
        self.var_sum_neg = 0
        self.camera.background_color = userInfo.background_color
        func = userInfo.continuous_function

        # Get Axis Ranges
        new_x_range = [userInfo.integral_xRange[0] - 1, userInfo.integral_xRange[1] + 1, 0]
        new_x_range[2] = math.ceil((new_x_range[1] - new_x_range[0]) / 10)

        min_res = minimize_scalar(func, bounds=(userInfo.integral_xRange[0], userInfo.integral_xRange[1]), method='bounded')
        max_res = minimize_scalar(lambda x: -func(x), bounds=(userInfo.integral_xRange[0], userInfo.integral_xRange[1]), method='bounded')

        custom_y_range = [func(min_res.x)-1, func(max_res.x)+1, 0]
        custom_y_range[2] = math.ceil((custom_y_range[1] - custom_y_range[0]) / 10)
        self.min_y = custom_y_range[0]*1.1
        self.max_y = custom_y_range[1]*1.1

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
        Area_box = Square(side_length=3, color=userInfo.sum_of_integral_boxes_outline_positive, fill_opacity=0.0).move_to(RIGHT * 5.25).set_z_index(3)
        Area_box_positive = Square(side_length=3, fill_color=userInfo.sum_of_integral_boxes_fill_positive, fill_opacity=1.0).set_stroke(RED, width=0).set_z_index(2)
        Area_box_negative = Square(side_length=3, fill_color=userInfo.sum_of_integral_boxes_fill_negative, fill_opacity=1.0).set_stroke(RED, width=0).set_z_index(2)
        updatedPositions = self.setPositionOfAreaBoxPositiveAndNegative(Area_box, Area_box_positive, Area_box_negative, 1, 0)
        Area_box_positive.become(updatedPositions[0])
        Area_box_negative.become(updatedPositions[1])
        #   Add text to box
        Area_text = MathTex(r"\text{Area}").scale(1.5).move_to(Area_box.get_center())
        Area_text.shift(UP * 1)
        Area_text.set_z_index(2)
        #   Add area amount to box
        number = DecimalNumber(0, num_decimal_places=2)
        number.move_to(Area_box.get_center()).shift(DOWN * 0.25)
        number.set_z_index(2)
        
        # Animate
        self.play(Create(ax), Create(Area_box), Create(Area_box_positive), Create(Area_box_negative))
        self.play(Create(parabola), Create(Area_text), Create(number))

        numBoxes = 5
        currentBoxes = []
        maxIterationsAmt = 4
        result, error = quad(userInfo.continuous_function, userInfo.integral_xRange[0], userInfo.integral_xRange[1])
        for i in range(maxIterationsAmt):
            numBoxes *= 2
            newBoxesToAdd = self.getSetOfNewBoxes(ax, numBoxes)
            currentBoxes = self.animateAllBoxes(ax, currentBoxes, newBoxesToAdd)
            self.wait(1)
            
            CopiedToShowArea = self.copyAllBoxes(currentBoxes)
            updatedPositions = self.setPositionOfAreaBoxPositiveAndNegative(Area_box, Area_box_positive, Area_box_negative, self.var_sum_pos, abs(self.var_sum_neg))
            self.add(*[box for box in CopiedToShowArea])
            self.play(*[box.animate.set_opacity(1) for box in CopiedToShowArea], run_time=0.3)
            self.play(*[Transform(box, Area_box) for box in CopiedToShowArea], Transform(Area_box_positive, updatedPositions[0]), Transform(Area_box_negative, updatedPositions[1]),
                    number.animate.set_value(self.var_sum).move_to(Area_box.get_center()).shift(DOWN * 0.25).set_z_index(2),
                    run_time=0.50)
            self.remove(*[box for box in CopiedToShowArea])

            if (abs(self.var_sum-result) <= 0.15):
                break
        
        # Make whole polygon
        xVals = self.createIntegralBoxXValues(int(numBoxes))
        points = [ ax.c2p(xVals[i],self.clampYPos(userInfo.continuous_function(xVals[i]))) for i in range(len(xVals)) ]
        points.append(ax.c2p(xVals[-1],0))
        points.append(ax.c2p(xVals[0],0))
        
        points_positive = [ ax.c2p(xVals[i],max(0,self.clampYPos(userInfo.continuous_function(xVals[i])))) for i in range(len(xVals)) ]
        points_negative = [ ax.c2p(xVals[i],min(0,self.clampYPos(userInfo.continuous_function(xVals[i])))) for i in range(len(xVals)) ]
        points_positive.append(ax.c2p(xVals[-1],0))
        points_positive.append(ax.c2p(xVals[0],0))
        points_negative.append(ax.c2p(xVals[-1],0))
        points_negative.append(ax.c2p(xVals[0],0))

        PerfectAreaUnderCurve_positive = Polygon(*points_positive)\
            .set_fill(color=userInfo.sum_of_integral_boxes_fill_positive, opacity=1)\
            .set_stroke(color=userInfo.sum_of_integral_boxes_outline_positive, width=2)
        PerfectAreaUnderCurve_negative = Polygon(*points_negative)\
            .set_fill(color=userInfo.sum_of_integral_boxes_fill_negative, opacity=1)\
            .set_stroke(color=userInfo.sum_of_integral_boxes_outline_negative, width=2)
        self.play(FadeIn(PerfectAreaUnderCurve_positive), FadeIn(PerfectAreaUnderCurve_negative), *[FadeOut(box) for box in currentBoxes], run_time=0.50)

        # Animate the area under the curve
        self.wait(1)
        PerfectAreaUnderCurveCopy = Polygon(*points, color=userInfo.box_of_area_under_curve_fill)\
            .set_fill(color=userInfo.box_of_area_under_curve_fill, opacity=1)\
            .set_stroke(color=userInfo.sum_of_integral_boxes_outline_positive, width=2)
        self.play(FadeIn(PerfectAreaUnderCurveCopy), run_time=0.3)
        self.play(Transform(PerfectAreaUnderCurveCopy, Area_box),
                    number.animate.set_value(result).move_to(Area_box.get_center()).shift(DOWN * 0.25).set_z_index(2),
                    run_time=0.50) # Doesn't update colors in Area box for ratio of positive and negative area

        self.wait(1)