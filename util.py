import random

import magiccube.solver
import magiccube.solver.basic.basic_solver
from config import conf

magiccube.cube.CubeMove


import magiccube

import magiccube.solver.basic
from magiccube.solver.basic.basic_solver import BasicSolver

def solution_from_file_scramble(solving_method: str):
    
    cube = magiccube.Cube(3)

    cube.rotate(conf.get('default_scramble'))

    solution = BasicSolver(cube).solve()
    
    sol_tmp = []
    for move in solution:
        sol_tmp.append(str(move))

    conf['beginner_solve'] = " ".join(sol_tmp)



solution_from_file_scramble('')

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
