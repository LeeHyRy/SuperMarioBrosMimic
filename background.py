import server

from pico2d import *


class TileBackground:

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = 512 * 8
        self.h = 512 * 3


        self.tiles = load_image('Background.png')

    def __getstate__(self):
        data = {'w': self.w, 'h': self.h}
        return data

    def __setstate__(self, data):
        self.tiles = load_image('Background.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.__dict__.update(data)

    def update(self):

        pass

    def draw(self):
        self.window_left = clamp(0,
                                 int(server.player.x) - self.canvas_width // 2,
                                 self.w - self.canvas_width)
        self.window_bottom = clamp(0,
                                   int(server.player.y) - self.canvas_height // 2,
                                   self.h - self.canvas_height)

        # 가로 세로 타일 8, 3칸
        tile_left = self.window_left // 512
        tile_right = min((self.window_left + self.canvas_width) // 512 + 1, 8)
        left_offset = self.window_left % 512

        tile_bottom = self.window_bottom // 512
        tile_top = min((self.window_bottom + self.canvas_height) // 512 + 1, 3)
        bottom_offset = self.window_bottom % 512

        for ty in range(tile_bottom, tile_top):
            for tx in range(tile_left, tile_right):
                if ty == 0:
                    self.tiles.clip_draw_to_origin(1, 6874 - 12 - 512, 512, 512,
                                               -left_offset + (tx - tile_left) * 512,
                                               -bottom_offset + (ty - tile_bottom) * 512)
                else:
                    self.tiles.clip_draw_to_origin(514, 6874 - 12 - 512, 512, 512,
                                               -left_offset + (tx - tile_left) * 512,
                                               -bottom_offset + (ty - tile_bottom) * 512)
