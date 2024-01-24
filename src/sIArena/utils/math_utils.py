
def scalade(array, new_min, new_max):
    cmax = array.max()
    cmin = array.min()

    if cmax == cmin:
        return array

    return (array - cmin)/(cmax-cmin) * (new_max - new_min) + new_min
