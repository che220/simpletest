def get_next_val(c_val, max_n):
    val = c_val + 1
    if val > max_n:
        val = -1
    return val

def permutations(arr):
    is_str = isinstance(arr, str)
    last_idx = len(arr) - 1
    idxs = [-1] * len(arr)
    work_idx = 0
    while 1:
        c_val = idxs[work_idx]
        while 1:
            n_val = get_next_val(c_val, last_idx)
            if n_val == -1 or n_val not in idxs:
                break
            c_val = n_val

        idxs[work_idx] = n_val
        if n_val == -1:
            work_idx -= 1
            if work_idx < 0:
                return
            continue
        elif work_idx < last_idx:
            work_idx += 1

        if idxs[last_idx] > -1:
            r_arr = [arr[i] for i in idxs]
            if is_str:
                r_arr = ''.join(r_arr)

            yield r_arr

if __name__ == '__main__':
    arr = [1, 2, 3, 4]
    exp_tot = 1
    for i in range(len(arr)):
        exp_tot *= (i+1)
    tot = 0
    for p in permutations(arr):
        print(p)
        tot += 1
    print('expect total:', exp_tot)
    print('total:', tot)
