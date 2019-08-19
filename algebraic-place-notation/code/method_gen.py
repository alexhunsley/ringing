

# we generate method rows from GPB internal notation, which looks like:
# [['x'], [3, 4, 9, 10], [1, 12], [3, 10], [1, 12], [3, 4, 9, 10]]

# row is a string "123456"
# gpn is an item from the gpn list as detailed previously, examples:
#   ['x']
#   [3, 4, 5, 6]
def permute(row, gpn):
    if gpn[0] == 'x':
        # nothing
        pass

    result = ""

    idx = 0

    while idx < len(row):
        print("idx = %d, gpn = %s" % (idx, gpn))
        # if we aren't at a place
        if len(gpn) == 0 or gpn[0] != idx + 1:
            # if we've reached end of row
            if idx == len(row) - 1:
                result += row[idx]
                break

            result += row[idx + 1]
            result += row[idx]

            idx += 2
        else:
            # we're at a place
            result += row[idx]
            gpn = gpn[1:]
            idx += 1

    return result


