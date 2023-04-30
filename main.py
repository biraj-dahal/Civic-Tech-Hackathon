import os
import openai
from flask import Flask, render_template, redirect, request # Import Flask Class
app = Flask(__name__) # Create an Instance
openai.api_key = "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"
@app.route('/') # Route the Function
def topics(): # Run the function
	return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
    return render_template("html_temp.html")

@app.route('/beginner', methods=["GET", "POST"])
def play():
  level = "Coin Flip (beginner)"
  problem_statement = "Your mission is to create a coin flipping game with the chance of getting a heads or a tails being random"
  python_tutor_link = "https://tinyurl.com/yu8cm293"
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Explain the following python program:\n\nnum = input(\"Enter an integer: \")\nif num % 2 == 0:\n    print(\"It is even!\")\nelse:\n    print(\"It is odd!\")\n\n",
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
  open_ai_explanation = response["choices"][0]["text"]
  return render_template("play.html", level=level, problem_statement=problem_statement, open_ai_explanation=open_ai_explanation,python_tutor_link=python_tutor_link)

@app.route('/intermediate', methods=["GET", "POST"])
def intermediate():
  level = "Trivia (intermediate)"
  problem_statement = "Your mission is to create a trivia game asking for 5 correct questions!"
  python_tutor_link = "https://tinyurl.com/5dps6pms"
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Explain the following python program:\n\nnum = input(\"Enter an integer: \")\nif num % 2 == 0:\n    print(\"It is even!\")\nelse:\n    print(\"It is odd!\")\n\n",
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
  open_ai_explanation = response["choices"][0]["text"]
  return render_template("intermediate.html", level=level, problem_statement=problem_statement, open_ai_explanation=open_ai_explanation, python_tutor_link=python_tutor_link)

@app.route('/hard', methods=["GET", "POST"])
def hard():
  level = "Wordle (hard)"
  problem_statement = "Your goal here is to guess the word in 5 tries or less. Everytime you guess you will be given a hint at what letters are and aren't in the secret word."
  python_tutor_link = "https://tinyurl.com/56z3f5v4"
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Explain the following python program:\n\nnum = input(\"Enter an integer: \")\nif num % 2 == 0:\n    print(\"It is even!\")\nelse:\n    print(\"It is odd!\")\n\n",
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
  open_ai_explanation = response["choices"][0]["text"]
  return render_template("hard.html", level=level, problem_statement=problem_statement, open_ai_explanation=open_ai_explanation,python_tutor_link=python_tutor_link)  

@app.route('/explanation', methods=["GET", "POST"])
def explanation():
  if request.method == "POST":
    print("hello, world!")
    code = request.form.get("code")
    prompt = "compare the following 2 python programs:\n\npython program 1: \nimport random\n\nprint(\"Welcome to the Heads or Tails game!\")\nprint(\"I will flip a coin, and you have to guess whether it will land on heads or tails.\")\nprint(\"Enter 'H' for heads or 'T' for tails.\")\n\ncoin = random.choice([\"H\", \"T\"])\nguess = input(\"Your guess: \")\n\nif guess == coin:\n    print(\"You guessed it! The coin landed on\", coin)\nelse:\n    print(\"Sorry, the coin landed on\", coin)\n\npython program 2:\n\n\n" + code
    response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
  open_ai_explanation = response["choices"][0]["text"]
  return render_template("explanation.html", open_ai_explanation=open_ai_explanation)
  
  
@app.route('/explanation2', methods=["GET", "POST"])
def explanation2():
  if request.method == "POST":
    print("hello, world!")
    code = request.form.get("code")
    prompt = "compare the following 2 python programs:\n\npython program 1: \nquestions = {\n  'What is the capital of France?': 'Paris',\n  'What is the largest planet in our solar system?': 'Jupiter',\n  'Who wrote the Harry Potter series?': 'J.K. Rowling',\n  'What is the smallest country in the world?': 'Vatican City',\n  'What is the currency of Japan?': 'Yen'\n}\n\nscore = 0\nfor question, value in questions.items():\n  answer = input(question + ' ')\n  if answer.lower() == questions[question].lower():\n    print('Correct!')\n    score += 1\n  else:\n    print('Incorrect! The correct answer was ' + questions[question])\nprint('You scored ' + str(score) + ' out of ' + str(len(questions)) +\n      ' questions!')\n\npython program 2:\n\n\n" + code
    response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
  open_ai_explanation = response["choices"][0]["text"]
  return render_template("explanation.html", open_ai_explanation=open_ai_explanation)

@app.route('/explanation3', methods=["GET", "POST"])
def explanation3():
  if request.method == "POST":
    print("hello, world!")
    code = request.form.get("code")
    prompt = "compare the following 2 python programs:\n\npython program 1: \ndef print_in_color(letter, color):\n  text = ''\n  if color == 'red':\n    text = '\\u001b[31m' + letter + '\\u001b[0m'\n  elif color == 'green':\n    text = '\\u001b[32m' + letter + '\\u001b[0m'\n  elif color == 'yellow':\n    text = '\\u001b[33m' + letter + '\\u001b[0m'\n  else:\n    print(\"Color is not supported\")\n    return None\n  print(text, end=\"\")\n  return text\n\n\ndef print_guess(secret_word, guess):\n    index = 0\n    required_letters=[]\n    for charac in guess:\n        if (charac == secret_word[index]):\n            required_letters.append(charac)\n            print_in_color(charac, 'green')\n        elif charac not in secret_word:\n            print_in_color(charac, 'red')\n        else:\n            required_letters.append(charac)\n            print_in_color(charac, 'yellow')\n        index += 1\n    return(required_letters)\n\n\n\ndef is_valid_guess(guess, required_letters):\n    for letter1 in required_letters:\n        if letter1 not in guess:\n            return False\n    return True\n\ndef is_game_over(secret_word, guess, tries_left):\n    if secret_word == guess :\n        print(f\"Correct! You got it in {6-tries_left} tries!\")\n        return True\n    elif tries_left <= 0 :\n        print(f\"Game over! The correct word is {secret_word}.\")\n        return True\n    else:\n        print(f\"Incorrect! You have {tries_left} tries left.\")\n        return False\n\ndef get_guess(required_letters):\n  while True:\n    guess = input(\"Enter your guess: \\n\").strip().upper()\n    if len(guess) < len_secret_word:\n        print(\"Length of guess is less than secret word.\")\n        print(\"Actual length of secret word is \", len_secret_word)\n    elif len(guess) > len_secret_word:\n        print(\"Length of guess is greater than secret word.\")\n        print(\"Actual length of secret word is \", len_secret_word)\n    if is_valid_guess(guess, required_letters):\n        return guess\n    else:\n        print(\"Your guess must contain all yellow and green letters from your previous guesses.\")\n        \n\ntries_left = 6 \nsecret_word = input(\"Enter the secret word: \").strip().upper()\nlen_secret_word = len(secret_word)\n\nrequired_letters=[]\n\nwhile True :\n  tries_left -= 1\n  guess = get_guess(required_letters)\n  if is_game_over(secret_word, guess, tries_left):\n    break\n  required_letters = print_guess(secret_word, guess)\n  print()\n\npython program 2:\n\n\n" + code
    response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  temperature=0.6,
  max_tokens=150,
  top_p=1,
  frequency_penalty=1,
  presence_penalty=1
)
  open_ai_explanation = response["choices"][0]["text"]
  return render_template("explanation.html", open_ai_explanation=open_ai_explanation)

  
  
# @app.route('/register', methods=["GET", "POST"])
# def register():
#   return render_template("html_temp.html")

# @app.route('/beginner', methods=["GET", "POST"])
# def beginner():
#   return render_template("beginner.html")
  
# @app.route('/intermediate', methods=["GET", "POST"])
# def intermediate():
#   return render_template("intermediate.html")
  
# @app.route('/advanced', methods=["GET", "POST"])
# def advanced():
#   return render_template("advanced.html")

app.run(host='0.0.0.0', port=8000, debug=True) # Run the Application (in debug mode)