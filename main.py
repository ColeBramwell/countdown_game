import random


def generate_letters():
    vowels = ['a', 'e', 'i', 'o', 'u']
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    given_letters = []
    for i in range(9):
        temp = [vowels, consonants][random.random() > 0.3]
        given_letters.append(temp[random.randint(0, len(temp))-1])
    print(''.join([str(letter) for letter in given_letters]))
    return


generate_letters()

