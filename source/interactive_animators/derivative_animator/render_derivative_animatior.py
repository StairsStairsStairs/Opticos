from manim import *

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
        
        def f(x):
            return x ** 3 * 3 + 2  

        def g(x):
            return x * 3 + 3  

        graph_f = ax.plot(f, x_range=[-10, 10, 0.1], color=BLUE)
        graph_g = ax.plot(g, x_range=[-10, 10, 0.1], color=RED)
        
        label_f = ax.get_graph_label(graph_f, label='f(x) = x^3 * 3 + 2')
        label_g = ax.get_graph_label(graph_g, label='g(x) = 3x + 3')
        label_g.shift(DOWN * 4)

        self.add(ax, graph_f, graph_g, label_f, label_g)
        self.wait(1)

        h = 0.0001
        x_point = 1  
        derivative_value = self.derivative_calc(f, x_point, h)

        derivative_text = Text(f"f'(x) at x = {x_point} is approximately {derivative_value:.2f}")
        derivative_text.to_edge(DOWN)
        self.play(Write(derivative_text))
        self.wait(2)

        tangent_line = self.plot_tangent_line(ax, f, x_point)
        self.add(tangent_line)

        self.wait(2)
    
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


