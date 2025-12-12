import sys, os, subprocess

def main():
    if len(sys.argv) < 5:
        print("Usage: python runner.py first a b c")
        sys.exit(1)

    choice = sys.argv[1]
    a, b, c = sys.argv[2:5]

    if choice != "first":
        print("Unknown choice. Only 'first' is supported.")
        sys.exit(1)

    env = os.environ.copy()
    env["POLY_A"] = a
    env["POLY_B"] = b
    env["POLY_C"] = c

    cmd = [sys.executable, "-m", "manim", "-pql", "basicGraph.py", "DefinitionOfADerivative"]
    subprocess.run(cmd, check=True, env=env)

if __name__ == "__main__":
    main()
