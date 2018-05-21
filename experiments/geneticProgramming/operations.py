

def add(arr):
    assert len(arr) == 2
    sum = 0
    for i in arr:
        sum += i
    return sum

def multipy(arr):
    assert len(arr) == 2
    mul = 1
    for i in arr:
        mul *= i
    return mul

def devide(arr):
    assert len(arr) == 2
    if arr[1] == 0:
        return arr[0]
    return arr[0] / arr[1]

def square(arr):
    assert len(arr) == 1
    return pow(arr[0], 2)

def power(arr):
    assert len(arr) == 2
    return pow(arr[0], arr[1])

def subtract(arr):
    assert len(arr) == 2
    return arr[0] - arr[1]
