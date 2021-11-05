import pico2d
image = pico2d.load_image('Tileset.png')

class normal:
    global image
    imageX = 154
    imageY = 3160 - 142 - 16

    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.frameM = 4
        self.frame = 0

    def draw(self):
        pico2d.image.clip_draw(normal.imageX + self.frame * 17, normal.imageY, 16, 16, self.x, self.y - 24)

class plat:
    global image
    imageX = 120
    imageY = 3160 - 74 - 16

    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.frameM = 3
        self.frame = 1

    def draw(self):
        pico2d.image.clip_draw(plat.imageX + self.frame * 17, plat.imageY, 16, 16, self.x, self.y - 24)

class ice:
    global image
    imageX = 137
    imageY = 3160 - 142 - 16

    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.frameM = 1
        self.frame = 0

    def draw(self):
        pico2d.image.clip_draw(ice.imageX + self.frame * 17, ice.imageY, 16, 16, self.x, self.y - 24)

class item:
    global image
    imageX = 35
    imageY = 3160 - 23 - 16

    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.frameM = 2
        self.frame = 0
        # 0-버섯
        self.item = 0

    def draw(self):
        pico2d.image.clip_draw(item.imageX + self.frame * 17 * 3, item.imageY, 16, 16, self.x, self.y - 24)