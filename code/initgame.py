from pico2d import *

from game_world import w_width, w_height
import game_framework
import initc_mode
import data


background = None
font = None
bgm = None

drawbg = True
last_time = 0.0


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_mode(initc_mode)


def init(*args):
    global background, font, bgm, last_time

    background = load_image('../image/title.png')
    font = load_font('../font/ENCR10B.TTF', 48)
    bgm = load_music('../sound/bgm.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

    last_time = get_time()


def update():
    global drawbg, last_time
    current_time = get_time()
    if current_time - last_time >= 0.5:
        drawbg = not drawbg
        last_time = current_time


def draw():
    clear_canvas()
    global background, font

    background.draw(w_width/2, w_height/2,w_width, w_height)
    if drawbg:
        font.draw(w_width * 2.8 / 10, w_height * 30 / 100, f'PRESS [ENTER] TO START', (0, 255, 0))

    update_canvas()


def finish():
    global background
    del background

def pause(): pass
def resume(): pass