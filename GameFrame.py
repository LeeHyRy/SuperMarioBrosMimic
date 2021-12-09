import time

tick_time = 0.0


class GameState:
    def __init__(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.pause = state.pause
        self.resume = state.resume
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw


running = None
stack = None


# 상태에 관한 초기 실행
def run(start_state):
    global running, stack, tick_time

    running = True

    # start_state 스택 생성
    stack = [start_state]
    start_state.enter()

    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        # 1프레임 길이 계산
        tick_time = time.time() - current_time
        current_time += tick_time

    # 게임 종료시
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()


# 상태 교체
def change_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    stack.append(state)
    state.enter()


# 상태 추가(+현재 상태 일시정지)
def push_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].pause
    stack.append(state)
    state.enter()


# 상태 제거(+이전 상태 불러오기)
def pop_state():
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    if len(stack) > 0:
        stack[-1].resume()


# 종료 유도
def quit_state():
    global running
    running = False
