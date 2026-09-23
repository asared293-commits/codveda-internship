# SIMPLE CALCULATOR PROGRAM
# Description: Develop a basic calculator that can
# perform four primary arithmetic operations:
# addition, subtraction, multiplication, and division.



def add(num1, num2):
    """Return the sum of two numbers."""
    return num1 + num2


def subtract(num1, num2):
    """Return the difference of two numbers."""
    return num1 - num2


def multiply(num1, num2):
    """Return the product of two numbers."""
    return num1 * num2


def divide(num1, num2):
    """Return the quotient of two numbers."""
    if num2 == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return num1 / num2


def get_valid_number(prompt):
    """Ask for a number until the user enters a valid value."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def show_menu():
    """Display the calculator menu."""
    print("\n===== SIMPLE CALCULATOR =====")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")


def main():
    """Run the calculator loop."""
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        if choice not in {"1", "2", "3", "4"}:
            print("Invalid choice. Please select a number from 1 to 5.")
            continue

        first_number = get_valid_number("Enter the first number: ")
        second_number = get_valid_number("Enter the second number: ")

        try:
            if choice == "1":
                result = add(first_number, second_number)
                print(f"Result: {first_number} + {second_number} = {result}")
            elif choice == "2":
                result = subtract(first_number, second_number)
                print(f"Result: {first_number} - {second_number} = {result}")
            elif choice == "3":
                result = multiply(first_number, second_number)
                print(f"Result: {first_number} * {second_number} = {result}")
            elif choice == "4":
                result = divide(first_number, second_number)
                print(f"Result: {first_number} / {second_number} = {result}")
        except ZeroDivisionError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
