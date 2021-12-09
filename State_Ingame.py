from pico2d import *
import GameFrame
import GameWorld

import mario
import item
import block
import flag
import enemy

import server
import collision
import State_Pause
import State_Clear
from background import TileBackground as Background

name = "InGameState"

PlaceKeyNumber = 1
PlaceFrameNumber = 0
StartTime = 0
PlaceOffsetX = 0
PlaceOffsetY = 0


def load_saved_world():
    GameWorld.load()
    for o in GameWorld.all_objects():
        if isinstance(o, mario.Mario):
            server.player = o
        elif isinstance(o, (item.Mushroom, item.Coin)):
            server.items.append(o)
        elif isinstance(o, (block.Normal, block.Plat, block.Item, block.Ice)):
            server.blocks.append(o)
        elif isinstance(o, (enemy.Gumba)):
            server.enemies.append(o)


def enter():
    global StartTime

    load_saved_world()
    if server.player is None:
        server.player = mario.Mario()
        GameWorld.add_object(server.player, 1)
    StartTime = get_time()

    server.background = Background()
    GameWorld.add_object(server.background, 0)



def exit():
    GameWorld.erase_objects()


def pause():
    pass


def resume():
    pass


def handle_events():
    global PlaceKeyNumber
    global PlaceOffsetX
    global PlaceOffsetY

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            GameFrame.quit_state()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # 이거 일시정지 화면으로 바꿔야함
            server.player.pause()
            GameFrame.push_state(State_Pause)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_EQUALS:
            GameWorld.save()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_MINUS:
            GameWorld.erase_objects()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_HOME:
            PlaceOffsetY += 512
        elif event.type == SDL_KEYDOWN and event.key == SDLK_END:
            PlaceOffsetY -= 512
        elif event.type == SDL_KEYDOWN and event.key == SDLK_DELETE:
            PlaceOffsetX -= 512
        elif event.type == SDL_KEYDOWN and event.key == SDLK_PAGEDOWN:
            PlaceOffsetX += 512


        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            PlaceKeyNumber = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            PlaceKeyNumber = 2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            PlaceKeyNumber = 3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            PlaceKeyNumber = 4
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            PlaceKeyNumber = 5
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            gridX = event.x - ((event.x + 8) % 16 - 8) + PlaceOffsetX
            gridY = event.y - ((event.y + 8) % 16 - 8) + PlaceOffsetY
            if PlaceKeyNumber == 1:
                tmp = block.Normal(gridX, server.window_height - gridY)
                server.blocks += [tmp]
                GameWorld.add_object(tmp, 1)
            elif PlaceKeyNumber == 2:
                tmp = block.Plat(gridX, server.window_height - gridY)
                server.blocks += [tmp]
                GameWorld.add_object(tmp, 1)
            elif PlaceKeyNumber == 3:
                tmp = block.Ice(gridX, server.window_height - gridY)
                server.blocks += [tmp]
                GameWorld.add_object(tmp, 1)
            elif PlaceKeyNumber == 4:
                tmp = block.Item(gridX, server.window_height - gridY, 1)
                server.blocks += [tmp]
                GameWorld.add_object(tmp, 1)
            elif PlaceKeyNumber == 5:
                tmp = block.Item(gridX, server.window_height - gridY, 0)
                server.blocks += [tmp]
                GameWorld.add_object(tmp, 1)
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_RIGHT:
            gridX = event.x - ((event.x + 8) % 16 - 8) + PlaceOffsetX
            gridY = event.y - ((event.y + 8) % 16 - 8) + PlaceOffsetY
            if PlaceKeyNumber == 1:
                tmp = item.Mushroom(gridX, server.window_height - gridY)
                server.items += [tmp]
                GameWorld.add_object(tmp, 1)
            elif PlaceKeyNumber == 2:
                tmp = item.Coin(gridX, server.window_height - gridY)
                server.items += [tmp]
                GameWorld.add_object(tmp, 1)
            elif PlaceKeyNumber == 3:
                tmp = flag.Flag(gridX, server.window_height - gridY)
                server.items += [tmp]
                GameWorld.add_object(tmp, 1)
            elif PlaceKeyNumber == 4:
                tmp = enemy.Gumba(gridX, server.window_height - gridY)
                server.enemies += [tmp]
                GameWorld.add_object(tmp, 1)
        else:
            server.player.handle_event(event)


def update():
    for gameObj in GameWorld.all_objects():
        gameObj.update()

    checkFall = True
    readyToKill = False
    readyToEnd = False

    for Item in server.items:
        if collision.collide(server.player, Item):
            if type(Item) is flag.Flag:
                Item.effect(server.player)
                readyToEnd = True
            else:
                Item.effect(server.player)
                server.items.remove(Item)
                GameWorld.remove_object(Item)
        if type(Item) is item.Mushroom:
            for Block in server.blocks:
                dir = collision.collide_dir(Block, Item)
                if dir == 0:
                    Item.is_fall = True
                elif dir == 1:
                    Item.is_fall = False
                    Item.fall_speed = 0
                elif dir == 3:
                    Item.dir = -1
                elif dir == 4:
                    Item.dir = 1

    for Enemy in server.enemies:
        checkFallEnemy = True

        for Block in server.blocks:
            dir = collision.collide_dir(Block, Enemy)
            if dir == 1:
                checkFallEnemy = False
                Enemy.is_fall = False
                Enemy.fall_speed = 0
            elif dir == 3:
                Enemy.dir = -1
            elif dir == 4:
                Enemy.dir = 1

        dir = collision.collide_dir(Enemy, server.player)
        if dir == 1:
            checkFall = False
            server.player.fall_speed = -2 * server.player.FALL_PPS / 5
            mario.frame = 0
            mario.jumped = True

            server.enemies.remove(Enemy)
            GameWorld.remove_object(Enemy)
        elif dir != 0:
            readyToKill = True

        if checkFallEnemy:
            Enemy.is_fall = True

    for Block in server.blocks:
        dir = collision.collide_dir(Block, server.player)
        if dir == 1:
            Block.effect(server.player)
            checkFall = False
            server.player.stop(Block)
        if type(Block) is block.Item:
            if dir == 2:
                if Block.frame == 0:
                    if Block.item == 0:
                        tmp = item.Mushroom(Block.x, Block.y + 16)
                        server.items += [tmp]
                        GameWorld.add_object(tmp, 1)
                    elif Block.item == 1:
                        server.mario_coin += 1
                checkFall = False
                server.player.headStop()
                Block.frame = 3
            elif dir == 3:
                server.player.collide_wall_left(Block)
            elif dir == 4:
                server.player.collide_wall_right(Block)
        elif type(Block) is not block.Plat:
            if dir == 2:
                checkFall = False
                server.player.headStop()
            elif dir == 3:
                server.player.collide_wall_left(Block)
            elif dir == 4:
                server.player.collide_wall_right(Block)

    if checkFall:
        server.player.inMiddle()

    if server.mario_life < 1:
        GameFrame.quit_state()

    if server.mario_coin >= 100:
        server.mario_coin -= 100
        server.mario_life += 1

    if readyToEnd:
        bring_time = 0
        while readyToEnd:
            if bring_time > 3000.0:
                GameFrame.push_state(State_Clear)
                break
            bring_time += 0.01 * GameFrame.tick_time

    if server.mario_time + StartTime - get_time() <= 0:
        readyToKill = True

    if server.player.y <= 10:
        server.player.state = ''
        readyToKill = True

    if readyToKill:
        kill_mario()


def draw():
    clear_canvas()
    for gameObj in GameWorld.all_objects():
        gameObj.draw()
    if server.mario_life > 0:
        font = load_font('CookieRun.ttf', 16)
        font.draw(server.window_width - 100, server.window_height - 40, "남은 목숨: %3d" % server.mario_life, (0, 0, 0))
        font.draw(server.window_width - 100, server.window_height - 60,
                  "지난 시간: %3d" % (int)(server.mario_time + StartTime - get_time()), (0, 0, 0))
        font.draw(server.window_width - 100, server.window_height - 80, "모은 코인: %2d" % server.mario_coin, (255, 255, 0))

    update_canvas()


def kill_mario():
    if server.player.invi == 0:
        if server.player.state == 'b':
            server.player.state = ''
            server.player.invi = 3
        else:
            server.mario_life -= 1
            GameWorld.erase_objects()
            server.init()
            GameFrame.pop_state()
