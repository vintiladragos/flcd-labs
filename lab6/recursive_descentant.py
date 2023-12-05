"""
Functions corresponding to the assigned parsing strategy + appropriate tests,  as detailed below:

Recursive Descendent - functions corresponding to moves (expand, advance, momentary insuccess, back, another try, success)
"""

from lab5 import grammar

class RecursiveDescendant:
    def __init__(self, grammar: grammar.Grammar):
        """
        current_state: string: q,b,f or e.
        q = normal state
        b = back state
        f = final state
        e = error state
        """
        self.__grammar = grammar
        self.__current_state = "q"
        self.__index_position = 1
        self.__working_stack = []
        self.__input_stack = [grammar.get_start_symbol()]

    def expand(self):
        """
        Expands the current state by moving the input stack's first element (non-terminal) to the working stack,
         and its first production to the input stack.
        """
        non_terminal = self.__input_stack.pop(0)
        productions_for_non_terminal = self.__grammar.get_list_of_productions_for_non_terminal(non_terminal)
        self.__working_stack.append((non_terminal, 1))
        production = productions_for_non_terminal[0]
        self.__input_stack = list(production) + self.__input_stack
        print("|- exp" + str(self))

    def advance(self):
        """
        Advances the current state by moving the input stack's first element (terminal) to the working stack, and
        incrementing the index position.

        """
        terminal = self.__input_stack.pop(0)
        self.__working_stack.append((terminal, -1))
        self.__index_position += 1
        print("|- adv" + str(self))

    def momentary_insuccess(self):
        """
        Modifies the current parsing state to back state (b)
        """
        self.__current_state = "b"
        print("|- mi" + str(self))

    def back(self):
        """
        Backtracks the current state by popping the working stack's last element, and moving it to the input stack.
        """
        terminal = self.__working_stack.pop()
        self.__input_stack.insert(0, terminal[0])
        self.__index_position -= 1
        print("|- back" + str(self))

    def another_try(self):
        """
        Modifies the current parsing state:
        1. if the non-terminal has more productions, the current state is set to normal state (q) and next production
        is moved to the input stack, with the index position of the non-terminal incremented by 1.
        2. if the non-terminal has no more productions, the current state is left as the back state (b), and the
        non-terminal is moved to the input stack in place of its last production.
            2.1 However, if the non-terminal is the start symbol and the index position is 1, the current state is set
            to error state (e).
        """
        non_terminal, non_terminal_index = self.__working_stack[-1]
        productions_for_non_terminal = self.__grammar.get_list_of_productions_for_non_terminal(non_terminal)

        number_of_symbols_to_pop = len(productions_for_non_terminal[non_terminal_index-1])
        for i in range(number_of_symbols_to_pop):
            self.__input_stack.pop(0)

        if non_terminal_index == len(productions_for_non_terminal):
            if non_terminal == self.__grammar.get_start_symbol() and self.__index_position == 1:
                self.__current_state = "e"
                self.__working_stack.pop()
                print("|- at" + str(self))
                return

            self.__input_stack.insert(0, non_terminal)
            self.__working_stack.pop()
            print("|- at" + str(self))
            return

        self.__current_state = "q"
        self.__working_stack[-1] = (non_terminal, non_terminal_index+1)

        production_to_add = productions_for_non_terminal[non_terminal_index+1-1] # because the python list starts from 0, and our index starts from 1
        self.__input_stack = list(production_to_add) + self.__input_stack
        print("|- at" + str(self))

    def success(self):
        self.__current_state = "f"
        print("|- success" + str(self))

    def __str__(self):
        return f"({self.__current_state},{self.__index_position},{self.__working_stack},{self.__input_stack})"

