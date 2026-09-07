import random

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 500
ICON_SIZE = 30
ICON_MARGIN = 4
APPLE_PERCENTAGE = 0.1
MAX_LIVES = 3
BIN_POSITIONS = [
        (1100, 125),
        (200,400),
        (1000,300),
    ]
BIKE_POSITIONS = [
    (600, random.randint(100, 300)),
    (900, random.randint(100, 200)),
    (700, random.randint(200, 300)),
    (1200, random.randint(50, 150)),
]

SCENES = [
    {"path": "media/map/road.tmx", "bg_speed": 1, "racoon_speed": 3, "allow_car": False},
    {"path": "media/map/road2.tmx", "bg_speed": 2, "racoon_speed": 4, "allow_car": True},
    {"path": "media/map/road2.tmx", "bg_speed": 3, "racoon_speed": 5, "allow_car": True},
]