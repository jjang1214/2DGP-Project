from pico2d import *

from game_world import w_width, w_height
import game_framework
import initgame
import initm_mode
import singleplay_mode
import multiplay_mode
import data
import time



from stair import *
from character1 import idle1, ACTION_PER_TIME1, FRAMES_PER_ACTION_idle1
from character2 import idle2, ACTION_PER_TIME2, FRAMES_PER_ACTION_idle2
from character3 import idle3, ACTION_PER_TIME3, FRAMES_PER_ACTION_idle3



background = None
image1 = None
image2 = None
image3 = None
font = None
bgm = None

frame1 = 0
frame2 = 0
frame3 = 0

isp1selected = False
isp2selected = False

current_time = 0.0
start_time = None

def handle_events():
    global start_time, isp1selected, isp2selected

    event_list = get_events()
    for event in event_list:
        if data.playing_mode == 1:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                if isp1selected:
                    isp1selected = False
                    data.p1_character = 0
                elif not isp1selected:
                    game_framework.change_mode(initgame)
            elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
                data.p1_character = 1
                isp1selected = True
                start_time = get_time()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
                data.p1_character = 2
                isp1selected = True
                start_time = get_time()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
                data.p1_character = 3
                isp1selected = True
                start_time = get_time()

        elif data.playing_mode == 2:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                if not isp1selected:
                    game_framework.change_mode(initm_mode)
                elif isp1selected and not isp2selected:
                    data.p1_character = 0
                    isp1selected = False
                elif isp1selected and isp2selected:
                    data.p2_character = 0
                    isp2selected = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
                if not isp1selected:
                    data.p1_character = 1
                    isp1selected = True
                else:
                    if data.p1_character == 1:
                        pass
                    else:
                        data.p2_character = 1
                        isp2selected = True
                        start_time = get_time()

            elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
                if not isp1selected:
                    data.p1_character = 2
                    isp1selected = True
                else:
                    if data.p1_character == 2:
                        pass
                    else:
                        data.p2_character = 2
                        isp2selected = True
                        start_time = get_time()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
                if not isp1selected:
                    data.p1_character = 3
                    isp1selected = True
                else:
                    if data.p1_character == 3:
                        pass
                    else:
                        data.p2_character = 3
                        isp2selected = True
                        start_time = get_time()

def init(*args):
    global isp1selected,isp2selected, bgm

    bgm = load_music('../sound/bgm.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

    isp1selected = False
    isp2selected = False

    data.p1_score = 0
    data.p2_score = 0
    data.p1_character = 0
    data.p2_character = 0
    data.stair_pattern.clear()
    data.p1_pattern.clear()
    data.p2_pattern.clear()
    game_world.clear()

    global background, image1, image2, image3, font

    background = load_image('../image/tuk.png')
    image1 = load_image('../image/girl1_Idle.png')
    image2 = load_image('../image/girl2_Idle.png')
    image3 = load_image('../image/girl3_Idle.png')

    font = load_font('../ENCR10B.TTF', 32)



def update():
    global start_time
    if data.playing_mode == 1:
        if isp1selected and start_time is not None:
            current_time = get_time()
            if current_time - start_time > 1.5:
                game_framework.change_mode(singleplay_mode)

    elif data.playing_mode == 2:
        if isp1selected and isp2selected and start_time is not None:
            current_time = get_time()
            if current_time - start_time > 1.5:
                game_framework.change_mode(multiplay_mode)


def draw():
    clear_canvas()
    global background, image1, image2, image3, font,frame1,frame2,frame3

    background.draw(w_width/2, w_height/2,w_width, w_height)

    frame1 = (frame1 + FRAMES_PER_ACTION_idle1 * 2 * game_framework.frame_time) % FRAMES_PER_ACTION_idle1
    frame_data1 = idle1[int(frame1)]
    left1, bottom1, width1, height1 = frame_data1

    frame2 = (frame2 + FRAMES_PER_ACTION_idle2 * 2 * game_framework.frame_time) % FRAMES_PER_ACTION_idle2
    frame_data2 = idle2[int(frame2)]
    left2, bottom2, width2, height2 = frame_data2

    frame3 = (frame3 + FRAMES_PER_ACTION_idle3 * 2 * game_framework.frame_time) % FRAMES_PER_ACTION_idle3
    frame_data3 = idle3[int(frame3)]
    left3, bottom3, width3, height3 = frame_data3

    def get_color(char_num):
        if data.p1_character == char_num:
            return (0, 255, 0)  # P1 → 초록색
        elif data.p2_character == char_num:
            return (0, 0, 255)  # P2 → 파란색
        else:
            return (255, 0, 0)  # 선택되지 않음 → 빨간색


    if data.playing_mode == 1:
        font.draw(w_width * 1 / 10, w_height * 60 / 100, f'[1] Character1', get_color(1))
        font.draw(w_width * 4 / 10, w_height * 60 / 100, f'[2] Character2', get_color(2))
        font.draw(w_width * 7 / 10, w_height * 60 / 100, f'[3] Character3', get_color(3))

        image1.clip_draw(left1, bottom1, width1, height1, w_width * 2 / 10, w_height * 50 / 100, 80, 100)
        image2.clip_draw(left2, bottom2, width2, height2, w_width * 5 / 10, w_height * 50 / 100, 80, 100)
        image3.clip_draw(left3, bottom3, width3, height3, w_width * 8 / 10, w_height * 50 / 100, 80, 100)

    elif data.playing_mode == 2:
        font.draw(w_width * 1 / 10, w_height * 90 / 100, f'[1] Character1', get_color(1))
        font.draw(w_width * 4 / 10, w_height * 90 / 100, f'[2] Character2', get_color(2))
        font.draw(w_width * 7 / 10, w_height * 90 / 100, f'[3] Character3', get_color(3))

        image1.clip_draw(left1, bottom1, width1, height1, w_width*2/10,w_height* 80 / 100,80,100)
        image2.clip_draw(left2, bottom2, width2, height2, w_width*5/10,w_height* 80 / 100,80,100)
        image3.clip_draw(left3, bottom3, width3, height3, w_width*8/10,w_height* 80 / 100,80,100)

        if isp1selected:
            if data.p1_character == 1:
                image1.clip_draw(left1, bottom1, width1, height1, w_width * 4 / 10, w_height * 50 / 100, 80, 100)
            elif data.p1_character == 2:
                image2.clip_draw(left2, bottom2, width2, height2, w_width * 4 / 10, w_height * 50 / 100, 80, 100)
            elif data.p1_character == 3:
                image3.clip_draw(left3, bottom3, width3, height3, w_width * 4 / 10, w_height * 50 / 100, 80, 100)

        if isp2selected:
            if data.p2_character == 1:
                image1.clip_draw(left1, bottom1, width1, height1, w_width * 7 / 10, w_height * 50 / 100, 80, 100)
            elif data.p2_character == 2:
                image2.clip_draw(left2, bottom2, width2, height2, w_width * 7 / 10, w_height * 50 / 100, 80, 100)
            elif data.p2_character == 3:
                image3.clip_draw(left3, bottom3, width3, height3, w_width * 7 / 10, w_height * 50 / 100, 80, 100)

    update_canvas()


def finish():
    global background, image1, image2, image3
    del background, image1, image2, image3

def pause(): pass
def resume(): pass