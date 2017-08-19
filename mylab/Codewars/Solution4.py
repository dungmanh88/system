def positive_sum(arr):
    arr.sort()
    if not arr:
        return 0
    j= 0
    for i in arr:
        if i < 0:
            print "i=" + str(i)
            arr[j]=0
        j = j + 1

    return sum(arr)

def positive_sum(arr):
    return sum(x for x in arr if x > 0)
