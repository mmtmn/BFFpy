import random
import string

class BFFInterpreter:
    def __init__(self, tape_size=64):
        self.initial_tape_size = tape_size
        self.tape = [0] * tape_size
        self.head0 = 0
        self.head1 = 0
        self.instruction_pointer = 0

    def reset(self):
        self.tape = [0] * self.initial_tape_size
        self.head0 = 0
        self.head1 = 0
        self.instruction_pointer = 0

    def load_program(self, program):
        tape_size = max(self.initial_tape_size, len(program))
        self.tape = [0] * tape_size  # Resize the tape if the program is longer
        for i, char in enumerate(program):
            self.tape[i] = ord(char)

    def execute(self):
        while self.instruction_pointer < len(self.tape):
            command = chr(self.tape[self.instruction_pointer])
            if command == '>':
                self.head0 = (self.head0 + 1) % len(self.tape)
            elif command == '<':
                self.head0 = (self.head0 - 1) % len(self.tape)
            elif command == '}':
                self.head1 = (self.head1 + 1) % len(self.tape)
            elif command == '{':
                self.head1 = (self.head1 - 1) % len(self.tape)
            elif command == '+':
                self.tape[self.head0] = (self.tape[self.head0] + 1) % 256
            elif command == '-':
                self.tape[self.head0] = (self.tape[self.head0] - 1) % 256
            elif command == '.':
                self.tape[self.head1] = self.tape[self.head0]
            elif command == ',':
                self.tape[self.head0] = self.tape[self.head1]
            elif command == '[':
                if self.tape[self.head0] == 0:
                    self.jump_forward()
            elif command == ']':
                if self.tape[self.head0] != 0:
                    self.jump_backward()
            self.instruction_pointer += 1

    def jump_forward(self):
        open_brackets = 1
        while open_brackets != 0:
            self.instruction_pointer += 1
            if self.instruction_pointer >= len(self.tape):
                break
            if chr(self.tape[self.instruction_pointer]) == '[':
                open_brackets += 1
            elif chr(self.tape[self.instruction_pointer]) == ']':
                open_brackets -= 1

    def jump_backward(self):
        open_brackets = 1
        while open_brackets != 0:
            self.instruction_pointer -= 1
            if self.instruction_pointer < 0:
                break
            if chr(self.tape[self.instruction_pointer]) == ']':
                open_brackets += 1
            elif chr(self.tape[self.instruction_pointer]) == '[':
                open_brackets -= 1
