from pico2d import *
from game_world import w_width, w_height
import game_framework
import play_mode
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



def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            data.main_character = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            data.main_character = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            data.main_character = 3

def init(*args):
    data.score1 = 0
    data.score2 = 0
    data.score3 = 0
    data.main_character = 0
    data.stair_pattern.clear()
    data.character_pattern.clear()
    game_world.clear()

    global background, image1, image2, image3, font

    background = load_image('../image/tuk.png')
    image1 = load_image('../image/girl1_Idle.png')
    image2 = load_image('../image/girl2_Idle.png')
    image3 = load_image('../image/girl3_Idle.png')

    font = load_font('../ENCR10B.TTF', 32)



def update():
    if data.main_character != 0:
        game_framework.change_mode(play_mode)





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

    font.draw(w_width*3.5/10, w_height * 80 / 100, f'Choose Character(1~3)', (255, 0, 0))

    image1.clip_draw(left1, bottom1, width1, height1, w_width*2/10,w_height/2,80,100)
    image2.clip_draw(left2, bottom2, width2, height2, w_width*5/10,w_height/2,80,100)
    image3.clip_draw(left3, bottom3, width3, height3, w_width*8/10,w_height/2,80,100)

    update_canvas()


def finish():
    global image1, image2, image3
    del image1, image2, image3

def pause(): pass
def resume(): pass