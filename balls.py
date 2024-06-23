"""
Example usage of the basic cube solver.
"""

import random
import magiccube


def solution_from_file_scramble(solving_method: str):
    
    cube = magiccube.Cube(3,"BBBBBBBBBWWWWWWWWWRRRRRRRRRYYYYYYYYYOOOOOOOOOGGGGGGGGG")
    
    print(cube)

solution_from_file_scramble('')