import random

print("Welcome to the Heads or Tails game!")
print("I will flip a coin, and you have to guess whether it will land on heads or tails.")
print("Enter 'H' for heads or 'T' for tails.")

coin = random.choice(["H", "T"])
guess = input("Your guess: ")

if guess == coin:
    print("You guessed it! The coin landed on", coin)
else:
    print("Sorry, the coin landed on", coin)

