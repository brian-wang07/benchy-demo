def maximalRectangle(matrix: list[list[int]]):
    if not matrix:
        return 0

    rows = len(matrix)
    cols = len(matrix[0])

    best = 0

    for r1 in range(rows):
        for c1 in range(cols):

            for r2 in range(r1, rows):
                for c2 in range(c1, cols):

                    all_ones = True

                    for r in range(r1, r2 + 1):
                        for c in range(c1, c2 + 1):

                            val = matrix[r][c]

                            if val == "0" or val == 0:
                                all_ones = False

                    if all_ones:

                        height = 0
                        i = r1
                        while i <= r2:
                            height = height + 1
                            i = i + 1

                        width = 0
                        j = c1
                        while j <= c2:
                            width = width + 1
                            j = j + 1

                        area = height * width

                        if area > best:
                            best = area

    return best
