import tkinter as tk
from tkinter import messagebox


class FAReader:
    """
    Documentation:
        The FAReader class is used to read a finite automaton from a file and check if a sequence is accepted by the FA.
        The file format is as follows (example):
            #States
            Q0 Q1 Q2
            #Alphabet
            0 1
            #Transitions
            Q0 0 Q1
            Q0 1 Q0
            Q1 0 Q2
            Q1 1 Q0
            Q2 0 Q2
            Q2 1 Q2
            #Initial State
            Q0
            #Final States
            Q2
        __init__(self, input_filepath):
            Reads the FA from the input file
            :param input_filepath: The path to the input file
        is_dfa(self):
            Checks if the FA is deterministic
            :return: True if the FA is deterministic, False otherwise
        accept_sequence(self, sequence):
            Checks if a sequence is accepted by the FA
            :param sequence: The sequence to be checked
            :return: "Accepted" if the sequence is accepted, the reason why it is not accepted otherwise
        get_states(self):
            :return: The states of the FA. Format: List[state1, state2, ...]
        get_alphabet(self):
            :return: The alphabet of the FA. Format: List[letter1, letter2, ...]
        get_transitions(self):
            :return: The transitions of the FA. Format: Dict[from_state][letter] = List[to_state1, to_state2, ...]
        get_initial_state(self):
            :return: The initial state of the FA. Format: String
        get_final_states(self):
            :return: The final states of the FA. Format: List[state1, state2, ...]
        get_input_filepath(self):
            :return: The path to the input file. Format: String
    """
    def __init__(self, input_filepath):
        self.__input_filepath = input_filepath
        with open(input_filepath, 'r') as file:
            if file.readline() != "#States\n":
                raise Exception("Invalid file format")
            line = file.readline()
            self.__states = [str(state) for state in line.strip().split(" ")]
            if file.readline() != "#Alphabet\n":
                raise Exception("Invalid file format")
            line = file.readline()
            self.__alphabet = [str(letter) for letter in line.strip().split(" ")]
            if file.readline() != "#Transitions\n":
                raise Exception("Invalid file format")
            self.__transitions = {}
            for line in file:
                if line == "#Initial State\n":
                    break
                tokens = line.strip().split(" ")
                if len(tokens) != 3:
                    raise Exception("Invalid file format")
                from_state = tokens[0]
                letter = tokens[1]
                to_state = tokens[2]
                if from_state not in self.__states and to_state not in self.__states:
                    raise Exception("Invalid file format")
                if letter not in self.__alphabet:
                    raise Exception("Invalid file format")

                if from_state not in self.__transitions:
                    self.__transitions[from_state] = {}
                if letter not in self.__transitions[from_state]:
                    self.__transitions[from_state][letter] = []
                self.__transitions[from_state][letter].append(to_state)

            line = file.readline()
            initial_state = line.strip()
            if initial_state not in self.__states:
                raise Exception("Invalid file format")
            self.__initial_state = initial_state
            if file.readline() != "#Final States\n":
                raise Exception("Invalid file format")
            line = file.readline()

            self.__final_states = []
            for state in line.strip().split(" "):
                if state not in self.__states:
                    raise Exception("Invalid file format")
                self.__final_states.append(state)

    def is_dfa(self):
        if '' in self.__alphabet:
            return False
        for from_state in self.__transitions:
            for letter in self.__transitions[from_state]:
                if len(self.__transitions[from_state][letter]) > 1:
                    return False
        return True

    def accept_sequence(self, sequence):
        current_state = self.__initial_state
        if not self.is_dfa():
            return "Not a DFA"
        for letter in sequence:
            if letter not in self.__alphabet:
                return f"\"{letter}\" is not in the alphabet"
            if letter not in self.__transitions[current_state]:
                return f"\"{letter}\" is not a valid transition from state {current_state}"
            current_state = self.__transitions[current_state][letter][0]
        if current_state in self.__final_states:
            return "Accepted"
        else:
            return "Did not get to a final state"

    def get_states(self):
        return self.__states

    def get_alphabet(self):
        return self.__alphabet

    def get_transitions(self):
        return self.__transitions

    def get_initial_state(self):
        return self.__initial_state

    def get_final_states(self):
        return self.__final_states

    def get_input_filepath(self):
        return self.__input_filepath


root = tk.Tk()
root.title("Finite Automaton Display")


fa_reader = None


def load_fa():
    file_path = entry_filepath.get()
    try:
        global fa_reader
        fa_reader = FAReader(file_path)
        states_txt = f"States:\n{', '.join(fa_reader.get_states())}"
        alphabet_txt = f"Alphabet:\n{', '.join(fa_reader.get_alphabet())}"
        transitions_txt = "Transitions:\n" + "\n".join(
            [f"{state} -> {letter} -> {', '.join(transitions)}" for state in fa_reader.get_transitions() for
             letter, transitions in fa_reader.get_transitions()[state].items()])
        initial_state_txt = f"Initial State:\n{fa_reader.get_initial_state()}"
        final_states_txt = f"Final States:\n{', '.join(fa_reader.get_final_states())}"

        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)
        display_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Display", menu=display_menu)
        display_menu.add_command(label="States", command=lambda: display_fa_info.config(text=states_txt))
        display_menu.add_command(label="Alphabet", command=lambda: display_fa_info.config(text=alphabet_txt))
        display_menu.add_command(label="Transitions", command=lambda: display_fa_info.config(text=transitions_txt))
        display_menu.add_command(label="Initial State", command=lambda: display_fa_info.config(text=initial_state_txt))
        display_menu.add_command(label="Final States", command=lambda: display_fa_info.config(text=final_states_txt))

        if fa_reader.is_dfa():
            display_is_dfa.config(text="Is DFA: Yes")
        else:
            display_is_dfa.config(text="Is DFA: No")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create and place widgets
label_filepath = tk.Label(root, text="File Path:")
label_filepath.grid(row=0, column=0, padx=5, pady=5)

entry_filepath = tk.Entry(root, width=30)
entry_filepath.grid(row=0, column=1, padx=5, pady=5)

button_load = tk.Button(root, text="Load FA", command=load_fa)
button_load.grid(row=0, column=2, padx=5, pady=5)

display_fa_info = tk.Label(root, text="\n")
display_fa_info.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

display_is_dfa = tk.Label(root, text="Is DFA: ")
display_is_dfa.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

label_sequence = tk.Label(root, text="Sequence:")
label_sequence.grid(row=7, column=0, padx=5, pady=5)

entry_sequence = tk.Entry(root, width=30)
entry_sequence.grid(row=7, column=1, padx=5, pady=5)

display_accepted_result = tk.Label(root, text="")
display_accepted_result.grid(row=8, column=0, columnspan=3, padx=5, pady=5)


# Function to check if a sequence is accepted by the FA


def check_sequence():
    try:
        if fa_reader is None:
            raise Exception("Please load a FA first")
        sequence = entry_sequence.get()
        result = fa_reader.accept_sequence(sequence)
        display_accepted_result.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", str(e))


button_check = tk.Button(root, text="Check Sequence", command=check_sequence)
button_check.grid(row=7, column=2, padx=5, pady=5)

# Run the Tkinter event loop
root.mainloop()
