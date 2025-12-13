import sys, os, subprocess

# its important to note that this acts less like a UI and more like a batch file
# This will make it easier for godot to run and compile manim files

def main():
    if len(sys.argv) < 5:
        print("Usage: python user_input_derivative.py definition a b c")
        sys.exit(1)

    choice = sys.argv[1]
    a, b, c = sys.argv[2:5]



    env = os.environ.copy()
    env["POLY_A"] = a
    env["POLY_B"] = b
    env["POLY_C"] = c

    # depending on the given choice the user can run the definition of a derivative animation
    # The Falling Ladder animation or the motion problem animation
    if choice == "definition":
        cmd = [sys.executable, "-m", "manim", "-pql", "basicGraph.py", "DefinitionOfADerivative"]
        subprocess.run(cmd, check=True, env=env)

    elif choice == "ladder":
        cmd = [sys.executable, "-m", "manim", "-pql", "basicGraph.py", "FallingLadder"]
        subprocess.run(cmd, check=True, env=env)

    elif choice == "motion":
        cmd = [sys.executable, "-m", "manim", "-pql", "basicGraph.py", "FallingLadder"]
        subprocess.run(cmd, check=True, env=env)
    else:
        print("Unknown choice.")
        sys.exit(1)

if __name__ == "__main__":
    main()
