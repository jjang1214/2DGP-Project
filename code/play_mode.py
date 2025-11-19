from pico2d import *
import random

import game_framework
import game_world
from game_world import w_width, w_height
from background import Background as bg
from stair import *
import character1
import character2
import character3
import data
import init_mode,result_mode

global stairs

char1 = None
char2 = None
char3 = None

play_character = 0

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            if play_character == 1:
                background.handle_event(event,char1.dir)
                for s in stairs:
                    s.handle_event(event, char1.dir)
                char1.handle_event(event)

            elif play_character == 2:
                background.handle_event(event,char2.dir)
                for s in stairs:
                    s.handle_event(event, char2.dir)
                char2.handle_event(event)

            elif play_character == 3:
                background.handle_event(event, char3.dir)
                for s in stairs:
                    s.handle_event(event, char3.dir)
                char3.handle_event(event)




def init(main_character):
    global background,play_character, char1, char2, char3, stairs

    play_character = main_character

    background = bg()
    game_world.add_object(background, 0)



    if play_character == 1:
        char1 = character1.character1()
        game_world.add_object(char1, 2)
        #game_world.add_collision_pair('character1:??', char1, None)

        stairs = create_stairs(char1.x, char1.y, 11)

    elif play_character == 2:
        char2 = character2.character2()
        game_world.add_object(char2, 2)
        #game_world.add_collision_pair('character2:??', character2, None)

        stairs = create_stairs(char2.x, char2.y, 11)

    elif play_character == 3:
        char3 = character3.character3()
        game_world.add_object(char3, 2)
        #game_world.add_collision_pair('character3:??', char3, None)

        stairs = create_stairs(char3.x, char3.y, 11)




    for s in stairs:
        game_world.add_object(s, 1)


def update():
    game_world.update()
    game_world.handle_collisions()

    idx = len(data.character_pattern) - 1
    if idx >= 0 and idx < len(data.stair_pattern):
        if data.stair_pattern[idx] != data.character_pattern[idx]:
            print(f"{idx + 1}번 계단에서 실패!")

            #game_framework.quit()
            game_framework.change_mode(result_mode, data.main_character)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    if play_character == 1 and char1:
        char1.x = w_width / 2
        char1.y = w_height / 2 - 100

    elif play_character == 2 and char2:
        char2.x = w_width / 2
        char2.y = w_height / 2 - 100

    elif play_character == 3 and char3:
        char3.x = w_width / 2
        char3.y = w_height / 2 - 100

    data.stair_pattern.clear()
    data.character_pattern.clear()
    game_world.clear()

def pause(): pass
def resume(): pass