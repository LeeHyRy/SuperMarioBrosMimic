import GameFrame
from pico2d import *

import server
import State_Ingame


name = "PauseState"
image = None


def enter():
    global image
    image = load_image('pause_screen.png')


def exit():
    global image
    del(image)


def update():
    pass


def draw():
    global image
    clear_canvas()
    image.draw(server.window_width / 2, server.window_height / 2)
    update_canvas()




def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrame.quit_state()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # 이거 일시정지 화면으로 바꿔야함
            GameFrame.pop_state()
    pass


def pause(): pass


def resume(): pass




