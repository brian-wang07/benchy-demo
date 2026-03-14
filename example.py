def inefficient_pipeline(n):
    # build large dataset
    data = [[i * j for j in range(n)] for i in range(n)]

    history = []

    for iteration in range(10):

        # unnecessary deep duplication
        duplicated = [row[:] for row in data]

        # convert everything to strings (wasteful)
        string_version = [[str(value) for value in row] for row in duplicated]

        # convert back to integers (identical to duplicated)
        reconverted = [row[:] for row in duplicated]

        # compute sums but store full intermediate structures
        sums = [sum(row) for row in reconverted]

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
    total = 0
    for snapshot in result:
        for s in snapshot["sums"]:
            total += s

    print("Final:", total)


if __name__ == "__main__":
    run()
