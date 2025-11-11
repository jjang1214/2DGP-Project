from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP,SDLK_RETURN, SDLK_SPACE

from character1 import *
import random
import game_world


def enter_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RETURN

def enter_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RETURN

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE


initstairs = False
stairs = []

def create_stairs(get_x, get_y, num):
    global initstairs, stairs

    if not initstairs:
        x, y = get_x - 70, get_y + 50 - 63  # 첫 계단: 캐릭터 왼쪽 위
        stairs.append(Stair(x, y))
        Stair.last_x, Stair.last_y = x, y
        for i in range(num):
            direction = random.choice([-1, 1])  # -1: 왼쪽, 1: 오른쪽
            x += direction * 70
            y += 50
            stairs.append(Stair(x, y))
            Stair.last_x, Stair.last_y = x, y
            print(f'{Stair.last_x=}, {Stair.last_y=}')

        initstairs = True

    else:
        x, y = get_x, get_y

        direction = random.choice([-1, 1])  # -1: 왼쪽, 1: 오른쪽
        x += direction * 70
        y += 50

        stairs.append(Stair(x, y))
        Stair.last_x, Stair.last_y = x, y
        print(f'{Stair.last_x=}, {Stair.last_y=}')




    return stairs





class Stair:
    image = None

    last_x = 0
    last_y = 0
    def __init__(self, x, y, width=70, height=50):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.offset_x = 0
        self.offset_y = 0
        if Stair.image is None:
            Stair.image = load_image('../image/stair.png')

    def move(self, direction):
        dx = 70 if direction == 'right' else -70
        dy = 50
        self.offset_x -= dx
        self.offset_y -= dy



    def draw(self):
        self.image.clip_draw(0, 0, 116, 63,
                             self.x + self.offset_x, self.y + self.offset_y,
                             self.w, self.h)
        draw_rectangle(self.x - self.w / 2 + self.offset_x,
                       self.y - self.h / 2 + self.offset_y,
                       self.x + self.w / 2 + self.offset_x,
                       self.y + self.h / 2 + self.offset_y)


    def get_bb(self):
        return (self.x - self.w / 2, self.y - self.h / 2,
                self.x + self.w / 2, self.y + self.h / 2)

    def handle_collision(self, group, other):
        pass

    def update(self):
        pass

    def handle_event(self,event,char_dir):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RETURN:
                self.move('right' if char_dir == 1 else 'left')
            elif event.key == SDLK_SPACE:
                self.move('left' if char_dir == 1 else 'right')