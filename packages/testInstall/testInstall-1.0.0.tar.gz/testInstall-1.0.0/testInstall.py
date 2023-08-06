def printList (the_list):
    for each_list in the_list:
        if isinstance(each_list, list):#默认递归不能超过100
            printList(each_list)
        else:
            print(each_list)