from pico2d import *
import GameFrame
import GameWorld

import mario
import item
import block

name = "InGameState"

# 보관 목록 선언
player = None
blocks = []
items = []
enemies = []


PlaceKeyNumber = 1
background = None


def collide(a, b):

    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def collide_top(a, b):

    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_top_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True




def enter():
    global player
    global background
    player = mario.Mario()
    GameWorld.add_object(player, 1)

    global blocks
    GameWorld.add_objects(blocks, 1)

    global items
    GameWorld.add_objects(items, 1)

    global enemies
    GameWorld.add_objects(enemies, 1)

    background = load_image('Background.png')



def exit():
    GameWorld.clear_objects()


def pause():
    pass


def resume():
    pass


def handle_events():
    global blocks
    global items
    global PlaceKeyNumber

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrame.quit_state()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # 이거 일시정지 화면으로 바꿔야함
            GameFrame.quit_state()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_MINUS:
            player.kill()


        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            PlaceKeyNumber = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            PlaceKeyNumber = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            PlaceKeyNumber = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            PlaceKeyNumber = 4
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            gridX = event.x - ((event.x + 8) % 16 - 8)
            gridY = event.y - ((event.y + 8) % 16 - 8)
            if PlaceKeyNumber == 1:
                GameWorld.add_object(block.Normal(gridX, 600 - gridY), 1)
                blocks += [block.Normal(gridX, 600 - gridY)]
            elif PlaceKeyNumber == 2:
                GameWorld.add_object(block.Plat(gridX, 600 - gridY), 1)
                blocks += [block.Plat(gridX, 600 - gridY)]
            elif PlaceKeyNumber == 3:
                GameWorld.add_object(block.Ice(gridX, 600 - gridY), 1)
                blocks += [block.Ice(gridX, 600 - gridY)]
            elif PlaceKeyNumber == 4:
                GameWorld.add_object(block.Item(gridX, 600 - gridY), 1)
                blocks += [block.Ice(gridX, 600 - gridY)]
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            if PlaceKeyNumber == 1:
                GameWorld.add_object(item.Mushroom(event.x, 600 - event.y), 1)
                items += [item.Mushroom(event.x, 600 - event.y)]
            if PlaceKeyNumber == 2:
                GameWorld.add_object(item.Coin(event.x, 600 - event.y), 1)
                items += [item.Coin(event.x, 600 - event.y)]
        else:
            player.handle_event(event)


def update():
    for gameObj in GameWorld.all_objects():
        gameObj.update()

    checkFall = True

    for Item in items:
        if collide(player, Item):
            items.remove(Item)
            Item.effect(player)
            GameWorld.remove_object(Item)

    for Block in blocks:
        if collide_top(player, Block):
            Block.effect(player)
            checkFall = False
            player.stop()
        elif collide(player, Block):
            checkFall = False
            player.headStop()

    if checkFall:
        player.inMiddle()

    if player.life < 1:
        GameFrame.quit_state()






def draw():
    global background
    clear_canvas()
    for i in range(10):
        background.clip_draw(1, 6874 - 12 - 512, 512, 512, 256 * i, 256)
    for gameObj in GameWorld.all_objects():
        gameObj.draw()
    font = load_font('CookieRun.ttf', 16)
    font.draw(1400, 570, "남은 목숨: %3d" % player.life, (0, 0, 0))
    font.draw(1400, 550, "지난 시간: %3d" % get_time(), (0, 0, 0))
    font.draw(1400, 530, "모은 코인: %2d" % player.coin, (255, 255, 0))
    update_canvas()
