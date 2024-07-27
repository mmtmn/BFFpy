import string
import numpy as np
import random
import matplotlib.pyplot as plt
import zlib
from mpl_toolkits.mplot3d import Axes3D

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
        tape_size = max(self.initial_tape_size, int(np.ceil(len(program) ** (1/3.0))))
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


class PrimordialSoup3D:
    def __init__(self, num_programs=128, tape_size=8):
        self.num_programs = num_programs
        self.tape_size = tape_size
        self.programs = [''.join(random.choices(string.ascii_letters + string.digits, k=tape_size**3)) for _ in range(num_programs)]
        self.interpreter = BFF3DInterpreter(tape_size=tape_size)

    def run_epoch(self):
        for i in range(self.num_programs):
            for j in range(i + 1, self.num_programs):
                self.run_interaction(i, j)

    def run_interaction(self, index_a, index_b):
        program_a = self.programs[index_a]
        program_b = self.programs[index_b]
        concatenated = program_a + program_b
        self.interpreter.reset()
        self.interpreter.load_program(concatenated)
        self.interpreter.execute()
        split_point = len(concatenated) // 2
        new_a = ''.join(chr(x) for x in self.interpreter.tape.flat[:split_point])
        new_b = ''.join(chr(x) for x in self.interpreter.tape.flat[split_point:split_point + len(program_b)])
        self.programs[index_a] = new_a
        self.programs[index_b] = new_b

    def mutate(self):
        for i in range(self.num_programs):
            if random.random() < 0.01:  # mutation rate
                tape = list(self.programs[i])
                idx = random.randint(0, len(tape) - 1)
                tape[idx] = random.choice(string.ascii_letters + string.digits)
                self.programs[i] = ''.join(tape)

    def observe(self):
        for program in self.programs:
            print(program)

    def visualize(self, epoch):
        matrix = [sum(ord(char) for char in program) for program in self.programs]
        side_length = int(np.ceil(np.cbrt(self.num_programs)))
        padded_matrix = np.zeros((side_length, side_length, side_length))
        
        for idx, value in enumerate(matrix):
            x, y, z = idx % side_length, (idx // side_length) % side_length, idx // (side_length * side_length)
            padded_matrix[x, y, z] = value

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(padded_matrix, edgecolor='k')
        plt.title(f'Epoch {epoch}')
        plt.show()

def calculate_high_order_entropy(programs):
    total_length = sum(len(p) for p in programs)
    if total_length == 0:
        return 0
    shannon_entropy = -sum((freq / total_length) * np.log2(freq / total_length) 
                           for freq in np.bincount([ord(c) for p in programs for c in p]) if freq > 0)
    kolmogorov_complexity = sum(len(zlib.compress(p.encode('utf-8'))) for p in programs) / len(programs)
    normalized_kolmogorov = kolmogorov_complexity / len(programs[0])
    high_order_entropy = shannon_entropy - normalized_kolmogorov
    return high_order_entropy

def main():
    soup = PrimordialSoup3D(num_programs=128, tape_size=8)
    plt.ion()
    complexities = []
    for epoch in range(10):  # Run for 10 epochs
        soup.run_epoch()
        soup.mutate()
        soup.visualize(epoch)
        complexity = calculate_high_order_entropy(soup.programs)
        complexities.append(complexity)
        input("Press Enter to continue to the next epoch...")  # Wait for user input

    plt.ioff()
    plt.show()

    # Plot complexity over time
    plt.figure()
    plt.plot(complexities)
    plt.xlabel('Epoch')
    plt.ylabel('High-order Entropy')
    plt.title('Complexity Over Time')
    plt.show()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
