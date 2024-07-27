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
        commands = {
            '>': lambda: self.move_head0(1),
            '<': lambda: self.move_head0(-1),
            '}': lambda: self.move_head1(1),
            '{': lambda: self.move_head1(-1),
            '+': lambda: self.modify_tape(1),
            '-': lambda: self.modify_tape(-1),
            '.': lambda: self.copy_head0_to_head1(),
            ',': lambda: self.copy_head1_to_head0(),
            '[': lambda: self.jump_forward() if self.tape[self.head0] == 0 else None,
            ']': lambda: self.jump_backward() if self.tape[self.head0] != 0 else None
        }

        while self.instruction_pointer < len(self.tape):
            command = chr(self.tape[self.instruction_pointer])
            if command in commands:
                commands[command]()
            self.instruction_pointer += 1

    def move_head0(self, step):
        self.head0 = (self.head0 + step) % len(self.tape)

    def move_head1(self, step):
        self.head1 = (self.head1 + step) % len(self.tape)

    def modify_tape(self, value):
        self.tape[self.head0] = (self.tape[self.head0] + value) % 256

    def copy_head0_to_head1(self):
        self.tape[self.head1] = self.tape[self.head0]

    def copy_head1_to_head0(self):
        self.tape[self.head0] = self.tape[self.head1]

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
