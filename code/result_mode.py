from pico2d import *
from game_world import w_width, w_height
import game_framework
import init_mode
import data

from stair import *
from character1 import idle1, ACTION_PER_TIME1, FRAMES_PER_ACTION_idle1
from character2 import idle2, ACTION_PER_TIME2, FRAMES_PER_ACTION_idle2
from character3 import idle3, ACTION_PER_TIME3, FRAMES_PER_ACTION_idle3

init_running = True

background = None
image1 = None
image2 = None
image3 = None
font = None

frame1 = 0
frame2 = 0
frame3 = 0

a = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def init(*args):
    global background, image1, image2, image3, font, result_time

    background = load_image('../image/tuk.png')
    image1 = load_image('../image/girl1_Idle.png')
    image2 = load_image('../image/girl2_Idle.png')
    image3 = load_image('../image/girl3_Idle.png')

    font = load_font('../ENCR10B.TTF', 32)

    result_time = get_time()


def update():
    global result_time
    if get_time() - result_time >= 5.0:
        result_time = get_time()
        game_framework.quit()
        #game_framework.change_mode(init_mode,a)


def draw():
    clear_canvas()
    global background, image1, image2, image3, font, frame1, frame2, frame3

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



    if data.main_character == 1:
        image1.clip_draw(left1, bottom1, width1, height1, w_width / 2, w_height / 2, 80, 100)
        font.draw(w_width *4.5/10, w_height * 80 / 100, f'Score:{data.score1 :^}', (255, 0, 0))
    elif data.main_character == 2:
        image2.clip_draw(left2, bottom2, width2, height2, w_width /2, w_height / 2, 80, 100)
        font.draw(w_width *4.5/10, w_height * 80 / 100, f'Score:{data.score2 :^}', (255, 0, 0))
    elif data.main_character == 3:
        image3.clip_draw(left3, bottom3, width3, height3, w_width /2, w_height / 2, 80, 100)
        font.draw(w_width *4.5/10, w_height * 80 / 100, f'Score:{data.score3 :^}', (255, 0, 0))



    update_canvas()


def finish():
    global image1, image2, image3
    del image1, image2, image3

    data.main_character = 0
    data.score1 = 0
    data.score2 = 0
    data.score3 = 0


def pause(): pass


def resume(): pass