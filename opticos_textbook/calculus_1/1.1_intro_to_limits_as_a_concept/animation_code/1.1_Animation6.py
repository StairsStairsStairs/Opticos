from manim import *
class Animation6(Scene):
    def construct(self):

        backgroundColor = BLACK
        functionColor = RED

        def func(x):
            return -1 * x**2 + 2
    
        ax = Axes(
            x_range=[-5, 5], y_range=[-5, 5], axis_config={"include_tip": False},
        )
        ax.add_coordinates()
        labels = ax.get_axis_labels(x_label="x", y_label="g(x)")

        xTrackerLeft = ValueTracker(-4)

        x_value_left = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0, 0]).set_value(xTrackerLeft.get_value()))
        y_value_left = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.8, -1, 0]).set_value(func(xTrackerLeft.get_value())))
        
        graph = ax.plot(func, color = RED, discontinuities=[1])

        hole = Circle(radius=0.08, color=functionColor, fill_color=backgroundColor, fill_opacity=1, stroke_width=3)
        hole.move_to(ax.c2p(0, func(0))) 

        initial_point_left = [ax.coords_to_point(xTrackerLeft.get_value(), func(xTrackerLeft.get_value()))]
        dot_left = Dot(point=initial_point_left, color = 'green')

        dot_left.add_updater(lambda x: x.move_to(ax.c2p(xTrackerLeft.get_value(), func(xTrackerLeft.get_value()))))

        xTextLeft = MathTex(r"x = ").to_edge(UL)
        functionTextLeft = MathTex(r"g(x) = ").to_edge(UL).shift([0, -1, 0])
        limitTextLeft = MathTex(r"\lim \limits_{x \to 0^-} g(x) = 2").to_edge(UL).shift([0, -2, 0])

        self.add(ax, labels, graph, hole, dot_left, x_value_left, xTextLeft, y_value_left, functionTextLeft)
        
        self.play(xTrackerLeft.animate.set_value(-0.05), run_time = 3)

        self.remove(x_value_left)
        self.remove(y_value_left)
        x_value_left = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0, 0]).set_value(-0.00001)
        y_value_left = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.8, -1, 0]).set_value(1.99999)
        self.add(x_value_left)
        self.add(y_value_left)

        self.play(FadeIn(limitTextLeft))
        
        self.wait(1)
        
        ###########
        xTrackerRight = ValueTracker(4)

        x_value_right = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([0, 0, 0]).set_value(xTrackerRight.get_value()))
        y_value_right = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([-0.5, -1, 0]).set_value(func(xTrackerRight.get_value())))

        initial_point_right = [ax.coords_to_point(xTrackerRight.get_value(), func(xTrackerRight.get_value()))]
        dot_right = Dot(point=initial_point_right, color = 'blue')

        dot_right.add_updater(lambda x: x.move_to(ax.c2p(xTrackerRight.get_value(), func(xTrackerRight.get_value()))))

        xTextRight = MathTex(r"x = ").to_edge(UR).shift([-2, 0, 0])
        functionTextRight = MathTex(r"g(x) = ").to_edge(UR).shift([-2.5, -1, 0])
        limitTextRight = MathTex(r"\lim \limits_{x \to 0^+} g(x) = 2").to_edge(UR).shift([0, -2, 0])

        self.add(dot_right, x_value_right, xTextRight, y_value_right, functionTextRight)
        
        self.play(xTrackerRight.animate.set_value(0.05), run_time = 3)

        self.remove(x_value_right)
        self.remove(y_value_right)
        x_value_right = DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([0, 0, 0]).set_value(0.00001)
        y_value_right = DecimalNumber(num_decimal_places = 5).to_edge(UR).shift([-0.5, -1, 0]).set_value(1.99999)
        self.add(x_value_right)
        self.add(y_value_right)

        self.play(FadeIn(limitTextRight))
        
        self.wait(1)

        rect = Rectangle(width = 4, height = 1.5, color = BLUE).shift([0, -2, 0])
        rect.set_fill("#0e5c9c", opacity = 1)
        self.play(Create(rect))
        limitTextCenter = MathTex(r"\lim \limits_{x \to 0} g(x) = 2").shift([0, -2, 0])
        self.play(FadeIn(limitTextCenter))

        self.wait(3)