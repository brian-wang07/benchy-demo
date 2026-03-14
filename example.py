def inefficient_pipeline(n):
    data = [[i * j for j in range(n)] for i in range(n)]

    history = []

    for iteration in range(10):
        duplicated = [row[:] for row in data]
        string_version = [list(map(str, row)) for row in data]
        sums = list(map(sum, data))

        history.append({
            "duplicated": duplicated,
            "strings": string_version,
            "reconverted": duplicated,
            "sums": sums
        })

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
