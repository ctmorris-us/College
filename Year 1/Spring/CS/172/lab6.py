#Interface Class for a Stack
#Only allows access to the
#Stack commands of the built in list
class Stack:
	#Create a New Empty Stack
	def __init__(self):
		self.__S = []
	#Display the Stack
	def __str__(self):
		return str(self.__S)
	#Add a new element to top of stack
	def push(self,x):
		self.__S.append(x)
	#Remove the top element from stack
	def pop(self):
		return self.__S.pop()
	#See what element is on top of stack
	#Leaves stack unchanged
	def top(self):
		return self.__S[-1]

def postfix(exp):
    exp_list = exp.split(' ')
    operators = {'+':float.__add__, '-':float.__sub__, '*':float.__mul__, '/':float.__truediv__}
    temp = Stack()
    for value in exp_list:
        if value not in operators:
            temp.push(value)
        else:
            a = float(temp.pop())
            b = float(temp.pop())
            temp.push(operators[value](b, a))
    print('Result: {}'.format(temp.top()))

print('Welcome to Postfix Calculator')
print('Enter exit to quit')
while True:
    user_input = input('Enter Expression:\n')
    if user_input == 'exit':
        break
    else:
        postfix(user_input)
