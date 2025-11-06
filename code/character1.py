from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT

import game_world
import game_framework

from state_machine import StateMachine


time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


move=[
    (49,0,36,71),
    (177,0,31,72),
    (304,0,29,73),
    (430,0,30,74),
    (558,0,32,73),
    (687,0,30,72),
    (817,0,36,71),
    (947,0,29,72),
    (1076,0,23,73),
    (1205,0,24,73),
    (1332,0,27,72),
    (1459,0,28,71)
]

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_move = 12

class Idle:
    def __init__(self, char1):
        self.char1 = char1

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.char1.frame = (self.char1.frame + FRAMES_PER_ACTION_move * ACTION_PER_TIME * game_framework.frame_time) % 12

    def draw(self):
        if self.char1.face_dir == 1: # right
            self.char1.image_idle.clip_draw(51 + int(self.char1.frame) * 128, 0, 36, 72, self.char1.x, self.char1.y)
        else: # face_dir == -1: # left
            self.char1.image_idle.clip_draw(51 + int(self.char1.frame) * 128, 0, 36, 72, self.char1.x, self.char1.y)




class Move:
    def __init__(self, char1):
        self.char1 = char1

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.char1.dir = self.char1.face_dir = 1
        elif left_down(e) or right_up(e):
            self.char1.dir = self.char1.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.char1.frame = (self.char1.frame + FRAMES_PER_ACTION_move * ACTION_PER_TIME * game_framework.frame_time) % 12
        #self.char1.x +=

    def draw(self):
        frame_data = move[int(self.char1.frame)]
        left, bottom, width, height = frame_data

        if self.char1.face_dir == 1:  # right
            self.char1.image_move.clip_draw(left, bottom, width, height, self.char1.x, self.char1.y)
        else:  # left
            self.char1.image_move.clip_composite_draw(left, bottom, width, height, 0,'h',self.char1.x, self.char1.y,width,height)


class character1:
    def __init__(self):
        self.x,self.y = 400,60
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image_idle = load_image('../image/girl1_Idle.png')
        self.image_move = load_image('../image/girl1_Walk.png')

        self.IDLE=Idle(self)
        self.MOVE=Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE:{right_down : self.MOVE, left_down : self.MOVE},
                self.MOVE:{right_up : self.IDLE, left_up : self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 40

    def handle_collision(self, group, other):
        pass