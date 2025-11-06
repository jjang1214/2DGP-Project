from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT

import game_world
import game_framework
from game_world import w_width, w_height

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


idle = [
    (49,0,30,72),
    (177,0,30,72),
    (304,0,31,73),
    (431,0,32,73),
    (560,0,31,73),
    (689,0,30,72)
]

move=[
    (46,0,35,73),
    (176,0,29,72),
    (304,0,26,73),
    (432,0,24,74),
    (559,0,27,74),
    (686,0,30,74),
    (814,0,35,73),
    (943,0,30,72),
    (1072,0,26,73),
    (1200,0,27,74),
    (1327,0,29,74),
    (1455,0,30,74)
]

char3_width = 30
char3_height = 72

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_idle = 6
FRAMES_PER_ACTION_move = 12

class Idle:
    def __init__(self, char3):
        self.char3 = char3

    def enter(self, e):
        self.char3.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.char3.frame = (self.char3.frame + FRAMES_PER_ACTION_idle * ACTION_PER_TIME * game_framework.frame_time) % 6

    def draw(self):
        frame_data = idle[int(self.char3.frame)]
        left, bottom, width, height = frame_data

        if self.char3.face_dir == 1:  # right
            self.char3.image_idle.clip_draw(left, bottom, width, height, self.char3.x, self.char3.y)
        else:  # left
            self.char3.image_idle.clip_composite_draw(left, bottom, width, height, 0, 'h', self.char3.x, self.char3.y, width, height)




class Move:
    def __init__(self, char3):
        self.char3 = char3

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.char3.dir = self.char3.face_dir = 1
        elif left_down(e) or right_up(e):
            self.char3.dir = self.char3.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.char3.frame = (self.char3.frame + FRAMES_PER_ACTION_move * ACTION_PER_TIME * game_framework.frame_time) % 12
        #self.char3.x +=

    def draw(self):
        frame_data = move[int(self.char3.frame)]
        left, bottom, width, height = frame_data

        if self.char3.face_dir == 1:  # right
            self.char3.image_move.clip_draw(left, bottom, width, height, self.char3.x, self.char3.y)
        else:  # left
            self.char3.image_move.clip_composite_draw(left, bottom, width, height, 0,'h',self.char3.x, self.char3.y,width,height)


class character3:
    def __init__(self):
        self.x,self.y = w_width/2, 100
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image_idle = load_image('../image/girl3_Idle.png')
        self.image_move = load_image('../image/girl3_Walk.png')

        self.IDLE=Idle(self)
        self.MOVE=Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE:{right_down : self.MOVE, left_down : self.MOVE, right_up: self.MOVE, left_up: self.MOVE},
                self.MOVE:{right_up : self.IDLE, left_up : self.IDLE, right_down: self.IDLE, left_down: self.IDLE}
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
        return self.x - char3_width/2, self.y - char3_height/2, self.x + char3_width/2, self.y + char3_height/2

    def handle_collision(self, group, other):
        pass