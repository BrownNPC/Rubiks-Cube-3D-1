import random
import magiccube

from rubik_solver import utils


cube = magiccube.Cube().rotate



def generate_rubiks_scramble(length=20):
    moves = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2"]
    scramble = []
    last_move = ""
    
    for _ in range(length):
        move = random.choice(moves)
        # Avoid consecutive moves of the same face
        while move[0] == last_move:
            move = random.choice(moves)
        
        scramble.append(move)
        last_move = move[0]
    
    return " ".join(scramble)
