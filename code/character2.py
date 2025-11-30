from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP,SDLK_RETURN, SDLK_SPACE

import game_world
import game_framework
from game_world import w_width, w_height
import data

from state_machine import StateMachine

time_out = lambda e: e[0] == 'TIMEOUT'


def enter_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RETURN

def enter_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RETURN

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

moved = lambda e: e[0] == 'MOVED'


idle2 = [
    (48+128*0,0,32,72),
    (48+128*1,0,32,72),
    (48+128*2,0,32,72),
    (48+128*3,0,32,72),
    (48+128*4,0,32,72),
    (48+128*5,0,32,72),
    (48+128*6,0,32,72)
]

move=[
    (45,0,36,72),
    (173,0,32,71),
    (301,0,29,72),
    (429,0,26,73),
    (557,0,29,73),
    (685,0,31,73),
    (813,0,36,72),
    (941,0,32,71),
    (1069,0,29,72),
    (1197,0,26,73),
    (1325,0,29,73),
    (1453,0,31,73)
]

char2_width = 32
char2_height = 72

TIME_PER_ACTION = 0.05
ACTION_PER_TIME2 = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_idle2 = 7
FRAMES_PER_ACTION_move = 12



class Idle:
    def __init__(self, char2):
        self.char2 = char2

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.char2.frame = (self.char2.frame + FRAMES_PER_ACTION_idle2 * ACTION_PER_TIME2 * game_framework.frame_time) % 7

    def draw(self):
        frame_data = idle2[int(self.char2.frame)]
        left, bottom, width, height = frame_data

        if self.char2.dir == 1:  # right
            self.char2.image_idle.clip_draw(left, bottom, width, height, self.char2.x, self.char2.y)
        else:  # left
            self.char2.image_idle.clip_composite_draw(left, bottom, width, height, 0, 'h', self.char2.x, self.char2.y, width, height)




class Move:
    def __init__(self, char2):
        self.char2 = char2

    def enter(self, e):
        if enter_down(e):
            data.character_pattern.append(self.char2.dir)

        elif space_down(e):
            self.char2.dir *= -1
            data.character_pattern.append(self.char2.dir)

        idx = len(data.character_pattern) - 1
        if idx >= 0 and idx < len(data.stair_pattern):
            if data.stair_pattern[idx] != data.character_pattern[idx]:
                pass
            else:
                data.score2 += 1

    def exit(self, e):
        pass

    def do(self):
        self.char2.frame += FRAMES_PER_ACTION_move * ACTION_PER_TIME2 * game_framework.frame_time
        if self.char2.frame >= FRAMES_PER_ACTION_move:
            self.char2.frame = 0
            self.char2.state_machine.handle_state_event(('MOVED', None))

    def draw(self):
        frame_data = move[int(self.char2.frame)]
        left, bottom, width, height = frame_data

        if self.char2.dir == 1:  # right
            self.char2.image_move.clip_draw(left, bottom, width, height, self.char2.x, self.char2.y)
        else:  # left 
            self.char2.image_move.clip_composite_draw(left, bottom, width, height, 0,'h',self.char2.x, self.char2.y,width,height)


class character2:
    def __init__(self):
        self.x,self.y = w_width/2, w_height / 2-100
        self.frame = 0
        self.dir = -1
        self.image_idle = load_image('../image/girl2_Idle.png')
        self.image_move = load_image('../image/girl2_Walk.png')

        self.IDLE=Idle(self)
        self.MOVE=Move(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {enter_down: self.MOVE, space_down: self.MOVE},
                self.MOVE: {moved: self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        pass#return self.x - char2_width/2, self.y - char2_height/2, self.x + char2_width/2, self.y + char2_height/2

    def handle_collision(self, group, other):
        pass