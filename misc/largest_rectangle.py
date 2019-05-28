import numpy as np

def largest_rectangle(arr):
    """

    :param arr: np array
    :return:
    """
    v_max = arr.max()
    max_area = 0
    for h in range(1, v_max+1, 1):
        max_continous_cnt = 0
        cnt = 0
        for i in range(arr.shape[0]):
            if arr[i] >= h:
                cnt += 1
            else:
                cnt = 0

            max_continous_cnt = max(max_continous_cnt, cnt)
        max_area = max(max_area, max_continous_cnt * h)
    return max_area


if __name__ == '__main__':
    a = [2,1,5,6,2,3]
    a = np.array(a)
    area = largest_rectangle(a)
    print(area)
