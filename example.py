def maximalRectangle(matrix: list[list[int]]):
    if not matrix or not matrix[0]:
        return 0

    cols = len(matrix[0])
    heights = [0] * (cols + 1)
    best = 0

    for row in matrix:
        for c in range(cols):
            val = row[c]
            if val == "1" or val == 1:
                heights[c] += 1
            else:
                heights[c] = 0

        stack = [-1]
        for i in range(cols + 1):
            while heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                area = h * w
                if area > best:
                    best = area
            stack.append(i)

    return best
