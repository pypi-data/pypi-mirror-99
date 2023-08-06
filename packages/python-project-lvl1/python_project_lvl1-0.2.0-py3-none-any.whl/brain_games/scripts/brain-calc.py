#!/usr/bin/env python


import prompt
import random


def main():
    print('Welcome to the Brain Games!')
    name = prompt.string('May I have your name? ')
    print('Hello, ' + name + '!')
    print('What is the result of the expression?')

    for i in range(0, 3):
        value1 = random.randint(1, 100)
        value2 = random.randint(1, 100)
        symbol = random.choice(['+', '-', '*'])

        print('Question: ', str(value1) + str(symbol) + str(value2))
        check = prompt.integer('Your answer: ')

        if symbol == '+':
            if value1 + value2 == check:
                print('Correct!')
            else:
                print(check + " is wrong answer ;(. Correct answer was " + value1+value2 + '\n',
                      "Let's try again, " + name + "!")
        if symbol == '-':
            if value1 - value2 == check:
                print('Correct!')
            else:
                print(check + " is wrong answer ;(. Correct answer was " + value1 - value2 + '\n',
                      "Let's try again, " + name + "!")
        if symbol == '*':
            if value1 * value2 == check:
                print('Correct!')
            else:
                print(check + " is wrong answer ;(. Correct answer was " + value1 * value2 + '\n',
                      "Let's try again, " + name + "!")
        else:
            print("'yes' is wrong answer ;(. Correct answer was 'no'.\n",
                  "Let's try again, " + name + '!')
            break

    print('Congratulations, ' + name + '!')


if __name__ == '__main__':
    main()
