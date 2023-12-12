from texttable import Texttable

from node import Node


class Position:
    def __init__(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def increment(self):
        self.__value += 1


class ParserOutput:
    def __init__(self, parser):
        self.__tree = []
        self.__parser = parser

    def __create_parsing_tree(self) -> Node:
        grammar = self.__parser.get_grammar()
        working_stack = self.__parser.get_working_stack()

        non_terminals = grammar.get_non_terminals()

        non_terminal_production_list = []
        for _, index in working_stack:
            if index != -1:
                non_terminal_production_list.append(index)

        parent = None
        node = Node(parent, grammar.get_start_symbol(), [])

        symbol, index = working_stack[0]
        children = grammar.get_list_of_productions_for_non_terminal(symbol)[index - 1]
        for child in children:
            child_node = Node(node, child, [])
            node.children.append(child_node)

        position = Position(1)

        def depth_search(auxiliary_node: Node):
            for each_child in auxiliary_node.children:
                if each_child.symbol in non_terminals:
                    children_of_non_terminal_child = \
                        grammar.get_list_of_productions_for_non_terminal(symbol)[
                            non_terminal_production_list[position.get_value()] - 1]
                    for child_of_non_terminal_child in children_of_non_terminal_child:
                        child_of_non_terminal_child_node = Node(each_child, child_of_non_terminal_child, [])
                        each_child.children.append(child_of_non_terminal_child_node)

                    position.increment()
                    depth_search(each_child)

        depth_search(node)

        return node

    def __create_parsing_tree_table_representation(self):
        node = self.__create_parsing_tree()
        node.number = 1
        index = 1
        self.__tree.append([index, node.symbol, 0, 0])
        index += 1

        queue = list(node.children)
        while len(queue):
            current_node = queue.pop(0)
            queue.extend(current_node.children)

            parent = current_node.parent
            if parent.children[0] == current_node:
                right_sibling = 0
            else:
                right_sibling = index - 1

            current_node.number = index

            self.__tree.append([index, current_node.symbol, current_node.parent.number, right_sibling])
            index += 1

    def get_tree_table_representation(self):
        self.__create_parsing_tree_table_representation()

        table_representation = [["Index", "Info", "Parent", "Right sibling"]]
        table_representation.extend(self.__tree)

        text_table = Texttable()
        text_table.add_rows(table_representation)

        return text_table.draw()

    def print_string_to_file(self, string: str):
        file_name = self.__parser.get_output_file()

        with open(file_name, 'a') as file:
            file.write(string)

    def print_string_to_file_and_console(self, string: str):
        self.print_string_to_file(f"{string}\n")
        print(string)
