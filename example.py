def maximalRectangle(matrix: list[list[int]]):
    if not matrix or not matrix[0]:
        return 0

    cols = len(matrix[0])
    heights = [0] * (cols + 1)
    best = 0

    for row in matrix:
        for i in range(cols):
            if row[i] == "1" or row[i] == 1:
                heights[i] += 1
            else:
                heights[i] = 0
        
        stack = [-1]
        for i in range(cols + 1):
            while heights[i] < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i - 1 - stack[-1]
                if h * w > best:
                    best = h * w
            stack.append(i)

    return best
