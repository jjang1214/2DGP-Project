from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP,SDLK_RETURN, SDLK_SPACE

import game_world
import game_framework
from game_world import w_width, w_height

from state_machine import StateMachine


def enter_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RETURN

def enter_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RETURN

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE


idle = [
    (51+128*0,0,26,72),
    (51+128*1,0,26,72),
    (51+128*2,0,26,72),
    (51+128*3,0,26,72),
    (51+128*4,0,26,72),
    (51+128*5,0,26,72),
    (51+128*6,0,26,72),
    (51+128*7,0,26,72),
    (51+128*8,0,26,72)
]

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

char1_width = 26
char1_height = 72

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_idle = 9
FRAMES_PER_ACTION_move = 12

class Idle:
    def __init__(self, char1):
        self.char1 = char1

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.char1.frame = (self.char1.frame + FRAMES_PER_ACTION_idle * ACTION_PER_TIME * game_framework.frame_time) % 9

    def draw(self):
        frame_data = idle[int(self.char1.frame)]
        left, bottom, width, height = frame_data

        if self.char1.dir == 1:  # right
            self.char1.image_idle.clip_draw(left, bottom, width, height, self.char1.x, self.char1.y)
        else:  # left
            self.char1.image_idle.clip_composite_draw(left, bottom, width, height, 0, 'h', self.char1.x, self.char1.y, width, height)




class Move:
    def __init__(self, char1):
        self.char1 = char1

    def enter(self, e):
        if enter_down(e):
            pass

        elif space_down(e):
            self.char1.dir *= -1

    def exit(self, e):
        pass

    def do(self):
        self.char1.frame = (self.char1.frame + FRAMES_PER_ACTION_move * ACTION_PER_TIME * game_framework.frame_time) % 12

    def draw(self):
        frame_data = move[int(self.char1.frame)]
        left, bottom, width, height = frame_data

        if self.char1.dir == 1:  # right
            self.char1.image_move.clip_draw(left, bottom, width, height, self.char1.x, self.char1.y)
        else:  # left
            self.char1.image_move.clip_composite_draw(left, bottom, width, height, 0,'h',self.char1.x, self.char1.y,width,height)


class character1:
    def __init__(self):
        self.x,self.y = w_width/2, w_height // 2
        self.frame = 0
        self.dir = -1
        self.image_idle = load_image('../image/girl1_Idle.png')
        self.image_move = load_image('../image/girl1_Walk.png')

        self.IDLE=Idle(self)
        self.MOVE=Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE:{enter_down : self.MOVE, space_down : self.MOVE},
                self.MOVE:{enter_up : self.IDLE, space_up : self.IDLE},
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
        return self.x - char1_width/2, self.y - char1_height/2, self.x + char1_width/2, self.y + char1_height/2

    def handle_collision(self, group, other):
        pass