_MOVE_STRS = {
    (1, 2): "1 2\n", (1, 3): "1 3\n",
    (2, 1): "2 1\n", (2, 3): "2 3\n",
    (3, 1): "3 1\n", (3, 2): "3 2\n"
}

def hanoi(n, source, auxiliary, destination, write):
    if n <= 0:
        return
    if n == 1:
        write(_MOVE_STRS[(source, destination)])
        return
    
    hanoi(n - 1, source, destination, auxiliary, write)
    write(_MOVE_STRS[(source, destination)])
    hanoi(n - 1, auxiliary, source, destination, write)


import sys

def main():
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # Directly output the count (2^n - 1) to avoid generating the full list
    sys.stdout.write(f"{2**n - 1}\n")
    
    # Stream moves directly to stdout to minimize memory usage
    hanoi(n, 1, 2, 3, sys.stdout.write)


if __name__ == "__main__":
    main()
