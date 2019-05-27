import numpy as np

def water_amount(elevations, max_idx, amount):
    """

    :param elevations: np array
    :return:
    """
    if elevations.shape[0] < 3:
        return amount

    if max_idx > 0:
        l_imax = np.argmax(elevations[0:max_idx]).flatten()[0]
        if l_imax <= max_idx - 2:
            h = elevations[l_imax]
            amount += np.sum(h - elevations[l_imax + 1:max_idx])
        amount = water_amount(elevations[0:l_imax + 1], l_imax, amount)

    if max_idx < elevations.shape[0]-2:
        idxs = np.argmax(elevations[max_idx+1:]).flatten()
        r_imax = idxs[idxs.shape[0]-1] + max_idx + 1
        if r_imax >= max_idx + 2:
            h = elevations[r_imax]
            amount += np.sum(h - elevations[max_idx + 1:r_imax])
        amount = water_amount(elevations[r_imax:], 0, amount)
    return amount


if __name__ == '__main__':
    a = np.array([0,1,0,2,1,0,1,3,2,1,2,1])
    max_idx = np.argmax(a).flatten()[0]
    out = water_amount(a, max_idx, 0)
    print(out)
