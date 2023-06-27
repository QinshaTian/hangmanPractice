import requests
import string
import random
# Requests library required

hangmanPic = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

hardCodedWords = 'appear border dinner detect burden county'.split(" ")
LETTERS = string.ascii_letters # Alphabet

def randomWord(useOnlineVersion):
    # Pull random word from the website or use hard coded words
    if useOnlineVersion:
        word = requests.get("https://random-word-api.herokuapp.com/word?length=6%").json()[0].lower()
    else:
        word = hardCodedWords[random.randint(0, len(hardCodedWords)-1)]
    return word

def info(missedChar, unknown):
    # Show info to the player
    print(hangmanPic[len(missedChar)])
    print(unknown)
    print(f"\nLetters not in the word: [{' '.join(missedChar)}]")

def hint(answer, unknown):
    # Give a hint
    print("\nDo you need a hint? (y/n)")
    if input().lower().startswith("y"):
            coveredIdx = []
            for i in range(len(unknown)):
                    if unknown[i] == "_":
                        coveredIdx.append(i)
            randomHintIdx = coveredIdx[random.randint(0, len(coveredIdx) - 1)]
            unknown = unknown[:randomHintIdx] + answer[randomHintIdx] + unknown[randomHintIdx+1:]
            print(f"Hint: The letter '{answer[randomHintIdx]}' is in the word.")
    return unknown

def hangman(word):
    answer = word
    unknown = "_" * len(answer)
    missedChar = []
    guessedChar = []
    hintGiven = False

    info(missedChar, unknown)

    while True:
        print ("\nLet's guess a letter:")
        guess = input().lower()

        if len(guess) != 1:
            print ("Hey! Let's guess one at a time :D")

        elif guess not in LETTERS:
            print (f"'{guess}'is not an alphabet, please try agian.")
            
        elif guess in guessedChar:
            print (f"You already guessed'{guess}', please try again.")

        elif guess not in answer:
            missedChar.append(guess)
            print(f"'{guess}'is not in the word.")
            info(missedChar,unknown)

        else:
            # Replace - to letter
            for i, letter in enumerate(answer):
                if guess == letter:
                    unknown = unknown[:i] + letter + unknown[i+1:]
            info(missedChar,unknown)
            print(f"\nYay! '{guess}'is in the word!")

        guessedChar.append(guess)

        # Check wether finished the game 
        if unknown == answer:
            print(f"\nYes! The answer is '{answer}'. You made it!")
            break
        elif len(missedChar) >= len(hangmanPic) - 1:
            print(f"\nAwww...Game over, the answer is '{answer}'.")
            break

        # Check wether hint
        if len(missedChar) == 4 and not hintGiven:
            unknown = hint(answer, unknown)
            hintGiven = True


def playAgain():
    # Ask the player
    print("\nDo you want to play again? (y/n)")
    return input().lower().startswith("y")

if __name__ == "__main__":
    print("Online word list or local word list? (o/l)")
    useOnlineVersion = False
    if input().lower().startswith("o"):
        useOnlineVersion = True
    # Keep playing if the player wish to play again
    word = randomWord(useOnlineVersion)
    hangman(word)
    while playAgain():
        hangman(word)