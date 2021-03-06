import GameFrame
from pico2d import *

import server
import State_Ingame


name = "LifeState"
image = None
bring_time = 0.0


def enter():
    global image
    image = load_image('black_screen.png')


def exit():
    global image
    del(image)



def update():
    global bring_time

    if server.mario_life > 0:
        if bring_time > 1.0:
            bring_time = 0

            GameFrame.push_state(State_Ingame)
    else:
        if bring_time > 3.0:
            bring_time = 0
            GameFrame.quit_state()

    delay(0.01)
    bring_time += 0.01



def draw():
    global image
    clear_canvas()
    image.draw(server.window_width / 2, server.window_height / 2)
    font = load_font('CookieRun.ttf', 50)
    if server.mario_life > 0:
        font.draw(3 * server.window_width / 8, server.window_height / 2, "남은 목숨: %3d" % server.mario_life,
                  (255, 255, 0))
    else:
        font.draw(3 * server.window_width / 8, server.window_height / 2, "GAME OVER",
                  (102, 0, 153))
    update_canvas()




def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




