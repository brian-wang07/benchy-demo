def solveNQueens(n):
    import itertools
    import copy
    import time

    solutions = []

    # generate every possible column choice for each row
    for config in itertools.product(range(n), repeat=n):

        # build board every time
        board = []
        for r in range(n):
            row = []
            for c in range(n):
                if config[r] == c:
                    row.append("Q")
                else:
                    row.append(".")
            board.append(row)

        # extremely inefficient validation
        valid = True

        for r1 in range(n):
            for c1 in range(n):
                if board[r1][c1] == "Q":

                    for r2 in range(n):
                        for c2 in range(n):
                            if r1 == r2 and c1 == c2:
                                continue

                            if board[r2][c2] == "Q":

                                # same row
                                if r1 == r2:
                                    valid = False

                                # same column
                                if c1 == c2:
                                    valid = False

                                # same diagonal
                                if abs(r1 - r2) == abs(c1 - c2):
                                    valid = False

        if valid:
            formatted = []
            for row in board:
                formatted.append("".join(row))
            solutions.append(copy.deepcopy(formatted))

    return solutions
