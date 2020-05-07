import time
import random
import pickle

from itertools import combinations
from collections import Counter

ANSWER_TIME = 30

try:
    valid_words = pickle.load(open('word_dict.p', 'rb'))
except FileNotFoundError:
    print(
        "No dictionary file found. "
        "Please ensure there is a non-empty file called 'word_dict.p' in the same folder as this program")
    exit()
except EOFError:
    print(
        "The dictionary file is empty. You may have accidentally overwritten the file. Please try undoing this action, "
        "or re-downloading the latest version from GitHub")
    exit()


def intro():
    """
    Runs once at the start of the program, functions as the 'title screen' for the project and the disclaimer

    :return: None
    """
    print("\nDISCLAIMER: All words generated are from an unfiltered dictionary")
    print("As such, 'foul language' and slurs may be present.")
    input("\nPress enter to accept and continue")
    print("______________________________")
    print("| Welcome to the Knockoff of |")
    print("|        'Countdown'         |")


def instructions():
    """
    Tells the user how to play each game

    :return: None
    """
    print("\nHow to play Countdown's 'Letter Round': ")
    print("First, you will select how many rounds you will play")
    print("At the start of each round, you will be given 9 letters, at least 3 vowels and 4 consonants")
    print("You will then have 30 seconds to construct the longest word using those letters")
    print("After the 30 seconds, you will have {} seconds to enter the longest word you have found".format(ANSWER_TIME))
    print("No letter may be used more than it appears, and no proper nouns")
    print("\nScoring for 'Letter Round':")
    print("Words are scored according to how many letters they contain")
    print("For example, the word 'table' is worth 5 points")
    print("Any word using all 9 letters scores double (18 points)")
    print("Your score will be tallied over the rounds")
    print("\nHow to play 'Countdown Conundrum': ")
    print("You will be given a phrase, which you must use to create a nine-letter word")
    print("For example, if you are given the phrase 'map casings', you could enter 'campaigns' and win the round")
    print("Alternate solutions are accepted!")
    print("\nGood luck!")
    input("\nPress enter to continue")


def menu():
    """
    Directs the user to other game or instructions functions based on their input.
    Inputs are treated as strings, so 4 != 4.0 when entering a choice

    :return: None
    """
    print("______________________________")
    print("|Please select an option:    |")
    print("|----------------------------|")
    print("|1) Play 'Letters round'     |")
    print("|2) Play 'Conundrum'         |")
    print("|3) See instructions         |")
    print("|4) Quit program             |")
    print("|____________________________|")

    menu_choice = input("\nPlease enter a number between 1 and 4: ")
    if menu_choice == "1":
        letters_game()
    elif menu_choice == "2":
        conundrum()
    elif menu_choice == "3":
        instructions()
    elif menu_choice == "4":
        print("Thanks for playing!")
        exit()
    else:
        print("That is not a valid input")
    menu()


def letters_game():
    """
    Function handles the main structure for the 'letters round' game

    :return None
    """
    num_rounds = get_pos_int("\nHow many rounds would you like to play? ")
    points = 0
    for game in range(1, num_rounds + 1):
        print("\nYou currently have {} points".format(points))
        _quit = input("\nType 'q' to quit, otherwise press enter to continue: ").strip().lower()
        if _quit == 'q':
            print("Exiting the game. Your score will not be recorded.")
            return

        letters = generate_letters()
        letters_str = ''.join(letters)
        print("\nStarting Round {} of {}...".format(game, num_rounds))
        print("Your letters are:")
        print("\n{}\n".format(letters_str))

        user_ans = timed_input("Enter the longest word you found", ANSWER_TIME)
        if user_ans is None:
            print("Sorry, you didn't enter in time")
        else:
            points += get_word_points(letters_str, user_ans)
        if get_choice("Would you like to see the answers? (y/n): ", "y", "n") == "y":
            solve(letters_str)

    print("\nYour final score was {}".format(points))
    print("Your 'points per round' score was {}".format(round(points / num_rounds, 2)))

    input("\nPress enter to return to the menu")


def generate_letters():
    """
    Generates random 9-length list of letters
    Samples letters based on their frequency in english (like scrabble).

    :return: 9 random letters, at least 3 vowels and 4 consonants
    :rtype: list
    """
    vowels_list = 'eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooouuuu'
    consonants_list = 'nnnnnnrrrrrrttttttllllssssddddgggbbccmmppffhhvvwwyykjxqz'
    n_vowels = random.randint(3, 5)
    vowels = random.sample(vowels_list, n_vowels)
    consonants = random.sample(consonants_list, 9 - n_vowels)
    letters = vowels + consonants
    random.shuffle(letters)
    return letters


def get_word_points(given_letters, user_str):
    """
    Determines if the user-entered string is a valid word, and can be made with the given letters.

    :param given_letters: 9 letters that valid words are constructed from
    :type given_letters: str
    :param user_str: A word to test
    :type user_str: str
    :return: The number of points a word is worth, based on length
    :rtype: int
    """

    for letter in user_str:
        if letter in given_letters:
            given_letters = given_letters.replace(letter, "", 1)
        else:
            print("That is not a valid combination of letters")
            return 0

    sorted_user_str = ''.join(sorted(user_str))
    if sorted_user_str in valid_words:
        if user_str in valid_words[sorted_user_str]:
            points = len(user_str)
            print("Nice! Your word '{}' is worth {} points".format(user_str, points))
            return points
    print("Not a valid word, Sorry")
    return 0


def solve(letters):
    """
    Function to return the 'winning' countdown words
    for a given string of letters.

    :param letters: A string or list of given letters for a round
    :type letters: list or str
    :rtype: None
    """
    letters = sorted(letters)
    for length in range(3, 10):
        found_words = set()
        for combined_letters in combinations(letters, length):
            sorted_word = ''.join(combined_letters)
            if sorted_word in valid_words:
                for word in valid_words[sorted_word]:
                    found_words.add(word)
        if len(found_words) > 0:
            print('\nLooking for {} letter words...\n'.format(length))
            found_words_string = ', '.join(sorted(found_words))
            print(found_words_string)
        else:
            print("\nNo {} letter words found".format(length))


def conundrum():
    """
    Handles game and input structure for the conundrum game
    Outsources selection of conundrum word and creation of anagrams.
    """
    anagrams = None
    while anagrams is None:
        conundrum_word = random_nine_letter()
        conundrum_str = ''.join(conundrum_word)
        anagrams = make_two_anagrams(conundrum_word)
    print("\nYour phrase is: '{}'\n".format(anagrams))

    user_ans = timed_input("Enter the nine-letter word", ANSWER_TIME)
    alt_solutions = conundrum_solutions(conundrum_str)
    if user_ans is None:
        print("Sorry, you didn't enter in time")
    else:
        if user_ans == conundrum_str:
            print("Nice! You got it!")
        elif user_ans in alt_solutions:
            print("Nice! You found an alternate solution!")
        else:
            print("That isn't it, sorry")

    if get_choice("Would you like to see the answer/s? (y/n): ", "y", "n") == "y":
        print("\nThe word was: '{}'".format(conundrum_str))
        if len(alt_solutions) > 0:
            print("\nThe alternate solutions were:\n")
            [print(word) for word in alt_solutions]
        else:
            print("There are no alternate solutions")

    input("\nPress enter to continue")


def conundrum_solutions(conundrum_str):
    """
    Finds alternate conundrum solutions for a word/letter sequence

    :param conundrum_str: conundrum word to find alternate solutions (anagrams) for
    :type conundrum_str: str
    :return: Alternate solutions, not including original word
    :rtype: list
    """
    alt_solutions = []
    sorted_conundrum_string = ''.join(sorted(conundrum_str))
    for word in valid_words[sorted_conundrum_string]:
        if word != conundrum_str:
            alt_solutions.append(word)
    return alt_solutions


def random_nine_letter():
    """
    Chooses and returns a random 9 letter word from the dictionary

    :return: 9 letter word
    :rtype: list
    """
    nine_letter_list = []
    for key in valid_words:
        if len(key) == 9:
            for word in valid_words[key]:
                nine_letter_list.append(word)
    chosen = list("".join(random.sample(nine_letter_list, 1)[0]))
    return chosen


def make_two_anagrams(letter_list):
    """
    Makes two English words which are a combined anagram of the letter_list

    :param letter_list: 9-length list of letters
    :type letter_list: list
    :return: Two English words which are a combined anagram of the letter_list, separated by ' '
    :rtype: str
    """
    word_string = ''.join(letter_list)
    sorted_word = sorted(letter_list)
    found_anagrams = set()
    for length in range(3, 5):
        for word in combinations(sorted_word, length):
            word1 = ''.join(word)
            word2 = ''.join(list((Counter(sorted_word) - Counter(
                word1)).elements()))  # sets word2 equal to all letters from the word that are not already in word1
            if check_word_in_dict(word1) and check_word_in_dict(word2):
                for x in list(valid_words[word1]):
                    for y in list(valid_words[word2]):
                        if x not in word_string and y not in word_string:  # prevents easy anagrams like 'sun' and 'flower' for 'sunflower'
                            found_anagrams.add(str(x + " " + y))
    try:
        return random.sample(found_anagrams, 1)[0]
    except ValueError:
        return  # repeat while loop on line 201 if no anagrams are found (chooses a new word)


def check_word_in_dict(word):
    """
    Checks whether or not a word is present in the dictionary

    :param word: desired word to check
    :type word: str
    :rtype: bool
    """
    if word in valid_words:
        return True
    else:
        return False


def timed_input(msg, t):
    """
    Prompts input using a message, returning none if the user does not enter an answer in t seconds.

    :param msg: Message to be displayed alongside live timer
    :type msg: str
    :param t: Number of seconds the user has for answering.
    :type t: int
    :return: User-entered answer
    :rtype: str
    """
    start_time = time.time()
    user_ans = input("{} - you have {} seconds: ".format(msg, t)).strip().lower()
    if time.time() - start_time > t:
        return
    else:
        return user_ans


def get_choice(msg, x, y):
    """
    Ensures that the user response to msg parameter is either x or y. Repeats otherwise.
    x and y parameters should be lowercase with no surrounding spaces

    :param msg: Message to be displayed when asking for choice
    :type msg: str
    :param x: Valid choice
    :type x: str
    :param y: Other valid choice
    :type y: str
    :return: Choice, either x or y
    :rtype: str
    """
    choice = input(msg).strip().lower()
    while choice != x and choice != y:
        print("Not a valid input, please try again")
        choice = input(msg).strip().lower()
    return choice


def get_pos_int(msg,):
    """
    Used to validate a positive integer. Will repeat if entered number is a string or if the entered number is < 0

    :param msg: prompt shown to user when asking for a positive integer
    :type msg: str
    :return: Chosen positive integer
    :rtype: int
    """
    while True:
        try:
            num = float(input(msg))
            if num <= 0 or int(num) != num:
                print("Please enter a positive integer")
            else:
                return int(num)
        except ValueError:
            print("Please enter a positive integer")


intro()
menu()
