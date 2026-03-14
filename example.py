def hanoi(n, source, auxiliary, destination, write, move_map):
    if n == 1:
        write(move_map[source][destination])
        return
    if n <= 0:
        return
    
    # move n-1 disks from source to auxiliary
    hanoi(n - 1, source, destination, auxiliary, write, move_map)
    
    # move largest disk
    write(move_map[source][destination])
    
    # move n-1 disks from auxiliary to destination
    hanoi(n - 1, auxiliary, source, destination, write, move_map)


def main():
    import sys
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    try:
        n = int(input_data[0])
    except (ValueError, IndexError):
        return
    
    # Pre-calculate move count: 2^n - 1
    sys.stdout.write(f"{2**n - 1}\n")
    
    if n <= 0:
        return

    # Pre-calculated strings for all 6 possible moves to avoid formatting overhead
    move_map = {
        1: {2: "1 2\n", 3: "1 3\n"},
        2: {1: "2 1\n", 3: "2 3\n"},
        3: {1: "3 1\n", 2: "3 2\n"}
    }
    
    # Buffered write strategy to batch small strings into fewer system calls
    buffer = []
    def buffered_write(s):
        buffer.append(s)
        if len(buffer) > 8192:
            sys.stdout.write("".join(buffer))
            buffer.clear()
            
    hanoi(n, 1, 2, 3, buffered_write, move_map)
    
    if buffer:
        sys.stdout.write("".join(buffer))


if __name__ == "__main__":
    main()
