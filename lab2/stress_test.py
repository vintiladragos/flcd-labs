from symbol_table import SymbolTable


def stress_test_symbol_table():
    """
    Stress test for the symbol table
    """
    import random
    import string
    import time
    import sys
    print("Stress testing symbol table...")
    sys.stdout.flush()
    start = time.time()
    table = SymbolTable()
    for i in range(100000):
        key = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        value = random.randint(0, 100000)
        table.insert(key, value)
        if i % 10000 == 0:
            print(f"{i} insertions done")
            sys.stdout.flush()
    for i in range(100000):
        key = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        table.lookup(key)
        if i % 10000 == 0:
            print(f"{i} lookups done")
            sys.stdout.flush()
    for i in range(100000):
        key = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        table.remove(key)
        if i % 10000 == 0:
            print(f"{i} removals done")
            sys.stdout.flush()
    end = time.time()
    print(f"Done in {end-start} seconds")


stress_test_symbol_table()
