from manim import *

#Note: if you want to have the camera move, you must put "MovingCameraScene" instead of "Scene" when defining the class
class hello(MovingCameraScene):
    def construct(self):
        
        #-------------------------------------------------
        #Customizable parameters
    
        backgroundColor = BLACK
        functionColor = BLUE

        approach = 1000 #value x approaches
        side = -1 #-1 to approach from left, 1 to approach from right

        def func(x):
            return 1 / x**2 if abs(x) > 0.1 else 10

        self.camera.background_color = backgroundColor
        x_min = -1000
        x_max = 1000
        tick_spacing = 20
        x_length = (x_max - x_min) / 10  # Just scale it reasonably to keep tick spacing consistent

        ax = Axes(
            x_range=[x_min, x_max, tick_spacing],
            y_range=[-0.01, 0.01, 0.002],
            x_length=x_length,
            y_length=7,
            tips=False
        ).move_to(ORIGIN)

        ax.add_coordinates()

        graph = ax.plot(
            func,
            color=functionColor,
            discontinuities=[-0.1, 0.1, 1],
            use_smoothing=False,
            x_range=[0.1,10000,1]
        )
        #In manim, a value tracker is an object that displays a constantly updated value
        #By default it starts at some initial value and increases or decreases at a constant rate
        #until it reaches it's defined ending value
        xTracker = ValueTracker(0.2)

        #Every frame the x and y value of the point gets updated by getting the current value of xTracker. The exact value gets directly displayed
        #for x and for y the value from the value tracker is plugged into the method func() and the output is what the y value gets set equal to
        x_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1, 0, 0]).set_value(xTracker.get_value()))
        y_value = always_redraw(lambda: DecimalNumber(num_decimal_places = 5).to_edge(UL).shift([1.8, -1, 0]).set_value(func(xTracker.get_value())))

        #Define starting point at the initial point xTracker is defined to
        initial_point = [ax.coords_to_point(xTracker.get_value(), func(xTracker.get_value()))]
        dot = Dot(point = initial_point) #Creates point that moves along function

        #Updates the x-coordinate of the point to match the most recent value of xTracker
        #also plugs the x-coordinate into func() to get the y-value
        dot.add_updater(lambda x: x.move_to(ax.c2p(xTracker.get_value(), func(xTracker.get_value()))))
        self.add(ax, graph, dot, x_value, y_value)
        #self.camera.frame.move_to([-100, 0, 1])
        #self.play(self.camera.frame.animate.move_to((-500, 0, 0)), run_time=0.000001)
        self.wait(1)
        self.play(self.camera.frame.animate.move_to((100, 0, 0)), xTracker.animate.set_value(approach + 0.05*side), run_time = 10, succession = False) 
        self.wait()