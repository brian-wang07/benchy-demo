def hanoi(n, source, auxiliary, destination, write):
    if n == 1:
        write(f"{source} {destination}\n")
        return
    
    # move n-1 disks from source to auxiliary
    hanoi(n - 1, source, destination, auxiliary, write)
    
    # move largest disk
    write(f"{source} {destination}\n")
    
    # move n-1 disks from auxiliary to destination
    hanoi(n - 1, auxiliary, source, destination, write)


import sys

def main():
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # The total number of moves for Tower of Hanoi is 2^n - 1
    sys.stdout.write(f"{(1 << n) - 1}\n")
    
    # Direct printing via sys.stdout.write to avoid list memory overhead
    hanoi(n, 1, 2, 3, sys.stdout.write)


if __name__ == "__main__":
    main()
