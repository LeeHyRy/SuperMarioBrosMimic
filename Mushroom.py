class Mushroom:
    def __init__(self, inX, inY):
        self.x, self.y = inX, inY
        self.speed = 2
        self.gravSpeed = 0
        self.mushX = 1
        self.mushY = charY - 4074 - 16
        self.dir = -1;
    def update(self):
        self.x -= self.speed * self.dir
        if self.y > 59:
            if self.gravSpeed < 8:
                self.gravSpeed += 0.6
            else :
                self.gravSpeed = 8
            self.y -= self.gravSpeed
        else :
            self.gravSpeed = 0
            self.y = 51
    def draw(self):
        character.clip_draw(self.mushX, self.mushY, 16, 16, self.x, self.y)