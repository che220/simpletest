def fix_node(arr, i, n):
    left = 2*i+1
    right = 2*i+2

    if left < n and arr[left] > arr[i]:
        largest = left
    else:
        largest = i

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        fix_node(arr, largest, n)

if __name__ == '__main__':
    arr = [4,7,8,3,2,6,5,10,12,0,1,100,500,300,200]
    n = len(arr)
    for i in range((n-1)//2, -1, -1):
        fix_node(arr, i, n)
    print(arr)

