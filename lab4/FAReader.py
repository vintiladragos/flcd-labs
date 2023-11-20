import tkinter as tk
from tkinter import messagebox


class FAReader:
    def __init__(self,input_filepath):
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


    # getters
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

# Function to load the FA from a file
fa_reader = None
def load_fa():
    file_path = entry_filepath.get()
    try:
        global fa_reader
        fa_reader = FAReader(file_path)
        display_states.config(text=f"States: {', '.join(fa_reader.get_states())}")
        display_alphabet.config(text=f"Alphabet: {', '.join(fa_reader.get_alphabet())}")
        display_transitions.config(text="Transitions:\n" + "\n".join([f"{state} -> {letter} -> {', '.join(transitions)}" for state in fa_reader.get_transitions() for letter, transitions in fa_reader.get_transitions()[state].items()]))
        display_initial_state.config(text=f"Initial State: {fa_reader.get_initial_state()}")
        display_final_states.config(text=f"Final States: {', '.join(fa_reader.get_final_states())}")
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

display_states = tk.Label(root, text="States: ")
display_states.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

display_alphabet = tk.Label(root, text="Alphabet: ")
display_alphabet.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

display_transitions = tk.Label(root, text="Transitions: ")
display_transitions.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

display_initial_state = tk.Label(root, text="Initial State: ")
display_initial_state.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

display_final_states = tk.Label(root, text="Final States: ")
display_final_states.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

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
    file_path = entry_filepath.get()
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