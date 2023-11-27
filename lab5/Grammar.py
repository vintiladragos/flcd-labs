class Grammar:
    """
    Class for representing a grammar
    terminals: list of terminals
    non-terminals: list of non-terminals
    productions: dictionary of productions
    structure:
        productions: {left: [right1, right2, ...]}
        left: (symbol, symbol, ...)
        right: (symbol, symbol, ...)
        symbol: terminal or non-terminal
        start_symbol: start symbol
    EPSILON: epsilon symbol string representation
    """
    EPSILON = "epsilon"
    def __init__(self, filename):
        self.filename = filename
        self.terminals = []
        self.nonterminals = []
        self.productions = {}
        self.start_symbol = None
        self.read_grammar()
    def read_grammar(self):
        with open(self.filename, 'r') as file:
            if file.readline() != "#Nonterminals\n":
                raise Exception("Invalid file format")
            self.nonterminals = [nonterminal for nonterminal in file.readline().strip().split(" ")]
            if file.readline() != "#Terminals\n":
                raise Exception("Invalid file format")
            self.terminals = [terminal for terminal in file.readline().strip().split(" ")]
            if file.readline() != "#Productions\n":
                raise Exception("Invalid file format")
            line = file.readline()
            while line != "#StartSymbol\n":
                line = line.strip().split("::=")

                # left of production processing
                left = line[0].strip()
                current_left = []
                for symbol in left.split(" "):
                    if symbol not in self.terminals and symbol not in self.nonterminals:
                        raise Exception(f"Invalid file format, {symbol} is not a terminal or non-terminal")
                    current_left.append(symbol)
                current_left = tuple(current_left)

                # right of production processing
                right = line[1].strip()
                current_right = []
                for single_right in right.split("|"):
                    current_single_right = []
                    for symbol in single_right.strip().split(" "):
                        if symbol not in self.terminals and symbol not in self.nonterminals and symbol != Grammar.EPSILON:
                            raise Exception(f"Invalid file format, {symbol} is not a terminal or non-terminal or epsilon")
                        current_single_right.append(symbol)
                    current_single_right = tuple(current_single_right)
                    current_right.append(current_single_right)

                self.productions[current_left] = current_right
                line = file.readline()

            start_symbol = file.readline().strip()
            if start_symbol not in self.nonterminals:
                raise Exception(f"Invalid file format, {start_symbol} is not a non-terminal")
            self.start_symbol = start_symbol
    def cfg_check(self):
        """
        productions: {nonterminal: [production1, production2, ...]}
        """
        for key, _ in self.productions.items():
            if key.__len__() > 1:
                return False
            if key[0] not in self.nonterminals:
                return False
        return True

    def __str__(self):
        return self.terminal_representation() + self.nonterminal_representation() + self.productions_representation() + self.start_symbol_representation()

    def terminal_representation(self):
        return "Terminals: " + str(self.terminals) + "\n"

    def nonterminal_representation(self):
        return "Non-terminals: " + str(self.nonterminals) + "\n"

    def productions_representation(self):
        string = "Productions:\n"
        for left, right in self.productions.items():
            for production in left:
                string += production + " "
            string += "::= "
            for production in right:
                for symbol in production:
                    string += symbol + " "
                string += "| "
            string = string[:-3]
            string += "\n"
        return string

    def productions_for_nonterminal(self, nonterminal):
        if nonterminal not in self.nonterminals:
            raise Exception(f"{nonterminal} is not a non-terminal")
        for left, right in self.productions.items():
            if left[0] == nonterminal and left.__len__() == 1:
                string = f"{nonterminal} ::= "
                for production in right:
                    for symbol in production:
                        string += symbol + " "
                    string += "| "
                string = string[:-3]
                return string
        return "No productions for this non-terminal"

    def start_symbol_representation(self):
        return "Start symbol: " + self.start_symbol + "\n"



a = Grammar("g2.txt")
print(a)
print(a.cfg_check())
print(a.productions_for_nonterminal("<statement>"))
