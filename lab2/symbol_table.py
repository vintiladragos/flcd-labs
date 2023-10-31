class SymbolTable:
    def __init__(self, size=35000):
        self.table = [None] * size
        self.size = size
        self.count = 0

    def hash(self, key):
        """
        :param key: Symbol to be hashed
        :return: Hash value of the symbol
        Raises TypeError if the symbol is not hashable
        """
        try:
            hash(key)
        except TypeError:
            raise TypeError("Symbol is not hashable")
        return key.__hash__() % self.size

    def insert(self, key, value):
        """
        :param key: Symbol to be inserted
        :param value: Value of the symbol
        :return: True if inserted, its value if already exists
        """
        index = self.hash(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
            self.count += 1
            return True
        else:
            for list_key, list_value in self.table[index]:
                if list_key == key:
                    return list_value
            self.table[index].append((key, value))
            self.count += 1
            return True

    def lookup(self, key):
        """
        :param key:  Symbol to be looked up
        :return: Value of the symbol if found, None otherwise
        """
        index = self.hash(key)
        if self.table[index] is None:
            return None
        else:
            for list_key, value in self.table[index]:
                if list_key == key:
                    return value
            return None

    def remove(self, key):
        """
        :param key: Symbol to be removed
        :return: Value of the symbol if found, None otherwise
        """
        index = self.hash(key)
        if self.table[index] is None:
            return None
        else:
            for list_key, value in self.table[index]:
                if list_key == key:
                    self.table[index].remove((list_key, value))
                    return value
            return None

    def __str__(self):
        result = ""
        for i in range(self.size):
            if self.table[i] is not None:
                for key, value in self.table[i]:
                    result += f"{key} -> {value}\n"
        return result