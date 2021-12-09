from pico2d import *
import server

class Normal:
    image = None
    imageX = 154
    imageY = 3160 - 142 - 16
    frameM = 4

    def __init__(self, inX, inY):
        if Normal.image == None:
            Normal.image = pico2d.load_image('TileSet.png')
        self.x, self.y = inX, inY
        self.frame = 0

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y, 'frame': self.frame}
        return data

    def __setstate__(self, data):
        if Normal.image == None:
            Normal.image = pico2d.load_image('TileSet.png')
        self.imageX = 154
        self.imageY = 3160 - 142 - 16
        self.frame = 0
        self.__dict__.update(data)

    def update(self):
        pass

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 8, cy - 8, cx + 8, cy + 8

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 16, cx, cy)

    def effect(self, mario):
        mario.setMPS2(120.0)


class Plat:
    image = None
    imageX = 120
    imageY = 3160 - 74 - 16

    def __init__(self, inX, inY):
        if Plat.image == None:
            Plat.image = pico2d.load_image('TileSet.png')
        self.x, self.y = inX, inY
        self.frameM = 3
        self.frame = 1

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y, 'frame': self.frame}
        return data

    def __setstate__(self, data):
        if Plat.image == None:
            Plat.image = pico2d.load_image('TileSet.png')
        self.imageX = 120
        self.imageY = 3160 - 74 - 16
        self.frame = 0
        self.__dict__.update(data)

    def update(self):
        pass

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 8, cy - 8, cx + 8, cy + 8

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 16, cx, cy)

    def effect(self, mario):
        mario.setMPS2(120.0)


class Ice:
    image = None
    imageX = 137
    imageY = 3160 - 142 - 16

    def __init__(self, inX, inY):
        if Ice.image == None:
            Ice.image = pico2d.load_image('TileSet.png')
        self.x, self.y = inX, inY
        self.frameM = 1
        self.frame = 0

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y, 'frame': self.frame}
        return data

    def __setstate__(self, data):
        if Ice.image == None:
            Ice.image = pico2d.load_image('TileSet.png')
        self.imageX = 137
        self.imageY = 3160 - 142 - 16
        self.frame = 0
        self.__dict__.update(data)

    def update(self):
        pass

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 8, cy - 8, cx + 8, cy + 8

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 16, cx, cy)

    def effect(self, mario):
        mario.setMPS2(1200.0)


class Item:
    image = None
    imageX = 35
    imageY = 3160 - 23 - 16

    def __init__(self, inX, inY, num):
        if Item.image == None:
            Item.image = load_image('Tileset.png')
        self.x, self.y = inX, inY
        # 0-활성화 3-비활성화
        self.frame = 0
        # 0-버섯
        self.item = num

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y, 'frame': self.frame,
                'item': self.item}
        return data

    def __setstate__(self, data):
        if Item.image == None:
            Item.image = pico2d.load_image('TileSet.png')
        self.imageX = 35
        self.imageY = 3160 - 23 - 16
        self.frame = 0
        self.__dict__.update(data)

    def update(self):
        pass

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 8, cy - 8, cx + 8, cy + 8

    def draw(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 16, cx, cy)

    def effect(self, mario):
        mario.setMPS2(120.0)

    def disable(self):
        self.frame = 3

