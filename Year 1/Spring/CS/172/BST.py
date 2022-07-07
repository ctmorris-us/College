class Node():
	def __init__(self,val):
		self.__value = val
		self.__right = None
		self.__left = None
	def setLeft(self,n):
		self.__left = n
	def setRight(self,n):
		self.__right = n
	def getLeft(self):
		return self.__left
	def getRight(self):
		return self.__right
	def getValue(self):
		return self.__value

class BST():
	def __init__(self):
		self.__root = None
	
	def append(self,val):
		node = Node(val)
		if self.__root == None:
			self.__root = node
			return
		
		current = self.__root
		while True:
			if val <= current.getValue():
				if current.getLeft() == None:
					current.setLeft(node)
					return
				else:
					current = current.getLeft()
			else:
				if current.getRight() == None:
					current.setRight(node)
					return
				else:
					current = current.getRight()
	
	def isin(self,val):
		if self.__root == None:
			return False
		
		current = self.__root
		while current != None:
			if current.getValue() == val:
				return True
			elif val < current.getValue():
				current = current.getLeft()
			else:
				current = current.getRight()
		
		
		