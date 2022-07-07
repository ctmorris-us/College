#Cs Lab 4

'''
Write the code for an if statement that adds 5 to the variable num1 if the value stored in the variable testA equals 25.
Otherwise subtract 5 from num1.

'''
testA = float(input('Please input a value:\n'))
num1 = 0
if testA == 25:
    num1 += 5
else:
    num1 -= 5
print(num1)


'''
Write a Python program that prompts the user for a word.
If the word comes between the words apple and pear alphabetically,
print a message that tells the user that the word is valid, otherwise,
tell the user the word is out of range.
'''

word = input('Please input a word:\n')
if 'apple' < word < 'pear':
    print('Your word is valid.')
else:
    print('Your word is out of range.')

'''
Write a Python program that prompts the user for the cost of two items to be purchased.
Then prompt the user for payment. If the amount entered is less than the total cost of the two items,
print a message that states how much is still owed. Otherwise, print a thank you message and state how much change will be given.

'''

price1 = float(input('Please input the price of the first item:\n'))
price2 = float(input('Please input the price of the second item:\n'))
payment = float(input('Please input payment:\n'))

if payment < (price1 + price2):
    print('You still owe ${}'.format(price1 + price2 - payment))
else:
    print('Thank you for your service. Your change is ${}'.format(payment - price1 - price2))

'''
Write a Python program that prompts the user for a multiple of 5 between 1 and 100.
Print a message telling the user whether the number they entered is valid.
'''
num1 = float(input('Input a number that is a multiple of 5 between 1 and 100:\n'))
if (1 < num1 < 100) and (num1 % 5 == 0):
    print('Valid')
else:
    print('Invalid')
