import GameFrame
import server
from pico2d import *

# 마리오 가로 10 세로 25
PIXEL_PER_METER = (25.0 / 1.8)  # 25 pixel 180cm
RUN_SPEED_KMPH = 100.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
RUN_ACCEL_MPS2 = RUN_SPEED_MPS / 120.0
RUN_ACCEL_PPS2 = RUN_ACCEL_MPS2 * PIXEL_PER_METER

FALL_SPEED_KMPH = 200.0
FALL_SPEED_MPM = (FALL_SPEED_KMPH * 1000.0 / 60.0)
FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)
FALL_ACCEL_MPS2 = FALL_SPEED_MPS / 120.0
FALL_ACCEL_PPS2 = FALL_ACCEL_MPS2 * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# 호출 인자 모음
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, \
SHIFT_UP, SHIFT_DOWN, ZERO_SPEED, SPACE, LANDING, END, PAUSE = range(11)

# 키 할당
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

# 마리오 스프라이트 정보
marioW, marioH, marioS = 779, 4158, 32

# 일반 '', 버섯 'b'
mDict = {
    'IdleX': 1,
    'IdleY': marioH - 22 - marioS,
    'IdleF': 1,
    'WalkX': 145,
    'WalkY': marioH - 22 - marioS,
    'WalkF': 2,
    'SkidX': 285,
    'SkidY': marioH - 22 - marioS,
    'SkidF': 1,
    'JumpX': 322,
    'JumpY': marioH - 22 - marioS,
    'JumpF': 2,

    'bIdleX': 1,
    'bIdleY': marioH - 222 - marioS,
    'bIdleF': 1,
    'bWalkX': 145,
    'bWalkY': marioH - 222 - marioS,
    'bWalkF': 3,
    'bSkidX': 351,
    'bSkidY': marioH - 222 - marioS,
    'bSkidF': 1,
    'bJumpX': 388,
    'bJumpY': marioH - 222 - marioS,
    'bJumpF': 2,
}

mFDict = {
    'IdleX': marioW - 1 - marioS,
    'IdleY': marioH - 22 - marioS,
    'IdleF': 1,
    'WalkX': marioW - 145 - marioS,
    'WalkY': marioH - 22 - marioS,
    'WalkF': 2,
    'SkidX': marioW - 285 - marioS,
    'SkidY': marioH - 22 - marioS,
    'SkidF': 1,
    'JumpX': marioW - 322 - marioS,
    'JumpY': marioH - 22 - marioS,
    'JumpF': 2,

    'bIdleX': marioW - 1 - marioS,
    'bIdleY': marioH - 222 - marioS,
    'bIdleF': 1,
    'bWalkX': marioW - 145 - marioS,
    'bWalkY': marioH - 222 - marioS,
    'bWalkF': 3,
    'bSkidX': marioW - 351 - marioS,
    'bSkidY': marioH - 222 - marioS,
    'bSkidF': 1,
    'bJumpX': marioW - 388 - marioS,
    'bJumpY': marioH - 222 - marioS,
    'bJumpF': 2,
}


def falling_mario(mario):
    if mario.fall_speed != 0 or mario.jumped:
        mario.fall_speed += FALL_ACCEL_PPS2
        mario.fall_speed = clamp(-FALL_SPEED_PPS, mario.fall_speed, FALL_SPEED_PPS)
        mario.y -= mario.fall_speed * GameFrame.tick_time
        mario.y = clamp(0, mario.y, 900 - 25)


def draw_falling(mario):
    if mario.fall_speed < 0:
        mario.frame = 0
    else:
        mario.frame = 1

    if mario.dir == 1:
        cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
        mario.image.clip_draw(mDict[mario.state + 'JumpX'] + int(mario.frame) * 33, mDict[mario.state + 'JumpY'], 32,
                              32, cx, cy)
    else:
        cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
        mario.imageF.clip_draw(mFDict[mario.state + 'JumpX'] - int(mario.frame) * 33, mFDict[mario.state + 'JumpY'], 32,
                               32, cx, cy)


class IdleState:

    def enter(mario, event):
        mario.velocity = 0
        mario.frame = 0

    def exit(mario, event):
        if event == SPACE:
            if not mario.jumped:
                mario.fall_speed = -2 * FALL_SPEED_PPS / 3
            mario.frame = 0
            mario.jumped = True

    def do(mario):
        falling_mario(mario)

    def draw(mario):
        if mario.dir == 1:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.image.clip_draw(mDict[mario.state + 'IdleX'] + int(mario.frame) * 33, mDict[mario.state + 'IdleY'], 32, 32,
                                  cx, cy)
        else:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.imageF.clip_draw(mFDict[mario.state + 'IdleX'] - int(mario.frame) * 33, mFDict[mario.state + 'IdleY'], 32,
                                  32, cx, cy)



class AccelState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.dir = 1
        elif event == LEFT_DOWN:
            mario.dir = -1
        elif event == RIGHT_UP:
            mario.dir = -1
        elif event == LEFT_UP:
            mario.dir = 1

    def exit(mario, event):
        if event == SPACE:
            if not mario.jumped:
                mario.fall_speed = -2 * FALL_SPEED_PPS / 3
            mario.frame = 0
            mario.jumped = True

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * GameFrame.tick_time * mario.velocity / RUN_SPEED_PPS) % mDict[mario.state + 'WalkF']
        mario.velocity += RUN_ACCEL_PPS2 * mario.dir
        mario.velocity = clamp(-RUN_SPEED_PPS, mario.velocity, RUN_SPEED_PPS)
        mario.x += mario.velocity * GameFrame.tick_time
        falling_mario(mario)

    def draw(mario):
        if mario.dir == 1:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.image.clip_draw(mDict[mario.state + 'WalkX'] + int(mario.frame) * 33, mDict[mario.state + 'WalkY'], 32, 32, cx, cy)
        else:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.imageF.clip_draw(mFDict[mario.state + 'WalkX'] - int(mario.frame) * 33, mFDict[mario.state + 'WalkY'], 32, 32, cx, cy)


# 일반 감속
class DecelState:

    def enter(mario, event):
        pass

    def exit(mario, event):
        if event == RIGHT_DOWN:
            mario.dir = 1
        elif event == LEFT_DOWN:
            mario.dir = -1
        elif event == SPACE:
            if not mario.jumped:
                mario.fall_speed = -2 * FALL_SPEED_PPS / 3
            mario.frame = 0
            mario.jumped = True

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * GameFrame.tick_time * mario.velocity / RUN_SPEED_PPS) % mDict[mario.state + 'WalkF']
        mario.velocity -= RUN_ACCEL_PPS2 * mario.dir
        if mario.velocity * mario.dir < 0:
            mario.velocity = 0
            mario.add_event(ZERO_SPEED)
        mario.x += mario.velocity * GameFrame.tick_time
        falling_mario(mario)

    def draw(mario):
        if mario.dir == 1:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.image.clip_draw(mDict[mario.state + 'WalkX'] + int(mario.frame) * 33, mDict[mario.state + 'WalkY'], 32, 32, cx, cy)
        else:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.imageF.clip_draw(mFDict[mario.state + 'WalkX'] - int(mario.frame) * 33, mFDict[mario.state + 'WalkY'], 32, 32, cx, cy)


# 빠른 감속(Skid)
class SkidState:

    def enter(mario, event):
        mario.frame = 0

    def exit(mario, event):
        if event == ZERO_SPEED:
            mario.dir *= -1
        elif event == SPACE:
            if not mario.jumped:
                mario.fall_speed = -2 * FALL_SPEED_PPS / 3
            mario.frame = 0
            mario.jumped = True

    def do(mario):
        mario.velocity -= 2 * RUN_ACCEL_PPS2 * mario.dir
        if mario.velocity * mario.dir < 0:
            mario.velocity = 0
            mario.add_event(ZERO_SPEED)
        mario.x += mario.velocity * GameFrame.tick_time
        falling_mario(mario)

    def draw(mario):
        if mario.dir == 1:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.image.clip_draw(mDict[mario.state + 'SkidX'] + int(mario.frame) * 33, mDict[mario.state + 'SkidY'], 32, 32,
                                  cx, cy)
        else:
            cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
            mario.imageF.clip_draw(mFDict[mario.state + 'SkidX'] - int(mario.frame) * 33, mFDict[mario.state + 'SkidY'], 32,
                                  32, cx, cy)


#
class GameEnd:
    def enter(mario, event):
        mario.velocity = 0
        mario.dir = 1
        mario.frame = 0
        pass

    def exit(mario, event):
        pass

    def do(mario):
        pass

    def draw(mario):
        cx, cy = mario.x - server.background.window_left, mario.y - server.background.window_bottom
        mario.image.clip_draw(mDict[mario.state + 'IdleX'] + int(mario.frame) * 33, mDict[mario.state + 'IdleY'], 32,
                              32, cx, cy)


# 상태 할당
next_state_table = {
    IdleState: {LEFT_UP: AccelState, RIGHT_UP: AccelState, RIGHT_DOWN: AccelState, LEFT_DOWN: AccelState,
                SPACE: IdleState, ZERO_SPEED: IdleState, END: GameEnd, PAUSE: IdleState},
    AccelState: {LEFT_UP: DecelState, RIGHT_UP: DecelState, LEFT_DOWN: SkidState, RIGHT_DOWN: SkidState,
                 SPACE: AccelState, ZERO_SPEED: AccelState, END: GameEnd, PAUSE: IdleState},
    DecelState: {LEFT_DOWN: AccelState, RIGHT_DOWN: AccelState, ZERO_SPEED: IdleState,
                 SPACE: DecelState, END: GameEnd, PAUSE: IdleState},
    SkidState: {LEFT_UP: AccelState, RIGHT_UP: AccelState, ZERO_SPEED: IdleState,
                SPACE: SkidState, END: GameEnd, PAUSE: IdleState},
    GameEnd: {LEFT_UP: GameEnd, RIGHT_UP: GameEnd, RIGHT_DOWN: GameEnd, LEFT_DOWN: GameEnd,
              ZERO_SPEED: GameEnd, SPACE: GameEnd, END: GameEnd, PAUSE: GameEnd}
}

class Mario:
    global FALL_SPEED_PPS
    FALL_PPS = FALL_SPEED_PPS

    def __init__(self):
        self.x, self.y = 800, 400
        self.image = load_image('Mario.png')
        self.imageF = load_image('MarioFlip.png')
        self.state = ''
        self.dir = 1
        self.velocity = 0.0
        self.fall_speed = 0
        self.jumped = False
        self.frame = 0

        self.invi = 0

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def __getstate__(self):
        data = {'x': self.x, 'y': self.y,
                'state': self.state,
                'dir': self.dir,
                'velocity': self.velocity,
                'fall_speed': self.fall_speed,
                'jumped': self.jumped,
                'frame': self.frame
        }

        return data

    def __setstate__(self, data):
        self.__init__()
        self.__dict__.update(data)

    def get_bb(self):
        cx, cy = self.x - server.background.window_left, self.y - server.background.window_bottom
        return cx - 5, cy - 16, cx + 5, cy + 4

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        if self.invi > 0:
            self.invi -= GameFrame.tick_time
        else:
            self.invi = 0
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

        self.x, self.y = clamp(0, self.x, server.background.w - 1), clamp(0, self.y, server.background.h - 1)


    def draw(self):
        if 0 <= (math.sqrt(max(0, self.invi)) * 20) % 2 < 1:
            if self.jumped:
                draw_falling(self)
            else:
                self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def stop(self, block):
        if self.fall_speed > 0:
            self.fall_speed = 0
            self.jumped = False
            self.frame = 0
            self.y = block.y + 8 + 16

    def headStop(self):
        if self.fall_speed < 0:
            self.fall_speed = FALL_SPEED_PPS / 5
            self.frame = 1

    def inMiddle(self):
        global RUN_ACCEL_MPS2
        global RUN_SPEED_MPS
        if not self.jumped:
            self.fall_speed = 0
            self.frame = 0
            self.jumped = True
            RUN_ACCEL_MPS2 = RUN_SPEED_MPS / 120.0

    def grow(self):
        self.state = 'b'

    def setMPS2(self, num):
        global RUN_ACCEL_MPS2
        global RUN_SPEED_MPS
        RUN_ACCEL_MPS2 = RUN_SPEED_MPS / num



    def collide_wall_left(self, block):
        self.velocity = 0
        self.x = block.x - 8 - 6

    def collide_wall_right(self, block):
        self.velocity = 0
        self.x = block.x + 8 + 6

    def pause(self):
        self.add_event(PAUSE)

    def game_end(self):
        self.add_event(END)

