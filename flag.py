from pico2d import *
import server

class Flag:
    image = None
    imageX = 766
    imageY = 753 - 502 - 176

    def __init__(self, inX, inY):
        if Flag.image == None:
            Flag.image = pico2d.load_image('Object.png')
        self.x, self.y = inX, inY
        self.frame = 0

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y, 'frame': self.frame}
        return data

    def __setstate__(self, data):
        if Flag.image == None:
            Flag.image = pico2d.load_image('Object.png')
        self.imageX = 766
        self.imageY = 753 - 502 - 176
        self.frame = 0
        self.__dict__.update(data)

    def update(self):
        pass

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 8, cy - 8, cx + 8, cy + 168

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 176, cx, cy + 80)

    def effect(self, mario):
        mario.game_end()