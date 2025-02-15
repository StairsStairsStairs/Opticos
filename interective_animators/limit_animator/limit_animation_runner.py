from manim import *

#config.frame_width = 8  # Default is 14 units wide
#config.frame_height = 8  # Default is 8 units high

class hello(Scene):
    def __init__(self, color = RED, approach = 0, side = -1, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.approach = approach
        self.side = side

    def construct(self):

        #-------------------------------------------------
        #Customizable parameters
    
        scale = 0.75
        backgroundColor = BLACK
        functionColor = self.color

        #approach = 0 #value x approaches
        #side = -1 #-1 to approach from left, 1 to approach from right

        #Function that is graphed out and used to find output values at each frame
        def func(x):
            return -1 * x**2 + 2
        #-------------------------------------------------

        
        self.camera.background_color = backgroundColor

        #initializes the x and y axes along with the range of values they display
        ax = Axes(
            x_range=[-5, 5], y_range=[-15, 5], axis_config={"include_tip": False},
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)").scale(scale) # Labels each axis

        #Draw graph that plot out function defined by func()
        graph = ax.plot(func, color = functionColor, discontinuities=[1])

        graph_group = VGroup(ax, graph)
        graph_group.scale(scale) 
        graph_group.to_corner(UR)

        #In manim, a value tracker is an object that displays a constantly updated value
        #By default it starts at some initial value and increases or decreases at a constant rate
        #until it reaches it's defined ending value
        xTracker = ValueTracker(4*self.side)

        #Every frame the x and y value of the point gets updated by getting the current value of xTracker. The exact value gets directly displayed
        #for x and for y the value from the value tracker is plugged into the method func() and the output is what the y value gets set equal to
        coordsRect = Rectangle(width = 4.6, height = 2, color = BLUE).to_edge(UL).shift([-0.5, 0.5, 0])
        x_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0.3, 0]).set_value(xTracker.get_value()))
        y_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.7, -0.75, 0]).set_value(func(xTracker.get_value())))

        #Define starting point at the initial point xTracker is defined to
        initial_point = [ax.coords_to_point(xTracker.get_value(), func(xTracker.get_value()))]
        dot = Dot(point = initial_point).scale(scale) #Creates point that moves along function

        #Updates the x-coordinate of the point to match the most recent value of xTracker
        #also plugs the x-coordinate into func() to get the y-value
        dot.add_updater(lambda x: x.move_to(ax.c2p(xTracker.get_value(), func(xTracker.get_value()))))

        #Draws text on screen using Latex
        xText = MathTex(r"x = ").to_edge(UL).shift([-0.3, 0.2, 0])
        functionText = MathTex(r"f(x) = ").to_edge(UL).shift([-0.3, -0.7, 0])
        limitText = MathTex(r"\lim \limits_{x \to 0^-} f(x) = " + str(func(self.approach))).to_edge(UL).shift([0, -2.75, 0])
        
        #Add all defined elements to the scene
        self.add(ax, labels, graph, dot, coordsRect, x_value, xText, y_value, functionText)
        
        #Run value tracker, starts from -4 and and at -0.05
        self.play(xTracker.animate.set_value(self.approach + 0.05*self.side), run_time = 3)
        
        #Since the actual values from the value tracker are a bit messy at the end (due to the nature of computer calculations)
        #The final values are manually set to slightly neater numbers that better explain the concept of a limit
        self.remove(x_value)
        self.remove(y_value)
        #x_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0, 0]).set_value(-0.00001)
        #y_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.8, -1, 0]).set_value(1.99999)
        if func(self.approach + self.side*0.05) > func(self.approach):
            offset = -1
        else:
            offset = 1
        x_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0.3, 0]).set_value(self.approach + self.side*0.00001)
        y_value = DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.7, -0.75, 0]).set_value(func(self.approach) + offset*self.side*0.00001)
        self.add(x_value)
        self.add(y_value)
        
        #Display text that shows the value of the limit
        self.play(FadeIn(limitText))
        
        self.wait(3)