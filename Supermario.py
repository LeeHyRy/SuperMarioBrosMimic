import GameFrame
import pico2d

import State_Ingame

pico2d.open_canvas(1600, 600)
GameFrame.run(State_Ingame)
pico2d.close_canvas()

