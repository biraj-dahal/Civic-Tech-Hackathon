
questions = {
  'What is the capital of France?': 'Paris',
  'What is the largest planet in our solar system?': 'Jupiter',
  'Who wrote the Harry Potter series?': 'J.K. Rowling',
  'What is the smallest country in the world?': 'Vatican City',
  'What is the currency of Japan?': 'Yen'
}

score = 0
for question, value in questions.items():
  answer = input(question + ' ')
  if answer.lower() == questions[question].lower():
    print('Correct!')
    score += 1
  else:
    print('Incorrect! The correct answer was ' + questions[question])
print('You scored ' + str(score) + ' out of ' + str(len(questions)) +
      ' questions!')

