from random import sample
from bisect import bisect_right, bisect_left
import datetime as dt

# len(list) is independent of list length

def millisec_since_epoch():
    """

    Returns: milliseconds since epoch

    """
    return (dt.datetime.now() - dt.datetime(1970, 1, 1)).total_seconds()*1000.0


def join_array(arr1, arr2):
    # 324 ns - 0.324 um - 0.000324 ms 50+60 elements
    # 46 um - 0.046 ms 5000+6000 elements
    # linear to the total length of arr1 and arr2
    return arr1 + arr2


def get_list_median(arr):
    """
    return the median of array arr

    :param arr: list
    :return: median of list. None if list is empty
    """
    if not arr:
        return None

    arr_len = len(arr)
    mid_idx = arr_len // 2
    if arr_len // 2 * 2 == arr_len:
        mid_idx -= 1
        return (arr[mid_idx]+arr[mid_idx+1])/2.0
    else:
        return arr[mid_idx]


def get_median_from_simple_joined_list(arr1, arr2):
    """
    two arrays arr1 and arr2 have no overlap and the largest element in arr1 is less than or equal
    to the smallest element in arr2

    :param arr1: list of smaller numbers
    :param arr2: list of larger numbers
    :return: median of arr1+arr2
    """
    arr1_len = len(arr1)
    arr2_len = len(arr2)
    tot_len = arr1_len + arr2_len

    def get_elememt_from_joined_array(idx):
        """
        return the element at index of the combined array

        :param idx: index of the element in arr1+arr2
        :return: element
        """
        if idx < arr1_len:
            return arr1[idx]
        else:
            idx -= arr1_len
            return arr2[idx]

    if tot_len // 2 * 2 == tot_len:  # even number of elements
        mid_idx = tot_len // 2 - 1
        elem1 = get_elememt_from_joined_array(mid_idx)
        elem2 = get_elememt_from_joined_array(mid_idx + 1)
        return (elem1 + elem2) / 2.0
    else:  # odd total number of elements
        mid_idx = tot_len // 2
        return get_elememt_from_joined_array(mid_idx)


def find_median(arr1, arr2):
    """
    Find the median of the combined array

    :param arr1: sorted list of numbers
    :param arr2: sorted list of numbers
    :return: median of arr1 + arr2
    """
    arr1_len = len(arr1)
    arr2_len = len(arr2)
    tot_len = arr1_len + arr2_len
    is_even = tot_len // 2 * 2 == tot_len
    mid_idx = tot_len // 2 - 1 if is_even else tot_len // 2

    if not arr1:
        # if arr1 is empty, return the median of arr2
        return get_list_median(arr2)
    if not arr2:
        # if arr2 is empty, return the median of arr1
        return get_list_median(arr1)

    # make sure arr1 contains the smallest element
    if arr1[0] > arr2[0]:
        arr1, arr2 = arr2, arr1

    # SIMPLE CASE: arr1 and arr2 have no overlap
    # if all arr1 elements are less than arr2[0], the two arrays can be joined in a simple way
    # and find the median
    if arr1[arr1_len-1] <= arr2[0]:
        return get_median_from_simple_joined_list(arr1, arr2)

    # COMPLICATED CASE: arr2 overlaps with arr1
    arr2_start_idx = bisect_right(arr1, arr2[0])  # arr2_start_idx < arr1_len - 1
    if arr2_start_idx + 1 > tot_len // 2:
        # median is in arr1
        if is_even:
            elem1 = arr1[mid_idx]
            elem2 = arr1[mid_idx + 1]
            return (elem1 + elem2) / 2.0
        else:
            mid_idx = tot_len // 2
            return arr1[mid_idx]

    arr1_end_idx = bisect_left(arr2, arr1[arr1_len-1])
    if arr2_len - arr1_end_idx > tot_len // 2:
        # median is in arr2
        mid_idx -= arr1_len
        if is_even:
            elem1 = arr2[mid_idx]
            elem2 = arr2[mid_idx + 1]
            return (elem1 + elem2) / 2.0
        else:
            return arr2[mid_idx]

    # median is in the overlapping part
    

if __name__ == '__main__':
    arr1 = sample(range(1, 100000), 50000)
    arr1.sort()
    arr2 = sample(range(1, 10000), 6000)
    arr2.sort()
    print("array 1:", arr1)
    print("array 2:", arr2)

    t0 = millisec_since_epoch()
    for i in range(1, 1000000):
        len(arr1)
    t1 = millisec_since_epoch()
    print('time:', t1-t0)

#    med = find_median(arr1, arr2)
#    print('median:', med)
