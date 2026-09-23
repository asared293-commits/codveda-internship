"""
word counter Task 3 of the codveda internship program

This program reads a text file and counts the number of words
contained in the file.

The user enters the name or path of the text file.
The program handles errors if the file cannot be found or read.
"""


def count_words(filename):
    """Read a text file and return the number of words."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()

        words = content.split()

        return len(words)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

    except PermissionError:
        print(f"Error: Permission denied when accessing '{filename}'.")
        return None

    except OSError as error:
        print(f"Error reading the file: {error}")
        return None


def main():
    """Run the word counter program."""

    print("=" * 40)
    print("          WORD COUNTER")
    print("=" * 40)

    filename = input("Enter the name of the text file: ").strip()

    if not filename:
        print("Error: You did not enter a file name.")
        return

    word_count = count_words(filename)

    if word_count is not None:
        print("\nFile successfully read.")
        print(f"The file contains {word_count} words.")


if __name__ == "__main__":
    main()
