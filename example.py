def inefficient_pipeline(n):
    # build large dataset
    data = [[i * j for j in range(n)] for i in range(n)]

    history = []

    for iteration in range(10):

        # unnecessary deep duplication
        duplicated = [row[:] for row in data]

        # convert everything to strings (wasteful)
        string_version = [list(map(str, row)) for row in data]

        # convert back to integers
        reconverted = [row[:] for row in data]

        # compute sums but store full intermediate structures
        sums = [sum(row) for row in data]

        # store snapshot of everything
        history.append({
            "duplicated": duplicated,
            "strings": string_version,
            "reconverted": reconverted,
            "sums": sums
        })

        # mutate data slightly
        data = [[value + 1 for value in row] for row in data]

    return history


def run():
    result = inefficient_pipeline(600)

    # pointless aggregation
    total = sum(sum(snapshot["sums"]) for snapshot in result)

    print("Final:", total)


if __name__ == "__main__":
    run()
