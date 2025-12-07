from pico2d import *
import random

import game_framework
import game_world
from game_world import w_width, w_height
from background import Background as bg
import stair
import character1
import character2
import character3
import data
import initc_mode,result_mode

#global stairs

char1 = None
char2 = None
char3 = None

current_time = None

font = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(initc_mode)
        else:
            if data.p1_character == 1:
                background.handle_event(event,char1.dir)
                for s in stairs:
                    s.handle_event(event, char1.dir)
                char1.handle_event(event)

            elif data.p1_character == 2:
                background.handle_event(event,char2.dir)
                for s in stairs:
                    s.handle_event(event, char2.dir)
                char2.handle_event(event)

            elif data.p1_character == 3:
                background.handle_event(event, char3.dir)
                for s in stairs:
                    s.handle_event(event, char3.dir)
                char3.handle_event(event)




def init(*args):
    global background, char1, char2, char3, stairs, font

    font = load_font('../ENCR10B.TTF', 32)


    background = bg()
    game_world.add_object(background, 0)



    if data.p1_character == 1:
        char1 = character1.character1()
        game_world.add_object(char1, 2)
        #game_world.add_collision_pair('character1:??', char1, None)

        stairs = stair.create_stairs(char1.x, char1.y, 11)

    elif data.p1_character == 2:
        char2 = character2.character2()
        game_world.add_object(char2, 2)
        #game_world.add_collision_pair('character2:??', character2, None)

        stairs = stair.create_stairs(char2.x, char2.y, 11)

    elif data.p1_character == 3:
        char3 = character3.character3()
        game_world.add_object(char3, 2)
        #game_world.add_collision_pair('character3:??', char3, None)

        stairs = stair.create_stairs(char3.x, char3.y, 11)




    for s in stairs:
        game_world.add_object(s, 1)


def update():
    game_world.update()
    game_world.handle_collisions()

    idx = len(data.p1_pattern) - 1
    if idx >= 0 and idx < len(data.stair_pattern):
        if data.stair_pattern[idx] != data.p1_pattern[idx]:
            print(f"{idx + 1}번 계단에서 실패!")
            data.isp1alive = False
            global current_time
            if current_time == None:
                current_time = get_time()
            else:
                if get_time() - current_time > 2:
                    #game_framework.quit()
                    game_framework.change_mode(result_mode)



def draw():
    global font
    clear_canvas()
    game_world.render()
    font.draw(w_width * 80 / 100, w_height * 80 / 100, f'Score: {data.p1_score :^}', (255, 0, 0))
    font.draw(w_width * 73 / 100, w_height * 90 / 100, f'Best Score: {data.best_score :^}', (255, 0, 0))
    update_canvas()


def finish():
    global stairs, current_time

    stairs.clear()
    stair.initstairs = False
    stair.stair_count = 0
    data.stair_pattern.clear()
    game_world.clear()
    current_time = None

    data.p1_pattern.clear()
    data.isp1alive = True



def pause(): pass
def resume(): pass