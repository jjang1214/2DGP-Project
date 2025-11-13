from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP,SDLK_RETURN, SDLK_SPACE

import game_world
import game_framework
from game_world import w_width, w_height
import character1
import stair

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


class Background:
    def __init__(self):
        self.tukground = load_image('../image/tuk.png')
        self.sky = load_image('../image/daytime.png')
        self.sky_height = self.sky.h
        self.ground_y = self.tukground.h / 2
        self.offset_x = 0
        self.offset_y = 0
        self.font = load_font('../ENCR10B.TTF',32)

    def move(self, direction):
        dx = 70 if direction == 'right' else -70
        dy = 50
        self.offset_x -= dx
        self.offset_y -= dy


        for s in stair.stairs:
            s.move(direction)


        new_stair_list = stair.create_stairs(stair.Stair.last_x, stair.Stair.last_y, 1)
        new_stair = new_stair_list[-1]
        new_stair.offset_x = self.offset_x
        new_stair.offset_y = self.offset_y
        game_world.add_object(new_stair, 1)

        if len(stair.stairs) > 20:
            first = stair.stairs.pop(0)
            try:
                game_world.remove_object(first)
            except Exception:
                pass

    def update(self):
        pass

    def draw(self):
        # 1. 하늘 반복 (세로 방향, 상하반전 교차)
        sky_start_y = self.ground_y + self.tukground.h / 2 + self.offset_y
        y = sky_start_y
        row = 0
        while y < w_height + self.sky_height:
            x = -self.sky.w * 2 + self.offset_x
            flip = False
            while x < w_width + self.sky.w:
                if row % 2 == 0:
                    # 그대로
                    if flip:
                        self.sky.clip_composite_draw(0, 0, self.sky.w, self.sky.h, 0, 'h', x, y, self.sky.w, self.sky.h)
                    else:
                        self.sky.draw(x, y)
                else:
                    # 상하반전
                    if flip:
                        self.sky.clip_composite_draw(0, 0, self.sky.w, self.sky.h, 0, 'hv', x, y, self.sky.w,
                                                     self.sky.h)
                    else:
                        self.sky.clip_composite_draw(0, 0, self.sky.w, self.sky.h, 0, 'v', x, y, self.sky.w, self.sky.h)
                x += self.sky.w
                flip = not flip
            y += self.sky.h
            row += 1

        # 2. 지면 반복 (가로 방향, 좌우반전)
        ground_y = self.ground_y + self.offset_y
        x = w_width//2#-self.tukground.w * 2 + self.offset_x
        flip = False
        while x < w_width + self.tukground.w:
            if flip:
                self.tukground.clip_composite_draw(0, 0, self.tukground.w, self.tukground.h, 0, 'h', x, ground_y,
                                                   self.tukground.w*2, self.tukground.h*2)
            else:
                self.tukground.draw(x, ground_y,self.tukground.w*2, self.tukground.h*2)
            x += self.tukground.w*2
            flip = not flip




        self.font.draw(w_width*80/100,w_height*80/100,f'Score:{character1.score :^}',(255,0,0))

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass

    def handle_event(self,event,char_dir):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RETURN:
                self.move('right' if char_dir == 1 else 'left')
            elif event.key == SDLK_SPACE:
                self.move('left' if char_dir == 1 else 'right')


