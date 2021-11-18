from pico2d import *
import GameFrame

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Mushroom:
    image = None
    imageX = 1
    imageY = 4158 - 4074 - 16

    def __init__(self, inX, inY):
        if Mushroom.image == None:
            Mushroom.image = load_image('Mario.png')
        self.x, self.y = inX, inY
        self.speed = 2
        self.gravSpeed = 0
        self.dir = -1

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def update(self):
        self.x -= self.speed * self.dir
        if self.y > 59:
            if self.gravSpeed < 4:
                self.gravSpeed += 0.2
            else:
                self.gravSpeed = 4
            self.y -= self.gravSpeed
        else:
            self.gravSpeed = 0
            self.y = 51

    def draw(self):
        self.image.clip_draw(self.imageX, self.imageY, 16, 16, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def effect(self, player):
        player.grow()


class Coin:
    image = None
    imageX = 154
    imageY = 753 - 1 - 16

    def __init__(self, inX, inY):
        if Coin.image == None:
            Coin.image = load_image('Object.png')
        self.x, self.y = inX, inY
        self.frame = 0

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * GameFrame.tick_time) % 8

    def draw(self):
        self.image.clip_draw(self.imageX + int(self.frame) * 17, self.imageY,  16, 16, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def effect(self, player):
        player.add_coin()
