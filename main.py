import argparse
import shutil
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("stack")
parser.add_argument("--requirements")
args = parser.parse_args()

command=args.command
stack=args.stack
requirement=args.requirements
def install_python():
    subprocess.run(
        ["winget", "install", "-e", "--id", "Python.Python.3.12"],
        check=True
    )
def install_vs_code():
    subprocess.run(
        ["winget", "install", "-e", "--id", "Microsoft.VisualStudioCode"],
        check=True
    )
def install_py_libs(requirements):
    if requirements is None:
        return
    elif requirements == "basic":
     subprocess.run(
        ["python","-m","pip", "install","pandas","requests","numpy","pillow","pyautogui" ],
        check=True
    )

def is_installed(command):
    return shutil.which(command) is not None

if command == "setup":
    if stack == "python":
        # check python
        if is_installed("python"):
            print("Python already installed ✅")
        else:
            print("Installing Python...")
            install_python()
        # check vscode
        if is_installed("code"):
            print("VS Code already installed ✅")
        else:
            print("Installing VS Code...")
            install_vs_code()

        if requirement == "basic":
          install_py_libs(requirement)

if command == "list":
    print("Available setups")


#print(args.command)
#print(args.stack)
#print(args.requirements)
#print(is_installed(args.stack))