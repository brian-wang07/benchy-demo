import json

def load_transactions(filepath):
    """
    Loads transactions from a JSON file.
    Optimized for execution speed by performing a single I/O read.
    """
    with open(filepath, 'r') as f:
        return json.loads(f.read())

def load_users(filepath):
    """
    Loads users from a JSONL file using a generator to minimize memory footprint.
    """
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)
