def hanoi(n, source, auxiliary, destination, buffer):
    if n == 1:
        buffer.append(f"{source} {destination}\n")
        if len(buffer) > 8192:
            sys.stdout.write("".join(buffer))
            buffer.clear()
        return
    
    # move n-1 disks from source to auxiliary
    hanoi(n - 1, source, destination, auxiliary, buffer)
    
    # move largest disk
    buffer.append(f"{source} {destination}\n")
    if len(buffer) > 8192:
        sys.stdout.write("".join(buffer))
        buffer.clear()
    
    # move n-1 disks from auxiliary to destination
    hanoi(n - 1, auxiliary, source, destination, buffer)


import sys

def main():
    # Use fast I/O
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    n = int(input_data)
    
    # The number of moves is always 2^n - 1. O(1) calculation.
    sys.stdout.write(f"{(1 << n) - 1}\n")
    
    # Use a list as a local string buffer to minimize syscalls
    output_buffer = []
    hanoi(n, 1, 2, 3, output_buffer)
    
    # Final flush of remaining moves
    if output_buffer:
        sys.stdout.write("".join(output_buffer))


if __name__ == "__main__":
    main()
