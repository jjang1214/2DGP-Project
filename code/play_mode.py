from pico2d import *
import random

import game_framework
import game_world

from background import Background as bg
from stair import *
from character1 import character1 as char1
from character2 import character2 as char2
from character3 import character3 as char3

global stairs

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            background.handle_event(event,char1.dir)
            for s in stairs:
                s.handle_event(event,char1.dir)
            char1.handle_event(event)
            #char2.handle_event(event)
            #char3.handle_event(event)


def init():
    global background

    background = bg()
    game_world.add_object(background, 0)

    global char1

    char1 = char1()
    game_world.add_object(char1, 2)
    game_world.add_collision_pair('char1:??', char1, None)

    global char2

    #char2 = char2()
    #game_world.add_object(char2, 2)
    #game_world.add_collision_pair('char2:??', char2, None)

    global char3

    #char3 = char3()
    #game_world.add_object(char3, 2)
    #game_world.add_collision_pair('char3:??', char3, None)

    global stairs
    stairs = create_stairs(char1.x, char1.y,11)

    for s in stairs:
        game_world.add_object(s, 1)


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass