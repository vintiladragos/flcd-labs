class PIF:
    def __init__(self):
        self.__pif = []

    def add(self, token, pointer):
        self.__pif.append((token, pointer))

    def __str__(self):
        return "\n".join([str(p) for p in self.__pif])

    # crud on pif
    def get(self, index):
        return self.__pif[index]

