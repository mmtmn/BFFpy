import random
import string
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

def main():
    soup = PrimordialSoup(num_programs=128, tape_size=64)
    for epoch in range(1000):  # Run for 1000 epochs
        soup.run_epoch()
        soup.mutate()
        soup.observe()

if __name__ == "__main__":
    main()
