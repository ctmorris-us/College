#CS Lab 5
'''
Write a code segment using a FOR loop that prints multiples of 5 from 5 to 500, one on a line.
'''

for val in range(5,505,5):
    print(val, end = ' ')

'''
Question 24 : 4 points
Write code segment that prompts the user for a letter from ’a-z’.
As long as the character is not between ’a-z’, the user should be given a message and prompted again for a letter between
’a-z’. Make sure not to accept words that start with letters. You should reject a word like robot.
'''
#
while True:
    val = input('Input a letter from (a-z):\n')
    if (len(val) == 1) and ('a' <= val <= 'z'):
        break
    else:
        print('Your input was invalid. Please try again.')
        continue

'''
For number between and including 1 to 100, if the number is divisible by 3, print out 'Fizz', else if the number is divisible by 5,
print out 'Buzz', if both print out 'Fizzbuzz'
'''
#
while True:
    num = float(input('Please input a number between 1 to 100 inclusive:\n'))
    if 1 <= num <= 100:
        break
    else:
        print('Invalid.')
        continue

num = float(input('Please input a number between 1 to 100 inclusive:\n'))
if num % 3 == 0:
    print('Fizz', end = '')
if num % 5 == 0:
    print('Buzz', end = '')
if (num % 3 != 0) and (num % 5 != 0):
    print('Not divisible by 3 and 5')
print()
