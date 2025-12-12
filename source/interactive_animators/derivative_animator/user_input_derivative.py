import sys
from manim import *
from render_derivative_animation import create_polynomial, DefinitionOfADerivative

def main():
    if len(sys.argv) < 5:
        print("Usage: python inputTest.py first a b c")
        sys.exit(1)

    choice = sys.argv[1]
    a, b, c = map(float, sys.argv[2:5])  # parse coefficients

    if choice == "first":
        func = create_polynomial(a, b, c)
        label = f"f(x) = {a}x^2 + {b}x + {c}"
        scene = DefinitionOfADerivative(func=func, label=label)
        scene.render()
    else:
        print("Unknown choice. Only 'first' is supported right now.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runner.py [first|second]")
        sys.exit(1)

    choice = sys.argv[1]
    func, label = parse_polynomial(choice)

    scene = DefinitionOfADerivative(func=func, label=label)
    scene.render()