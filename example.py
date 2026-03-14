def inefficient_pipeline(n):
    data = []

    # build large dataset
    for i in range(n):
        row = []
        for j in range(n):
            row.append(i * j)
        data.append(row)

    history = []

    for iteration in range(10):

        # unnecessary deep duplication
        duplicated = []
        for row in data:
            new_row = []
            for value in row:
                new_row.append(value)
            duplicated.append(new_row)

        # convert everything to strings (wasteful)
        string_version = []
        for row in duplicated:
            srow = []
            for value in row:
                srow.append(str(value))
            string_version.append(srow)

        # convert back to integers
        reconverted = []
        for row in string_version:
            new_row = []
            for value in row:
                new_row.append(int(value))
            reconverted.append(new_row)

        # compute sums but store full intermediate structures
        sums = []
        for row in reconverted:
            total = 0
            for value in row:
                total += value
            sums.append(total)

        # store snapshot of everything
        history.append({
            "duplicated": duplicated,
            "strings": string_version,
            "reconverted": reconverted,
            "sums": sums
        })

        # mutate data slightly
        new_data = []
        for row in data:
            new_row = []
            for value in row:
                new_row.append(value + 1)
            new_data.append(new_row)

        data = new_data

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
