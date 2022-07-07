import random
import numpy as np
from BST import BST, Node
import time
import matplotlib.pyplot as plt

def populate(n):
    list = np.random.randint(0, n+1, n).tolist()
    bst = BST()
    for item in list:
        bst.append(item)
    return list, bst

def check(list, n):
    return n in list

if __name__ == '__main__':
    max_val = 10000
    val = 0

    time_ls_list = []
    time_bst_list = []
    number_of_entries = []

    while val < max_val:
        list, bst = populate(val)

        count_ls  = 0
        count_bst = 0

        time_ls = time.time()
        for item in list:
            if check(list, item):
                count_ls += 1
        time_ls = time.time() - time_ls

        time_bst = time.time()
        for item in list:
            if bst.isin(item):
                count_bst+= 1
        time_bst = time.time() - time_bst

        time_ls_list.append(time_ls)
        time_bst_list.append(time_bst)
        number_of_entries.append(val)

        val += 1000

    plt.plot(number_of_entries, time_ls_list, 'b-', label = 'list')
    plt.plot(number_of_entries, time_bst_list, 'r-', label = 'bst')
    plt.xlim(0, 10000)
    plt.legend()
    plt.show()

        # print(count_ls, count_bst)
        # print(time_ls, time_bst)
