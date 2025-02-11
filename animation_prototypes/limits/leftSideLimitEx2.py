from manim import *
class hello(Scene):
    def construct(self):
        
        #-------------------------------------------------
        #Customizable parameters
    
        backgroundColor = BLACK
        functionColor = RED

        approach = 0 #value x approaches
        side = -1 #-1 to approach from left, 1 to approach from right

        #Function that is graphed out and used to find output values at each frame
        def func(x):
            return -1 * x**2 + 2
        #-------------------------------------------------


        self.camera.background_color = backgroundColor

        #initializes the x and y axes along with the range of values they display
        ax = Axes(
            x_range=[-5, 5], y_range=[-15, 5], axis_config={"include_tip": False},
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)") # Labels each axis

        #In manim, a value tracker is an object that displays a constantly updated value
        #By default it starts at some initial value and increases or decreases at a constant rate
        #until it reaches it's defined ending value
        xTracker = ValueTracker(4*side)

        #Every frame the x and y value of the point gets updated by getting the current value of xTracker. The exact value gets directly displayed
        #for x and for y the value from the value tracker is plugged into the method func() and the output is what the y value gets set equal to
        x_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0, 0]).set_value(xTracker.get_value()))
        y_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.8, -1, 0]).set_value(func(xTracker.get_value())))
        
        #Draw graph that plot out function defined by func()
        graph = ax.plot(func, color = functionColor, discontinuities=[1])

        #Place a point discontinutiy at (0, f(0))
        hole = Circle(radius=0.08, color=functionColor, fill_color=backgroundColor, fill_opacity=1, stroke_width=3)
        hole.move_to(ax.c2p(0, func(0))) 

        #Define starting point at the initial point xTracker is defined to
        initial_point = [ax.coords_to_point(xTracker.get_value(), func(xTracker.get_value()))]
        dot = Dot(point = initial_point) #Creates point that moves along function

        #Updates the x-coordinate of the point to match the most recent value of xTracker
        #also plugs the x-coordinate into func() to get the y-value
        dot.add_updater(lambda x: x.move_to(ax.c2p(xTracker.get_value(), func(xTracker.get_value()))))

        #Draws text on screen using Latex
        xText = MathTex(r"x = ").to_edge(UL)
        functionText = MathTex(r"f(x) = ").to_edge(UL).shift([0, -1, 0])
        limitText = MathTex(r"\lim \limits_{x \to 0^-} f(x) = 2").to_edge(UL).shift([0, -2.75, 0])
        
        #Add all defined elements to the scene
        self.add(ax, labels, graph, hole, dot, x_value, xText, y_value, functionText)
        
        #Run value tracker, starts from -4 and and at -0.05
        self.play(xTracker.animate.set_value(approach + 0.05*side), run_time = 3)
        
        #Since the actual values from the value tracker are a bit messy at the end (due to the nature of computer calculations)
        #The final values are manually set to slightly neater numbers that better explain the concept of a limit
        self.remove(x_value)
        self.remove(y_value)
        x_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0, 0]).set_value(-0.00001)
        y_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.8, -1, 0]).set_value(1.99999)
        self.add(x_value)
        self.add(y_value)
        
        #Display text that shows the value of the limit
        self.play(FadeIn(limitText))
        
        self.wait(3)