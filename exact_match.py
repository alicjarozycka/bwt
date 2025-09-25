def exact_match(pattern, o_array, c_array, bwt):
    '''
    Function name: exact_match
    Arguments: pattern, o_array, c_array, bwt
    Returns: lower_bound, upper bound
    Function performs backward search for an exact match. It starts with the last character of the pattern, then it proceedes to the left (backwards) and at each step, it refines the range.
    The final SA interval that function returns, shows where the pattern is located in the sequence.
    '''
    pattern = list(reversed(pattern))
    x = list(c_array.keys())

    first_char = pattern[0]

    if first_char not in c_array:
        return None

    lower_bound = c_array[first_char]

    if x.index(first_char) + 1 < len(x):
        upper_bound = c_array[x[x.index(first_char) + 1]] - 1
    else:
        upper_bound = len(bwt) - 1

    for i in range(1, len(pattern)):
        character = pattern[i]

        if character in c_array:
            if lower_bound > 0:
                lower_o = o_array[character][lower_bound - 1]
            else:
                lower_o = 0

            if upper_bound >= 0:
                 upper_o = o_array[character][upper_bound]
            else:
                upper_oc = 0

            lower_bound = c_array[character] + lower_o
            upper_bound = c_array[character] + upper_o - 1

        else:
            return None

        if lower_bound > upper_bound:
            return None

    return lower_bound, upper_bound


def extract_positions(SA_intervals, SA, pattern):
    '''
    Function name: extract_positions
    Arguments: SA_intervals, SA, pattern
    Returns: start_end_pos
    This function extracts positions from the intervals obtained during the exact match. Intervals correspond to the positions in the SA.
    As the result funtion returns start and end positions where the pattern is located in the sequence.
    '''
    if SA_intervals is None:
        return
    else:
        positions = SA[SA_intervals[0]:SA_intervals[1] + 1 ][::-1]
        start_end_pos = []
        for i in positions:
            start_end_pos.append([i+1, i+len(pattern)])

    return sorted(start_end_pos)