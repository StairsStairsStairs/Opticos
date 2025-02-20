from manim import *
from limit_animation_runner import hello

if __name__ == "__main__":
    function = str(input("Enter a function: f(x) = "))
    function = "".join(function.split())
    approach = float(input("Enter value you want x to approach: "))
    side = int(input("Do you want to approach it from the left or from the right? (-1 for left, 1 for right): "))
    s = hello(GREEN, function, approach, side)
    s.render()