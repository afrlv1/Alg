#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'staircase' function below.
#
# The function accepts INTEGER n as parameter.
#


def miniMaxSum(arr):
    # Write your code here
    arr_sorted = sorted(arr)
    print(sum(arr_sorted[:4]), sum(arr_sorted[-4:]))


if __name__ == '__main__':
    arr = [5, 5, 5, 5, 5]

    miniMaxSum(arr)
