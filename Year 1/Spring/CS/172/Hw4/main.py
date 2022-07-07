'''
Hw4

Christopher Morris
Id: 14289226

The Linked List and Node classes are modified versions of the ones provided on BBLearn.
The only modifications are that the linked list has been made an iterator, and searching returns ID numbers.

This is the main program. This includes functions so the user can display and interact with the menu.

This program is made so that an employer can create a database that stores many instances of of the Employee class.
The employer is able to interact with the employee class by updating their pay, hours, adding, and removing them from the database.
The employer can also display the entire payroll for easy display of their employees.
The database is made from a modified linked list.

'''
from Employee import Employee
from Node import Node
from Linked import LinkedList

def display_menu(): #Outputs Menu and and gets user input
    print('\n*** Menu ***')
    print('1) Add a new employee.')
    print('2) Enter hours the employees.')
    print('3) Display Payroll.')
    print('4) Update the Hourly wage of an employee.')
    print('5) Remove an employee from payroll.')
    print('6) Exit Program')

    while True: #Verifies that the user input is 1-6 inclusive
        user_input = input('\nEnter in 1-6 to select item on menu:\n')
        try:
            if 1 <= int(user_input) <= 6:
                return int(user_input)
            else:
                print('Value must be inbetween 1-6 (inclusive)')
                continue
        except:
            print('Bad input, try again.')
            continue

def add_employee(Employees): #Adds an employee to linked list
    while True:
        user_input_id = input('\nEnter an ID\n')
        if Employees.search(user_input_id) != False: #Searches linked list for the ID, if found returns True which means it exists
            print('Input ID already exists, try another.')
            continue
        else:
            break

    Employees.append(Employee(user_input_id)) #Adss employee to main Employees list

def update_hours(Employees): #Iterates through Employees and runs their setHours method
    for employee in Employees:
        employee.setHours()

def display_payroll(Employees): #Iterates through Employees and calls their __str__ method
    print('*** Payroll ***')
    for employee in Employees:
        print(employee)

def update_pay_rate(Employees): #Searches for specific emplyee ID, if found calls setPayrate method
    user_input_id = input('\nEnter an ID\n')
    employee = Employees.search(user_input_id)
    if employee == False: #Not found
        print('Employee does not exist.')
    else:
        employee.setPayrate()

def remove_employee(Employees): #Searches for employee ID, and if found verifies user wants to delete and deletes employee from list
    user_input_id = input('\nEnter an ID:\n')
    employee = Employees.search(user_input_id) #checks for employee

    if employee == False: #employee not found
        print('\nEmployee does not exist.')
    else: #If found verifies user wants to delete
        user_input_remove = input("\nEmployee does exist. Input 'R' to continue deletion or 'K' to not continue:\n")
        while True:
            if user_input_remove.lower() == 'r': #Removes from payroll
                Employees.remove(user_input_id)
                print('Employee {} has been removed from the payroll.'.format(user_input_id))
                break
            elif user_input_remove.lower() == 'k': #Keeps on payroll
                print('Employee {} has been kept on the payroll.'.format(user_input_id))
                break
            else: #Input was invalid
                print("Invalid input, must be either 'R' or 'K', try again.")
                user_input_remove = input("Enter either 'R' or 'K':\n")
                continue

if __name__ == '__main__':

    Employees = LinkedList() #Main linked list
    menu_actions = {1: add_employee, 2:update_hours, 3:display_payroll, 4:update_pay_rate, 5: remove_employee}
    #Dictionary of functions to call each where the index is the menu input from the display menu function

    while True:
        a = display_menu() #Gets user's input
        if a == 6: #If user input is to exit
            print('Have a nice day.')
            break
        else: #Calls functions from the dictionary
            menu_actions[a](Employees)
