from grammar import Grammar
from recursive_descendant import RecursiveDescendant


def parse_grammar(grammar_file_name: str, sequence_file_name: str, output_file_name: str):
    grammar = Grammar(grammar_file_name)
    parser = RecursiveDescendant(grammar, sequence_file_name, output_file_name)
    parser.parse()


if __name__ == '__main__':
    parse_grammar("grammar.txt", "good_sequence.txt", "good_output.txt")
    parse_grammar("grammar.txt", "bad_sequence.txt", "bad_output.txt")

    parse_grammar("g1.txt", "seq.txt", "o1.txt")
