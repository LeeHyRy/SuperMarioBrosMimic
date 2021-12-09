import GameFrame
from pico2d import *

import server



name = "ClearState"
image = None
bring_time = 0.0


def enter():
    global image
    image = load_image('Clear.png')


def exit():
    global image
    del(image)


def update():
    global bring_time

    if bring_time > 2.0:
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
                  (0, 0, 0))
        font.draw(3 * server.window_width / 8, server.window_height / 3, "모은 코인: %3d" % server.mario_coin,
                  (0, 0, 0))

    update_canvas()




def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




