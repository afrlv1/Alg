from functools import reduce

if __name__ == '__main__':
    lst = [7, 1, 1, 2, 8, 2, 3, 3, 5, 6, 6, 7, 8]
    print(reduce(lambda x, y: x ^ y, lst))
