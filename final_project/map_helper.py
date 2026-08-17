from char_helper import *
import pytmx
from pytmx.util_pygame import load_pygame
from screens import *


def render_tmx_layers(tmx_data): #render map
    width = tmx_data.width * tmx_data.tilewidth
    height = tmx_data.height * tmx_data.tileheight
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    return surface

def get_collision_rects(tmx_data, scale=1):
    return [
        pygame.Rect(obj.x * scale, obj.y * scale, obj.width * scale, obj.height * scale)
        for layer in tmx_data.objectgroups
        for obj in layer
    ]

# ----------scrolling background (roads)----------
class ScrollingBackground:

    def __init__(self, tmx_path, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, speed=1):
        tmx_data = load_pygame(tmx_path)
        map_surface = render_tmx_layers(tmx_data)
        map_pixel_width, map_pixel_height = map_surface.get_size()

        scale = height / map_pixel_height
        scaled_width = max(1, int(map_pixel_width * scale))
        self.surface = pygame.transform.scale(map_surface, (scaled_width, height))

        self.tile_width = scaled_width  # width of map
        self.screen_width = width
        self.height = height
        self.speed = speed + 1
        self.scroll_x = 0  # scroll pos
        # how far scroll_x can go
        self.max_scroll = max(0, self.tile_width - self.screen_width)
        self.finished = self.max_scroll == 0
        self.collision_rects = get_collision_rects(tmx_data, scale)

    def update(self, speed=None):
        if speed is not None:
            self.speed = speed
        # never past max_scroll
        self.scroll_x = min(self.scroll_x + self.speed, self.max_scroll)
        self.finished = self.scroll_x >= self.max_scroll

    def draw(self, screen):
        screen.blit(self.surface, (-self.scroll_x, 0))


def load_map_background(tmx_path, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    bg = ScrollingBackground(tmx_path, width, height)
    crop_width = min(width, bg.tile_width)
    return bg.surface.subsurface(pygame.Rect(0, 0, crop_width, height)).copy()

# ---------city
class CityCamera:  # for city: different "camera", player focused

    def __init__(self, tmx_path, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, zoom=1.8):
        tmx_data = load_pygame(tmx_path)
        self.map_surface = render_tmx_layers(tmx_data)
        self.world_width, self.world_height = self.map_surface.get_size()
        self.zoom = zoom  # convert coordinates with zoom using this

        scaled_w = int(self.world_width * zoom)
        scaled_h = int(self.world_height * zoom)
        self.map_surface = pygame.transform.scale(self.map_surface, (scaled_w, scaled_h))

        self.collision_rects = get_collision_rects(tmx_data)

        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2()
        self.half_w = width // 2
        self.half_h = height // 2

    def center_camera(self, target):  # target is racoon
        self.offset.x = target.pos_x * self.zoom - self.half_w
        self.offset.y = target.pos_y * self.zoom - self.half_h
        self.offset.x = max(0, min(self.offset.x, self.map_surface.get_width() - self.width))
        self.offset.y = max(0, min(self.offset.y, self.map_surface.get_height() - self.height))

    def draw_camera(self, screen, racoon):
        self.center_camera(racoon)
        screen.blit(self.map_surface, (-self.offset.x, -self.offset.y))

    def to_screen_pos(self, x, y):  # convert world pos to screen pos
        return x * self.zoom - self.offset.x, y * self.zoom - self.offset.y

    def player_screen_pos(self, racoon):
        return self.to_screen_pos(racoon.pos_x, racoon.pos_y)