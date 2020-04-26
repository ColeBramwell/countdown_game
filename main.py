import random
from itertools import combinations
import pickle
import time

ANSWER_TIME = 5


def intro():
    print("|----------------------------|")
    print("| Welcome to the Knockoff of |")
    print("|        'Countdown'         |")


def menu():
    print("|----------------------------|")
    print("|Please select an option:    |")
    print("|----------------------------|")
    print("|1) Play 'Letters round'     |")
    print("|2) Quit program             |")
    print("|----------------------------|")

    choice = input("\nPlease enter a number between 1 and 2: ")
    if choice == "1":
        letters_game()
    elif choice == "2":
        print("Thanks for playing!")
        return
    else:
        print("That is not a valid input")
    menu()


def letters_game():
    """
    Function handles the main structure for the 'letters round' game
    """
    letters = generate_letters()
    letters_str = ''.join([str(elem) for elem in letters])
    print("\nYour letters are:\n")
    print(letters_str, "\n")

    timer(30, letters_str)
    user_ans = timed_input(ANSWER_TIME)
    if user_ans is None:
        print("Sorry, you didn't enter in time")
    else:
        check_word_valid(letters_str, user_ans)
    if get_choice("Would you like to see the answers? (y/n): ", "y", "n") == "y":
        solve(letters)


def generate_letters():
    """
    Generates random 9-length list of letters
    It samples letters based on their frequency in english (like scrabble).

    :return list of 9 random letters, at least 3 vowels and 4 consonants
    """
    vowels_list = 'eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooouuuu'
    consonants_list = 'nnnnnnrrrrrrttttttllllssssddddgggbbccmmppffhhvvwwyykjxqz'
    n_vowels = random.randint(3, 5)
    vowels = random.sample(vowels_list, n_vowels)
    consonants = random.sample(consonants_list, 9 - n_vowels)
    letters = vowels + consonants
    random.shuffle(letters)
    return letters


def timed_input(t):
    """
    Prompts input, returning none if the user does not enter an answer in t seconds.

    :param t: Number of seconds the user has for answering.
    :return: None if answer is entered after t seconds, otherwise returns answer
    """
    start_time = time.time()
    user_ans = input("Enter your string - you have {} seconds: ".format(t)).strip().lower()
    if time.time() - start_time > t:
        return None
    else:
        return user_ans


def check_word_valid(given_letters, user_str):
    """
    Determines if the user-entered string is a valid word, and can be made with the given letters.

    :param given_letters: The random letters generated by generate_letters()
    :param user_str: The user's answer (string) returned from timed_input()
    :return: None If user_str cannot be made with given_letters - saves processing later. (used to break function)
    """
    for letter in user_str:
        if letter in given_letters:
            given_letters = given_letters.replace(letter, "", 1)
        else:
            print("That is not a valid combination of letters")
            return

    valid_words = pickle.load(open('word_dict.p', 'rb'))
    sorted_user_str = ''.join(sorted(user_str))
    if sorted_user_str in valid_words:
        if user_str in valid_words[sorted_user_str]:
            print("Nice! Your word '{}' is worth {} points".format(user_str, len(user_str)))
        else:
            print("Not a valid word, Sorry")
    else:
        print("Not a valid word, Sorry")


def solve(letters):
    """
    Function to return the 'winning' countdown words
    for a given string of letters.

    :param letters: A string or list of given letters for a round
    :return: N/A
    """
    valid_words = pickle.load(open('word_dict.p', 'rb'))
    letters = sorted(letters)
    for length in range(3, 10):
        log = set()
        for combined_letters in combinations(letters, length):
            sorted_word = ''.join(combined_letters)
            if sorted_word in valid_words:
                for word in valid_words[sorted_word]:
                    log.add(word)
        if len(log) > 0:
            print('\nLooking for {} letter words...\n'.format(length))
            found_words = ', '.join(sorted(word for word in log))
            print(found_words)
        else:
            print("\nNo {} letter words found".format(length))


def timer(t, game_txt):
    """
    Function to count down from t seconds, mimicking the clock in the game show

    :param t: Seconds to count down from
    :param game_txt: Message to be displayed alongside timer
    :return: N/A
    """
    while t:
        mins, secs = divmod(t, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        print(game_txt, "---", time_format)
        time.sleep(1)
        t -= 1
    print("Time Up!")


def get_choice(msg, x, y):
    """
    Ensures that the user response to msg parameter is either x or y. Repeats otherwise.
    x and y parameters should be lowercase with no surrounding spaces

    :param msg: Message to be displayed when asking for choice
    :param x: Valid choice
    :param y: Other valid choice
    :return: Choice, either x or y
    """
    choice = input(msg).strip().lower()
    while choice != x and choice != y:
        print("Not a valid input, please try again")
        choice = input(msg).strip().lower()
    return choice


intro()
menu()
