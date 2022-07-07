# import sys
# sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/')
#
# import turtle
#
# steps = 5
#
# turtle.pendown()
# turtle.forward(steps)
# turtle.right(90)
# turtle.forward(steps)
# turtle.right(90)

# def hanoi1HardCoded(start,end):
#     print(start + ' -> ' + end)
#
# def hanoi2HardCoded(start ,spare ,end):
#     print(start+" -> "+spare)
#     print(start+" -> "+end)
#     print(spare+" -> "+end)
#
# def hanoi3HardCoded( start , spare , end):
#     print( start+" -> "+end)
#     print(start+" -> "+spare)
#     print(end+" -> "+spare)
#     print(start + " -> " + end)
#     print(spare +" -> " + start)
#     print(spare + " -> " + end)
#     print(start + " -> " + end)

def hanoi1CallingSimplerMethods(start , end):
    print(start + " -> " + end)

def hanoi2CallingSimplerMethods(start , spare , end):
    hanoi1CallingSimplerMethods ( start , spare )
    print(start + " -> " + end)
    hanoi1CallingSimplerMethods(spare , end)

def hanoi3CallingSimplerMethods(start , spare , end):
    hanoi2CallingSimplerMethods ( start , end , spare )
    print(start + " -> " + end)
    hanoi2CallingSimplerMethods(spare , start , end)

def hanoi4CallingSimplerMethods(start, spare, end):
    hanoi3CallingSimplerMethods(start, end, spare)
    print(start + ' -> ' + end)
    hanoi3CallingSimplerMethods(spare, start, end)

def hanoi(start, spare, end, n):
    # if n==1:
    #     print( start+" -> "+end)
    # else:
    n -= 1
    hanoi(start ,end,spare ,n)
    print( start+" -> "+end)
    hanoi(spare ,start ,end, n)

def hanoi_debug(start, spare, end, n):
    print("start=",start ,"spare=",spare ,"end=",end)
    if n==1:
        print( start+" -> "+end)
    else :
        # n -=1
        hanoi_debug(start ,end,spare ,n)
        print( start+" -> "+end)
        hanoi_debug(spare,start,end,n)

hanoi_debug("A" ,"B" ,"C" ,3)


# else :
# print( start+" -> "+end)
# hanoi debug(start ,end,spare ,n−1) print( start+" -> "+end)
# hanoi debug(spare,start,end,n−1)
#
# # hanoi4CallingSimplerMethods('A', 'B', 'C')
# hanoi('A', 'B', 'C', 3)
