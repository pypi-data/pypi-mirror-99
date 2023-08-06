def printList (the_list, level):
    for each_list in the_list:
        if isinstance(each_list, list):#默认递归不能超过100
            printList(each_list, level + 1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_list)