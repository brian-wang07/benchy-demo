def hanoi(n, source, auxiliary, destination, moves):
    if n == 1:
        moves.append((source, destination))
        return
    
    # move n-1 disks from source to auxiliary
    hanoi(n - 1, source, destination, auxiliary, moves)
    
    # move largest disk
    moves.append((source, destination))
    
    # move n-1 disks from auxiliary to destination
    hanoi(n - 1, auxiliary, source, destination, moves)


def main():
    n = int(input())
    
    moves = []
    hanoi(n, 1, 2, 3, moves)
    
    print(len(moves))
    for a, b in moves:
        print(a, b)


if __name__ == "__main__":
    main()
