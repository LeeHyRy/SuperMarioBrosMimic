import GameFrame
import pico2d

import State_Life
import server

pico2d.open_canvas(server.window_width, server.window_height)
GameFrame.run(State_Life)
pico2d.close_canvas()

