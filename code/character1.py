from pico2d import load_image, draw_rectangle, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RETURN, SDLK_SPACE, SDLK_LSHIFT, SDLK_LCTRL

import game_world
import game_framework
from game_world import w_width, w_height
import data

from state_machine import StateMachine


def enter_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RETURN

def enter_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RETURN

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE

def lshift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def lshift_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LSHIFT

def lctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

def lctrl_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LCTRL

moved = lambda e: e[0] == 'MOVED'


idle1 = [
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

TIME_PER_ACTION1 = 0.1
ACTION_PER_TIME1 = 1.0 / TIME_PER_ACTION1
FRAMES_PER_ACTION_idle1 = 9
FRAMES_PER_ACTION_move1 = 12

current_time = None

class Idle:
    def __init__(self, char1):
        self.char1 = char1

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.char1.frame = (self.char1.frame + FRAMES_PER_ACTION_idle1 * ACTION_PER_TIME1 * game_framework.frame_time) % FRAMES_PER_ACTION_idle1

    def draw(self):
        frame_data = idle1[int(self.char1.frame)]
        left, bottom, width, height = frame_data

        if self.char1.dir == 1:  # right
            self.char1.image_idle.clip_draw(left, bottom, width, height, self.char1.x, self.char1.y)
        else:  # left
            self.char1.image_idle.clip_composite_draw(left, bottom, width, height, 0, 'h', self.char1.x, self.char1.y, width, height)




class Move:
    def __init__(self, char1):
        self.char1 = char1

    def enter(self, e):
        if data.p1_character == 1:
            if enter_down(e):
                data.p1_pattern.append(self.char1.dir)

            elif space_down(e):
                self.char1.dir *= -1
                data.p1_pattern.append(self.char1.dir)

            idx = len(data.p1_pattern) - 1
            if idx >= 0 and idx < len(data.stair_pattern):
                if data.stair_pattern[idx] != data.p1_pattern[idx]:
                    pass
                else:
                    data.p1_score += 1

        elif data.p2_character == 1:
            if lshift_down(e):
                data.p2_pattern.append(self.char1.dir)

            elif lctrl_down(e):
                self.char1.dir *= -1
                data.p2_pattern.append(self.char1.dir)

            idx = len(data.p2_pattern) - 1
            if idx >= 0 and idx < len(data.stair_pattern):
                if data.stair_pattern[idx] != data.p2_pattern[idx]:
                    pass
                else:
                    data.p2_score += 1




    def exit(self, e):
        pass

    def do(self):
        self.char1.frame += FRAMES_PER_ACTION_move1 * ACTION_PER_TIME1 * game_framework.frame_time
        if self.char1.frame >= FRAMES_PER_ACTION_move1:
            self.char1.frame = 0
            self.char1.state_machine.handle_state_event(('MOVED', None))

    def draw(self):
        frame_data = move[int(self.char1.frame)]
        left, bottom, width, height = frame_data

        if self.char1.dir == 1:  # right
            self.char1.image_move.clip_draw(left, bottom, width, height, self.char1.x, self.char1.y)
        else:  # left
            self.char1.image_move.clip_composite_draw(left, bottom, width, height, 0,'h',self.char1.x, self.char1.y,width,height)


class character1:
    def __init__(self):
        self.x,self.y = w_width/2, w_height / 2-100
        self.frame = 0
        self.dir = -1
        self.image_idle = load_image('../image/girl1_Idle.png')
        self.image_move = load_image('../image/girl1_Walk.png')
        self.image_exclamation = load_image('../image/exclamation_mark.png')

        self.IDLE=Idle(self)
        self.MOVE=Move(self)
        if data.p1_character == 1:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE:{enter_down : self.MOVE, space_down : self.MOVE},
                    self.MOVE:{moved : self.IDLE},
                }
            )
        if data.p2_character == 1:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE:{lshift_down : self.MOVE, lctrl_down : self.MOVE},
                    self.MOVE:{moved : self.IDLE},
                }
            )

    def update(self):
        global current_time

        if data.p1_character == 1:
            if data.isp1alive:
                current_time = None
            if not data.isp1alive:
                if current_time == None:
                    current_time = get_time()
                else:
                    if get_time() - current_time > 1:
                        self.y -= 10.0

        if data.p2_character == 1:
            if data.isp2alive:
                current_time = None
            if not data.isp2alive:
                if current_time == None:
                    current_time = get_time()
                else:
                    if get_time() - current_time > 1:
                        self.y -= 10.0

        self.state_machine.update()

    def handle_event(self, event):
        if data.isp1alive:
            self.state_machine.handle_state_event(('INPUT', event))
        else:
            return

    def draw(self):
        self.state_machine.draw()
        if not data.isp1alive:
            self.image_exclamation.draw(self.x, self.y+char1_height/2+40,40,40)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        pass#return self.x - char1_width/2, self.y - char1_height/2, self.x + char1_width/2, self.y + char1_height/2

    def handle_collision(self, group, other):
        pass