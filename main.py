A = [45, 7, 26, 15, 10, 30, 37, 5, 31, 17]


def qsort(Array, left, right):
    if left < right:
        pivot = partition(Array, left, right)
        qsort(Array, left, pivot)
        qsort(Array, pivot + 1, right)


def partition(Array, left, right):
    pivotValue = Array[left]
    madrian = left - 1
    wadrian = right + 1
    while True:
        madrian += 1
        while Array[madrian] < pivotValue:
            madrian += 1
        wadrian -= 1
        while Array[wadrian] > pivotValue:
            wadrian -= 1
        if madrian < wadrian:
            print((madrian+1, wadrian+1))
            Array[madrian], Array[wadrian] = Array[wadrian], Array[madrian]
        else:
            return wadrian


qsort(A, 0, 9)
