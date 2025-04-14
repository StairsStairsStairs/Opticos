from manim import *

class MovingCameraCenter(MovingCameraScene):
    def construct(self):
        functionColor = RED

        def func(x):
            return 1 / x**2 if abs(x) > 0.1 else 0

        x_min = -1000
        x_max = 1000
        tick_spacing = 20
        x_length = (x_max - x_min) / 10  # Just scale it reasonably to keep tick spacing consistent

        axes = Axes(
            x_range=[x_min, x_max, tick_spacing],
            y_range=[-0.01, 0.01, 0.002],
            x_length=x_length,
            y_length=7,
            tips=False
        ).move_to(ORIGIN)

        axes.add_coordinates()

        # Now plot using samples (should work in 0.18.1)
        graph = axes.plot(
            func,
            color=functionColor,
            discontinuities=[-0.1, 0.1],
            use_smoothing=False,
            x_range=[0.1,10000,1]
        )

        self.add(axes, graph)
        #self.camera.frame.move_to([-100, 0, 1])
        #self.play(self.camera.frame.animate.move_to((-500, 0, 0)), run_time=0.000001)
        self.wait(1)
        self.play(self.camera.frame.animate.move_to((100, 0, 0)), run_time=10)
        self.wait()
