class Node:
    def __init__(self, parent, symbol: str, children: list):
        self.parent = parent
        self.symbol = symbol
        self.children = children
        self.number = -1
