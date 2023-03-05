# Homework 2
# Priyesh Patel -PHP180002
# This program reads a raw text file and get the most popular nouns
# within the text using the NLTK library. After getting the nouns
# a simple word guessing games is played using the nouns


import sys
import nltk
import random
import pathlib
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords


def preprocess(data):
    # Input: raw data of strings
    # Return: list of tokens from original data
    #         list of nouns from the tokens

    # tokenize the raw data
    tokens = word_tokenize(data)

    # calculate the lexical diversity by dividing unqiue words from total
    print('Original Text - Lexical Diversity %.2f' % (len(set(tokens)) / len(tokens)))

    # lower case the tokens
    tokens = [token.lower() for token in tokens]

    # reduced tokens to only alpha, not in the NLTK stopword list, and length greater than 5
    tokens = [token for token in tokens if token.isalpha() and
              token not in stopwords.words('english') and
              len(token) > 5]

    # get lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(token) for token in tokens]

    # get unique lemmas
    unique_lemmas = list(set(lemmas))

    # print the first 20 tagged tokens
    tagged_token = nltk.pos_tag(unique_lemmas)
    print(tagged_token[:20])

    nouns = []

    # get all nouns from the tagged tokens
    for word, pos in tagged_token:
        if pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS':
            nouns.append(word)

    print('The number of tokens: ', len(tokens))
    print('The number of nouns: ', len(nouns))
    return tokens, nouns


def guessing_game(words):
    # Input: list of words that are possible in the game

    # the current score starts at 5
    print('Let\'s play a word guessing game!')
    score = 5

    # completed track if the current word has been guessed
    completed = True
    while score > 0:

        if completed:
            # get random word and set completed to false
            random_word = random.choice(words)
            guess = ['_'] * len(random_word)
            attempts = []
            completed = False
            #print(random_word) # testing purposes
            for char in guess:
                print(char, end=" ")

        user_guess = input('\nGuess a letter: ')

        # user want to quit
        if user_guess == '!':
            print('Game Ended!')
            break

        # guess was correct
        if user_guess in random_word and user_guess not in attempts:
            index = 0
            for char in random_word:
                if char == user_guess:
                    guess[index] = user_guess
                index += 1
            attempts.append(user_guess)
            score += 1
            print("Right! Score is ", score)

        # character was already picked
        elif user_guess in attempts:
            print("Already Guessed", user_guess, 'Score is', score)

        # guess is incorrect
        else:
            score -= 1
            attempts.append(user_guess)
            if score == 0:
                print('Sorry game over! Score is ', score)
            else:
                print('Sorry, guess again. Score is ', score)

        # print current guess
        for char in guess:
            print(char, end=" ")

        # check if completed
        if '_' not in guess:
            print('\nYou solved it!')
            print('\nGuess another word')
            completed = True


if __name__ == '__main__':
    # Check if user enter at least two arguments, if not display error and quit
    if len(sys.argv) < 2:
        print('Error: Please enter a filename as a system argument')
        quit()

    # get data file
    relativePath = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(relativePath), 'r') as file:
        raw_text = file.read()

    # get tokens and nouns from raw data file
    tokens, nouns = preprocess(raw_text)

    # calculate number of times a noun occurred
    noun_dict = {}
    for noun in tokens:
        if noun in set(nouns):
            noun_dict[noun] = noun_dict.get(noun, 0) + 1

    # sort nouns by popularity
    popular_nouns = []
    for noun in sorted(noun_dict, key=noun_dict.get, reverse=True)[:50]:
        print(noun, ':', noun_dict[noun])
        popular_nouns.append(noun)

    print()
    # play game with most popular nouns
    guessing_game(popular_nouns)




