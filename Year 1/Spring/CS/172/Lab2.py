import datetime
from amuse.lab import Particles

class Item():
    def __init__(self):
        self.__name = input('Enter Item Name: ')
        self.__price = float(input('Enter Item Price: '))
        self.__taxable = self.taxable()

    def taxable(self):
        test = input('Is the item taxable (yes/no): ')
        if test.lower() == 'no':
            return False
        else:
            return True

    def __str__(self):
        return self.__name

    def getPrice(self):
        return float(self.__price)

    def getTax(self, taxrate):
        if self.__taxable:
            return float(self.__price * taxrate)
        else:
            return 0

class Receipt():
    def __init__(self):
        self.__tax_rate = float(input('Enter taxrate: '))
        self.__purchases = []

    def addItem(self):
        self.__purchases.append(Item())

    def __str__(self):
        print('---- Receipt{}----'.format(str(datetime.datetime.now())))
        total_cost = 0
        total_tax = 0
        for item in self.__purchases:
            print('{:_<20}{:_>20.2f}'.format(item.__str__(), item.getPrice()))
            total_cost += item.getPrice()
            total_tax += item.getTax(self.__tax_rate)
        print('\n{:_<20}{:_>20.2f}'.format('Sub Total', total_cost))
        print('{:_<20}{:_>20.2f}'.format('Tax', total_tax))
        print('{:_<20}{:_>20.2f}'.format('Total',total_cost + total_tax))

if __name__ == '__main__':
    print('Welcome to Receipt Creator')
    receipt = Receipt()
    while True:
        receipt.addItem()
        user_input = input('Add another item (yes/no): ')
        if user_input.lower() == 'no':
            break
        else:
            continue
    receipt.__str__()
