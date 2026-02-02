from functions.write_file import write_file


def main():
    print("Test 1: overwrite lorem.txt")
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)
    print()

    print("Test 2: write pkg/morelorem.txt")
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)
    print()

    print("Test 3: attempt to write outside working directory")
    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)


if __name__ == "__main__":
    main()
