import random


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


def generate_letters():
    """
    This function generates a length-9 list of letters, at least 3 vowels and 4 consonants.
    It samples letters based on their frequency in english (like scrabble)
    """
    vowels_list = 'eeeeeeeeeeeeaaaaaaaaaiiiiiiiiioooooooouuuu'
    consonants_list = 'nnnnnnrrrrrrttttttllllssssddddgggbbccmmppffhhvvwwyykjxqz'
    n_vowels = random.randint(3,5)
    vowels = random.sample(vowels_list, n_vowels)
    consonants = random.sample(vowels_list, 9 - n_vowels)
    letters = vowels + consonants
    random.shuffle(letters)
    return letters


intro()
menu()

