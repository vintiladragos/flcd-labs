from grammar import Grammar

if __name__ == '__main__':
    filename = "g1.txt"
    grammar = Grammar(filename)

    print(grammar)

    if grammar.cfg_check():
        print("The grammar is a Context-Free Grammar (CFG).\n")
    else:
        print("The grammar is not a Context-Free Grammar (CFG).\n")

    non_terminal = "C"
    print(f"Productions of the non-terminal {non_terminal}:\n\t{grammar.productions_for_non_terminal(non_terminal)}")
