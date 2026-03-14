def inefficient_pipeline(n):
    data = [[i * j for j in range(n)] for i in range(n)]

    history = []

    for iteration in range(10):
        duplicated = [row[:] for row in data]
        string_version = [[str(value) for value in row] for row in data]
        reconverted = duplicated
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
    total = sum(s for snapshot in result for s in snapshot["sums"])

    print("Final:", total)


if __name__ == "__main__":
    run()
