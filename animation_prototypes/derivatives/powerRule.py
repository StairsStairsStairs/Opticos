#code heavily inspired by https://github.com/malhotra5/Manim-Tutorial?tab=readme-ov-file
#at this link, go to the graphing tutorial

from manim import *
import math

class Graphing(Scene):
    
    def construct(self):
        #Make graph
        global slope
        slope = 3
        axes = Axes(
            x_range = [-4, 4, 1],
            y_range = [-5, 5, 1],
            axis_config={"include_numbers": True}
        )

        graph = axes.plot(lambda x: x**2, color=BLUE)
        graph_label = axes.get_graph_label(graph, label="x^2")
        label_position = axes.coords_to_point(2, 2)
        graph_label.next_to(label_position, UP)
        
        graph2 = axes.plot(lambda x: 2*x, color=BLUE)
        graph_label_2 = axes.get_graph_label(graph, label="2x")
        graph_label_2.next_to(label_position, UP)
        
        def update_dot(mob, alpha):
            x = interpolate(2, 1, alpha)
            y = x**2
            mob.move_to(axes.c2p(x,y))

        def update_end_dot(mob, alpha):
            x = interpolate(0.5, 1, alpha)
            y = x**2
            mob.move_to(axes.c2p(x,y))

        def update_offscreen_dot(mob, alpha):
            x = interpolate(2, 1, alpha)
            y = x**2
            mob.move_to(axes.c2p(x*5,y*5))

        # Create a dot and set its starting position
        dot = Dot(color=WHITE).move_to(axes.c2p(2, 4))
        offscreen_dot = Dot(color = GREEN).move_to(axes.c2p(4, 10))
        end_dot = Dot(color=RED).move_to(axes.c2p(1,1))
        end_offscreen_dot = Dot(color = BLACK).move_to(axes.c2p(-2, -8))


        

        #end dot: (1,1)
        #dot: 
        line = always_redraw(lambda: Line(end_offscreen_dot.get_center(), offscreen_dot.get_center(), color = YELLOW))
        
        #axes.c2p(dot.get_center()[0]+5*slope, dot.get_center()[1] + 5*slope)
        #end_dot.get_center()-(5*slope), dot.get_center()+(5*slope), color = YELLOW))
        #slope = (dot.get_center()[1] - 1)/(dot.get_center()[0] - 1))

        #Display graph
        self.play(Create(axes), run_time = 2.5)
        self.play(Create(graph), run_time = 3)
        self.play(Create(graph_label), run_time = 0.5)
        self.wait(0.5)
        self.add(dot)
        self.add(end_dot)
        self.wait(0.5)
        self.add(line)
        self.wait(0.5)
        self.play(UpdateFromAlphaFunc(dot, update_dot, run_time = 2, rate_func = linear),
            UpdateFromAlphaFunc(offscreen_dot, update_offscreen_dot, run_time = 2, rate_func = linear))
        self.wait(1)
        self.remove(dot)
        self.remove(end_dot)
        self.play(Transform(graph, graph2), Transform(graph_label, graph_label_2))
        self.wait(1)

        

        