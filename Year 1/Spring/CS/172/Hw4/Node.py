'''
Christopher Morris
Id: 14289226

The Linked List and Node classes are modified versions of the ones provided on BBLearn.
The only modifications are that the linked list has been made an iterator, and searching returns ID numbers.

Node for linked list
'''

class Node():
    def __init__(self, data, next = None):
        self.__data = data
        self.__next = next

    # getters
    def getData(self):
        return self.__data

    def getNext(self):
        return self.__next

    #setters
    def setData(self,d):
        self.__data = d

    def setNext(self,n):
        self.__next = n

    #overloaded operators
    def __str__(self):
        return str(self.__data) + " whose next node is " + str(self.__next)
