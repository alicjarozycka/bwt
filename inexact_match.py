#function that generates c_array
def c_array(bwt):
    c_array = {}
    sorted_bwt = sorted(bwt)
    sorted_bwt = sorted_bwt[1:]
    starting_number = 0

    for character in sorted_bwt:
        if character not in c_array:
            c_array[character] = starting_number
        starting_number += 1

    return c_array

#funaction that generates o_array
def o_array(bwt):
    o_array = {}

    for element in bwt:
        o_array[element] = [0]

    for index, element in enumerate(bwt):
        for key in o_array:
            if key == element:
                o_array[key].append(o_array[key][-1] + 1)
            else:
                o_array[key].append(o_array[key][-1])

    for element in o_array:
        o_array[element] = o_array[element][1:]

    return o_array

def inex_recur(W, i, z, k, l, c_array, o_array, chars):
    '''
    Function name: inex_recur
    Arguments: W, i, z, k, l, c_array, o_array, chars
    Returns: I
    Function that performs recursive search (aligning query to refrence). It allows for mismatches only to z limit.
    At each i position in W, it checks all possible mismatches, updating intervals.
    '''
    if z < 0:
        return []

    if i < 0:
        occurences = []

        for j in range (k, l + 1):
            occurences.append(j)

        return occurences

    I = []

    for b in chars:
        if k == 0:
            newK = c_array[b] + 1
        else:
            newK = c_array[b] + o_array[b][k - 1] + 1

        newL = c_array[b] + o_array[b][l]

        if k <= l:
            if b == W[i]:
                I = union(I, inex_recur(W, i - 1, z, newK, newL, c_array, o_array, chars))
            else:
                I = union(I, inex_recur(W, i - 1, z - 1, newK, newL, c_array, o_array, chars))

    return I


def union(a, b):
    '''
    Function name: union
    Arguments: a, b
    Returns: list(set(a+b))
    Function combines values of a and b with '+' operation. It returns a list of merged a and b, removing duplicates.
    '''
    return list(set(a+b))


def inexact_search(W, z, bwt, X):
    '''
    Function name: inexact_search
    Arguments: W, z, bwt, X
    Returns: inex_recur
    Function performs inexact search with up to z differences.
    '''
    c = c_array(bwt)
    o = o_array(bwt)

    chars = [c_ for c_ in c if c_ != "$"]

    return inex_recur(W, len(W)-1, z, 0, len(X)-1, c, o, chars)


def positions(SA_intervals, SA, pattern):
    '''
    Function name: positions
    Arguments: SA_intervals, SA, pattern
    Returns: sorted(start_end_pos)
    This function extracts positions from the intervals obtained in the inexact search. Intervals correspond to the positions in the SA.
    As the result funtion return start and end positions where the matched pattern is located in the sequence.
    '''
    start_positions = []
    start_end_pos = []

    if SA_intervals is None:
        return

    else:
        for i in SA_intervals:
            start_pos = SA[i]
            start_positions.append(start_pos)

    for j in start_positions:
        start_end_pos.append([j+1, j+len(pattern)])

    return sorted(start_end_pos)