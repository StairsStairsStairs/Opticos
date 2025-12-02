from manim import *
import numpy as np

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


from manim import *

class DefinitionOfADerivative(Scene):
    
    def construct(self):
        ax = Axes(
            x_range=[-10, 10, 5],
            y_range=[-10, 10, 5],
            tips=False,
            axis_config={"include_numbers": True},
        )
        """
        def f(x):
            return np.sign(x) * abs(x) ** 3 + x * 3 + 2
        """

        def f(x):
            return  x ** 2 + x * 3 + 2

        def g(x):
            return 2 * x + 3

        polynomial = ax.plot(f, x_range=[-10, 10, 5], color=BLUE, use_smoothing=True)
        linear = ax.plot(g, x_range=[-10, 10, 5], color=RED, use_smoothing=False)
        
        poly_label = ax.get_graph_label(polynomial, label='f(x) = x^2 + x * 3 + 2')
        poly_label.shift(DOWN * 2)
        linear_label = ax.get_graph_label(linear, label='g(x) = 2 * x + 3')
        linear_label2 = ax.get_graph_label(linear, label='(Derivative)')
        linear_label.shift(DOWN * 4)
        linear_label2.shift(DOWN * 5)

        #self.add(ax, graph_f, graph_g, label_f, label_g)
        #self.wait(1)

        self.add(ax)
        self.wait(1)
        self.play(Create(polynomial, run_time=5))
        self.play(FadeIn(poly_label))

        h = 0.0001
        x_point = 1  
        #derivative_value = self.derivative_calc(f, x_point, h)

        #derivative_text = Text(f"f'(x) at x = {x_point} is approximately {derivative_value:.2f}")
        #derivative_text.to_edge(DOWN)
        #self.play(Write(derivative_text))
        #self.wait(2)

        tangent_line = self.plot_tangent_line(ax, f, x_point)
        tangent_label = ax.get_graph_label(tangent_line, label='Tangent Line at x = 1')
        tangent_label.shift(DOWN * 3)



        self.play(Create(tangent_line, run_time=4))
        self.play(FadeIn(tangent_label))

        self.wait(2)


        self.play(
            Create(linear, run_time=5),
            FadeIn(linear_label),
            FadeIn(linear_label2)
            )
    
    def derivative_calc(self, func, x, h):
        """Calculates the numerical derivative using the difference quotient"""
        return (func(x + h) - func(x)) / h
    
    def plot_tangent_line(self, ax, func, x_point):
        """Returns a Line object representing the tangent at x_point"""
        tangent_slope = self.derivative_calc(func, x_point, 0.0001)
        tangent_intercept = func(x_point) - tangent_slope * x_point
        tangent_line = ax.plot(lambda x: tangent_slope * x + tangent_intercept, x_range=[-10, 10, 0.1], color=YELLOW)
        return tangent_line


if __name__=="__main__":
    main()


def main():
    DefinitionOfADerivitive.derivative_calc(2, 3, 4)


