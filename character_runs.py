from pico2d import *
import math
from Mushroom import *



class nBlock:
    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.nbX = 154
        self.nbY = tileY - 142 - 16
        self.nbF = 4
        self.frame = 0
    def draw(self):
        tile.clip_draw(self.nbX + self.frame * 17, self.nbY, 16, 16, self.x, self.y - 24)

class platBlock:
    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.nbX = 120
        self.nbY = tileY - 74 - 16
        self.nbF = 3
        self.frame = 1
    def draw(self):
        tile.clip_draw(self.nbX + self.frame * 17, self.nbY, 16, 16, self.x, self.y - 24)

class iceBlock:
    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.nbX = 137
        self.nbY = tileY - 142 - 16
        self.nbF = 1
        self.frame = 0
    def draw(self):
        tile.clip_draw(self.nbX + self.frame * 17, self.nbY, 16, 16, self.x, self.y - 24)

class itemBlock:
    def __init__(self, inX, inY):
        self.x, self.y = inX + 8, inY + 16
        self.nbX = 35
        self.nbY = tileY - 23 - 16
        self.nbF = 2
        self.frame = 0
        # 0은 버섯
        self.item = 0
    def draw(self):
        tile.clip_draw(self.nbX + self.frame * 17 * 3, self.nbY, 16, 16, self.x, self.y - 24)

open_canvas()

tile = load_image('Tileset.png')
character = load_image('Mario.png')
back = load_image('Background.png')

charX, charY = 779, 4158
tileX, tileY = 1369, 3160
cDict = {
    'IdleX': 1,
    'IdleY': charY - 22 - 32,
    'IdleF': 1,
    'WalkX': 145,
    'WalkY': charY - 22 - 32,
    'WalkF': 2,
    'bIdleX': 1,
    'bIdleY': charY - 222 - 32,
    'bIdleF': 1,
    'bWalkX': 145,
    'bWalkY': charY - 222 - 32,
    'bWalkF': 3
}

backX, backY = 1608, 6874
bDict = {
    'skyX': 1,
    'skyY': backY - 12 - 512,
}



def handle_events():
    global running
    global chaDir
    global chaJumped
    global chaFalled
    global chaGravSpeed
    global mushroomList
    global nBlockList
    global iceBlockList
    global platBlockList
    global itemBlockList
    global blockSelect
    KeyEvents = get_events()
    for event in KeyEvents:
        if event.type == SDL_MOUSEBUTTONDOWN:
            tmpEventY = 600 - event.y
            if event.button == SDL_BUTTON_LEFT:
                mushroomList.append(Mushroom(event.x, tmpEventY))
            if event.button == SDL_BUTTON_RIGHT:
                if blockSelect == 0:
                    nBlockList.append(nBlock(event.x - (event.x % 16), tmpEventY + (16 - tmpEventY % 16)))
                elif blockSelect == 1:
                    platBlockList.append(platBlock(event.x - (event.x % 16), tmpEventY + (16 - tmpEventY % 16)))
                elif blockSelect == 2:
                    iceBlockList.append(iceBlock(event.x - (event.x % 16), tmpEventY + (16 - tmpEventY % 16)))
                elif blockSelect == 3:
                    itemBlockList.append(itemBlock(event.x - (event.x % 16), tmpEventY + (16 - tmpEventY % 16)))
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                chaDir = 1
            elif event.key == SDLK_LEFT:
                chaDir = -1
            elif event.key == SDLK_SPACE:
                if chaJumped == False:
                    chaGravSpeed = -12
                    chaJumped = True
                    chaFalled = True
            elif event.type == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_1:
                blockSelect = 0
            elif event.key == SDLK_2:
                blockSelect = 1
            elif event.key == SDLK_3:
                blockSelect = 2
            elif event.key == SDLK_4:
                blockSelect = 3

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if chaDir == 1:
                    chaDir = 0
            elif event.key == SDLK_LEFT:
                if chaDir == -1:
                    chaDir = 0

# 속도 계산
def char_Accel():
    global chaSpeed
    global chaGravSpeed
    global chaJumped
    global chaFalled
    global chaAcc
    global y
    global mushroomList


    chaFalled = True


    for mush in mushroomList:
        mush.update()

    #점프
    y -= chaGravSpeed
    if chaFalled:
        if chaGravSpeed < 8:
            chaGravSpeed += 0.6
        else:
            chaGravSpeed = 8

    #중력
    if y < 59:
        y = 60
        chaGravSpeed = 0
        chaJumped = False
        chaFalled = False

    #좌우이동
    if chaDir == 1:
        if chaSpeed < 5:
            chaSpeed += 0.17
    elif chaDir == -1:
        if chaSpeed > -5:
            chaSpeed -= 0.17
    else:
        if chaSpeed > 0.5:
            chaSpeed -= 0.17 * chaAcc
        elif chaSpeed < -0.5:
            chaSpeed += 0.17 * chaAcc
        elif chaSpeed <= 0.5 and chaSpeed >= -0.5:
            chaSpeed = 0


# 이미지 프레임 계산
def frame_calc():
    global chaFrame
    global frame
    frame += 1

    #character
    if chaDir == 0:
        chaFrame = 0
    elif chaDir == 1:
        chaFrame = math.floor(frame / 10) % cDict[chaImageKey+'WalkF']
    elif chaDir == -1:
        chaFrame = math.floor(frame / 10) % cDict[chaImageKey+'WalkF']


# sprite 구역 찾아서 출력
def clip_select():
    global mushroomList
    global nBlockList
    global platBlockList
    global iceBlockList
    global itemBlockList
    global chaImageKey
    for mush in mushroomList:
        mush.draw()
    for nB in nBlockList:
        nB.draw()
    for ptB in platBlockList:
        ptB.draw()
    for iB in iceBlockList:
        iB.draw()
    for itB in itemBlockList:
        itB.draw()

    if chaDir == 0:
        character.clip_draw(cDict[chaImageKey+'IdleX'] + chaFrame * 33, cDict[chaImageKey+'IdleY'], 32, 32, x, y)
    elif chaDir == 1:
        character.clip_draw(cDict[chaImageKey+'WalkX'] + chaFrame * 33, cDict[chaImageKey+'WalkY'], 32, 32, x, y)
    elif chaDir == -1:
        character.clip_draw(cDict[chaImageKey+'WalkX'] + chaFrame * 33, cDict[chaImageKey+'WalkY'], 32, 32, x, y)

# 충돌체크
def conflict_check():
    global x
    global y
    global mushroomList
    global nBlockList
    global platBlockList
    global iceBlockList
    global itemBlockList
    global chaImageKey
    global chaGravSpeed
    global chaJumped
    global chaFalled
    global chaHead
    global chaAcc
    for mush in mushroomList:
        if abs(mush.x - x) < 16 and abs(mush.y - y) < 16:
            chaImageKey = 'b'
            chaHead = 48
            mushroomList.remove(mush)

    for nB in nBlockList:
        if abs(nB.x - x) < 16 and 0 < nB.y - y < 8:
            y = nB.y
            chaJumped = False
            chaFalled = False
            chaGravSpeed = 0
            chaAcc = 1
        if abs(nB.x - x) < 16 and 8 < nB.y - y < chaHead:
            y = nB.y - chaHead
            chaGravSpeed = 0

    for ptB in platBlockList:
        if abs(ptB.x - x) < 16 and 0 < ptB.y - y < 8 and chaGravSpeed >= 0:
            y = ptB.y
            chaJumped = False
            chaFalled = False
            chaAcc = 1
            chaGravSpeed = 0

    for iB in iceBlockList:
        if abs(iB.x - x) < 16 and 0 < iB.y - y < 8:
            y = iB.y
            chaJumped = False
            chaFalled = False
            chaGravSpeed = 0
            chaAcc = 0.25
        if abs(iB.x - x) < 16 and 8 < iB.y - y < chaHead:
            y = iB.y - chaHead
            chaGravSpeed = 0

    for itB in itemBlockList:
        if abs(itB.x - x) < 16 and 0 < itB.y - y < 8:
            y = itB.y
            chaJumped = False
            chaFalled = False
            chaGravSpeed = 0
            chaAcc = 1
        if abs(itB.x - x) < 18 and 8 < itB.y - y < chaHead:
            y = itB.y - chaHead
            if itB.frame == 0:
                mushroomList.append(Mushroom(itB.x, itB.y + 4))
            itB.frame = 1
            chaGravSpeed = 0


# dir에 따라 캐릭터의 상태가 다름
# 0 - 멈춤
# -1 - 왼쪽
# 1 - 오른쪽
running = True
chaDir = 0
chaSpeed = 0
chaFrame = 0
chaGravSpeed = 10
chaJumped = False
chaFalled = False
count_StepBlock = 0
chaImageKey = ''
chaHead = 32
chaAcc = 1
mushroomList = []
nBlockList = []
platBlockList = []
iceBlockList = []
itemBlockList = []
blockSelect = 0
x = 30
y = 90
frame = 0


while running:
    clear_canvas()
    # x위치, y위치, 가로폭, 세로폭, 출력위치 x, 출력위치 y
    # 145, 22
    back.clip_draw(bDict['skyX'], bDict['skyY'], 512, 512, 256, 256)
    back.clip_draw(bDict['skyX'], bDict['skyY'], 512, 512, 256 + 512, 256)
    clip_select()
    update_canvas()

    conflict_check()
    handle_events()
    frame_calc()
    char_Accel()
    x += chaSpeed
    delay(0.01)


close_canvas()
