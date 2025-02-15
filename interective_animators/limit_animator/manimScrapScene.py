from manim import *
class hello(Scene):
    def construct(self):
        coordsRect = Rectangle(width = 5, height = 2, color = BLUE).to_edge(UL).shift([-0.5, 0.5, 0])
        x_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0.3, 0])
        y_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.7, -0.75, 0])
        xText = MathTex(r"x = ").to_edge(UL).shift([-0.3, 0.2, 0])
        functionText = MathTex(r"f(x) = ").to_edge(UL).shift([-0.3, -0.7, 0])
        self.add(coordsRect, x_value, xText, y_value, functionText)