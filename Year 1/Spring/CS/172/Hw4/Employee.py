'''
Christopher Morris

ID: 14289226

Employee class

This is made as a template for the employees. It comes equipped with a ID, hours worked, wage, and payrate attributes.
The setters for Payrate and Hours and specific to make sure that no invalid values are inputted.

'''


class Employee():
    def __init__(self, ID): #Generator
        self.__ID = ID
        self.__hours_worked = 0
        self.__wage = 0
        self.setPayrate()

    def setWage(self): #hours * payrate = wage
        self.__wage = self.__hours_worked * self.__pay_rate

    def setPayrate(self): #Set Payrate that must be above 6.00 or will default to 6.00 if exitted
        while True:
            user_input_pay_rate = input("\nInput a payrate value above 6.00$ (type 'exit' if you don't want to.):\n")
            try:
                if user_input_pay_rate.lower() == 'exit': #Default
                    user_input_pay_rate = 6
                    break
                else:
                    user_input_pay_rate = float(user_input_pay_rate)
                    if user_input_pay_rate < 6: #Must be above 6
                        print('Inputted payrate must be above 6.00$, try again')
                        continue
                    else:
                        break
            except:
                print("Invalid Input, input must be a number above 6.00 or 'exit' if you don't want to input a payrate.")
                continue
        self.__pay_rate = float(user_input_pay_rate) #Updates payrate

    def setHours(self): #Set hours that must not be negative
        while True:
            user_input_hours = input("\nInput the number of hours worked by {} (No negative hours):\n".format(self.__ID))
            try:
                if float(user_input_hours) >= 0: #Checks not negative
                    break
                else:
                    print('The inputed hours must be not be negative, try again.')
                    continue
            except:
                print('The input was invalid. Make sure the input is a number greater than or equal zero.')
                continue

        self.__hours_worked = float(user_input_hours) #Sets hours
        self.setWage() #Calculates total wage

    def getID(self): #Gets ID
        return self.__ID

    def __str__(self): #Overload print
        self.setWage() #Make sure wage is up to date
        return (
        '''
        ID: {}
        Hours Worked: {}
        Hourly Rate: {}
        Gross Wage: {}'''.format(self.__ID, self.__hours_worked, self.__pay_rate, self.__wage))
