
# 1. print the fibonacci series
#   0 1 1 2 3 5 8 ...
#   0 1 2 3 4 5 6 ...
def printd(i: int):
    print(i, end=',')

def mainx():
    series_size = 10
    p1 = 0
    p2 = 1
    for cur in range(0, series_size):
        printd(p1)
        printd(p2)
        p1 = p1 + p2
        p2 = p2 + p1



def get_fib(ith: int) -> int:
    if ith <= 0: 
        return 0
    if ith == 1: 
        return 1
    return get_fib(ith - 1) + get_fib(ith - 2)

def mainy():
    printd(get_fib(6))


# if this file is used as the main program
#   __name__ will be set as __main__ by the interpreter
#   __name will be set as  the modules name if it is being imported
if __name__ ==  "__main__":
    main() 
else: 
    """ imported in some other file """
