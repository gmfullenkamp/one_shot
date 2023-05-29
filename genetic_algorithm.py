import random
import string
from tqdm import tqdm

DNA_CHOICES = string.ascii_lowercase + " "
TARGET_DNA = "wubba lubba dub dub"
POPULATION_SIZE = 1000
MUTATION_CHANCE = 0.1


class GeneticAlgorithm:
    population = []
    generation_number = 0
    target_found = False
    closest_dna = ""
    closest_dna_metric = 0
    closest_dna_parents = ("", "")

    def __init__(self, population_size: int, dna_choices: str, target_dna: str, mutation_chance: float):
        self.dna_length = len(target_dna)
        self.population_size = int(population_size)
        self.dna_choices = dna_choices
        self.target_dna = target_dna
        self.mutation_chance = mutation_chance
        self.set_random_population()

    def set_random_population(self):
        for _ in range(self.population_size):
            char_list = random.choices(self.dna_choices, k=self.dna_length)
            self.population.append(''.join(char_list))

    def calc_next_generation(self):
        # Calculates the fitness and parent_chance
        parent_chance = []
        for subject in self.population:
            metric = self.calc_fitness(subject)
            if metric >= self.closest_dna_metric:
                self.closest_dna_metric = metric
                self.closest_dna = subject
            parent_chance += (metric * [subject])
        next_population = []
        # Makes children from the parent_chance
        for _ in range(self.population_size):
            parent1, parent2 = random.choices(parent_chance, k=2)
            child = self.calc_child_dna(parent1, parent2)
            # Keeps track of the closest dna
            metric = self.calc_fitness(child)
            if metric >= self.closest_dna_metric:
                self.closest_dna_metric = metric
                self.closest_dna = child
                self.closest_dna_parents = (parent1, parent2)
            # Adds the child to the next_population
            next_population.append(child)
            if child == self.target_dna:
                self.target_found = True
        self.population = next_population
        self.generation_number += 1

    def calc_fitness(self, subject: str) -> int:
        metric = 0
        for sub, tar in zip(subject, self.target_dna):
            if sub == tar:
                metric += 1
        return metric

    def calc_child_dna(self, parent1: str, parent2: str) -> str:
        middle_index = int(self.dna_length / 2)
        child = parent1[:middle_index] + parent2[middle_index:]
        # Adds mutations to the child DNA
        mutated_child = ""
        for ch in child:
            if random.uniform(0, 1) < self.mutation_chance:
                mutated_child += random.choice(self.dna_choices)
            else:
                mutated_child += ch
        return mutated_child


def main():
    jeans = GeneticAlgorithm(population_size=POPULATION_SIZE, dna_choices=DNA_CHOICES, target_dna=TARGET_DNA,
                             mutation_chance=MUTATION_CHANCE)
    for _ in (pbar := tqdm(range(10000))):
        jeans.calc_next_generation()
        pbar.set_description(f"Closest DNA: '{jeans.closest_dna}'")
        if jeans.target_found:
            print(f"Target '{jeans.target_dna}' found!")
            print(f"Generations: {jeans.generation_number}")
            print(f"Final Population: {jeans.population}")
            print(f"Target's parent DNA: {jeans.closest_dna_parents}")
            break
    if not jeans.target_found:
        print(f"Target '{jeans.target_dna}' not found...")
        print(f"Generations: {jeans.generation_number}")
        print(f"Final Population: {jeans.population}")
        print(f"Closest DNA: {jeans.closest_dna}")
        print(f"Closest parent DNA: {jeans.closest_dna_parents}")


main()
