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


idle3 = [
    (49,0,30,72),
    (177,0,30,72),
    (304,0,31,73),
    (431,0,32,73),
    (560,0,31,73),
    (689,0,30,72)
]

move3=[
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

TIME_PER_ACTION = 0.25
ACTION_PER_TIME3 = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_idle3 = 6
FRAMES_PER_ACTION_move3 = 12



current_time = None

class Idle:
    def __init__(self, char3):
        self.char3 = char3

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.char3.frame = (self.char3.frame + FRAMES_PER_ACTION_idle3 * ACTION_PER_TIME3 * game_framework.frame_time) % FRAMES_PER_ACTION_idle3

    def draw(self):
        frame_data = idle3[int(self.char3.frame)]
        left, bottom, width, height = frame_data

        if self.char3.dir == 1:  # right
            self.char3.image_idle.clip_draw(left, bottom, width, height, self.char3.x, self.char3.y)
        else:  # left
            self.char3.image_idle.clip_composite_draw(left, bottom, width, height, 0, 'h', self.char3.x, self.char3.y, width, height)




class Move:
    def __init__(self, char3):
        self.char3 = char3

    def enter(self, e):
        if data.p1_character == 3:
            if enter_down(e):
                data.p1_pattern.append(self.char3.dir)

            elif space_down(e):
                self.char3.dir *= -1
                data.p1_pattern.append(self.char3.dir)

            idx = len(data.p1_pattern) - 1
            if idx >= 0 and idx < len(data.stair_pattern):
                if data.stair_pattern[idx] != data.p1_pattern[idx]:
                    pass
                else:
                    data.p1_score += 1

        elif data.p2_character == 1:
            if lshift_down(e):
                data.p2_pattern.append(self.char3.dir)

            elif lctrl_down(e):
                self.char3.dir *= -1
                data.p2_pattern.append(self.char3.dir)

            idx = len(data.p2_pattern) - 1
            if idx >= 0 and idx < len(data.stair_pattern):
                if data.stair_pattern[idx] != data.p2_pattern[idx]:
                    pass
                else:
                    data.p2_score += 1




    def exit(self, e):
        pass

    def do(self):
        self.char3.frame += FRAMES_PER_ACTION_move3 * ACTION_PER_TIME3 * game_framework.frame_time
        if self.char3.frame >= FRAMES_PER_ACTION_move3:
            self.char3.frame = 0
            self.char3.state_machine.handle_state_event(('MOVED', None))

    def draw(self):
        frame_data = move3[int(self.char3.frame)]
        left, bottom, width, height = frame_data

        if self.char3.dir == 1:  # right
            self.char3.image_move.clip_draw(left, bottom, width, height, self.char3.x, self.char3.y)
        else:  # left
            self.char3.image_move.clip_composite_draw(left, bottom, width, height, 0,'h',self.char3.x, self.char3.y,width,height)


class character3:
    def __init__(self):
        self.x,self.y = w_width/2, w_height / 2-100
        self.frame = 0
        self.dir = -1
        self.image_idle = load_image('../image/girl3_Idle.png')
        self.image_move = load_image('../image/girl3_Walk.png')
        self.image_exclamation = load_image('../image/exclamation_mark.png')

        self.IDLE=Idle(self)
        self.MOVE=Move(self)
        if data.p1_character == 3:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE:{enter_down : self.MOVE, space_down : self.MOVE},
                    self.MOVE:{moved : self.IDLE, enter_down : self.MOVE, space_down : self.MOVE},
                }
            )
        if data.p2_character == 3:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE:{lshift_down : self.MOVE, lctrl_down : self.MOVE},
                    self.MOVE:{moved : self.IDLE, enter_down : self.MOVE, space_down : self.MOVE},
                }
            )

    def update(self):
        global current_time

        if data.p1_character == 3:
            if data.isp1alive:
                current_time = None
            if not data.isp1alive:
                if current_time == None:
                    current_time = get_time()
                else:
                    if get_time() - current_time > 1:
                        self.y -= 10.0

        if data.p2_character == 3:
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
            self.image_exclamation.draw(self.x, self.y+char3_height/2+40,40,40)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        pass#return self.x - char1_width/2, self.y - char1_height/2, self.x + char1_width/2, self.y + char1_height/2

    def handle_collision(self, group, other):
        pass