"""Number guessing game"""

import random
import time


def game(number_of_tries):
    """game"""
    game_on = True
    win_game = False
    print("Let's start the game!\n")

    guess_count = 0
    computer_guess = random.randint(1, 100)
    while guess_count < number_of_tries and game_on:
        user_guess = input("Enter your guess: ")

        if int(user_guess) < 1 or int(user_guess) > 100:
            print("Invalid guess. Choose a number between 1 and 100\n")
            continue

        guess_count += 1
        if int(user_guess) == computer_guess:
            game_on = False
            win_game = True
        else:
            if int(user_guess) > computer_guess:
                print(f"Incorrect! The number is less than {user_guess}")
            else:
                print(f"Incorrect! The number is greater than {user_guess}")
        print()

    if win_game:
        print(f"Congratulations! You guessed the correct number in {guess_count} attempts.\n")
    else:
        print(f"Sorry, you lost the game. Computer guess was {computer_guess}\n")



def welcome():
    """game welcome message"""
    print(
        "Welcome to the Number Guessing Game!\n"
        "I'm thinking of a number between 1 and 100.\n"
        "You have limited chances to guess the correct number.\n\n"
        "Please select the difficulty level:\n"
        "Use 'q' to quit the game\n"
        "1. Easy (10 chances)\n"
        "2. Medium (5 chances)\n"
        "3. Hard (3 chances)\n"
    )

def main():
    """main func"""
    play_again = True

    while play_again:
        welcome()
        game_difficulty = input("Enter your choice: ")
        print()

        if game_difficulty == "easy":
            print("Great! You have selected the Easy difficulty level.")
            number_of_tries = 10
        elif game_difficulty == "medium":
            print("Great! You have selected the Medium difficulty level.")
            number_of_tries = 5
        elif game_difficulty == "hard":
            print("Great! You have selected the Hard difficulty level.")
            number_of_tries = 3
        elif game_difficulty == "q":
            return
        else:
            print("Invalid input")
            return

        start_time = time.time()
        game(number_of_tries)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"It took you {round(elapsed_time, 2)} seconds")
        print()

        continue_playing = input("Do you want to play again (y/n)? ")
        print()
        if continue_playing == "n":
            play_again = False


if __name__ == "__main__":
    main()
