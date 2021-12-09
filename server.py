# 보관 목록 선언
player = None
blocks = []
items = []
enemies = []
background = None

mario_life = 5
mario_coin = 0
mario_time = 500

window_width = 1024
window_height = 760

def init():
    global player
    global blocks
    global items
    global enemies
    global background
    global mario_time

    player = None
    blocks = []
    items = []
    enemies = []
    background = None
    mario_time = 500