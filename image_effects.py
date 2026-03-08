import pygame
pygame.init()
# Slicing the frame
def slicing(object, section, frame_width, frame_height):
    sliced = []
    for i in range(section):
        frame = object.subsurface(
            (i * frame_width, 0, frame_width, frame_height))
        sliced.append(frame)
    return sliced


# character image
walk = pygame.image.load("images\\64x64\\2d\\walk.png")
frames = slicing(walk, 6, 64, 64)


# Backgrounds
layers = [
    pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-7-sky-background.png"),
    pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-6-clouds.png"),
    pygame.image.load("images\\Adventure 2D Tileset\\Layers\\x32-layer-5-mountains-3.png"), pygame.image.load("images\\Adventure 2D Tileset\\Layers\\x32-layer-3-mountains-1.png"), pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-4-mountains-2.png"), pygame.image.load("images\\Adventure 2D Tileset\\Layers\\x32-layer-2-trees-2.png"),
    pygame.image.load(
        "images\\Adventure 2D Tileset\\Layers\\x32-layer-1-trees-1.png")
]
# *scale down
layers = [pygame.transform.scale(layer, (853, 213)) for layer in layers]

char = pygame.image.load("images\\64x64\\2d\\idle.png")
frames_char = slicing(char, 6, 64, 64)

jump = pygame.image.load("images\\64x64\\2d\\jump.png")
frames_jump = slicing(jump, 6, 64, 64)

food = pygame.image.load("images\\PixelFishes\\PixelFishes.png")
frames_food = slicing(food, 1, 32, 32)

bullet_sound = pygame.mixer.Sound("Sounds\\mixkit-little-cat-pain-meow-87.wav")
hit_sound = pygame.mixer.Sound("Sounds\\anime-ahh.wav")
bg_music = pygame.mixer.music.load(
    "Sounds\\SSvid.net--Twinkle-Twinkle-Little-StarChildren-s-Song-Music-Box.mp3")
pygame.mixer.music.play(-1)