import random
import string
import matplotlib.pyplot as plt
import numpy as np
import zlib
from bff_interpreter import BFFInterpreter

class PrimordialSoup:
    def __init__(self, num_programs=128, tape_size=64):
        self.num_programs = num_programs
        self.tape_size = tape_size
        self.programs = [''.join(random.choices(string.ascii_letters + string.digits, k=tape_size)) for _ in range(num_programs)]
        self.interpreter = BFFInterpreter(tape_size=tape_size)

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
        new_a = ''.join(chr(x) for x in self.interpreter.tape[:split_point])
        new_b = ''.join(chr(x) for x in self.interpreter.tape[split_point:split_point + len(program_b)])
        self.programs[index_a] = new_a
        self.programs[index_b] = new_b

    def mutate(self):
        for i in range(self.num_programs):
            if random.random() < 0.01:  # mutation rate
                tape = list(self.programs[i])
                tape[random.randint(0, self.tape_size - 1)] = random.choice(string.ascii_letters + string.digits)
                self.programs[i] = ''.join(tape)

    def observe(self):
        for program in self.programs:
            print(program)

    def visualize(self, epoch):
        matrix = [sum(ord(char) for char in program) for program in self.programs]
        side_length = int(np.ceil(np.sqrt(self.num_programs)))
        padded_matrix = np.zeros((side_length, side_length))
        
        for idx, value in enumerate(matrix):
            row = idx // side_length
            col = idx % side_length
            padded_matrix[row, col] = value

        plt.clf()
        plt.imshow(padded_matrix, cmap='Greens', interpolation='nearest')
        plt.axis('off')
        plt.gcf().set_size_inches(10, 10)
        plt.title(f'Epoch {epoch}')
        plt.pause(0.01)

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
    soup = PrimordialSoup(num_programs=128, tape_size=64)
    plt.ion()
    complexities = []
    for epoch in range(100):
        soup.run_epoch()
        soup.mutate()
        soup.visualize(epoch)
        complexity = calculate_high_order_entropy(soup.programs)
        complexities.append(complexity)
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
