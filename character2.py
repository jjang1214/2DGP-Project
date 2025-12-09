from pico2d import load_image, draw_rectangle, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RETURN, SDLK_SPACE, SDLK_LSHIFT, SDLK_LCTRL

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

def lshift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def lshift_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LSHIFT

def lctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

def lctrl_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LCTRL

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

move2=[
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

TIME_PER_ACTION = 0.25
ACTION_PER_TIME2 = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_idle2 = 7
FRAMES_PER_ACTION_move2 = 12



current_time = None

class Idle:
    def __init__(self, char2):
        self.char2 = char2

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.char2.frame = (self.char2.frame + FRAMES_PER_ACTION_idle2 * ACTION_PER_TIME2 * game_framework.frame_time) % FRAMES_PER_ACTION_idle2

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
        if data.p1_character == 2:
            if enter_down(e):
                data.p1_pattern.append(self.char2.dir)

            elif space_down(e):
                self.char2.dir *= -1
                data.p1_pattern.append(self.char2.dir)

            idx = len(data.p1_pattern) - 1
            if idx >= 0 and idx < len(data.stair_pattern):
                if data.stair_pattern[idx] != data.p1_pattern[idx]:
                    pass
                else:
                    data.p1_score += 1

        elif data.p2_character == 2:
            if lshift_down(e):
                data.p2_pattern.append(self.char2.dir)

            elif lctrl_down(e):
                self.char2.dir *= -1
                data.p2_pattern.append(self.char2.dir)

            idx = len(data.p2_pattern) - 1
            if idx >= 0 and idx < len(data.stair_pattern):
                if data.stair_pattern[idx] != data.p2_pattern[idx]:
                    pass
                else:
                    data.p2_score += 1




    def exit(self, e):
        pass

    def do(self):
        self.char2.frame += FRAMES_PER_ACTION_move2 * ACTION_PER_TIME2 * game_framework.frame_time
        if self.char2.frame >= FRAMES_PER_ACTION_move2:
            self.char2.frame = 0
            self.char2.state_machine.handle_state_event(('MOVED', None))

    def draw(self):
        frame_data = move2[int(self.char2.frame)]
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
        self.image_idle = load_image('image/girl2_Idle.png')
        self.image_move = load_image('image/girl2_Walk.png')
        self.image_exclamation = load_image('image/exclamation_mark.png')

        self.IDLE=Idle(self)
        self.MOVE=Move(self)
        if data.p1_character == 2:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE:{enter_down : self.MOVE, space_down : self.MOVE},
                    self.MOVE:{moved : self.IDLE, enter_down : self.MOVE, space_down : self.MOVE},
                }
            )
        if data.p2_character == 2:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE:{lshift_down : self.MOVE, lctrl_down : self.MOVE},
                    self.MOVE:{moved : self.IDLE, enter_down : self.MOVE, space_down : self.MOVE},
                }
            )

    def update(self):
        global current_time

        if data.p1_character == 2:
            if data.isp1alive:
                current_time = None
            if not data.isp1alive:
                if current_time == None:
                    current_time = get_time()
                else:
                    if get_time() - current_time > 1:
                        self.y -= 10.0

        if data.p2_character == 2:
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
            self.image_exclamation.draw(self.x, self.y+char2_height/2+40,40,40)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        pass#return self.x - char2_width/2, self.y - char2_height/2, self.x + char2_width/2, self.y + char2_height/2

    def handle_collision(self, group, other):
        pass