import random
from itertools import combinations
import pickle
import time


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
        letters_game(generate_letters())
    elif choice == "2":
        print("Thanks for playing!")
        return
    else:
        print("That is not a valid input")
    menu()


def letters_game(letters):
    """
    Function handles the main structure for the 'letters round' game
    """
    letters_str = ''.join([str(elem) for elem in letters])
    print("\nYour letters are:\n")
    print(letters_str, "\n")
    timer(30, letters_str)
    solve(letters)


def generate_letters():
    """
    This function generates a length-9 list of letters, at least 3 vowels and 4 consonants.
    It samples letters based on their frequency in english (like scrabble)
    """
    vowels_list = 'eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooouuuu'
    consonants_list = 'nnnnnnrrrrrrttttttllllssssddddgggbbccmmppffhhvvwwyykjxqz'
    n_vowels = random.randint(3,5)
    vowels = random.sample(vowels_list, n_vowels)
    consonants = random.sample(consonants_list, 9 - n_vowels)
    letters = vowels + consonants
    random.shuffle(letters)
    return letters


def solve(letters):
    """
    Function to return the 'winning' countdown words
    for a given string of letters.
    """
    valid_words = pickle.load(open('word_dict.p', 'rb'))
    letters = sorted(letters)
    for length in range(5, 10):
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
    function to count down from t seconds, mimicking the clock in the game show
    """
    while t:
        mins, secs = divmod(t, 60)
        time_format = '{:02d}:{:02d}'.format(mins, secs)
        print(game_txt, "---", time_format)
        time.sleep(1)
        t -= 1
    print("Time Up!")


intro()
menu()

