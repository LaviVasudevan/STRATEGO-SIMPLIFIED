# chromosome.py
import random
from piece import Piece
from constants import BOARD_SIZE, POPULATION_SIZE, GENERATIONS, MUTATION_RATE

class Chromosome:
    BOARD_SIZE = 8
    def __init__(self, board_config=None):
        # Chromosome contains both AI and Human board configuration
        self.board_config = board_config if board_config else self.random_config()
        self.fitness = 0

    def random_config(self):
        board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        # AI Fixed rows
        ai_row_0 = ['B', 'F', 2, 2, 1, 5, 3, 4]
        ai_row_1 = [2, 2, 2, 2, 6, 3, 4, 'B']
        
        # Human Fixed rows
        human_row_7 = ['B', 'F', 2, 2, 1, 5, 3, 4]
        human_row_6 = [2, 2, 2, 2, 6, 3, 4, 'B']

        # Place AI pieces in randomized columns within the fixed row structure
        board[0] = [Piece(rank, 'AI') for rank in random.sample(ai_row_0, len(ai_row_0))]
        board[1] = [Piece(rank, 'AI') for rank in random.sample(ai_row_1, len(ai_row_1))]

        # Place Human pieces in randomized columns within the fixed row structure
        board[6] = [Piece(rank, 'Human') for rank in random.sample(human_row_6, len(human_row_6))]
        board[7] = [Piece(rank, 'Human') for rank in random.sample(human_row_7, len(human_row_7))]

        return board

def is_adjacent_to_flag(row, col, chromosome):
    """Check if a given cell is adjacent to the AI's flag."""
    flag_position = None
    for r in range(2):  # Only search AI's first two rows
        for c in range(Chromosome.BOARD_SIZE):
            piece = chromosome.board_config[r][c]
            if piece and piece.player == "AI" and piece.rank == 'F':
                flag_position = (r, c)
                break
    if flag_position:
        # Check if the piece is one row away or one column away, but not both
        row_diff = abs(flag_position[0] - row)
        col_diff = abs(flag_position[1] - col)
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
    return False


def is_near_bomb_zone(position, chromosome):
    """Check if a Miner is near any AI bombs."""
    row, col = position
    for r in range(2):  # Only search AI's first two rows
        for c in range(Chromosome.BOARD_SIZE):
            piece = chromosome.board_config[r][c]
            if piece and piece.player == "AI" and piece.rank == 'B':
                if abs(r - row) <= 1 and abs(c - col) <= 1:
                    return True
    return False

def calculate_fitness(chromosome):
    fitness = 0
    
    # Iterate through the entire board
    for row in range(Chromosome.BOARD_SIZE):
        for col in range(Chromosome.BOARD_SIZE):
            piece = chromosome.board_config[row][col]
            
            if piece and piece.player == "AI":
                if piece.rank == 'F':
                    fitness += 100  # Reward flag protection
                elif piece.rank == 'B' and is_adjacent_to_flag(row, col, chromosome):
                    fitness += 30  # Reward bombs adjacent to flag

                if piece.rank in [2, 4]:  # Scouts or Sergeants (AI)
                    if row == 1:  # Reward for AI being in row 1 (closer to opponent)
                        fitness += 20
                    elif row == 0:  # Penalize for AI being too far back (row 0)
                        fitness -= 10

                if piece.rank == 3:  # Miner (AI)
                    if is_near_bomb_zone((row, col), chromosome):
                        fitness += 20  # Reward Miners near bombs

                if piece.rank == 1:  # Spy (AI)
                    fitness -= row * 3  # Penalize Spy near frontlines
                
            elif piece and piece.player == "Human":
                if piece.rank == 'F':
                    fitness += 100  # Reward flag protection
                elif piece.rank == 'B' and is_adjacent_to_flag(row, col, chromosome):
                    fitness += 30  # Reward bombs adjacent to flag

                if piece.rank in [2, 4]:  # Scouts or Sergeants (Human)
                    if row == 6:  # Reward for human being in row 6 (closer to opponent)
                        fitness += 20
                    elif row == 7:  # Penalize for human being too far back (row 7)
                        fitness -= 10

                if piece.rank == 3:  # Miner (Human)
                    if is_near_bomb_zone((row, col), chromosome):
                        fitness += 20  # Reward Miners near bombs

                if piece.rank == 1:  # Spy (Human)
                    fitness -= row * 3  # Penalize Spy near frontlines

    chromosome.fitness = fitness


def crossover(parent1, parent2):
    child_config = [[None for _ in range(Chromosome.BOARD_SIZE)] for _ in range(Chromosome.BOARD_SIZE)]
    
    # Iterate through each row
    for row in range(Chromosome.BOARD_SIZE):
        # Randomly select one of the parents' rows for the child
        if random.random() < 0.5:
            # Select row from parent1
            child_config[row] = parent1.board_config[row].copy()
        else:
            # Select row from parent2
            child_config[row] = parent2.board_config[row].copy()

    return Chromosome(child_config)

def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        ai_positions_row_0 = [(0, j) for j in range(Chromosome.BOARD_SIZE)]
        ai_positions_row_1 = [(1, j) for j in range(Chromosome.BOARD_SIZE)]
        random.shuffle(ai_positions_row_0)
        random.shuffle(ai_positions_row_1)
        
        # Mutate AI rows by swapping pieces within rows
        pos1, pos2 = ai_positions_row_0[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]

        pos1, pos2 = ai_positions_row_1[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]

        human_positions_row_6 = [(6, j) for j in range(Chromosome.BOARD_SIZE)]
        human_positions_row_7 = [(7, j) for j in range(Chromosome.BOARD_SIZE)]
        random.shuffle(human_positions_row_6)
        random.shuffle(human_positions_row_7)

        # Mutate Human rows by swapping pieces within rows
        pos1, pos2 = human_positions_row_6[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]

        pos1, pos2 = human_positions_row_7[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]

def genetic_algorithm():
    population = [Chromosome() for _ in range(POPULATION_SIZE)]

    for gen in range(GENERATIONS):
        for chrom in population:
            calculate_fitness(chrom)

        population.sort(key=lambda x: x.fitness, reverse=True)
        population = population[:POPULATION_SIZE // 2]

        while len(population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:POPULATION_SIZE // 4], 2)
            child = crossover(parent1, parent2)
            mutate(child)
            population.append(child)

        print(f"Generation {gen+1} - Best Fitness: {population[0].fitness}")

    return population[0]

