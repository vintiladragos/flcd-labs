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
        self.__filename = filename
        self.__terminals = []
        self.__non_terminals = []
        self.__productions = {}
        self.__start_symbol = None
        self.__read_grammar()

    def get_start_symbol(self):
        return self.__start_symbol

    def get_terminals(self):
        return self.__terminals

    def get_non_terminals(self):
        return self.__non_terminals

    def __read_grammar(self):
        """
        Reads the grammar from the specified file and initializes the Grammar object.

        The grammar file is expected to have the following format:
        #Non-terminals
        non_terminal1 non_terminal2 ...

        #Terminals
        terminal1 terminal2 ...

        #Productions
        left1 ::= right1_1 | right1_2 | ...
        left2 ::= right2_1 | right2_2 | ...
        ...

        #StartSymbol
        start_symbol

        Raises:
            Exception: If the file format is invalid or if a symbol in the grammar is not a valid terminal,
                        non-terminal, or epsilon.
        """
        with open(self.__filename, 'r') as file:
            if file.readline() != "#Non-terminals\n":
                raise Exception("Invalid file format")
            # process non-terminals
            self.__non_terminals = [non_terminal for non_terminal in file.readline().strip().split(" ")]

            if file.readline() != "#Terminals\n":
                raise Exception("Invalid file format")
            # process terminals
            self.__terminals = [terminal for terminal in file.readline().strip().split(" ")]

            if file.readline() != "#Productions\n":
                raise Exception("Invalid file format")

            line = file.readline()
            while line != "#StartSymbol\n":
                line = line.strip().split("::=")

                # left hand side of production processing
                left = line[0].strip()
                current_left = []
                for symbol in left.split(" "):
                    if symbol not in self.__terminals and symbol not in self.__non_terminals:
                        raise Exception(f"Invalid file format: {symbol} is not a terminal or non-terminal")
                    current_left.append(symbol)
                current_left = tuple(current_left)

                # right hand side of production processing
                right = line[1].strip()
                current_right = []
                for single_right in right.split("|"):
                    current_single_right = []
                    for symbol in single_right.strip().split(" "):
                        if symbol not in self.__terminals and symbol not in self.__non_terminals and symbol != Grammar.EPSILON:
                            raise Exception(
                                f"Invalid file format: {symbol} is not a terminal or non-terminal or epsilon")
                        current_single_right.append(symbol)
                    current_single_right = tuple(current_single_right)
                    current_right.append(current_single_right)

                if current_left in self.__productions:
                    self.__productions[current_left].extend(current_right)
                else:
                    self.__productions[current_left] = current_right

                line = file.readline()

            start_symbol = file.readline().strip()
            if start_symbol not in self.__non_terminals:
                raise Exception(f"Invalid file format: {start_symbol} is not a non-terminal")

            self.__start_symbol = start_symbol

    def cfg_check(self):
        """
        Checks whether the grammar adheres to the definition of a Context-Free Grammar (CFG).

        A CFG is defined as follows:
        - Each production has exactly one non-terminal on the left side.
        - The left side of each production is a single non-terminal.
        - All non-terminals on the left side of productions must belong to the set of non-terminals.

        Returns:
            bool: True if the grammar is a valid Context-Free Grammar (CFG), False otherwise.

        Raises:
            None
        """
        for key, _ in self.__productions.items():
            if len(key) > 1 or key[0] not in self.__non_terminals:
                return False

        return True

    def productions_for_non_terminal(self, non_terminal):
        if non_terminal not in self.__non_terminals:
            raise Exception(f"{non_terminal} is not a non-terminal")

        for left, right in self.__productions.items():
            if left[0] == non_terminal and len(left) == 1:
                string = f"{non_terminal} ::= "

                for production in right:
                    for symbol in production:
                        string += symbol + " "
                    string += "| "

                string = string[:-3]
                return string

        return "No productions found for this non-terminal"

    def get_list_of_productions_for_non_terminal(self, non_terminal):
        if non_terminal not in self.__non_terminals:
            raise Exception(f"{non_terminal} is not a non-terminal")

        for left, right in self.__productions.items():
            if left[0] == non_terminal and len(left) == 1:
                return right

        return []

    def __terminal_representation(self):
        return f"Terminals:\n\t{self.__terminals}\n"

    def __non_terminal_representation(self):
        return f"Non-terminals:\n\t{self.__non_terminals}\n"

    def __productions_representation(self):
        string = "Productions:\n\t"
        for left, right in self.__productions.items():
            for production in left:
                string += production + " "

            string += "::= "

            for production in right:
                for symbol in production:
                    string += symbol + " "
                string += "| "

            string = string[:-3]
            string += "\n\t"

        string = string[:-1]
        return string

    def __start_symbol_representation(self):
        return f"Start symbol:\n\t{self.__start_symbol}\n"

    def __str__(self):
        return (
                self.__terminal_representation()
                + self.__non_terminal_representation()
                + self.__productions_representation()
                + self.__start_symbol_representation()
        )
