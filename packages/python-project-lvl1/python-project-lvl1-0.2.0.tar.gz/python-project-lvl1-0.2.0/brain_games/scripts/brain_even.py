#!/usr/bin/env python


import prompt
import random


def main():
    print('Welcome to the Brain Games!')
    name = prompt.string('May I have your name? ')
    print('Hello, ' + name + '!')
    print('Answer "yes" if the number is even, otherwise answer "no".')

    for i in range(0, 3):
        value = random.randint(1, 100)

        print('Question: ', value)
        check = prompt.string('Your answer: ')
        if (value % 2) == 0 and check == 'yes':
            print('Correct!')
        elif (value % 2) == 1 and check == 'no':
            print('Correct!')
        else:
            print("'yes' is wrong answer ;(. Correct answer was 'no'.\n",
                  "Let's try again, " + name + '!')
            break

    print('Congratulations, ' + name + '!')


if __name__ == '__main__':
    main()
