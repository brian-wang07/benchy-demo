def hanoi(n, source, auxiliary, destination):
    if n == 0:
        return
    
    # move n-1 disks from source to auxiliary
    yield from hanoi(n - 1, source, destination, auxiliary)
    
    # yield move as a pre-formatted string to reduce overhead in main
    yield f"{source} {destination}\n"
    
    # move n-1 disks from auxiliary to destination
    yield from hanoi(n - 1, auxiliary, source, destination)


def main():
    import sys
    line = sys.stdin.readline()
    if not line:
        return
    try:
        n = int(line.strip())
    except ValueError:
        return
    
    # The total number of moves in Hanoi is 2^n - 1
    # We use bit shifting (1 << n) for a fast calculation
    sys.stdout.write(f"{(1 << n) - 1}\n")
    
    # Process moves via generator to keep memory footprint constant O(n)
    # sys.stdout.write is faster than print() for large volumes of output
    for move_str in hanoi(n, 1, 2, 3):
        sys.stdout.write(move_str)


if __name__ == "__main__":
    main()
