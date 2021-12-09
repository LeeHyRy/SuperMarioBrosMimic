from pico2d import *
import GameFrame
import server



TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Mushroom:
    image = None
    imageX = 1
    imageY = 4158 - 4074 - 16

    PIXEL_PER_METER = (25.0 / 1.8)  # 25 pixel 180cm
    MOVE_SPEED_KMPH = 50.0  # Km / Hour
    MOVE_SPEED_MPM = (MOVE_SPEED_KMPH * 1000.0 / 60.0)
    MOVE_SPEED_MPS = (MOVE_SPEED_MPM / 60.0)
    MOVE_SPEED_PPS = (MOVE_SPEED_MPS * PIXEL_PER_METER)

    FALL_SPEED_KMPH = 200.0
    FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
    FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
    FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)
    FALL_ACCEL_MPS2 = FALL_SPEED_MPS / 120.0
    FALL_ACCEL_PPS2 = FALL_ACCEL_MPS2 * PIXEL_PER_METER

    def __init__(self, inX, inY):
        if Mushroom.image == None:
            Mushroom.image = load_image('Mario.png')
        self.x, self.y = inX, inY
        self.is_fall = True
        self.fall_speed = 0.1
        self.velocity = Mushroom.MOVE_SPEED_PPS
        self.dir = 1

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y, 'dir': self.dir}
        return data

    def __setstate__(self, data):
        if Mushroom.image == None:
            Mushroom.image = load_image('Mario.png')
        self.imageX = 1
        self.imageY = 4158 - 4074 - 16
        self.is_fall = True
        self.fall_speed = 0.1
        self.velocity = Mushroom.MOVE_SPEED_PPS
        self.__dict__.update(data)

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 8, cy - 8, cx + 8, cy + 8

    def update(self):
        self.x += self.dir * self.velocity * GameFrame.tick_time
        # 낙하
        if self.is_fall is True:
            self.fall_speed += Mushroom.FALL_ACCEL_PPS2
            self.fall_speed = clamp(0, self.fall_speed, Mushroom.FALL_SPEED_PPS)
            self.y -= self.fall_speed * GameFrame.tick_time
            self.y = clamp(30, self.y, 900 - 25)

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.imageX, self.imageY, 16, 16, cx, cy)

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

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y}
        return data

    def __setstate__(self, data):
        if Coin.image == None:
            Coin.image = load_image('Object.png')
        self.imageX = 154
        self.imageY = 753 - 1 - 16
        self.is_fall = True
        self.fall_speed = 0.1
        self.velocity = Mushroom.MOVE_SPEED_PPS
        self.frame = 0
        self.__dict__.update(data)

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * GameFrame.tick_time) % 8

    def draw(self):
        self.image.clip_draw(self.imageX + int(self.frame) * 17, self.imageY,  16, 16, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def effect(self, player):
        server.mario_coin += 1
