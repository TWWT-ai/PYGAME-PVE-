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

down = pygame.image.load("images\\64x64\\top-down\\attack_5.png")
frames_down = slicing(down, 4, 64, 64)

bullet_sound = pygame.mixer.Sound("Sounds\\mixkit-little-cat-pain-meow-87.wav")
hit_sound = pygame.mixer.Sound("Sounds\\fish-you-me-gas-station-clip.mp3")
bg_music = pygame.mixer.music.load(
    "Sounds\\SSvid.net--Twinkle-Twinkle-Little-StarChildren-s-Song-Music-Box.mp3")
pygame.mixer.music.play(-1)

main_menu_bg = pygame.image.load("images\\2306.w026.n002.3506B.p1.3506.jpg")
main_menu_bg = pygame.transform.scale(main_menu_bg, (853, 213))

default_button = pygame.image.load("images\\button_template.png")
default_button = pygame.transform.scale(main_menu_bg, (200, 100))
