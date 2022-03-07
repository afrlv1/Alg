def digital_root(n):
    n1 = 0
    number = str(n)
    for i1 in range(0, len(number)):
        for i2 in number:
            n1 += int(i2)
        print(n1)
    return n1


if __name__ == '__main__':
    digital_root(16)
