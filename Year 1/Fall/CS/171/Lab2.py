# Lab 2 Worksheet

hamburgerNum = int(input('Please input the number of hamburgers ($2.00) you would like:\n'))
friesNum = int(input('Please input the number of fries ($1.50) you would like:\n'))
drinkNum = int(input('Please input the number of drinks ($1.00) you would like:\n'))

print('\t{} Hamburgers: ${:10.2f}'.format(hamburgerNum, hamburgerNum * 2.0))
print('\t{} Fries: ${:15.2f}'.format(friesNum, friesNum * 1.5))
print('\t{} Drinks: ${:14.2f}'.format(drinkNum, drinkNum * 1.0))
print('\t\tTotal: ${:.2f}'.format(hamburgerNum * 2.0 + friesNum * 1.5 + drinkNum * 1.0))
