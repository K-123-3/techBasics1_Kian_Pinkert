from char_helper import *
import pytmx
from pytmx.util_pygame import load_pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500


#----------bike background----------
class ScrollingBackground:

    def __init__(self, tmx_path, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, speed=1):
        tmx_data = load_pygame(tmx_path)

        map_pixel_width = tmx_data.width * tmx_data.tilewidth
        map_pixel_height = tmx_data.height * tmx_data.tileheight
        map_surface = pygame.Surface((map_pixel_width, map_pixel_height), pygame.SRCALPHA)

        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        map_surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

        scale = height / map_pixel_height
        scaled_width = max(1, int(map_pixel_width * scale))
        self.surface = pygame.transform.scale(map_surface, (scaled_width, height))

        self.tile_width = scaled_width  # width of one full copy of the map
        self.screen_width = width
        self.height = height
        self.speed = speed
        self.scroll_x = 0
        # how far scroll_x can go
        self.max_scroll = max(0, self.tile_width - self.screen_width)
        self.finished = self.max_scroll == 0

    def update(self, speed=None):
        if speed is not None:
            self.speed = speed
        #never past max_scroll
        self.scroll_x = min(self.scroll_x + self.speed, self.max_scroll)
        self.finished = self.scroll_x >= self.max_scroll

    def draw(self, screen):
        screen.blit(self.surface, (-self.scroll_x, 0))


def load_map_background(tmx_path, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    bg = ScrollingBackground(tmx_path, width, height)
    crop_width = min(width, bg.tile_width)
    return bg.surface.subsurface(pygame.Rect(0, 0, crop_width, height)).copy()
