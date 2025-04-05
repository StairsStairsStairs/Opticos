from manim import *

class MovingCameraCenter(MovingCameraScene):
    def construct(self):
        functionColor = RED

        def func(x):
            return 1 / x if abs(x) > 0.1 else 0

        x_min = -1000
        x_max = 1000
        tick_spacing = 100
        x_length = (x_max - x_min) / 10  # Just scale it reasonably to keep tick spacing consistent

        axes = Axes(
            x_range=[x_min, x_max, tick_spacing],
            y_range=[-2, 2, 1],
            x_length=x_length,
            y_length=4,
            tips=False
        ).move_to(ORIGIN)

        axes.add_coordinates()

        # Now plot using samples (should work in 0.18.1)
        graph = axes.plot(
            func,
            color=functionColor,
            discontinuities=[-0.1, 0.1],
            use_smoothing=False,
            samples=3000
        )

        self.add(axes, graph)
        self.wait(1)
        self.play(self.camera.frame.animate.move_to((100, 0, 0)), run_time=3)
        self.wait()
