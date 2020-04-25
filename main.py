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
    print("|2) Play 'Conundrum'         |")
    print("|3) Quit program             |")
    print("|----------------------------|")

    choice = input("\nPlease enter a number between 1 and 2: ")
    if choice == "1":
        generate_letters()
    elif choice == "2":
        print("Thanks for playing!")
        return
    else:
        print("That is not a valid input")
    menu()


def generate_letters():
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    given_letters = []
    for i in range(9):
        temp = [vowels, consonants][random.random() > 0.3]
        given_letters.append(temp[random.randint(0, len(temp))-1])
    print(''.join([str(letter) for letter in given_letters]))
    return


intro()
menu()

