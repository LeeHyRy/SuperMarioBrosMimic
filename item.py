import pico2d
image = pico2d.load_image('Mario.png')

class mushroom:
    global image
    imageX = 1
    imageY = 4158 - 4074 - 16

    def __init__(self, inX, inY):
        self.x, self.y = inX, inY
        self.speed = 2
        self.gravSpeed = 0
        self.dir = -1;

    def update(self):
        self.x -= self.speed * self.dir
        if self.y > 59:
            if self.gravSpeed < 8:
                self.gravSpeed += 0.6
            else:
                self.gravSpeed = 8
            self.y -= self.gravSpeed
        else:
            self.gravSpeed = 0
            self.y = 51

    def draw(self):
        pico2d.character.clip_draw(mushroom.imageX, mushroom.imageY, 16, 16, self.x, self.y)

