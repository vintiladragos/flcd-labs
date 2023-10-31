from lab2.symbol_table import SymbolTable
import re
from program_internal_form import PIF

filename = "../lab1a/p3.txt"

# read token.in to get the reserved words, operators, and separators
reserved_words = []
operators = []
separators = []
pif = PIF()

identifier_regex = r'[a-zA-Z]([a-zA-Z]|[0-9]|_)*'

const_int_regex = r'-?\d+'
const_string_regex = r'"[a-zA-Z0-9_]*"'
const_char_regex = r"'[a-zA-Z0-9]'"
constant_regex = r'(?:' + const_int_regex + r'|' + const_string_regex + r'|' + const_char_regex + r')'
with open("../lab1b/token.in", 'r') as file:
    line = file.readline()
    while line != "#reserved_words\n":
        line = file.readline()
    line = file.readline()
    while line != "#operators\n":
        reserved_words.append(line.strip())
        line = file.readline()
    line = file.readline()
    while line != "#separators\n":
        operators.append(line.strip())
        line = file.readline()
    line = file.readline()
    while line != "":
        separators.append(line.strip())
        line = file.readline()
separators.append(' ')
# whole words only
reserved_words_regex = r'(?:' + '|'.join(re.escape(c) for c in reserved_words) + r')'
# reserved_words_regex = r'(?:^|\W)(' + '|'.join(re.escape(c) for c in reserved_words) + r')(?:$|\W)'
separators_regex = r'[' + ''.join(re.escape(c) for c in separators) + r']'
operators_regex = '|'.join(re.escape(c) for c in operators)


identifiers = SymbolTable()
constants = SymbolTable()

with open(filename, 'r') as file:
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
        token_pattern = re.compile(r'(' + reserved_words_regex + r'|' + operators_regex + r'|' + separators_regex + r'|' + identifier_regex + r'|' + constant_regex + r')')
        remaining_line = line
        for token in token_pattern.findall(line):
            actual_token = token[0]
            remaining_line = remaining_line.replace(actual_token, '', 1)
            # if the token is a reserved word, operator, or separator
            if re.match(reserved_words_regex, actual_token) or re.match(operators_regex, actual_token) or re.match(separators_regex, actual_token):
                if actual_token != ' ':
                    # add it to the pif
                    pif.add(actual_token, -1)
            # if the token is an identifier
            elif re.match(identifier_regex, actual_token):
                # if the identifier is not in the symbol table
                value = identifiers.lookup(actual_token)
                if value is None:
                    # add it to the symbol table
                    value = identifiers.count
                    identifiers.insert(actual_token, value)
                # add it to the pif
                pif.add("id", value)
            # if the token is a constant
            elif re.match(constant_regex, actual_token):
                # if the constant is not in the symbol table
                value = constants.lookup(actual_token)
                if value is None:
                    # add it to the symbol table
                    value = constants.count
                    constants.insert(actual_token, value)
                # add it to the pif
                pif.add("const", value)
            else:
                raise Exception(f"Invalid token {actual_token} at line {line_number}")
        if remaining_line != '':
            raise Exception(f"Invalid token {remaining_line} at line {line_number}")
        line_number += 1

# pif.out
with open("pif.out", 'w') as file:
    file.write(str(pif))

# identifiers.out
with open("identifiers.out", 'w') as file:
    file.write(str(identifiers))

# constants.out
with open("constants.out", 'w') as file:
    file.write(str(constants))

# message if the program is lexically correct
print("Lexically correct")
