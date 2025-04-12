from manim import *

background_color = rgb_to_color((0.16, 0.16, 0.16))

integral_xRange = [-2, 2]
integral_box_color_outline = rgb_to_color((0.0, 0.0, 0.0))
integral_box_color_fill = rgb_to_color((0.6, 0.4, 0.6))

sum_of_integral_boxes_outline_positive = rgb_to_color((0.0, 0.0, 0.0))
sum_of_integral_boxes_fill_positive = rgb_to_color((0.0, 0.6, 0.6))
sum_of_integral_boxes_outline_negative = rgb_to_color((0.0, 0.0, 0.0))
sum_of_integral_boxes_fill_negative = rgb_to_color((0.6, 0.4, 0.0))

box_of_area_under_curve_outline = rgb_to_color((6.0, 6.0, 0.0))
box_of_area_under_curve_fill = rgb_to_color((0.6, 0.6, 0.0))

function_color = rgb_to_color((0.2, 0.6, 0.8))
def continuous_function(x):
    return x**5-x