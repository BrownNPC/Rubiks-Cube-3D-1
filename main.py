from ursina import *
import asyncio
from threading import Thread
import time

from config import conf

class Game(Ursina.__closure__[0].cell_contents):
    def __init__(self):
        super().__init__()
        self.animate_turns = True
        
        self.last_toggle = time.time()
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)  # plane
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # sky
        EditorCamera()

        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'models/custom_cube', 'textures/rubik_texture'
        self.default_move_speed=0.3
        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {
            'L': 'x', 
            'R': 'x', 
            'U': 'y', 
            'B': 'z', 
            'F': 'z', 
            'D': 'y',
            'M': 'x'  # Define rotation axis for the MIDDLE layer
        }
        self.cubes_side_positions = {
            'L': self.LEFT, 
            'D': self.BOTTOM, 
            'R': self.RIGHT, 
            'F': self.FACE,
            'B': self.BACK, 
            'U': self.TOP,
            'M': self.MIDDLE  # Include positions for the MIDDLE layer
        }

        self.animation_time = self.default_move_speed
        self.action_trigger = True
        self.action_mode = True
        self.message = Text(origin=(0, 0), color=color.white)
        self.toggle_anim()
        window.fullscreen = True
    def solve_cube(self, method:str):
        Thread(target=self.perform_moves, kwargs={'move_string': conf.get(method)}).start()
        ...

    def rotate_side_without_animation(self, side_name, rotation_deg= 90):
        self.action_trigger = False

        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} = {rotation_deg}')

        invoke(self.toggle_animation_trigger, delay=0.007)

    def toggle_anim(self):
        '''switching Rubik's cube turn animation'''
        self.animate_turns = not self.animate_turns

        msg = dedent('S to shuffle | M to Reset | B for beginner | C for CFOP | K for Kociemba | O to toggle animation').strip()
        
        self.message.text = msg
        self.message.origin = (0,19)
    def toggle_animation_trigger(self):
        '''prohibiting side rotation during rotation animation'''
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name, rotation_deg=90):
        self.action_trigger = False
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}({rotation_deg}, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.MIDDLE = {Vec3(0, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP | self.MIDDLE

    def reset_cube(self):
        if self.action_trigger:
            for cube in self.CUBES:
                destroy(cube)
            self.load_game()
            ...

    def perform_moves(self,move_string: str):
        animate = self.animate_turns
        start_time = time.perf_counter()
        """
        move_string = 'R L R'
        """
        if type(move_string) == str: move_string = move_string.split(' ')

        rotation_deg = 90 # how much to turn the cube

        anti_clockwise_moves= [
            "L",
            "B",
            "D",
            ]
        
        clock_wise_prime = [
            "L'",
            "B'",
            "D'"
        ]
        
        for move in move_string:
            rotation_deg = 90
            if '2' in move: # double turn
                rotation_deg = 180
            if move in anti_clockwise_moves:
                rotation_deg *= -1
            if "'" in move and move not in clock_wise_prime:
                rotation_deg *= -1



            while not self.action_trigger:
                time.sleep(0.017)
            
            if animate:
                self.rotate_side(move[0], rotation_deg) # rotate using move letter
            else:
                self.rotate_side_without_animation(move[0], rotation_deg)
        
    def input(self, key, *released):
       
        if key in 'mouse1 mouse3' and self.action_mode and self.action_trigger:
            for hitinfo in mouse.collisions:
                collider_name = hitinfo.entity.name
                if (key == 'mouse1' and collider_name in 'LEFT RIGHT FACE BACK' or
                        key == 'mouse3' and collider_name in 'TOP BOTTOM'):
                    # self.rotate_side(collider_name)
                    break
        if key == 's' and self.action_trigger :
            Thread(target=self.perform_moves, kwargs={'move_string': conf.get('default_scramble')}).start()          
        if key == 'm' :
            self.reset_cube()

        if key == 'b' and self.action_trigger:
            self.solve_cube('beginner_solve')     
        if key == 'c' and self.action_trigger:
            self.solve_cube('cfop_solve')     
        if key == 'k' and self.action_trigger:
            self.solve_cube('20_move_solve')     
        if key == 'o' and time.time()-self.last_toggle > 0.1 :
            self.last_toggle = time.time()
            self.animate_turns = not self.animate_turns

        super().input(key)


if __name__ == '__main__':
    game = Game()
    game.run()