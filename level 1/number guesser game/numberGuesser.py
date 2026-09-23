

"""
Number Guessing Game. Task 2 of the codveda internship program

The computer randomly generates a number between 1 and 100.
The player has a maximum of 10 attempts to guess the number.

The program provides feedback:
Too high
Too low
Correct

The player can also choose to play again after finishing a game.

"""

import random


def play_game():
    """Run one round of the number guessing game."""

    correct_number = random.randint(1, 100)
    max_attempts = 10
    attempts = 0

    print("\n" + "=" * 40)
    print("       NUMBER GUESSING GAME")
    print("=" * 40)
    print("I have selected a number between 1 and 100.")
    print(f"You have {max_attempts} attempts to guess it.\n")

    while attempts < max_attempts:

        try:
            guess = int(input(
                f"Attempt {attempts + 1}/{max_attempts} - "
                "Enter your guess: "
            ))

            # Make sure the guess is within the allowed range
            if guess < 1 or guess > 100:
                print("Please enter a number between 1 and 100.\n")
                continue

        except ValueError:
            print("Invalid input! Please enter a whole number.\n")
            continue

        attempts += 1

        if guess < correct_number:
            print("Too low! Try again.\n")

        elif guess > correct_number:
            print("Too high! Try again.\n")

        else:
            print(
                f"\nCongratulations! 🎉 "
                f"You guessed the correct number "
                f"({correct_number}) in {attempts} attempts!"
            )
            return

    print("\nYou've used all your attempts.")
    print(f"The correct number was {correct_number}.")


def main():
    """Start the game and allow the player to replay."""

    while True:

        play_game()

        while True:
            play_again = input(
                "\nWould you like to play again? (yes/no): "
            ).strip().lower()

            if play_again in ("yes", "y"):
                break

            elif play_again in ("no", "n"):
                print("\nThanks for playing! Goodbye.")
                return

            else:
                print("Please enter yes or no.")


if __name__ == "__main__":
    main() 
