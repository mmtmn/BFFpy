import string
import numpy as np

class BFF3DInterpreter:
    def __init__(self, tape_size=64):
        self.initial_tape_size = tape_size
        self.tape = np.zeros((tape_size, tape_size, tape_size), dtype=int)
        self.head = [0, 0, 0]
        self.instruction_pointer = 0

    def reset(self):
        self.tape.fill(0)
        self.head = [0, 0, 0]
        self.instruction_pointer = 0

    def load_program(self, program):
        tape_size = max(self.initial_tape_size, len(program))
        self.tape = np.zeros((tape_size, tape_size, tape_size), dtype=int)  # Resize the tape if the program is longer
        for i, char in enumerate(program):
            x, y, z = i % tape_size, (i // tape_size) % tape_size, i // (tape_size * tape_size)
            self.tape[x, y, z] = ord(char)

    def execute(self):
        commands = {
            '>': lambda: self.move_head(0, 1),
            '<': lambda: self.move_head(0, -1),
            '}': lambda: self.move_head(1, 1),
            '{': lambda: self.move_head(1, -1),
            ']': lambda: self.move_head(2, 1),
            '[': lambda: self.move_head(2, -1),
            '+': lambda: self.modify_tape(1),
            '-': lambda: self.modify_tape(-1),
            '.': lambda: self.output_head_value(),
            ',': lambda: self.input_to_head_value(),
        }

        while self.instruction_pointer < self.tape.size:
            x, y, z = self.head
            command = chr(self.tape[x, y, z])
            if command in commands:
                commands[command]()
            self.instruction_pointer += 1

    def move_head(self, dimension, step):
        self.head[dimension] = (self.head[dimension] + step) % len(self.tape)

    def modify_tape(self, value):
        x, y, z = self.head
        self.tape[x, y, z] = (self.tape[x, y, z] + value) % 256

    def output_head_value(self):
        x, y, z = self.head
        print(chr(self.tape[x, y, z]), end='')

    def input_to_head_value(self):
        x, y, z = self.head
        self.tape[x, y, z] = ord(input()[0])

# Example usage:
interpreter = BFF3DInterpreter(tape_size=8)
program = "some 3D Brainfuck variant program"
interpreter.load_program(program)
interpreter.execute()
