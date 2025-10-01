'''
The following script prompts the user for input in the terminal
When the script is run it will ask the user for the following:
    1. The function you would like to plot out
        * Note that at this time, the limit animator only accepts polynomial functions 
        * Your input must be of the form <term> <operator> <term> <operator> ...
            * <term> is of the form mx^n, where m is an integer, and n is a nonnegative integer
            * <operator> is either '+' or '-'
        
    2. The value you want x to approach
    3. Whether you want x to approach the point from the left or from the right

After collecting all three input values creates an instance of limit_animation, passing
all three input values as arguments. The animation is then rendered.
'''

from manim import *
from limit_animation_runner import limit_animation

if __name__ == "__main__":
    function = str(input("Enter a function: f(x) = "))
    function = "".join(function.split())
    approach = float(input("Enter value you want x to approach: "))
    side = int(input("Do you want to approach it from the left or from the right? (-1 for left, 1 for right): "))
    s = limit_animation(GREEN, function, approach, side)
    s.render()