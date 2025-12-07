from pico2d import *

import initm_mode
from game_world import w_width, w_height
import game_framework
import initc_mode
import data

from stair import *
from character1 import idle1, ACTION_PER_TIME1, FRAMES_PER_ACTION_idle1
from character2 import idle2, ACTION_PER_TIME2, FRAMES_PER_ACTION_idle2
from character3 import idle3, ACTION_PER_TIME3, FRAMES_PER_ACTION_idle3



background = None
image1 = None
image2 = None
image3 = None
font = None

frame1 = 0
frame2 = 0
frame3 = 0

restart = False

new_record = False

rainbow_colors = [
    (255, 0, 0),      # 빨
    (255, 128, 0),    # 주
    (255, 255, 0),    # 노
    (0, 255, 0),      # 초
    (0, 0, 255),      # 파
    (128, 0, 255)     # 보
]

def rainbow_color(t):
    index = int(t*5) % len(rainbow_colors)
    return rainbow_colors[index]

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            global restart
            restart = True


def init(*args):
    global background, image1, image2, image3, font, result_time, restart, new_record
    restart = False

    background = load_image('../image/tuk.png')
    image1 = load_image('../image/girl1_Idle.png')
    image2 = load_image('../image/girl2_Idle.png')
    image3 = load_image('../image/girl3_Idle.png')

    font = load_font('../ENCR10B.TTF', 32)

    result_time = get_time()


    if data.p1_score > data.best_score:
        data.best_score = data.p1_score
        new_record = True


def update():
    global result_time
    #if get_time() - result_time >= 5.0:
        #result_time = get_time()
    if restart:
        #game_framework.change_mode(initm_mode)
        game_framework.change_mode(initc_mode)


def draw():
    clear_canvas()
    global background, image1, image2, image3, font, frame1, frame2, frame3, new_record

    background.draw(w_width / 2, w_height / 2, w_width, w_height)

    frame1 = (frame1 + FRAMES_PER_ACTION_idle1 * 2 * game_framework.frame_time) % FRAMES_PER_ACTION_idle1
    frame_data1 = idle1[int(frame1)]
    left1, bottom1, width1, height1 = frame_data1

    frame2 = (frame2 + FRAMES_PER_ACTION_idle2 * 2 * game_framework.frame_time) % FRAMES_PER_ACTION_idle2
    frame_data2 = idle2[int(frame2)]
    left2, bottom2, width2, height2 = frame_data2

    frame3 = (frame3 + FRAMES_PER_ACTION_idle3 * 2 * game_framework.frame_time) % FRAMES_PER_ACTION_idle3
    frame_data3 = idle3[int(frame3)]
    left3, bottom3, width3, height3 = frame_data3


    if data.playing_mode == 1:
        if data.p1_character == 1:
            image1.clip_draw(left1, bottom1, width1, height1, w_width / 2, w_height / 2, 80, 100)
        elif data.p1_character == 2:
            image2.clip_draw(left2, bottom2, width2, height2, w_width /2, w_height / 2, 80, 100)
        elif data.p1_character == 3:
            image3.clip_draw(left3, bottom3, width3, height3, w_width /2, w_height / 2, 80, 100)

        if not new_record:
            font.draw(w_width * 4.5 / 10, w_height * 80 / 100, f'Score:{data.p1_score :^}', (255, 0, 0))
        if new_record:
            t = get_time()
            color = rainbow_color(t)
            font.draw(w_width * 4.2 / 10, w_height * 90 / 100, f'New Record!!', color)
            font.draw(w_width * 4.5 / 10, w_height * 80 / 100, f'Score:{data.p1_score :^}', (255, 0, 0))
        font.draw(w_width * 3.6 / 10, w_height * 40 / 100, f'PRESS [R] TO RESTART', (255,0,128))




    update_canvas()


def finish():
    global image1, image2, image3, new_record
    del image1, image2, image3

    data.p1_character = 0
    data.p1_score= 0
    #data.p2_score = 0

    new_record = False


def pause(): pass


def resume(): pass