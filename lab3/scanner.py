from lab2.symbol_table import SymbolTable
import re
from program_internal_form import PIF


class Scanner:
    def __init__(self, input_filepath, tokens_filepath):
        self.__input_filepath = input_filepath
        self.__tokens_filepath = tokens_filepath
        self.__reserved_words = []
        self.__operators = []
        self.__separators = []
        self.__read_token_in()
        self.__pif = PIF()
        self.__identifiers = SymbolTable()
        self.__constants = SymbolTable()
        # is a sequence of letters, digits, and underscores, starting with a letter
        self.__identifier_regex = r'[a-zA-Z]([a-zA-Z]|[0-9]|_)*'
        # is a sequence of digits that can optionally have a - in front of it
        self.__const_int_regex = r'-?\d+'
        # is a sequence of characters between double quotes
        self.__const_string_regex = r'"[a-zA-Z0-9_]*"'
        # is a single character between single quotes
        self.__const_char_regex = r"'[a-zA-Z0-9]'"
        # is a constant int, string, or char
        self.__constant_regex = r'(?:' + self.__const_int_regex + r'|' + self.__const_string_regex + r'|' + self.__const_char_regex + r')'

        # is a reserved word
        self.__reserved_words_regex = r'(?:' + '|'.join(re.escape(c) for c in self.__reserved_words) + r')'
        # is a separator
        self.__separators_regex = r'[' + ''.join(re.escape(c) for c in self.__separators) + r']'
        # is an operator
        self.__operators_regex = '|'.join(re.escape(c) for c in self.__operators)

    def scan(self):
        with open(self.__input_filepath, 'r') as file:
            # while file hasn't ended
            line_number = 1
            token = ""
            for line in file:
                # check if the line is a comment
                if line.startswith('#'):
                    line_number += 1
                    continue
                if line.endswith('\n'):
                    line = line[:-1]

                # tokenize the line with regex
                token_pattern = re.compile(
                    r'(' + self.__reserved_words_regex + r'|' + self.__operators_regex + r'|' + self.__separators_regex + r'|' + self.__identifier_regex + r'|' + self.__constant_regex + r')'
                )
                remaining_line = line
                for token in token_pattern.findall(line):
                    actual_token = token[0]
                    remaining_line = remaining_line.replace(actual_token, '', 1)
                    # if the token is a reserved word, operator, or separator
                    if re.match(self.__reserved_words_regex, actual_token) or re.match(self.__operators_regex, actual_token) or re.match(self.__separators_regex, actual_token):
                        if actual_token != ' ':
                            # add it to the pif
                            self.__pif.add(actual_token, -1)
                    # if the token is an identifier
                    elif re.match(self.__identifier_regex, actual_token):
                        # if the identifier is not in the symbol table
                        value = self.__identifiers.lookup(actual_token)
                        if value is None:
                            # add it to the symbol table
                            value = self.__identifiers.count
                            self.__identifiers.insert(actual_token, value)
                        # add it to the pif
                        self.__pif.add("id", value)
                    # if the token is a constant
                    elif re.match(self.__constant_regex, actual_token):
                        # if the constant is not in the symbol table
                        value = self.__constants.lookup(actual_token)
                        if value is None:
                            # add it to the symbol table
                            value = self.__constants.count
                            self.__constants.insert(actual_token, value)
                        # add it to the pif
                        self.__pif.add("const", value)
                    else:
                        raise Exception(f"Invalid token {actual_token} at line {line_number}")

                if remaining_line != '':
                    raise Exception(f"Invalid token {remaining_line} at line {line_number}")
                line_number += 1

        self.__pif_out()
        self.__identifiers_out()
        self.__constants_out()
        print("Lexically correct")

    def __read_token_in(self):
        with open(self.__tokens_filepath, 'r') as file:
            line = file.readline()
            while line != "#reserved_words\n":
                line = file.readline()
            line = file.readline()
            while line != "#operators\n":
                self.__reserved_words.append(line.strip())
                line = file.readline()
            line = file.readline()
            while line != "#separators\n":
                self.__operators.append(line.strip())
                line = file.readline()
            line = file.readline()
            while line != "":
                self.__separators.append(line.strip())
                line = file.readline()
        self.__separators.append(' ')

    # pif.out
    def __pif_out(self):
        with open("pif.out", 'w') as file:
            file.write(str(self.__pif))

    # identifiers.out
    def __identifiers_out(self):
        with open("identifiers.out", 'w') as file:
            file.write(str(self.__identifiers))

    # constants.out
    def __constants_out(self):
        with open("constants.out", 'w') as file:
            file.write(str(self.__constants))

