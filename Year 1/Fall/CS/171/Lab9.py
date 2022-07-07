#Lab 9 CS

def Merge(A, B):
    C = []
    while (len(A) > 0) and (len(B) > 0):
        if A[0] < B[0]:
            C.append(A[0])
            del A[0]
        else:
            C.append(B[0])
            del B[0]
    while len(A) > 0:
        C.append(A[0])
        del A[0]
    while len(B) > 0:
        C.append(B[0])
        del B[0]
    return C

def msort(X):
    if len(X) > 1:
        middle = len(X)//2
        A = msort(X[:middle])
        B = msort(X[middle:])
        C = Merge(A,B)
        return C
    else:
        return X

def quicksort(A):
    qsort(A, 0, len(A)-1)
    return

def qsort(A, start, stop):
    if start < stop:
        p = partition(A,start,stop)
        qsort(A, start, p-1)
        qsort(A, p+1, stop)

def partition(A, start, stop):
    p = A[stop]
    i = start
    for j in range(start, stop):
        if A[j] <= p:
            temp1 = A[j]
            A[j] = A[i]
            A[i] = temp1
            i += 1
    temp = A[stop]
    A[stop] = A[i]
    A[i] = temp
    return i

import random
for x in range(0,10):
    L=[random.randint(0,100) for k in range(0,10)]
    print("Merge Input:" ,L)
    L=msort(L)
    print("Result after Merge Sort:" ,L)
for x in range(0,10):
    L=[random.randint(0,100) for k in range(0,10)]
    print("Quick Sort Input:" ,L)
    qsort(L,0 ,(len(L) - 1))
    print("Result After Quick Sort:" ,L)
