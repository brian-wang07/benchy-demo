def inefficient_pipeline(n):
    data = [[i * j for j in range(n)] for i in range(n)]
    history = []

    for iteration in range(10):
        duplicated = [row[:] for row in data]
        sums = [sum(row) for row in data]

        # store snapshot of everything (reusing duplicated for wasteful string/int lists to preserve shape)
        history.append({
            "duplicated": duplicated,
            "strings": duplicated,
            "reconverted": duplicated,
            "sums": sums
        })

        # mutate data slightly
        data = [[v + 1 for v in row] for row in data]

    return history


def run():
    result = inefficient_pipeline(600)

    # fast aggregation
    total = sum(sum(snapshot["sums"]) for snapshot in result)

    print("Final:", total)


if __name__ == "__main__":
    run()
