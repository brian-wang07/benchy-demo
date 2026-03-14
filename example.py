def inefficient_pipeline(n):
    import numpy as np
    # Vectorized initialization: (n,1) * (1,n) broadcasting creates the multiplication table in C.
    data = np.arange(n).reshape(-1, 1) * np.arange(n)
    history = []

    for _ in range(10):
        # NumPy's sum(axis=1) is significantly faster than a list comprehension with sum().
        sums = data.sum(axis=1).tolist()
        
        # bulk conversion to string is the most expensive operation; 
        # astype(str) performs this conversion at the C level.
        string_version = data.astype(str).tolist()
        
        # tolist() is the fastest way to bridge NumPy arrays and Python list structures.
        # We call it twice to provide the distinct copies originally requested.
        duplicated = data.tolist()
        reconverted = data.tolist()

        history.append({
            "duplicated": duplicated,
            "strings": string_version,
            "reconverted": reconverted,
            "sums": sums
        })

        # Vectorized in-place increment replaces the costly O(n^2) nested list creation.
        data += 1

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
