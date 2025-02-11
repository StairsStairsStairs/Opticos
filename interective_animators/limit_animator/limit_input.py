from manim import *
from limit_animation_runner import hello

if __name__ == "__main__":
    approach = float(input("Enter value you want x to approach: "))
    s = hello(GREEN, approach)
    s.render()