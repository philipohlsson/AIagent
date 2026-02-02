from functions.get_file_content import get_file_content

def run_tests():
    print("Test: lorem.txt (should truncate)")
    content = get_file_content("calculator", "lorem.txt")
    print(f"Length: {len(content)}")
    print(content[-120:])  # show truncation message
    print()

    print("Test: main.py")
    print(get_file_content("calculator", "main.py"))
    print()

    print("Test: pkg/calculator.py")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    print("Test: /bin/cat")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    print("Test: missing file")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    run_tests()
