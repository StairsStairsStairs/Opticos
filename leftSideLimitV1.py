from manim import *
class hello(Scene):
    def construct(self):
        
        #self.camera.background_color=GREEN
        xText = Text("x = ").to_edge(UL)
        functionText = Text("f(x) = ").to_edge(UL).shift([0, -1, 0])

        ax = Axes(
            x_range=[-5, 5], y_range=[-15, 5], axis_config={"include_tip": False},
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")

        t = ValueTracker(-4)
        k = ValueTracker(-4)
        j = ValueTracker(-14)

        #x_value = DecimalNumber()
        x_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0, 0]).set_value(k.get_value()))
        y_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.8, -1, 0]).set_value(j.get_value()))
        #y_value = DecimalNumber().to_edge(UL).shift([1.8, -1, 0])
        def func(x):
            return -1 * x**2 + 2
        graph = ax.plot(func, color=MAROON)

        initial_point = [ax.coords_to_point(t.get_value(), func(t.get_value()))]
        dot = Dot(point=initial_point)

        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), func(t.get_value()))))
        x_space = np.linspace(*ax.x_range[:2],200)
        maximum_index = func(x_space).argmax()

        self.add(ax, labels, graph, dot, x_value, xText, y_value, functionText)
        #self.play()
        self.play(t.animate.set_value(x_space[maximum_index]), k.animate.set_value(x_space[maximum_index]), j.animate.set_value(func(x_space[maximum_index])), run_time = 3)
        self.wait(3)