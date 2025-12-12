import sys
import subprocess

def main():
    if len(sys.argv) < 5:
        print("Usage: python runner.py first a b c")
        sys.exit(1)

    choice = sys.argv[1]
    a, b, c = sys.argv[2:5]

    if choice != "first":
        print("Unknown choice. Only 'first' is supported.")
        sys.exit(1)

    cmd = [
        "manim",
        "-pql",
        "animations.py",
        "DefinitionOfADerivative",
        "--a", a,
        "--b", b,
        "--c", c,
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()

