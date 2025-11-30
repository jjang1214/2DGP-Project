from pico2d import open_canvas, delay, close_canvas
import game_framework
from game_world import w_width,w_height

import initc_mode as start_mode

open_canvas(w_width, w_height)
game_framework.run(start_mode)
close_canvas()
