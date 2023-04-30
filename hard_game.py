def print_in_color(letter, color):
  text = ''
  if color == 'red':
    text = '\u001b[31m' + letter + '\u001b[0m'
  elif color == 'green':
    text = '\u001b[32m' + letter + '\u001b[0m'
  elif color == 'yellow':
    text = '\u001b[33m' + letter + '\u001b[0m'
  else:
    print("Color is not supported")
    return None
  print(text, end="")
  return text


def print_guess(secret_word, guess):
    index = 0
    required_letters=[]
    for charac in guess:
        if (charac == secret_word[index]):
            required_letters.append(charac)
            print_in_color(charac, 'green')
        elif charac not in secret_word:
            print_in_color(charac, 'red')
        else:
            required_letters.append(charac)
            print_in_color(charac, 'yellow')
        index += 1
    return(required_letters)



def is_valid_guess(guess, required_letters):
    for letter1 in required_letters:
        if letter1 not in guess:
            return False
    return True

def is_game_over(secret_word, guess, tries_left):
    if secret_word == guess :
        print(f"Correct! You got it in {6-tries_left} tries!")
        return True
    elif tries_left <= 0 :
        print(f"Game over! The correct word is {secret_word}.")
        return True
    else:
        print(f"Incorrect! You have {tries_left} tries left.")
        return False

def get_guess(required_letters):
  while True:
    guess = input("Enter your guess: \n").strip().upper()
    if len(guess) < len_secret_word:
        print("Length of guess is less than secret word.")
        print("Actual length of secret word is ", len_secret_word)
    elif len(guess) > len_secret_word:
        print("Length of guess is greater than secret word.")
        print("Actual length of secret word is ", len_secret_word)
    if is_valid_guess(guess, required_letters):
        return guess
    else:
        print("Your guess must contain all yellow and green letters from your previous guesses.")
        

tries_left = 6 
secret_word = input("Enter the secret word: ").strip().upper()
len_secret_word = len(secret_word)

required_letters=[]

while True :
  tries_left -= 1
  guess = get_guess(required_letters)
  if is_game_over(secret_word, guess, tries_left):
    break
  required_letters = print_guess(secret_word, guess)
  print()

