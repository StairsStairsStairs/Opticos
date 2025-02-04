from manim import *
class hello(Scene):
    def construct(self):
        def func(x):
            return -1 * x**2 + 2
        
        #self.camera.background_color=GREEN

        ax = Axes(
            x_range=[-5, 5], y_range=[-15, 5], axis_config={"include_tip": False},
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

        xTracker = ValueTracker(4)

        x_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([0, 0, 0]).set_value(xTracker.get_value()))
        y_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([-0.5, -1, 0]).set_value(func(xTracker.get_value())))
        
        graph = ax.plot(func, color=MAROON, discontinuities=[1])

        initial_point = [ax.coords_to_point(xTracker.get_value(), func(xTracker.get_value()))]
        dot = Dot(point=initial_point)

        dot.add_updater(lambda x: x.move_to(ax.c2p(xTracker.get_value(), func(xTracker.get_value()))))
        x_space = np.linspace(-10, 0, 20)
        maximum_index = func(x_space).argmax()

        xText = MathTex(r"x = ").to_edge(UR).shift([-2, 0, 0])
        functionText = MathTex(r"f(x) = ").to_edge(UR).shift([-2.5, -1, 0])
        limitText = MathTex(r"\lim \limits_{x \to 0^+} f(x) = 2").to_edge(UR).shift([0, -2.75, 0])

        self.add(ax, labels, graph, dot, x_value, xText, y_value, functionText)
        
        self.play(xTracker.animate.set_value(x_space[maximum_index] + 0.05), run_time = 3)

        self.remove(x_value)
        self.remove(y_value)
        x_value = DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([0, 0, 0]).set_value(0.00001)
        y_value = DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([-0.5, -1, 0]).set_value(1.99999)
        self.add(x_value)
        self.add(y_value)

        self.play(FadeIn(limitText))
        
        self.wait(3)
        
        '''
        def func(x):
            return -1 * x**3 / x
        ax = Axes((-3, 3), (-4, 4))
        graph = ax.plot(func, discontinuities=[0], color=BLUE)
        self.add(ax, graph)
        '''