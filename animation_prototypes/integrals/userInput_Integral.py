from manim import *

integral_xRange = [-5, 5]
integral_box_color_outline = rgb_to_color((0.0, 0.0, 0.0))
integral_box_color_fill = (rgb_to_color((0.0, 0.0, 1.0)), rgb_to_color((0.0, 1.0, 0.0)), rgb_to_color((1.0, 0.0, 0.0)))

function_color = rgb_to_color((0.2, 0.6, 0.8))
def continuous_function(x):
    return x**3 + 2