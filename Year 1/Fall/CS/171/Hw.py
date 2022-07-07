#Python Lab 1
#1/11/19
print('Hello.')

num = input('Pick a secret number between 0 and 100.')
print()

def user_input():
    while True:
        x = input('Enter yes/higher/lower:\n')
        if x == 'yes' or x == 'higher' or x == 'lower':
            return x
        else:
            print('I did not understand.')
            print('Is your secret number', guess)


low = 0
high = 101
guess = 50

while True:
    print('Is your secret number', guess)
    user_response = user_input()
    if user_response == 'yes':
        print('Great!')
        break
    elif user_response == 'higher':
        low = guess
        guess = ((high - guess) // 2) + guess
    elif user_response == 'lower':
        high = guess
        guess = ((guess - low) // 2) + low
    print('Next is', guess)
    
# print('Solve the Two Trains Problem.')
# first_speed = int(input('Enter First Speed:\n'))
# first_place = input('Enter First Place:\n')
# second_speed = int(input('Enter Second Speed:\n'))
# second_place = input('Enter Second Place:\n')
# total_dist = int(input('Enter total distance:\n'))
# meet_time = total_dist / (first_speed + second_speed)
#
# print('Word Problem')
# print('Train A, traveling {} miles per hour, leaves {} heading toward {} , {} miles away.'.format(first_speed, first_place, second_place, total_dist) +
# ' At the same time Train B, traveling {} mph, leaves {} heading toward {} .'.format(second_speed, second_place, first_place)+
# ' When do the two trains meet? How far are they from each city?')
# print('Answers')
# print('They meet after {} hours.'.format(round(meet_time, 2)))
# print('Train A is {} miles from {}'.format(round(meet_time*first_speed,2), first_place))
# print('Train B is {} miles from {}'.format(round(meet_time*second_speed,2), second_place))

# check_value = float(input('Enter Check Value as a decimal:\n'))
# check_value *= 100
# print('Twenties: {}'.format(int(check_value//2000)))
# check_value %= 2000
# print('Tens: {}'.format(int(check_value//1000)))
# check_value %= 1000
# print('Fives: {}'.format(int(check_value//500)))
# check_value %= 500
# print('Ones: {}'.format(int(check_value//100)))
# check_value %= 100
# print('Quarters: {}'.format(int(check_value//25)))
# check_value %= 25
# print('Dimes: {}'.format(int(check_value//10)))
# check_value %= 10
# print('Nickels: {}'.format(int(check_value//5)))
# check_value %= 5
# print('Pennies: {}'.format(int(check_value//1)))





# itemName1 = input('Enter food item name:\n')
# itemPrice1 = float(input('Enter item price:\n'))
# itemQuant1 = int(input('Enter item quantity:\n'))
# totalPrice = itemPrice1 * itemQuant1
#
# print('\nRECEIPT')
# print('{} {} @ $ {} = $ {}'.format(itemQuant1, itemName1, itemPrice1, itemQuant1*itemPrice1))
# print('Total cost: $ {}\n'.format(itemQuant1*itemPrice1))
#
# itemName2 = input('\nEnter second food item name:\n')
# itemPrice2 = float(input('Enter item price:\n'))
# itemQuant2 = int(input('Enter item quantity:\n'))
# totalPrice += itemPrice2 * itemQuant2
#
# print('\nRECEIPT')
# print('{} {} @ $ {} = $ {}'.format(itemQuant1, itemName1, itemPrice1, itemQuant1*itemPrice1))
# print('{} {} @ $ {} = $ {}'.format(itemQuant2, itemName2, itemPrice2, itemQuant2*itemPrice2))
# print('Total cost: $ {}'.format(totalPrice))
#
# print('\n15% gratuity: $ {}'.format(totalPrice * .15))
# print('Total with tip: $ {}'.format(totalPrice * .15 + totalPrice))


# print('RECEIPT')
# for food_list in cart:
#     print('{} {} @ $ {} = $ {}'.format(food_list[2], food_list[0], food_list[1], food_list[1] * food_list[2]))
# print('Total cost: $ {}'.format(sum(item[1] * item[2] for item in cart)))

# cart_total = sum(item[1] * item[2] for item in cart) * .15

# print('15% gratuity: $ {}'.format(sum(cart_total * .15)))
# print('Total with tip: $ {}'.format(sum(cart_total * .15 + cart_total)))



# FIXME (2): Read in a second food item name, price, and quantity, then output a second receipt

# FIXME (3): Add a gratuity and total with tip to the second receipt





# animal = input('Please type the name of an animal. ')
# color = input('Please type the name of a color. ')
# vehicle = input('Please type the name of a vehicle. ')
# city = input('Please type the name of a city. ')
# print('The', color, animal, 'drove the', vehicle, 'to', city + '.' )


# a = int(input('Enter integer a:\n'))
# b = int(input('Enter integer b:\n'))

# lemonJuiceCups = float(input('Enter amount of lemon juice (in cups):\n'))
# waterCups = float(input('Enter amount of water (in cups):\n'))
# agaveCups = float(input('Enter amount of agave nectar (in cups):\n'))
# servings = float(input('How many servings does this make?\n'))
#
#
# print('\nLemonade ingredients - yields {} servings'.format(servings))
# print('{} cup(s) lemon juice\n{} cup(s) water\n{} cup(s) agave nectar'.format(lemonJuiceCups, waterCups, agaveCups))
#
# servings_make = float(input('\nHow many servings would you like to make?\n'))
#
# lemonJuiceCups *= servings_make/servings
# waterCups *= servings_make/servings
# agaveCups *= servings_make/servings
#
# print('\nLemonade ingredients - yields {} servings'.format(servings_make))
# print('{} cup(s) lemon juice\n{} cup(s) water\n{} cup(s) agave nectar\n'.format(lemonJuiceCups, waterCups, agaveCups))
#
# lemonJuiceCups /= 16
# waterCups /= 16
# agaveCups /= 16
#
# print('Lemonade ingredients - yields {} servings'.format(servings_make))
# print('{} gallon(s) lemon juice\n{} gallon(s) water\n{} gallon(s) agave nectar'.format(lemonJuiceCups, waterCups, agaveCups))

# FIXME (3): Convert the integer to a characer, and output that character


# print('a+b=', a+b)
# print('a-b=', a-b)
# print('b-a=', b-a)
# print('a*b=', a*b)
# print('a/b=', a/b)
# print('a//b=', a//b)
# print('a%b=', a%b)
# print('a**b=', a**b)
# print(' (a*b) ** (a+b)=', (a*b) ** (a+b))
