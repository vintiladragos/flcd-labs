"""
Functions corresponding to the assigned parsing strategy + appropriate tests,  as detailed below:

Recursive Descendant - functions corresponding to moves (expand, advance, momentary insuccess, back, another try, success)
"""
from grammar import Grammar
from parser_output import ParserOutput


class RecursiveDescendant:
    def __init__(self, grammar: Grammar, sequence_file_name: str, output_file_name: str):
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
        self.__input_stack = [self.__grammar.get_start_symbol()]

        self.__parser_output = ParserOutput(self)

        self.__output_file = output_file_name
        self.__initialize_output_file()
        self.__sequence_file_name = sequence_file_name

    def get_grammar(self):
        return self.__grammar

    def get_working_stack(self):
        return self.__working_stack

    def get_output_file(self):
        return self.__output_file

    def __initialize_configuration(self):
        self.__current_state = "q"
        self.__index_position = 1
        self.__working_stack = []
        self.__input_stack = [self.__grammar.get_start_symbol()]

    def __initialize_output_file(self):
        open(self.__output_file, 'w').close()

    def __read_sequence_from_file(self):
        with open(self.__sequence_file_name) as file:
            line = file.readline()

        split_sequence = line.strip().split()
        terminals = self.__grammar.get_terminals()

        for element in split_sequence:
            if element not in terminals:
                raise Exception(f"'{element}' from the sequence is not a terminal!")

        return split_sequence

    def expand(self):
        """
        Expands the current state by moving the input stack's first element (non-terminal) to the working stack,
         and its first production to the input stack.
        """
        non_terminal = self.__input_stack.pop(0)
        self.__working_stack.append((non_terminal, 1))

        productions_for_non_terminal = self.__grammar.get_list_of_productions_for_non_terminal(non_terminal)
        production = productions_for_non_terminal[0]
        self.__input_stack = list(production) + self.__input_stack

        self.__parser_output.print_string_to_file_and_console(f"|- exp {self}")

    def advance(self):
        """
        Advances the current state by moving the input stack's first element (terminal) to the working stack, and
        incrementing the index position.

        """
        terminal = self.__input_stack.pop(0)
        self.__working_stack.append((terminal, -1))
        self.__index_position += 1

        self.__parser_output.print_string_to_file_and_console(f"|- adv {self}")

    def momentary_insuccess(self):
        """
        Modifies the current parsing state to back state (b)
        """
        self.__current_state = "b"

        self.__parser_output.print_string_to_file_and_console(f"|- mi {self}")

    def back(self):
        """
        Backtracks the current state by popping the working stack's last element, and moving it to the input stack.
        """
        terminal = self.__working_stack.pop()
        self.__input_stack.insert(0, terminal[0])
        self.__index_position -= 1

        self.__parser_output.print_string_to_file_and_console(f"|- back {self}")

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

        number_of_symbols_to_pop = len(productions_for_non_terminal[non_terminal_index - 1])
        for i in range(number_of_symbols_to_pop):
            self.__input_stack.pop(0)

        if non_terminal_index == len(productions_for_non_terminal):
            if non_terminal == self.__grammar.get_start_symbol() and self.__index_position == 1:
                self.__current_state = "e"
                self.__working_stack.pop()

                self.__parser_output.print_string_to_file_and_console(f"|- at {self}")
                return

            self.__input_stack.insert(0, non_terminal)
            self.__working_stack.pop()

            self.__parser_output.print_string_to_file_and_console(f"|- at {self}")
            return

        self.__current_state = "q"
        self.__working_stack[-1] = (non_terminal, non_terminal_index + 1)

        # because the python list starts from 0, and our index starts from 1
        production_to_add = productions_for_non_terminal[non_terminal_index + 1 - 1]
        self.__input_stack = list(production_to_add) + self.__input_stack

        self.__parser_output.print_string_to_file_and_console(f"|- at {self}")

    def success(self):
        self.__current_state = "f"

        self.__parser_output.print_string_to_file_and_console(f"|- success {self}")

    def parse(self):
        split_sequence = self.__read_sequence_from_file()
        self.__parser_output.print_string_to_file_and_console(f"The sequence is w = "
                                                              f"{' '.join(split_sequence)}\n{str(self)}")

        terminals = self.__grammar.get_terminals()
        non_terminals = self.__grammar.get_non_terminals()

        while self.__current_state != 'f' and self.__current_state != 'e':
            if self.__current_state == 'q':
                if self.__index_position == len(split_sequence) + 1 and len(self.__input_stack) == 0:
                    self.success()

                elif self.__input_stack[0] in non_terminals:
                    self.expand()

                elif self.__input_stack[0] in terminals:
                    if (self.__index_position <= len(split_sequence) and self.__input_stack[0] ==
                            split_sequence[self.__index_position - 1]):
                        self.advance()
                    else:
                        self.momentary_insuccess()

            elif self.__current_state == 'b':
                if self.__working_stack[-1][0] in terminals:
                    self.back()

                elif self.__working_stack[-1][0] in non_terminals:
                    self.another_try()

        if self.__current_state == 'e':
            self.__parser_output.print_string_to_file_and_console("Sequence is not accepted!\n\n")
        else:
            tree_table_representation = self.__parser_output.get_tree_table_representation()
            message = f"Sequence is accepted!\n\nThe table representation is:\n{tree_table_representation}\n\n"
            self.__parser_output.print_string_to_file_and_console(message)

        self.__initialize_configuration()

    def __str__(self):
        formatted_stack = ' '.join(f"{element[0]}{element[1] if element[1] != -1 else ''}"
                                   for element in self.__working_stack) or self.__grammar.EPSILON

        return (f"({self.__current_state}, {self.__index_position}, "
                f"{formatted_stack}, {' '.join(map(str, self.__input_stack))}"
                f"{self.__grammar.EPSILON if not self.__input_stack else ''})")
