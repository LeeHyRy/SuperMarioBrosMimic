from pico2d import *
import mario

class Normal:
    image = None
    imageX = 154
    imageY = 3160 - 142 - 16

    def __init__(self, inX, inY):
        if Normal.image == None:
            Normal.image = pico2d.load_image('TileSet.png')
        self.x, self.y = inX, inY
        self.frameM = 4
        self.frame = 0

    def update(self):
        pass

    def get_top_bb(self):
        return self.x - 8, self.y, self.x + 8, self.y + 8

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y

    def draw(self):
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 16, self.x, self.y)
        draw_rectangle(*self.get_bb())

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

    def update(self):
        pass

    def get_top_bb(self):
        return self.x - 8, self.y, self.x + 8, self.y + 8

    def get_bb(self):
        return self.x, self.y, self.x, self.y

    def draw(self):
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 16, self.x, self.y)

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

    def update(self):
        pass

    def get_top_bb(self):
        return self.x - 8, self.y, self.x + 8, self.y + 8

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def draw(self):
        self.image.clip_draw(self.imageX + self.frame * 17, self.imageY, 16, 16, self.x, self.y)

    def effect(self, mario):
        mario.setMPS2(12000.0)


class Item:
    imageX = 35
    imageY = 3160 - 23 - 16

    def __init__(self, inX, inY):
        if Ice.image == None:
            Ice.image = load_image('Tileset.png')
        self.x, self.y = inX, inY
        self.frameM = 2
        self.frame = 0
        # 0-버섯
        self.item = 0

    def update(self):
        pass

    def get_top_bb(self):
        return self.x - 8, self.y, self.x + 8, self.y + 8

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def draw(self):
        self.image.clip_draw(self.imageX + self.frame * 17 * 3, self.imageY, 16, 16, self.x, self.y)

    def effect(self, mario):
        mario.setMPS2(120.0)

