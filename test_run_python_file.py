from functions.run_python_file import run_python_file


def main():
    print("Test 1: calculator main.py (no args)")
    print(run_python_file("calculator", "main.py"))
    print()

    print("Test 2: calculator main.py with expression")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print("Test 3: calculator tests.py")
    print(run_python_file("calculator", "tests.py"))
    print()

    print("Test 4: outside working directory")
    print(run_python_file("calculator", "../main.py"))
    print()

    print("Test 5: nonexistent file")
    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print("Test 6: not a Python file")
    print(run_python_file("calculator", "lorem.txt"))


if __name__ == "__main__":
    main()
